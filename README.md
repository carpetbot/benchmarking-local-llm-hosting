# Benchmarking Local LLM Hosting

Real-world benchmarks for running local LLMs on SBCs, Mac Mini, and edge AI hardware.

**Every data point is field-measured, not theoretical.** Vendor spec sheets and "estimated" TOPS numbers are explicitly excluded.

---

## Why this exists

The local-LLM hardware market is full of marketing claims and zero apples-to-apples data. This repo collects measured tokens-per-second, power draw, and total-cost-of-ownership numbers across:

- **SBCs** — Orange Pi 6+, Raspberry Pi 5, Rock 5B, Jetson Orin Nano
- **Apple Silicon** — Mac Mini M4 / M4 Pro
- **AI accelerators** — Hailo-8/8L/10H, Coral, future entrants
- **Hosting** — power, networking, and operational cost

If you're deciding what hardware to deploy for a local LLM workload, this is the data Calvin wanted but couldn't get from vendor slides.

---

## Reports

### 📊 [SBC vs Mac Mini M4 — Cost-Performance Analysis](./reports/sbc-vs-macmini-m4-2026-08.md)
*Aug 2026 · 14 cited sources*

The headline question: **can SBCs compete with Mac Mini M4 for local LLM inference?**

**Answer: no on $/tok/s, yes on edge deployment.** Mac Mini M4 16GB delivers **4× the tokens-per-second** of the Orange Pi 6+ (Vulkan path) for **1.9× the price** — and that's *before* power. With power factored in, the gap widens because the OPi 6+ draws 25W under LLM load, not the 5–10W most marketing material claims.

Headline numbers:

| Device | Sticker | W (load) | tok/s (Qwen 3.5 4B equiv) | tok/$/day @ 24/7 |
|---|---|---|---|---|
| OrangePi 6+ 32GB (Vulkan) | $320 | 25 | 9.9 | 3,557 |
| OrangePi 6+ + Hailo-10H M.2 | $450 | 28 | 11.0 | 3,518 |
| Raspberry Pi 5 + AI HAT+ 2 | $305 | 8 | 11.0 | 12,064 |
| **Mac Mini M4 16GB** | **$599** | 25 | **40.0** | **14,350** |
| **Mac Mini M4 Pro 24GB** | **$1,199** | 35 | **84.0** | **21,401** |

*Full data, methodology, and source citations in the [report](./reports/sbc-vs-macmini-m4-2026-08.md).*

---

## How to contribute data

We accept PRs with new benchmark data. Every submission must include:

1. **Hardware** — exact model, RAM, storage config
2. **Software** — llama.cpp / MLX / Ollama version, commit SHA if built from source
3. **Model** — exact HuggingFace repo + quantization (e.g. `bartowski/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M`)
4. **Workload** — `llama-bench` command, prompt length, generation length
5. **Result** — raw output of `llama-bench` (not paraphrased)
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
│   ├── bench_macmini_mlx.sh
│   └── cost_calc.py
├── data/                       # CSV/JSON of aggregated results
│   └── cost-perf-matrix.csv
├── methodology.md              # How measurements are taken, what's excluded
└── LICENSE
```

---

## Methodology in brief

- **What we measure:** tokens-per-second generation (`tg`), prompt processing (`pp`), peak and idle watts
- **What's excluded:** theoretical TOPS, marketing claims, "estimated" numbers from vendor blogs
- **How we measure:** `llama-bench -m <model> -p 512 -n 128 -t <threads>` for SBC, Ollama API `eval_duration` for Apple Silicon
- **Power:** wall-meter measurement or `powertop` / `smartplug` data, averaged over 30 days where possible
- **Cost-perf formula:** `tok_per_dollar_per_day = (tok/s × hours_per_day × 365) / ((device_USD / lifespan_days) + (watts / 1000 × hours_per_year × $0.11/kWh))`

See [methodology.md](./methodology.md) for the full version.

---

## Roadmap

- [ ] Jetson Orin Nano 8GB benchmarks (claimed 5–10× faster than RK3588 SBCs)
- [ ] AMD Ryzen AI Max mini PCs (Strix Halo, 128GB unified memory)
- [ ] DGX Spark (744 TOPS) for comparison anchor at the high end
- [ ] Multi-node inference (cluster of 4× Mac Mini for 70B models)
- [ ] Power efficiency over time (thermal throttling under sustained load)
- [ ] Real-world RAG workload benchmarks (long context, not synthetic)

---

## License

MIT — fork, remix, and benchmark freely. Citation appreciated.

## Maintainers

Maintained by [Severus](https://github.com/carpetbot) (agent) on behalf of [Shuenrui](https://github.com/shuenrui). Data collected from public community benchmarks plus field measurements on the maintainers' own hardware.

If you spot a number that's wrong or out of date, open an issue.
