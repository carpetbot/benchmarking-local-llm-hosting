# Local LLM on ARM SBC — What a $268.89 Board Actually Does

**First-party research report · CIX P1 CD8160 (Orange Pi 6 Plus 32GB) · 2026-08-27**
**Author:** Severus | **Standard:** primary-measurement-research + The Comparison Standard
**Status:** every performance number below was measured on our own hardware. Nothing inherited.

---

## THE ANSWER FIRST

Three findings, in order of how much money they move:

1. **A 30B MoE decodes 35% faster than a dense 8B on ARM CPU** (6.45 vs 4.79 tok/s),
   while being 3.5x larger on disk. Active parameters drive decode; total parameters
   drive RAM only. **The dense 8B is the worst buy on this board.**
2. **Local inference on this class of hardware is not a cost play.** At the cheapest
   API rate the board pays back in ~58 years on token economics. Buy it for data
   residency, not for savings.
3. **The advertised 45 TOPS is unreachable for LLMs by architecture**, not by driver
   immaturity. We measured zero of it.

---

## 1. THE MEASURED LADDER

Machine: `CIX P1 CD8160 / 12 cores / 30.9GB LPDDR5 / Mali-G720-Immortalis /
ollama 0.18.0 / kernel 6.6.89-cix / Ubuntu Noble`
Conditions: 100% CPU (0 layers offloaded), **no swap configured**, cold prefill
forced with a unique per-run prefix, Q4_K_M, 4096 ctx window.

| model | params active | disk | peak RSS | ctx | prefill tok/s | decode tok/s |
|---|---|---|---|---|---|---|
| qwen3:0.6b dense | 0.6B | 0.5GB | — | 24 | 73.78 | **27.38** |
| qwen3:0.6b dense | 0.6B | 0.5GB | — | 2232 | 49.90 | 12.56 |
| qwen3:4b dense | 4B | 2.5GB | — | 24 | 20.04 | 7.19 |
| qwen3:4b dense | 4B | 2.5GB | — | 2232 | 12.40 | 5.10 |
| qwen3:8b dense | 8B | 5.2GB | 5.58GB | 24 | 77.13 | 4.79 |
| qwen3:8b dense | 8B | 5.2GB | 5.69GB | 2250 | **8.13** | 3.69 |
| qwen3:30b-a3b **MoE** | **3B** | 18GB | 17.81GB | 48 | 24.96 | **6.45** |
| qwen3:30b-a3b **MoE** | **3B** | 18GB | 17.90GB | 2257 | 14.23 | **4.67** |

Thermals: 45°C idle → 72°C sustained. No throttling observed. No swap at any tier.

### Cost per tok/s at 2.2k context (the realistic agent case)

| model | $/tok/s |
|---|---|
| qwen3:0.6b | **$21.41** |
| qwen3:4b | $52.72 |
| qwen3:30b-a3b MoE | $57.58 |
| qwen3:8b dense | **$72.87** ← worst |

---

## 2. THE PREFILL WALL — the number nobody publishes

Decode speed is what gets quoted. Prefill is what you actually feel.

**qwen3:8b with a 2,250-token system prompt: 276.66 seconds — 4 min 37 s of
silence before the first token.** Then it generates at 3.69 tok/s.

At the 0.6B tier the wall is ~45s. At the MoE tier, 158s.

**Implication:** this is not a chat device above ~1B parameters. It is a batch
device. Any product design that puts a human in front of an 8B on this board
with a real system prompt is broken before it ships.

---

## 3. DENSE vs MoE — the finding, and the counter-finding

**Finding:** the 30B MoE beats the dense 8B at every context measured
(6.45 vs 4.79 short; 4.67 vs 3.69 long) despite 3.5x the disk footprint.
3B active parameters vs 8B is the entire explanation. "How big is the model"
is the wrong question. "How many parameters activate per token" is the right one.

**Counter-finding (stated because it cuts against the headline):** the MoE
degrades *slightly faster* with context — −27.6% vs −23.0% for the dense 8B.
I initially wrote that MoE was "gentler on long context." That was wrong and is
retracted. The absolute win holds at every context; the trend claim does not.

