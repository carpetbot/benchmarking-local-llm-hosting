# Benchmark Data: Orange Pi 6 Plus (CIX P1)

> **First-party measurements taken on our own board, 2026-08-27.** Everything in the
> "First-party" section below was produced by scripts in this repo on hardware we own.
> Third-party figures are kept separately and labelled.

---

## ⚠️ CORRECTIONS ISSUED 2026-08-27

This page and the root README previously carried errors. They are corrected below and
the retractions are left visible on purpose.

| Claim (before) | Reality (measured) | Evidence |
|---|---|---|
| SoC is **CD8180** | Our board is **CD8160** — a different SKU with lower clocks (4×A720 @2.6GHz + 4×A720 @2.2GHz vs 2.8/2.4) | `/proc/cpuinfo` |
| Backend "llama.cpp Vulkan", ~32 tok/s | **ollama offloads 0 layers to GPU.** 100% CPU on every run | ollama logs: `offloaded 0/49 layers to GPU` |
| Sticker $300 | **$268.89** (32GB, incl. heatsink + PSU) | [CNX Software, 2025-10-15](https://www.cnx-software.com/2025/10/15/orange-pi-6-plus-cix-p1-sbc-64gb-lpddr5-45-tops-ai-performance) |
| ~32 tok/s at 0.8B class | **27.38 tok/s** measured (qwen3:0.6b, short ctx), **12.56** at 2.2k ctx | this page |

The CD8180 clock figures in the old page may still be accurate *for a CD8180 board*.
We cannot verify them — we do not own one. They are now labelled third-party.

---

## Hardware (ours, verified)

- **Board:** Orange Pi 6 Plus 32GB — **$268.89**
- **SoC:** CIX P1 **CD8160** — 12 cores (4× A720 @2.6GHz + 4× A720 @2.2GHz + 4× A520 @1.8GHz)
- **GPU:** Mali Immortalis-G720 MC10 — Vulkan 1.3.275, exposes `QUEUE_COMPUTE_BIT`
- **NPU:** Zhouyi, 28.8–30 TOPS — **does NOT do autoregressive LLM decode** (see below)
- **RAM:** 30.9 GB usable LPDDR5
- **Swap:** none configured (so OOM is a hard fail, not a slow degrade — useful for testing)
- **OS:** Orange Pi 1.0.2 Noble (Ubuntu), kernel **6.6.89-cix**
- **Runtime:** ollama 0.18.0
- **Machine ID string:** `CIX P1 CD8160/30.9GB/Mali-G720-Immortalis/ollama0.18.0/k6.6.89-cix`

### On the "45 TOPS"

The board advertises 45 TOPS **combined** (CPU+GPU+NPU); the NPU alone is 28.8–30.
**LLM inference reaches none of it.**

- The Zhouyi NPU is an embeddings / agentic-memory processor. It does not perform
  autoregressive decode at all — architectural, not a driver gap.
  ([Interfacing Linux, 2026-05-31](https://interfacinglinux.com/community/sbcsoftware/vulkan-powered-llama-cpp-on-the-orion-o6-and-o6n))
- Independently corroborated on the same CIX P1 silicon:
  [minisforum-docs issue #20, 2026-03-22](https://github.com/minisforum-docs/MS-R1-Docs/issues/20)
  — "NPU is operational (NOE and ONNX+Zhouyi work with reference models), but LLM
  workloads currently run only on CPU."
- Mainstream runtimes (ollama, llama.cpp, LM Studio) do not route to NPUs regardless.

**Buy this class of board on memory bandwidth and RAM capacity. Never on the TOPS number.**

---

## First-party results (2026-08-27)

Method: ollama `/api/generate` with `stream:false`, reading `prompt_eval_duration`
(prefill) and `eval_duration` (decode) **separately**. Cold prefill forced with a
unique per-run prefix (see the KV-cache warning below). Q4_K_M, 4096 ctx window,
temperature 0. Harness: [`scripts/bench_cix_p1_v2.py`](../../scripts/bench_cix_p1_v2.py).

| model | active params | disk | peak RSS | ctx | prefill tok/s | decode tok/s | thermal |
|---|---|---|---|---|---|---|---|
| qwen3:0.6b dense | 0.6B | 0.5GB | — | 24 | 73.78 | **27.38** | 57°C |
| qwen3:0.6b dense | 0.6B | 0.5GB | — | 2232 | 49.90 | 12.56 | 61°C |
| qwen3:4b dense | 4B | 2.5GB | — | 24 | 20.04 | 7.19 | 70°C |
| qwen3:4b dense | 4B | 2.5GB | — | 2232 | 12.40 | 5.10 | 68°C |
| qwen3:8b dense | 8B | 5.2GB | 5.58GB | 24 | 77.13 | 4.79 | 72°C |
| qwen3:8b dense | 8B | 5.2GB | 5.69GB | 2250 | **8.13** | 3.69 | 72°C |
| qwen3:30b-a3b **MoE** | **3B** | 18GB | 17.81GB | 48 | 24.96 | **6.45** | 63°C |
| qwen3:30b-a3b **MoE** | **3B** | 18GB | 17.90GB | 2257 | 14.23 | **4.67** | 68°C |

45°C idle → 72°C sustained. No throttling observed. **No swap at any tier.**

Raw JSON: [`raw/`](./raw/)

### Cost per tok/s at 2.2k context (realistic agent workload)

| model | $/tok/s |
|---|---|
| qwen3:0.6b | **$21.41** |
| qwen3:4b | $52.72 |
| qwen3:30b-a3b MoE | $57.58 |
| qwen3:8b dense | **$72.87** ← worst on the board |

---

## Finding 1 — MoE beats dense, decisively

**A 30B MoE decodes 35% faster than a dense 8B** (6.45 vs 4.79 tok/s at short context;
4.67 vs 3.69 at 2.2k) while being **3.5× larger on disk**.

Active parameters (3B vs 8B) drive decode. Total parameters drive RAM only.
*"How big is the model"* is the wrong question; *"how many parameters activate per
token"* is the right one.

**Counter-finding**, stated because it cuts against the headline: the MoE degrades
slightly *faster* with context — **−27.6% vs −23.0%** for the dense 8B. An earlier
draft of this page claimed MoE was "gentler on long context." That was wrong and is
retracted. The absolute win holds at every context; the trend claim does not.

**Cost of the MoE win:** 17.9GB RSS. **On a 16GB board it does not load at all.**
This finding is only purchasable on the 32GB SKU.

---

## Finding 2 — the prefill wall

Decode speed gets quoted. Prefill is what you feel.

**qwen3:8b with a 2,250-token system prompt: 276.66 seconds — 4 min 37 s of silence
before the first token appears.** Then 3.69 tok/s.

- qwen3:0.6b @2.2k → ~45 s
- qwen3:30b-a3b @2.2k → ~159 s

**This is a batch device, not a chat device, above ~1B parameters.** Any product design
that puts a human in front of an 8B on this board with a real system prompt is broken
before it ships. No published SBC benchmark we found reports this number.

---

## ⚠️ Finding 3 — the KV-cache trap (read this before benchmarking anything)

Our own v2 harness reported **2,899 tok/s prefill** on qwen3:8b. Physically impossible
on this silicon. Cause: **ollama/llama.cpp reuse the KV cache when a prompt repeats**,
so `prompt_eval_duration` times a *cache hit*, not prefill compute.

| condition | reported prefill |
|---|---|
| Cache hit (identical prompt) | **7,962.74 tok/s** |
| Median of 2 repeats | 2,899.71 tok/s |
| **Cold, unique prefix** | **8.13 tok/s** |

A **979× overstatement.** Isolated with [`scripts/probe_prefill.py`](../../scripts/probe_prefill.py).

**The trap:** *adding repeats for statistical rigor is what introduced it.* The
single-run v1 numbers were cold and correct; more rigor produced a worse number.

**Fix:** prepend a unique token to every run (`bench_cix_p1_v2.py` now does this).

**Sanity rule:** if prefill exceeds ~20× your measured decode rate on CPU, you are
timing a cache, not the model.

---

## Finding 4 — verified headroom we are not yet using

llama.cpp built with Vulkan on the Mali G720 takes the same SoC from **4.3 → 9.9 tok/s
(2.3×)** ([Interfacing Linux, 2026-05-31](https://interfacinglinux.com/community/sbcsoftware/vulkan-powered-llama-cpp-on-the-orion-o6-and-o6n)).

We confirmed our Mali exposes `QUEUE_COMPUTE_BIT` under Vulkan 1.3.275, so this is
reachable on our stack — **despite** the reference guide targeting Debian 13 / kernel 7.0
while we run Ubuntu Noble / 6.6.89-cix.

**Status: not yet measured by us.** Blocked on dev packages:

```bash
sudo apt-get install -y glslc glslang-dev libshaderc-dev libvulkan-dev libssl-dev
cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_VULKAN=ON -DGGML_NATIVE=ON \
      -DGGML_OPENMP=ON -DGGML_CPU_KLEIDIAI=ON
cmake --build build -j$(nproc)
./build/bin/llama-cli -m <model>.gguf -ngl 60 -c 16384
```

If it reproduces, every decode row above moves up to 2.3×, which would likely take the
dense 8B off the skip list.

---

## Finding 5 — local is not a cost play at this tier

Qwen3-30B-A3B is the one model where we hold both a measured local number and a public
API price. API: **$0.048/M input, $0.193/M output**
([pricepertoken.com](https://pricepertoken.com/pricing-page/model/qwen-qwen3-30b-a3b-instruct-2507),
StreamLake, cheapest of 7 providers, updated 2026-08-16). Assumes 4:1 input:output.

| monthly output | API cost | local duty cycle @4.67 tok/s | payback on $268.89 |
|---|---|---|---|
| 1M tokens | $0.39 | 8.3% | 698 months (58 years) |
| 10M tokens | $3.85 | 82.6% | 70 months |
| 100M tokens | $38.50 | **826% — impossible** | n/a |

**The board saturates at ~12M output tokens/month.** Local inference on this hardware
class is not a cost play and never was. The surviving buy reasons: data residency,
fixed-budget predictability, offline operation, network-independent latency.

Anyone pitching SBC local-LLM on "cheaper than the API" is selling a story the
arithmetic does not support at 4.67 tok/s.

---

## Skip list

| tier | verdict | failure mode |
|---|---|---|
| qwen3:8b dense on this board | **SKIP** | Worst $/tok/s ($72.87). The MoE is faster, the 4B is cheaper. Trap tier — looks fine on a spec sheet, loses on every measured axis. |
| 16GB SKU for MoE work | **SKIP** | 17.9GB RSS. The model does not load. Buying 16GB for 30B-class MoE is buying a model you cannot open. |
| This board for interactive chat >4B | **SKIP** | 4 min 37 s prefill wall. Batch only. |
| Any NPU-marketed SBC bought for LLM TOPS | **SKIP** | The TOPS is architecturally unreachable. |

## Buy list

| tier | verdict |
|---|---|
| qwen3:0.6b | **BUY** — 27.38 tok/s, $21.41/tok/s. The only genuinely interactive tier. |
| qwen3:30b-a3b MoE (32GB SKU) | **BUY** — best quality-per-token on the box, 4.67 tok/s at agent context, 12GB headroom. |
| qwen3:4b | **CONDITIONAL** — if 0.6B quality is insufficient and 18GB RSS is unaffordable. |

---

## What would change these conclusions

| trigger | effect | re-check |
|---|---|---|
| llama.cpp Vulkan build lands | up to 2.3× on every decode row; may move 8B off skip list | on sudo access |
| ollama > 0.18.0 | unblocks `qwen3.8:27b` (dense 27B) — currently refuses to pull on 0.18.0 | next release |
| DRAM prices unwind | board price and the entire $/tok/s table shift | Q4 2026 |
| A 3B-active MoE ships under 8GB RSS | would beat 0.6B on quality at similar speed | ongoing |

**Not verified in public sources reviewed:** sustained power draw under LLM load on our
board (the 15–30W figures below are third-party); CD8180 variant performance; whether
the Vulkan 2.3× reproduces on kernel 6.6.89-cix rather than 7.0.

---

## Third-party data (not ours — retained, labelled)

### Power (Tao of Mac 30-day measurement, interfacinglinux hands-on)

| State | Watts | Source |
|---|---|---|
| Idle (board only) | 15.0 W | [Tao of Mac](https://taoofmac.com/space/reviews/2026/04/11/1900) |
| Daily cycle (mixed use) | 20–27 W | Tao of Mac |
| LLM load (Vulkan, sustained) | 25–30 W | interfacinglinux.com |
| Peak (CPU+GPU+NPU+NVMe) | 30 W | Tao of Mac |

⚠️ The "5–15W" idle figures from some vendor blogs are wrong. The CIX P1 reference
design runs hot. Plan for 15W minimum even at idle.
**We did not measure power ourselves — no wall meter on this board yet.**

### Qwen2.5-3B-Instruct Q5_K_M, llama.cpp Vulkan (third-party)

Source: [interfacinglinux.com](https://interfacinglinux.com/community/sbcsoftware/vulkan-powered-llama-cpp-on-the-orion-o6-and-o6n)

| Backend | tg (tok/s) | Notes |
|---|---|---|
| CPU only | 4.3 | baseline |
| Vulkan (Mali G720) | 9.9 | **2.3× uplift** |

Measured on Debian 13 / kernel 7.0 with CIX PPA closed-source drivers, on an
Orion O6 / MS-R1 class board. Not reproduced on our stack yet.

### Memory bandwidth

40.1 GB/s measured (8 threads, large buffers) — third-party, CD8180.
We have not re-measured on CD8160.

---

## Reproduce our numbers

```bash
# 1. Pull the models
ollama pull qwen3:0.6b && ollama pull qwen3:4b
ollama pull qwen3:8b   && ollama pull qwen3:30b-a3b

# 2. Run the harness (BENCH_REPEATS controls samples per cell)
BENCH_REPEATS=3 python3 scripts/bench_cix_p1_v2.py qwen3:0.6b qwen3:4b
BENCH_REPEATS=2 python3 scripts/bench_cix_p1_v2.py qwen3:8b qwen3:30b-a3b

# 3. Verify you are not timing a cache
python3 scripts/probe_prefill.py
```

Output is auditable JSON containing machine identity, peak RSS, swap delta, thermal
state, and the GPU-offload line from ollama's own logs.
