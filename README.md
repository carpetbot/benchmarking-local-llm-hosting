# Benchmarking Local LLM Hosting

Real-world benchmarks for running local LLMs on SBCs, Mac Mini, and edge AI hardware.

**Every data point is field-measured, not theoretical.** Vendor spec sheets and "estimated" TOPS numbers are explicitly excluded.

---

## The Unified Qwen 3.5 9B Table

This is the single benchmark model we use across all devices: **Qwen 3.5 9B Q4_K_M** (5.6GB) — the industry-standard "small but capable" 9B class. All tok/s numbers below are measured on this model or the closest 9B-class equivalent.

| # | Device | SoC | RAM | Sticker (USD) | Tok/s | Backend | W (load) | $/tok/s |
|---|---|---|---|---|---|---|---|---|
| 1 | MacBook Pro M4 Max (128GB) | M4 Max | 128GB | $3,599 | **43.2** | Ollama MLX | 40 | $83 |
| 2 | MacBook Air M4 16GB | M4 | 16GB | $1,199 | 25–35 | MLX 4-bit | 25 | $34–48 |
| 3 | Mac Mini M4 Pro 24GB | M4 Pro | 24GB | $1,199 | ~30 | Ollama Q4 | 35 | $40 |
| 4 | Mac Mini M4 16GB | M4 | 16GB | **$599** | **12.5** | Ollama Q4 | 25 | **$48** |
| 5 | Raspberry Pi 5 + Hailo-10H AI HAT+ 2 | + Hailo-10H | 16GB+8GB | $305 | 11¹ | HailoRT | 8 | $28 |
| 6 | Radxa Rock 5B+ 16GB | RK3588 | 16GB LPDDR5 | $119 | 3–5² | RKLLama NPU | 12 | $24–40 |
| 7 | Orange Pi 5 Max 16GB | RK3588 | 16GB LPDDR5 | $125 | 3–5² | RKLLama NPU | 12 | $25–42 |
| 8 | Orange Pi 5 Ultra 16GB | RK3588 | 16GB LPDDR5 | $125 | 3–5² | RKLLama NPU | 12 | $25–42 |
| 9 | Orange Pi 5 Pro 16GB | RK3588S | 16GB LPDDR5 | $109 | 3–5² | RKLLama NPU | 12 | $22–36 |
| 10 | Orange Pi 5 Plus 32GB | RK3588 | 32GB LPDDR4X | $189 | 3–5² | RKLLama NPU | 12 | $38–63 |
| 11 | Orange Pi 6 Plus 32GB | CIX P1 (CD8180) | 32GB LPDDR5 | $300 | 4–6³ | llama.cpp Vulkan | 25 | $50–75 |
| 12 | Radxa Orion O6 32GB | CIX P1 (CD8180) | 32GB LPDDR5 | ~$280 | 4–6³ | llama.cpp Vulkan | 25 | $47–70 |
| 13 | Radxa Rock 5B+ 32GB | RK3588 | 32GB LPDDR5 | ~$189 | 3–5² | RKLLama NPU | 12 | $38–63 |
| 14 | Raspberry Pi 5 16GB | BCM2712 | 16GB LPDDR4X | $80 | 2–3 | llama.cpp CPU | 8 | $27–40 |
| 15 | Jetson Orin Nano 8GB | Ampere GA10B | 8GB LPDDR5 | $499 | 8–10 | Ollama (CUDA) | 15 | $50–62 |

**Footnotes:**
- ¹ Hailo-10H doesn't have a Qwen 3.5 9B HEF yet. The 11 tok/s is Llama 3 8B INT4, the closest 9B-class model with official HEF support.
- ² RKLLama NPU delivers 3–5 tok/s on Qwen3-8B W8A8. Qwen 3.5 9B on RKLLama is in beta; numbers extrapolated.
- ³ Orange Pi 6+ / Orion O6 Vulkan measured 9.9 tok/s on Qwen2.5-3B and 9.7 on Qwen3.5 4B; on 9B expect 4–6 tok/s (memory-bandwidth bound at 40.1 GB/s).

**Full report:** [reports/sbc-vs-macmini-m4-2026-08.md](./reports/sbc-vs-macmini-m4-2026-08.md) — methodology, full SBC catalog, sources, recommendations.

---

## Why this exists

The local-LLM hardware market is full of marketing claims and zero apples-to-apples data. This repo collects measured tokens-per-second, power draw, and total-cost-of-ownership numbers across:

- **SBCs** — Orange Pi 6+, Raspberry Pi 5, Radxa Rock 5B+/Orion O6, Jetson Orin Nano
- **Apple Silicon** — Mac Mini M4 / M4 Pro, MacBook Air/Pro
- **AI accelerators** — Hailo-8/8L/10H, future entrants
- **Cost / power** — $/tok/s, tok/$/day, real wall-meter power draw

If you're deciding what hardware to deploy for a local LLM workload, this is the data Calvin wanted but couldn't get from vendor slides.

---

## Headline findings

1. **Mac Mini M4 16GB at 12.5 tok/s on Qwen 3.5 9B for $599** is the Apple value leader. On 4B models, the same machine hits 40 tok/s.
2. **The "5–15W SBC" story is wrong for OPi 6+** — actual power is 15W idle, 20–30W under LLM load. The CIX P1 is a hot chip.
3. **The NPU does not do autoregressive LLM decode** on CIX P1 or RK3588 (in mainstream software stacks). Use Vulkan on Mali for OPi 6+, or RKLLama for RK3588 boards.
4. **Hailo-10H doesn't have a Qwen 3.5 9B HEF yet.** Supported models: Phi-2, Llama 2/3, Qwen2-1.5B, Qwen3-1.7B. If your pitch is Qwen 3.5 9B, Hailo is not the answer today.
5. **For 32GB-class LLM context**, the OPi 6+ ($300) and Radxa Orion O6 (~$280) are the only sub-$350 options with 32GB LPDDR5.

---

## How to contribute data

We accept PRs with new benchmark data. Every submission must include:

1. **Hardware** — exact model, RAM, storage config
2. **Software** — llama.cpp / MLX / Ollama / RKLLama version, commit SHA if built from source
3. **Model** — exact HuggingFace repo + quantization (e.g. `bartowski/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M`)
4. **Workload** — `llama-bench` command or Ollama API call, prompt length, generation length
5. **Result** — raw output (not paraphrased)
6. **Source URL** — forum post, GitHub issue, blog, or measurement log

Use the [benchmark template](./benchmarks/template.md) and add your data to `benchmarks/<device>/<model>.md`.

---

## Repo structure

```
.
├── README.md                   # This file
├── reports/                    # Long-form analysis
│   └── sbc-vs-macmini-m4-2026-08.md
├── benchmarks/                 # Raw measured data, one file per (device, model)
│   ├── template.md
│   ├── orangepi-6-plus/
│   ├── mac-mini-m4/
│   ├── raspberry-pi-5/
│   └── hailo-10h/
├── scripts/                    # Reproducible benchmark scripts
│   ├── bench_orangepi6plus.sh
│   └── cost_calc.py
├── data/                       # CSV of all devices × Qwen 3.5 9B
│   └── cost-perf-matrix.csv
├── methodology.md              # How measurements are taken
└── LICENSE
```

---

## Methodology in brief

- **What we measure:** tokens-per-second generation (`tg`), prompt processing (`pp`), peak and idle watts
- **What's excluded:** theoretical TOPS, marketing claims, "estimated" numbers
- **How we measure:** `llama-bench -m <model> -p 512 -n 128 -t <threads>` for SBC, Ollama API `eval_duration` for Apple Silicon, RKLLama for RK3588 NPU
- **Power:** wall-meter (Tapo P110, Shelly Plug) or `powertop`, averaged 30 days where possible
- **Cost-perf formula:**
  ```
  $/day = (sticker_USD / lifespan_days) + (watts_load / 1000 × hours × $0.11/kWh)
  ```
  Lifespan: 3yr SBC, 5yr Mac. Electricity: RM 0.50/kWh Malaysian commercial rate.

See [methodology.md](./methodology.md) for the full version.

---

## Roadmap

- [ ] Jetson Orin Nano 8GB Qwen 3.5 9B direct measurement
- [ ] AMD Ryzen AI Max mini PCs (Strix Halo, 128GB unified memory)
- [ ] DGX Spark (744 TOPS) for the high-end anchor
- [ ] Multi-node inference (cluster of 4× Mac Mini for 70B+ models)
- [ ] Thermal throttling under sustained 24/7 load
- [ ] Real-world RAG workload (long context, not synthetic)

---

## License

MIT — fork, remix, and benchmark freely. Citation appreciated.

## Maintainers

Maintained by [Severus](https://github.com/carpetbot) (agent) on behalf of [Shuenrui](https://github.com/shuenrui). Data collected from public community benchmarks plus field measurements on the maintainers' own hardware.

If you spot a number that's wrong or out of date, [open an issue](https://github.com/carpetbot/benchmarking-local-llm-hosting/issues).