**Cost of the MoE win:** 17.9GB RSS vs 5.6GB. On a 16GB board the MoE does not
load at all. The win is only available to the 32GB SKU.

---

## 4. THE 45 TOPS THAT DOES NOT EXIST

The board advertises **45 TOPS (CPU+GPU+NPU combined)**; the Zhouyi NPU alone is
rated 28.8–30 TOPS. LLM inference reaches **none of it**.

- The Zhouyi NPU is an embeddings / agentic-memory processor. It **does not
  perform autoregressive decode at all** — architectural, not a driver gap
  (Interfacing Linux, 2026-05-31; corroborated by minisforum-docs issue #20,
  2026-03-22, on the same CIX P1 silicon).
- Mainstream runtimes (ollama, llama.cpp, LM Studio) do not route to NPUs at all;
  they need hand-converted ONNX on a vendor SDK.
- Our ollama logs confirm `offloaded 0/49 layers to GPU` on every single run.

**Verified headroom we are not using:** llama.cpp built with Vulkan on the Mali
G720 takes the same SoC from 4.3 → 9.9 tok/s (**2.3x**). I confirmed our Mali
exposes `QUEUE_COMPUTE_BIT` under Vulkan 1.3.275 on our Ubuntu/6.6.89-cix stack,
so this is reachable here despite the reference guide targeting Debian 13/kernel 7.0.
**Blocked on one sudo command** (see Open Items).

---

## 5. LOCAL vs API — the economics that kill the pitch

Qwen3-30B-A3B is the one tier where we hold both a measured local number and a
public API price.

API: **$0.048/M input, $0.193/M output** (StreamLake, cheapest of 7 providers,
pricepertoken.com, updated 2026-08-16). Assumed 4:1 input:output agent traffic.

| monthly output | API cost | local duty cycle | payback |
|---|---|---|---|
| 1M tokens | $0.39 | 8.3% | 698 months (58 yrs) |
| 10M tokens | $3.85 | 82.6% | 70 months |
| 100M tokens | $38.50 | **826% — impossible** | n/a |

**The board cannot physically produce 100M output tokens/month at 4.67 tok/s.**
It saturates at ~12M.

**Verdict:** local inference on this hardware class is not a cost play and never
was. The surviving buy reasons are data residency, fixed-budget predictability,
offline operation, and network-independent latency. Anyone pitching SBC local-LLM
on "cheaper than the API" is selling a story the arithmetic does not support.

---

## 6. SKIP LIST

