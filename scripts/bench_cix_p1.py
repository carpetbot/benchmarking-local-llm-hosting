#!/usr/bin/env python3
"""
First-party LLM benchmark for the CIX P1 desk.
Measures prefill (prompt eval) and decode (generation) SEPARATELY,
because that is the axis everyone conflates.

Emits JSON with full machine identity so the row is auditable.
"""
import json, subprocess, time, urllib.request, os, sys

OLLAMA = "http://localhost:11434"

def machine_id():
    d = {}
    try:
        for line in open("/proc/cpuinfo"):
            if "model name" in line:
                d["cpu"] = line.split(":", 1)[1].strip(); break
    except Exception: pass
    d["cores"] = os.cpu_count()
    try:
        for line in open("/proc/meminfo"):
            if line.startswith("MemTotal"):
                d["ram_gb"] = round(int(line.split()[1]) / 1024 / 1024, 1); break
    except Exception: pass
    try:
        d["board"] = open("/proc/device-tree/model").read().strip("\x00").strip()
    except Exception: d["board"] = "unknown"
    try:
        out = subprocess.run(["vulkaninfo", "--summary"], capture_output=True,
                             text=True, timeout=30).stdout
        for line in out.splitlines():
            if "deviceName" in line:
                d["gpu"] = line.split("=", 1)[1].strip(); break
    except Exception: d["gpu"] = "unknown"
    try:
        d["ollama"] = json.load(urllib.request.urlopen(OLLAMA + "/api/version"))["version"]
    except Exception: d["ollama"] = "unknown"
    try:
        d["kernel"] = subprocess.run(["uname", "-r"], capture_output=True,
                                     text=True).stdout.strip()
    except Exception: pass
    return d

def thermal():
    """Report thermal state — a benchmark without it is not reproducible."""
    temps = []
    base = "/sys/class/thermal"
    if os.path.isdir(base):
        for z in sorted(os.listdir(base)):
            if z.startswith("thermal_zone"):
                try:
                    t = int(open(f"{base}/{z}/temp").read().strip()) / 1000.0
                    temps.append(round(t, 1))
                except Exception: pass
    return {"max_c": max(temps) if temps else None, "zones_c": temps}

def run(model, prompt, num_predict=256, label=""):
    body = json.dumps({
        "model": model, "prompt": prompt, "stream": False,
        "options": {"num_predict": num_predict, "temperature": 0}
    }).encode()
    req = urllib.request.Request(OLLAMA + "/api/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    r = json.load(urllib.request.urlopen(req, timeout=1800))
    wall = time.time() - t0

    pe_n = r.get("prompt_eval_count", 0)
    pe_d = r.get("prompt_eval_duration", 0)   # ns
    ev_n = r.get("eval_count", 0)
    ev_d = r.get("eval_duration", 0)          # ns

    return {
        "label": label,
        "model": model,
        "prompt_tokens": pe_n,
        # PREFILL: how fast it ingests. This is what vendor "4x AI" claims measure.
        "prefill_tok_s": round(pe_n / (pe_d / 1e9), 2) if pe_d else None,
        "prefill_wall_s": round(pe_d / 1e9, 2) if pe_d else None,
        "gen_tokens": ev_n,
        # DECODE: how fast it answers. This is what you actually feel.
        "decode_tok_s": round(ev_n / (ev_d / 1e9), 2) if ev_d else None,
        "decode_wall_s": round(ev_d / 1e9, 2) if ev_d else None,
        "total_wall_s": round(wall, 2),
        "thermal_after": thermal(),
    }

SHORT = "Explain what a mixture-of-experts layer does in one paragraph."
# ~2.5k token prompt to expose the prefill wall the short prompt hides
LONG = ("You are reviewing a technical document. Here is the document:\n\n"
        + ("A single-board computer integrates a processor, memory, storage and I/O "
           "onto one printed circuit board. Memory bandwidth constrains token "
           "generation speed for large language model inference, while compute "
           "throughput constrains prompt processing. These are distinct axes and "
           "should never be conflated when evaluating hardware. ") * 40
        + "\n\nSummarize the document in three sentences.")

def main():
    models = sys.argv[1:] or ["qwen3:0.6b", "qwen3:4b"]
    out = {
        "benchmark": "cix-p1-first-party",
        "date_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "machine": machine_id(),
        "thermal_start": thermal(),
        "backend": "ollama (llama.cpp) — CPU path unless GPU offload confirmed",
        "runs": [],
    }
    for m in models:
        print(f"[*] {m} short-context ...", flush=True)
        try:
            out["runs"].append(run(m, SHORT, 256, "short"))
        except Exception as e:
            out["runs"].append({"model": m, "label": "short", "error": str(e)})
        print(f"[*] {m} long-context (~2.5k tok) ...", flush=True)
        try:
            out["runs"].append(run(m, LONG, 128, "long_2.5k"))
        except Exception as e:
            out["runs"].append({"model": m, "label": "long_2.5k", "error": str(e)})

    path = f"/home/orangepi/bench_cix_p1_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"\nSaved: {path}")

if __name__ == "__main__":
    main()
