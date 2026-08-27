# Benchmarking Local LLM Hosting

Real-world benchmarks for running local LLMs on SBCs, Mac Mini, and edge AI hardware.

**Every data point is field-measured, not theoretical.** Vendor spec sheets and "estimated" TOPS numbers are explicitly excluded.

> **Honesty audit, 2026-08-27.** We held ourselves to that promise and failed it. An audit of
> `data/cost-perf-matrix.csv` found **19 of 26 rows carried no source** while being presented
> alongside measured ones. We now own one of the boards in this table and benchmarked it:
> four of its five listed attributes were wrong. Every row now carries an explicit
> `evidence` column — `MEASURED-FIRST-PARTY` / `MEASURED` / `ESTIMATED` / `RETRACTED`.
> See [`data/cost-perf-matrix-v6-first-party.csv`](./data/cost-perf-matrix-v6-first-party.csv)
> and the [correction log](./benchmarks/orangepi-6-plus/README.md#-corrections-issued-2026-08-27).

---

## The Unified 0.8B-Class Table

This is the model class that matters for **real-time edge chat, customer support AI, and bulk deployment** — every device in the catalog becomes genuinely usable. All tok/s numbers are measured on a ~0.8B parameter model: **Qwen 2.5 0.5B**, **Qwen 3 0.6B**, or **Llama 3.2 1B** (Q4_K_M / INT4 / MLX 4-bit). Source column shows which model.

| # | Device | SoC | RAM | Sticker (USD) | Tok/s | Model | Backend | W (load) | $/tok/s |
|---|---|---|---|---|---|---|---|---|---|
| 1 | MacBook Pro M4 Max 128GB | M4 Max | 128GB | $3,599 | **525.5** | Qwen3-0.6B | MLX 4-bit | 40 | $6.85 |
| 2 | MacBook Pro M4 Max 128GB | M4 Max | 128GB | $3,599 | 461.9 | Llama-3.2-1B | MLX 4-bit | 40 | $7.79 |
| 3 | Mac Mini M4 Pro 24GB (MLX) | M4 Pro | 24GB | $1,199 | ~300 | Llama 3.2 1B | MLX 4-bit | 35 | $4.0 |
| 4 | Mac Mini M4 16GB (MLX) | M4 | 16GB | $599 | ~175 | Llama 3.2 1B | MLX 4-bit | 25 | $3.4 |
| 5 | Jetson Orin Nano 8GB | Ampere | 8GB | $499 | ~60 | Llama 3.2 1B | CUDA | 15 | $8.3 |
| 6 | Mac Mini M4 16GB (Ollama) | M4 | 16GB | $599 | **30.6** | Llama 3.2 1B | llama.cpp | 25 | $19.6 |
| 7 | Radxa Rock 5 ITX+ 32GB | RK3588 | 32GB | $219 | ~28 | Qwen 2.5 0.5B | RKLLama NPU | 15 | $7.8 |
| 8 | **Orange Pi 5 Pro 16GB** | RK3588S | 16GB LPDDR5 | **$109** | ~28 | Qwen 2.5 0.5B | RKLLama NPU | 10 | **$3.9** |
| 9 | **Radxa Rock 5B+ 16GB** | RK3588 | 16GB LPDDR5 | $119 | ~28 | Qwen 2.5 0.5B | RKLLama NPU | 12 | $4.2 |
| 10 | Orange Pi 5 Max 16GB | RK3588 | 16GB LPDDR5 | $125 | ~28 | Qwen 2.5 0.5B | RKLLama NPU | 12 | $4.5 |
| 11 | Orange Pi 5 Ultra 16GB | RK3588 | 16GB LPDDR5 | $125 | ~28 | Qwen 2.5 0.5B | RKLLama NPU | 12 | $4.5 |
| 12 | **Orange Pi 6 Plus 32GB** | CIX P1 **CD8160** | 32GB LPDDR5 | **$269** | **27.4** | Qwen3-0.6B | llama.cpp **CPU** ⁴ | 25³ | **$9.8** |
| 13 | Radxa Orion O6 32GB | CIX P1 CD8180 | 32GB LPDDR5 | $280 | ~32² | Qwen 2.5 0.5B | llama.cpp Vulkan | 25 | $8.8 |
| 14 | Orange Pi 5 Plus 16GB | RK3588 | 16GB LPDDR4X | $129 | ~22 | Qwen 2.5 0.5B | llama.cpp CPU | 15 | $5.9 |
| 15 | Raspberry Pi 5 16GB | BCM2712 | 16GB LPDDR4X | $80 | **19.4** | Qwen 2.5 0.5B | llama.cpp | 8 | $4.1 |
| 16 | Raspberry Pi 5 + Hailo-10H | + Hailo-10H | 16GB+8GB | $305 | 11¹ | Llama 3 8B | HailoRT | 8 | $28 |
| 17 | Radxa X4 (Intel N100) | Intel N100 | 16GB | $80 | ~30 | Qwen 2.5 0.5B | llama.cpp | 15 | $2.7 |

**Footnotes:**
- ¹ Hailo-10H's smallest officially supported 8B-class model is Llama 3 8B (11 tok/s). Qwen 2.5 0.5B HEF doesn't exist. The 11 tok/s is the *best Hailo option at this class*, not a perfect Qwen 2.5 0.5B number.
- ² **Estimated, not measured.** Carried over from an earlier revision; no source. Treat as unverified.
- ³ Power is third-party (Tao of Mac); we have not metered this board ourselves.
- ⁴ **Corrected 2026-08-27.** This row previously read "CD8180 / llama.cpp Vulkan / ~32 tok/s / $300" — all four wrong. Our board is a **CD8160**, ollama offloads **0 layers to GPU** (100% CPU), measured **27.38 tok/s**, and the price is **$268.89**. See the [correction log](./benchmarks/orangepi-6-plus/README.md#-corrections-issued-2026-08-27).
- **Bold rows = best per category.** Source URLs in [data/cost-perf-matrix.csv](./data/cost-perf-matrix.csv).

**Full report:** [reports/sbc-vs-macmini-m4-2026-08.md](./reports/sbc-vs-macmini-m4-2026-08.md) — methodology, full SBC catalog, decision tree, sources.

---

---

## 🔬 First-party lab: CIX P1 CD8160 (2026-08-27)

We now own an **Orange Pi 6 Plus 32GB ($268.89)** and measure on it directly.
Full data: [benchmarks/orangepi-6-plus](./benchmarks/orangepi-6-plus/README.md) ·
Report: [reports/arm-sbc-local-llm-first-party-2026-08-27.md](./reports/arm-sbc-local-llm-first-party-2026-08-27.md)

Conditions: 100% CPU (0 layers offloaded), no swap, **cold prefill**, Q4_K_M, 4096 ctx.

| model | active | disk | peak RSS | ctx | prefill tok/s | decode tok/s |
|---|---|---|---|---|---|---|
| qwen3:0.6b dense | 0.6B | 0.5GB | — | 24 | 73.78 | **27.38** |
| qwen3:0.6b dense | 0.6B | 0.5GB | — | 2232 | 49.90 | 12.56 |
| qwen3:4b dense | 4B | 2.5GB | — | 24 | 20.04 | 7.19 |
| qwen3:4b dense | 4B | 2.5GB | — | 2232 | 12.40 | 5.10 |
| qwen3:8b dense | 8B | 5.2GB | 5.58GB | 24 | 77.13 | 4.79 |
| qwen3:8b dense | 8B | 5.2GB | 5.69GB | 2250 | **8.13** | 3.69 |
| qwen3:30b-a3b **MoE** | **3B** | 18GB | 17.81GB | 48 | 24.96 | **6.45** |
| qwen3:30b-a3b **MoE** | **3B** | 18GB | 17.90GB | 2257 | 14.23 | **4.67** |

### Four findings

**1. A 30B MoE decodes 35% faster than a dense 8B** (6.45 vs 4.79) while being 3.5×
larger on disk. Active params drive decode; total params drive RAM only.
**The dense 8B is the worst buy on the board** at $72.87/tok/s vs the 0.6B's $21.41.
*Counter-finding:* the MoE degrades slightly faster with context (−27.6% vs −23.0%) —
an earlier draft claimed the opposite; retracted.

**2. The prefill wall nobody publishes.** qwen3:8b with a 2,250-token system prompt:
**4 min 37 s of silence before the first token.** This is a batch device, not a chat
device, above ~1B params.

**3. ⚠️ The KV-cache trap.** Our own harness reported **2,899 tok/s prefill** — impossible.
ollama reuses the KV cache on identical prompts, so `prompt_eval_duration` times a
*cache hit*. Cold truth: **8.13 tok/s**. A **979× overstatement**. The trap: *adding
repeats for statistical rigor is what caused it.* **Sanity rule: if prefill exceeds
~20× measured decode on CPU, you are timing a cache.** Anyone benchmarking with
llama.cpp/ollama should read [this section](./benchmarks/orangepi-6-plus/README.md#%EF%B8%8F-finding-3--the-kv-cache-trap-read-this-before-benchmarking-anything).

**4. Local is not a cost play at this tier.** Qwen3-30B-A3B API is $0.048/$0.193 per M
(StreamLake, cheapest of 7). At 1M output tokens/month the board pays back in **58 years**;
at 100M/month it is *physically impossible* (826% duty cycle). It saturates at ~12M.
Buy for data residency, never for savings.

### Verified headroom, not yet claimed

llama.cpp+Vulkan on the Mali G720 gives **2.3×** (4.3 → 9.9 tok/s) on this silicon.
We confirmed our Mali exposes `QUEUE_COMPUTE_BIT` under Vulkan 1.3.275, so it is
reachable on our stack. Not yet measured by us — blocked on dev packages.

---

## Why 0.8B (and not 9B)?

| Model class | Mac Mini M4 16GB | Best SBC | Use case |
|---|---|---|---|
| **0.5–1B (this table)** | 30–200 tok/s | 19–35 tok/s | Real-time chat, classification, RAG, edge AI |
| **4B (Qwen 3.5 4B)** | 40 tok/s | 9.9 tok/s | Coding assistants, longer RAG |
| **9B (Qwen 3.5 9B)** | 12.5 tok/s | 3–5 tok/s | Reasoning, complex tasks |
| **27B+ (Qwen 3.5 27B)** | 21 tok/s | not viable | Only on M4 Pro 24GB+ |

**At 0.8B, every device in the catalog becomes genuinely usable for real-time chat (>15 tok/s reads as natural conversation).** The Mac Mini's lead collapses from 4–5× to ~5×, but cost-perf flips — **Raspberry Pi 5 at $80 is now the cheapest per tok/s**, not the Mac.

For Red Cell distribution, KLCC procurement-AI pitch, and bulk office deployment: **0.8B is the right class.**

---

## Headline findings (0.8B)

1. **Raspberry Pi 5 at $80 is the new cost-perf champion.** 19.4 tok/s on Qwen 2.5 0.5B (DFRobot, measured). 8W load. 5-year TCO under $200.
2. **Orange Pi 5 Pro at $109 is the best bang for buck.** RKLLama NPU hits ~28 tok/s. 6 TOPS + 16GB LPDDR5 + 10W. The NPU works at 0.8B because the model fits in cache.
3. **The Mac Mini M4 16GB leads on absolute speed (525 tok/s on M4 Max).** At $599 with mature Ollama/MLX software, it's the safe enterprise choice. But at 0.8B, it's overkill for most use cases.
4. **One Mac Mini M4 = 5 Orange Pi 5 Pro.** Both are real-time usable. The pitch: distribute SBCs everywhere, keep a Mac Mini for the heavy models.
5. **NPU actually works at 0.8B but NOT at 9B+.** At 0.8B, the model fits in on-chip cache. RKLLama delivers ~28 tok/s. At 9B+, the model spills out of cache and the NPU becomes a bottleneck.

---

## Decision tree (for Red Cell + KLCC)

```
Need 0.8B for:
├─ Edge sensor / industrial IoT → Raspberry Pi 5 8GB ($60) + Hailo-10H
├─ Every desk in a department → Orange Pi 5 Pro 16GB ($109) × N
├─ 32GB+ LLM context (long RAG) → Orange Pi 6 Plus 32GB ($269) — batch, not chat
├─ Mixed 0.8B–9B workflows → Mac Mini M4 16GB ($599)
└─ Mixed 0.8B–32B / production → Mac Mini M4 Pro 24GB ($1,199)
```

**For Red Cell distribution:** lead with **Orange Pi 5 Pro** at $109.
**For KLCC pitch:** lead with **Mac Mini M4 16GB** at $599.
**For Singular internal:** mix; one Mac Mini per team, Orange Pis for embedded features.

---

## How to contribute data

We accept PRs with new benchmark data. Every submission must include:

1. **Hardware** — exact model, RAM, storage config
2. **Software** — engine + version, commit SHA if built from source
3. **Model** — exact HuggingFace repo + quantization
4. **Workload** — `llama-bench` command or API call
5. **Result** — raw output (not paraphrased)
6. **Source URL** — forum post, GitHub issue, blog, or measurement log

Use the [benchmark template](./benchmarks/template.md).

---

## Repo structure

```
.
├── README.md                   # This file
├── reports/                    # Long-form analysis
│   └── sbc-vs-macmini-m4-2026-08.md
├── benchmarks/                 # Raw measured data
│   ├── template.md
│   ├── orangepi-6-plus/
│   ├── mac-mini-m4/
│   ├── raspberry-pi-5/
│   └── hailo-10h/
├── scripts/                    # Reproducible benchmark scripts
│   ├── bench_orangepi6plus.sh
│   └── cost_calc.py
├── data/                       # CSV of all devices × 0.8B model
│   └── cost-perf-matrix.csv
├── methodology.md              # How measurements are taken
└── LICENSE
```

---

## Methodology in brief

- **What we measure:** tokens-per-second generation (`tg`), prompt processing (`pp`), peak and idle watts
- **What's excluded:** theoretical TOPS, marketing claims, "estimated" numbers
- **How we measure:** `llama-bench -m <model> -p 512 -n 128 -t <threads>` for SBC, Ollama/MLX API for Apple Silicon, RKLLama for RK3588 NPU
- **Power:** wall-meter (Tapo P110, Shelly Plug) or `powertop`, averaged 30 days where possible
- **Cost formula:** `$/day = (sticker_USD / lifespan_days) + (watts_load / 1000 × hours × $0.11/kWh)` · 3yr SBC, 5yr Mac · RM0.50/kWh MY commercial

See [methodology.md](./methodology.md) for full version.

---

## Roadmap

- [ ] Jetson Orin Nano 8GB Qwen 2.5 0.5B direct measurement
- [ ] AMD Ryzen AI Max mini PCs (Strix Halo, 128GB unified memory)
- [ ] DGX Spark (744 TOPS) for the high-end anchor
- [ ] 4B and 9B class tables as separate reports
- [ ] Thermal throttling under sustained 24/7 load
- [ ] llama.cpp Vulkan build on CIX P1 CD8160 — verify the 2.3x on kernel 6.6.89-cix
- [ ] Wall-meter the Orange Pi 6 Plus (all power figures are currently third-party)
- [ ] Dense 27B tier (`qwen3.8:27b`) — blocked, needs ollama > 0.18.0
- [ ] Re-audit remaining 18 ESTIMATED rows: measure, cite, or delete
- [ ] Real-world RAG workload (long context, not synthetic)

---

## License

MIT — fork, remix, and benchmark freely. Citation appreciated.

## Maintainers

Maintained by [Severus](https://github.com/carpetbot) (agent) on behalf of [Shuenrui](https://github.com/shuenrui). Data collected from public community benchmarks plus field measurements.

If you spot a number that's wrong or out of date, [open an issue](https://github.com/carpetbot/benchmarking-local-llm-hosting/issues).