| tier | verdict | failure mode |
|---|---|---|
| **qwen3:8b dense on this board** | **SKIP** | Worst $/tok/s ($72.87). The MoE is faster, the 4B is cheaper. It is the trap tier — looks reasonable on a spec sheet, loses on every measured axis. |
| **16GB SKU for MoE work** | **SKIP** | 17.9GB RSS. The MoE simply does not load. Buying 16GB to run 30B-class MoE is buying a model you cannot open. |
| **This board for interactive chat >4B** | **SKIP** | 4 min 37 s prefill wall on 8B. Batch only. |
| **Any NPU-marketed SBC bought for LLM TOPS** | **SKIP** | The TOPS is unreachable. Buy on memory bandwidth and RAM capacity, never on the TOPS number. |
| **Raspberry Pi 5 16GB as the alternative** | **SKIP** | $205–$299 (Feb–Apr 2026 hikes, Tom's Hardware / Geerling) for 16GB and far less compute. Worse than this board on both axes now. |

## 7. BUY LIST

| tier | verdict |
|---|---|
| **qwen3:0.6b on this board** | **BUY** — 27.38 tok/s, $21.41 per tok/s, genuinely interactive. The only real-time tier. |
| **qwen3:30b-a3b MoE, 32GB SKU** | **BUY** — best quality-per-token available on the box, 4.67 tok/s at agent context, fits with 12GB headroom. |
| **qwen3:4b** | **CONDITIONAL** — the middle. Take it if 0.6B quality is insufficient and 18GB RSS is unaffordable. |

---

## 8. WHAT WOULD CHANGE THESE CONCLUSIONS

| trigger | effect | re-check |
|---|---|---|
| llama.cpp Vulkan build lands | up to 2.3x on every decode row; could move the 8B off the skip list | on sudo access |
| ollama > 0.18.0 installed | unblocks qwen3.8:27b (dense 27B) — the missing tier | next ollama release |
| DRAM prices unwind | board price and the whole $/tok/s table shift | Q4 2026 |
| A 3B-active MoE ships under 8GB RSS | would beat 0.6B on quality at similar speed; changes the buy list | ongoing |

**Not verified in public sources reviewed:** sustained power draw under load
(25W is a vendor claim, we did not measure it); performance on the CD8180 variant;
whether the Vulkan 2.3x reproduces on kernel 6.6.89-cix rather than 7.0.

---

## 9. WHAT WE GOT WRONG (and fixed)

Publishing our own errors, per the standard.

1. **`cost-perf-matrix-v3.csv` claimed this machine was a CD8180 running
   "llama.cpp Vulkan" at 32 tok/s.** It is a **CD8160**, and the Vulkan path
   offloads zero layers. Both errors were copied forward for months because
   nobody ever ran the box. Row now marked `RETRACTED`.
2. **19 of 26 rows in that matrix were `est` with no source.** Now every row
   carries an explicit `evidence` column.
3. **Price was listed at $300.** Actual $268.89 (CNX Software, 2025-10-15).
4. **Our own v2 harness reported 2,899 tok/s prefill** — physically impossible.
   ollama reuses the KV cache on identical prompts, so `prompt_eval_duration`
   timed a cache hit. Cold: **8.13 tok/s**. A **979x** overstatement. The trap:
   *adding repeats for statistical rigor is what introduced it*; the single-run
   v1 numbers were cold and correct. Fixed with a unique per-run prefix.
   New sanity rule: **if prefill exceeds ~20x measured decode on CPU, you are
   timing a cache.**
5. **I claimed MoE degrades more gently with context.** It does not. Retracted
   in §3.

---

## 10. SOURCES

**Timed machines (first-party — ours)**
- `bench_cix_p1.py` / `bench_cix_p1_v2.py`, CIX P1 CD8160, 2026-08-27. Machine ID
  `CIX P1 CD8160/30.9GB/Mali-G720-Immortalis/ollama0.18.0/k6.6.89-cix`.
  Raw JSON: `bench_cix_p1_20260827_104241.json`,
  `bench_cix_p1_v2_20260827_110827.json`, `bench_cix_p1_v2_20260827_114129.json`.
- `probe_prefill.py` — cache-artifact isolation, 2026-08-27.

**Official**
- Orange Pi product page — CIX CD8180/CD8160, 45 TOPS combined, 28.8 TOPS NPU.
- CNX Software, 2025-10-15 — $268.89 for 32GB incl. heatsink + PSU (AliExpress).
- AndroidPimp — CD8180 vs CD8160 clock table (2.8/2.4 vs 2.6/2.2 GHz).

**Third-party timed / technical**
- Interfacing Linux, 2026-05-31 — Zhouyi NPU does not do autoregressive decode;
  llama.cpp+Vulkan on Mali G720 = 4.3 → 9.9 tok/s. Build recipe.
- minisforum-docs issue #20, 2026-03-22 — same CIX P1 silicon, NPU works for
  reference models, LLMs CPU-only, no supported AIPU path.

**Market**
- pricepertoken.com, updated 2026-08-16 — Qwen3-30B-A3B $0.048/$0.193 per M,
  7 providers, StreamLake cheapest.
- Tom's Hardware, Feb 2026 / Jeff Geerling, 2026-04-01 — Pi 5 16GB $205 → $299.99.

**Artifacts**
- `cost-perf-matrix-v6.csv` — 34 rows: 8 MEASURED-FIRST-PARTY, 6 MEASURED,
  18 ESTIMATED, 1 RETRACTED, 1 ESTIMATED-DISPUTED.
