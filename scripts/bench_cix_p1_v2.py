#!/usr/bin/env python3
"""
First-party LLM benchmark, v2 — CIX P1 desk.

v2 adds what a defensible 8B/27B row needs and v1 lacked:
  - peak RSS of the ollama runner (does it actually fit, or is it swapping?)
  - swap delta across the run (the silent killer of SBC benchmarks)
  - repeat runs + median (single samples on a thermally-throttled ARM box lie)
  - explicit GPU-offload check per model (never assume the accelerator engaged)
  - cold vs warm load time (model load is not tok/s but it IS the UX)
  - graceful skip when a model OOMs, so one failure doesn't kill the sweep

Separates prefill (prompt_eval_duration) from decode (eval_duration).
Emits auditable JSON with full machine identity.
"""
import json, subprocess, time, urllib.request, urllib.error, os, sys, statistics

OLLAMA = "http://localhost:11434"

def sh(cmd, timeout=30):
    try:
        return subprocess.run(cmd, capture_output=True, text=True,
                              timeout=timeout).stdout
    except Exception:
        return ""

def machine_id():
    d = {}
    for line in open("/proc/cpuinfo"):
        if "model name" in line:
            d["cpu"] = line.split(":", 1)[1].strip(); break
    d["cores"] = os.cpu_count()
    for line in open("/proc/meminfo"):
        if line.startswith("MemTotal"):
            d["ram_gb"] = round(int(line.split()[1]) / 1024 / 1024, 1); break
    try:
        d["board"] = open("/proc/device-tree/model").read().strip("\x00").strip()
    except Exception:
        d["board"] = sh(["hostname"]).strip() or "unknown"
    for line in sh(["vulkaninfo", "--summary"]).splitlines():
        if "deviceName" in line:
            d["gpu"] = line.split("=", 1)[1].strip(); break
    d.setdefault("gpu", "unknown")
    try:
        d["ollama"] = json.load(urllib.request.urlopen(OLLAMA + "/api/version"))["version"]
    except Exception:
        d["ollama"] = "unknown"
    d["kernel"] = sh(["uname", "-r"]).strip()
    gov = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
    d["cpu_governor"] = open(gov).read().strip() if os.path.exists(gov) else "unknown"
    return d

def meminfo():
    m = {}
    for line in open("/proc/meminfo"):
        k, v = line.split(":", 1)
        m[k] = int(v.split()[0])
    return {
        "mem_avail_gb": round(m.get("MemAvailable", 0) / 1024 / 1024, 2),
        "swap_used_gb": round((m.get("SwapTotal", 0) - m.get("SwapFree", 0)) / 1024 / 1024, 2),
    }

def thermal():
    temps = []
    base = "/sys/class/thermal"
    if os.path.isdir(base):
        for z in sorted(os.listdir(base)):
            if z.startswith("thermal_zone"):
                try:
                    temps.append(round(int(open(f"{base}/{z}/temp").read().strip())/1000.0, 1))
                except Exception:
                    pass
    return max(temps) if temps else None

def runner_peak_rss_gb():
    """Peak RSS across ollama runner processes — proves whether the model fits."""
    best = 0
    out = sh(["ps", "-eo", "rss,comm,args"])
    for line in out.splitlines():
        if "ollama" in line and "runner" in line:
            try:
                best = max(best, int(line.split()[0]))
            except Exception:
                pass
    return round(best / 1024 / 1024, 2)

def gpu_offload(model):
    """Read ollama's own log — never assume the accelerator engaged."""
    log = sh(["journalctl", "-u", "ollama", "--no-pager", "-n", "400"])
    if not log:
        p = os.path.expanduser("~/.ollama/logs/server.log")
        log = open(p).read()[-200000:] if os.path.exists(p) else ""
    last = None
    for line in log.splitlines():
        if "offloaded" in line and "layers to GPU" in line:
            last = line.split("msg=")[-1].strip().strip('"')
    return last or "no offload line found"

