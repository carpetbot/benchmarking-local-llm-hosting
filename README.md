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

## ⚠️ 2026 PRICE COLLAPSE — this table's cost rankings are void

**Read this before using any number below.** The DRAM shortage repriced the entire
SBC market between late 2025 and April 2026. **Every price this repo originally
published is stale**, and the two headline "cost-perf champion" claims are dead.

| device | price in old table | Aug 2026 | change | source |
|---|---|---|---|---|
| Raspberry Pi 5 16GB | $80 | **$299.99** | **+275%** | [Geerling, 2026-04-01](https://www.jeffgeerling.com/blog/2026/dram-pricing-is-killing-the-hobbyist-sbc-market) |
| Raspberry Pi 5 8GB | $60 | **$175** | +192% | [CNX, 2026-04-28](https://www.cnx-software.com/2026/04/28/what-a-difference-two-years-make-comparing-sbc-prices-in-2024-and-2026) |
| Radxa X4 (N100) 8GB | $79.96 | **$265.99** | **+233%** | CNX, 2026-04-28 |
| Orange Pi 5 Ultra 16GB | $125 | **$309** | +147% | CNX, 2026-04-28 |
| Radxa Rock 5B+ 8GB | $90 | **$129.99** (sold out) | +44% | CNX, 2026-04-28 |
| Mac Mini M4 16GB | $599 | **$799** | +33% | [MacRumors, 2026-05-01](https://www.macrumors.com/2026/05/01/mac-mini-now-starts-at-799) — $599 SKU discontinued |
| Jetson Orin Nano Super | $499 | **$399** | −20% | [HW Busters](https://hwbusters.com/news/nvidia-jetson-prices-jump-up-to-101-the-249-orin-nano-super-is-now-399) — NVIDIA repriced $249→$399; our $499 was the *old* non-Super kit |
| **Orange Pi 6 Plus 32GB** | $300 | **$268.89** | −10% | [CNX, 2025-10-15](https://www.cnx-software.com/2025/10/15/orange-pi-6-plus-cix-p1-sbc-64gb-lpddr5-45-tops-ai-performance) |

Jeff Geerling's read, which we agree with:
> *"Unless the DRAM pricing situation changes radically, the hobbyist SBC market is
> dying — or at least on life support. LPDDR chips now account for the majority of
> board cost."*

### Two dead claims, retracted

**❌ "Raspberry Pi 5 at $80 is the new cost-perf champion."**
The tok/s (19.4, DFRobot) is real. The price is **2.5–3.7× stale**.
$/tok/s: $4.12 → **$15.46**. The claim is void.

**❌ "Orange Pi 5 Pro at $109 is the best bang for buck — RKLLama NPU ~28 tok/s."**
That 28 was `ESTIMATED` with **no source**, and it was copy-pasted across **8 different
boards spanning 3 SoCs**. Real published RK3588 NPU figures:

| model | quant | tok/s | source |
|---|---|---|---|
| Qwen2 0.5B | W8A8 | **42.58** | Rockchip official (via tinycomputers.io) |
| TinyLlama 1.1B | W8A8 | 10–15 | Rockchip official |
| Qwen2.5 1.5B | W4A16 | 19.55 | [Hackster](https://www.hackster.io/HanzoHuang/run-an-llm-on-rk3576-rk3588-with-one-command-6f4f77) |
| Qwen3 1.7B | W4A16 | 13.31 | Hackster |
| Qwen3 4B | W4A16 | 8.30 | Hackster |

The "~28" matches **none** of them — it looks like an average across different models,
quantizations and SoCs, which must never be averaged. Claim withdrawn.

---

## The honest table: both price AND tok/s sourced

Only three rows in this entire repo survive that test today.

| # | device | price (dated) | tok/s | $/tok/s | evidence |
|---|---|---|---|---|---|
| 1 | **Orange Pi 6 Plus 32GB** (ours) | $268.89 (2025-10) | **27.38** | **$9.82** | `MEASURED-FIRST-PARTY` |
| 2 | Raspberry Pi 5 16GB | $299.99 (2026-04) | 19.40 | $15.46 | tok/s measured (DFRobot) |
| 3 | Mac Mini M4 16GB (Ollama) | $799 (2026-05) | 30.60 | $26.11 | tok/s measured (Geeky Gadgets) |

**The board we own now leads on cost-perf** — not because it got faster, but because
everything else got expensive. That reversal was invisible while the Pi was priced at $80.

### Everything else (retained, explicitly downgraded)

These rows have a **measured tok/s but a stale price**, so treat the speed as real and
the ranking as void:

| device | tok/s | model | backend | price status |
|---|---|---|---|---|
| MacBook Pro M4 Max 128GB | 525.5 / 461.9 | Qwen3-0.6B / Llama-3.2-1B | MLX 4-bit | $3,599 unverified for 2026 |
| Mac Mini M4 16GB | 30.6 | Llama 3.2 1B | llama.cpp | repriced to $799 |
| Raspberry Pi 5 16GB | 19.4 / 18.4 | Qwen 2.5 0.5B / TinyLlama 1.1B | llama.cpp | repriced to $299.99 |
| Raspberry Pi 5 + Hailo-10H | 11 | Llama 3 8B | HailoRT | $305 unverified |

And these are **`ESTIMATED` — no source, do not quote**: Orange Pi 5 Pro/Max/Ultra/Plus,
Radxa Rock 5B+ (all RAM tiers), Rock 5 ITX+, Rock 5T, Radxa X4, Radxa Orion O6,
Jetson Orin Nano, and all MLX projections. **19 devices total.** See
[`data/cost-perf-matrix-v6-first-party.csv`](./data/cost-perf-matrix-v6-first-party.csv).

---

## Why 0.8B (and not 9B)?

| Model class | Mac Mini M4 16GB | Best SBC | Use case |
|---|---|---|---|
| **0.5–1B (this table)** | 30–200 tok/s | 19–35 tok/s | Real-time chat, classification, RAG, edge AI |
| **4B (Qwen 3.5 4B)** | 40 tok/s | 9.9 tok/s | Coding assistants, longer RAG |
| **9B (Qwen 3.5 9B)** | 12.5 tok/s | 3–5 tok/s | Reasoning, complex tasks |
| **27B+ (Qwen 3.5 27B)** | 21 tok/s | not viable | Only on M4 Pro 24GB+ |

**At 0.8B, every device in the catalog becomes genuinely usable for real-time chat (>15 tok/s reads as natural conversation).** That observation still holds. The *cost* conclusion that used to follow it does not: at Aug-2026 prices the cheapest-per-tok/s board is the one we measured ($9.82), not the Raspberry Pi ($15.46 at $299.99).

For Red Cell distribution, KLCC procurement-AI pitch, and bulk office deployment: **0.8B is the right class.**

---

## Headline findings

*Rewritten 2026-08-27. The previous five findings were priced on a market that no
longer exists; three of them were also built on unsourced numbers. Superseded list
is preserved in git history.*

**1. A 30B MoE decodes 35% faster than a dense 8B on ARM CPU.**
Measured on our board: 6.45 vs 4.79 tok/s short-context, 4.67 vs 3.69 at 2.2k.
The MoE is **3.5× larger on disk**. Active parameters (3B vs 8B) drive decode;
total parameters drive RAM only. *"How big is the model"* is the wrong question.
**This is the only finding here that price changes cannot invalidate** — it is a
fact about architecture, not about DRAM.
*Counter-finding:* the MoE degrades slightly **faster** with context (−27.6% vs
−23.0%). An earlier draft claimed the opposite; retracted.

**2. The dense 8B is the worst buy on the board.** $72.87/tok/s vs $21.41 for the
0.6B and $57.58 for the 30B MoE. It looks perfectly reasonable on a spec sheet and
loses on every measured axis. **Trap tier.**

**3. The prefill wall nobody publishes.** qwen3:8b with a 2,250-token system prompt:
**4 min 37 s of silence before the first token.** Then 3.69 tok/s. Above ~1B
parameters this is a batch device, not a chat device. Every published SBC tok/s
figure we could find is a short-prompt number.

**4. Vendor NPU TOPS is unreachable for LLM decode.** Our board advertises 45 TOPS
combined / 28.8–30 NPU. LLM inference reaches **none** of it — the Zhouyi NPU does
not perform autoregressive decode at all (architectural, not a driver gap), and no
mainstream runtime routes to NPUs anyway.
**Buy on memory bandwidth and RAM capacity. Never on the TOPS number.**
*This also retires the old finding #5 ("NPU works at 0.8B but not 9B+"), which was
built on the unsourced ~28 tok/s figure.*

**5. Local inference is not a cost play at this tier.** Qwen3-30B-A3B API costs
$0.048/$0.193 per M tokens (StreamLake, cheapest of 7 providers). At 1M output
tokens/month our $268.89 board pays back in **58 years**; at 100M/month it is
*physically incapable* (826% duty cycle). It saturates around 12M.
Buy for data residency, fixed-budget predictability, offline operation — never for
savings.

**6. The market moved more than the hardware did.** Between late 2025 and Apr 2026,
SBC prices moved −20% to **+275%**. The Pi 5 16GB went $80 → $299.99; the Radxa X4
went $79.96 → $265.99. Any local-AI cost analysis older than about three months is
now wrong, including every earlier revision of this repo.

---

## Decision tree (for Red Cell + KLCC)

⚠️ **Prices below are Aug-2026 and were moving fast.** Re-verify before quoting a client.

```
Need local inference for:
├─ Interactive chat (>15 tok/s)     → 0.6B-class ONLY. Nothing bigger is interactive
│                                     on an SBC. Our board: 27.4 tok/s, $9.82/tok/s.
├─ Best quality on one SBC          → 30B MoE (3B active) on a 32GB board.
│                                     4.67 tok/s at agent context. Batch workloads.
├─ Anything >4B with a real prompt  → accept a 2-5 minute wait before the first
│                                     token, or do not use an SBC.
├─ Absolute speed, budget available → Mac Mini M4 ($799, was $599 — SKU discontinued)
└─ Cheapest per tok/s today         → the 32GB CIX P1 board, by default, because the
                                      cheap alternatives repriced above it.
```

**Honest position for Red Cell:** the "distribute cheap SBCs everywhere" pitch was
built on $80–$109 boards. **Those prices are gone.** At $175–$309 per board the
economics need re-deriving from scratch, and the API comparison (finding #5) says
the case must rest on data residency, not cost.

**For KLCC / procurement:** lead with data residency and predictable fixed cost.
Do **not** lead with "cheaper than the API" — the arithmetic does not support it.

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