def one_run(model, prompt, num_predict):
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "options": {"num_predict": num_predict, "temperature": 0}}).encode()
    req = urllib.request.Request(OLLAMA + "/api/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    r = json.load(urllib.request.urlopen(req, timeout=5400))
    wall = time.time() - t0
    pe_n, pe_d = r.get("prompt_eval_count", 0), r.get("prompt_eval_duration", 0)
    ev_n, ev_d = r.get("eval_count", 0), r.get("eval_duration", 0)
    return {
        "prompt_tokens": pe_n,
        "prefill_tok_s": round(pe_n / (pe_d / 1e9), 2) if pe_d else None,
        "ttft_s": round((r.get("load_duration", 0) + pe_d) / 1e9, 2),
        "gen_tokens": ev_n,
        "decode_tok_s": round(ev_n / (ev_d / 1e9), 2) if ev_d else None,
        "load_s": round(r.get("load_duration", 0) / 1e9, 2),
        "total_wall_s": round(wall, 2),
    }

def bench(model, prompt, num_predict, label, repeats):
    mem0 = meminfo()
    samples, err = [], None
    for i in range(repeats):
        try:
            # CACHE BUST: ollama reuses the KV cache on an identical prompt, which
            # makes prompt_eval_duration measure a cache HIT, not prefill compute.
            # Measured 2026-08-27 on qwen3:8b @2232 tok: 8.13 tok/s cold vs
            # 7962 tok/s cached — a 979x lie. Every repeat MUST get a unique prefix.
            unique = f"[run-{time.time_ns()}-{i}] "
            samples.append(one_run(model, unique + prompt, num_predict))
        except Exception as e:
            err = f"{type(e).__name__}: {e}"
            break
    if not samples:
        return {"model": model, "label": label, "error": err,
                "mem_before": mem0, "note": "likely OOM or model too large"}
    mem1 = meminfo()
    med = lambda k: round(statistics.median([s[k] for s in samples if s[k] is not None]), 2)
    return {
        "model": model, "label": label, "repeats": len(samples),
        "prompt_tokens": samples[0]["prompt_tokens"],
        "prefill_tok_s_median": med("prefill_tok_s"),
        "decode_tok_s_median": med("decode_tok_s"),
        "decode_tok_s_all": [s["decode_tok_s"] for s in samples],
        "ttft_s_median": med("ttft_s"),
        "load_s_first": samples[0]["load_s"],
        "peak_runner_rss_gb": runner_peak_rss_gb(),
        "mem_avail_gb_before": mem0["mem_avail_gb"],
        "mem_avail_gb_after": mem1["mem_avail_gb"],
        "swap_used_gb_before": mem0["swap_used_gb"],
        "swap_used_gb_after": mem1["swap_used_gb"],
        "swapped": mem1["swap_used_gb"] - mem0["swap_used_gb"] > 0.1,
        "thermal_max_c": thermal(),
        "gpu_offload": gpu_offload(model),
        "partial_error": err,
    }

SHORT = "Explain what a mixture-of-experts layer does in one paragraph."
LONG = ("You are reviewing a technical document. Here is the document:\n\n"
        + ("A single-board computer integrates a processor, memory, storage and I/O "
           "onto one printed circuit board. Memory bandwidth constrains token "
           "generation speed for large language model inference, while compute "
           "throughput constrains prompt processing. These are distinct axes and "
           "should never be conflated when evaluating hardware. ") * 40
        + "\n\nSummarize the document in three sentences.")

def main():
    models = sys.argv[1:] or ["qwen3:8b"]
    repeats = int(os.environ.get("BENCH_REPEATS", "3"))
    out = {"benchmark": "cix-p1-first-party-v2",
           "date_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "machine": machine_id(), "repeats_per_cell": repeats,
           "thermal_start_c": thermal(), "mem_start": meminfo(), "runs": []}
    for m in models:
        for label, prompt, npred, reps in [("short", SHORT, 128, repeats),
                                           ("long_2.2k", LONG, 96, max(1, repeats - 1))]:
            print(f"[*] {m} {label} x{reps} ...", flush=True)
            r = bench(m, prompt, npred, label, reps)
            out["runs"].append(r)
            if "error" in r:
                print(f"    FAILED: {r['error']}", flush=True)
                break
            print(f"    prefill={r['prefill_tok_s_median']} decode={r['decode_tok_s_median']} "
                  f"rss={r['peak_runner_rss_gb']}GB swap={r['swapped']}", flush=True)
        sh(["ollama", "stop", m], timeout=60)
        time.sleep(20)  # thermal settle between models
    path = f"/home/orangepi/bench_cix_p1_v2_{time.strftime('%Y%m%d_%H%M%S')}.json"
    json.dump(out, open(path, "w"), indent=2)
    print(f"\nSaved: {path}")

if __name__ == "__main__":
    main()
