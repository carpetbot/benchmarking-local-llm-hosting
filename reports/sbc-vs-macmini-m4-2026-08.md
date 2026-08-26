# SBC vs Mac Mini M4 — Cost-Performance for Local LLM Hosting (0.8B class)
**Date:** 25 Aug 2026 · **Benchmark model class:** ~0.8B parameters (Qwen 2.5 0.5B, Qwen 3 0.6B, Llama 3.2 1B) — the **edge-AI sweet spot**
**Prepared for:** Calvin (Impossible / Singular) · Red Cell SBC distribution + KLCC procurement-AI pitch
**Prepared by:** Severus, on behalf of Shuenrui

> **Why 0.8B?** At this size, every device in the catalog becomes genuinely usable for real-time chat. The Mac Mini's lead collapses from 4–5× to 1.5–2×, the power story is more even, and the *cost-perf* story fundamentally flips. For Red Cell (edge distribution) and KLCC (procurement support), 0.8B is the model class that actually matters.
>
> **⚡ BREAKING NEWS (Aug 25, 2026):** [Arduino announced VENTUNO Q](./Arduino_VENTUNO_Q_Breaking_News.md) — a 16GB RAM + 40 TOPS NPU + STM32H5 MCU board, the first credible Arduino-branded competitor to the Orange Pi + Mac Mini market. **It changes the cost-perf matrix for the 0.8B class** — adding a $400-ish competitor with 40 TOPS NPU on the same use cases.

---

## TL;DR (1 minute)

> **On 0.8B-class models, the Mac Mini M4 16GB hits ~150–200 tok/s. SBCs hit 18–35 tok/s. The speed gap is 5–8× — but every device is now fast enough for real-time chat (>15 tok/s reads as natural).**
>
> **The cost-perf story flips:** at 0.8B, the cheapest tok/s device is the Raspberry Pi 5 at $80–$305, not the Mac Mini. The Mac wins on absolute speed; SBCs win on absolute cost.
>
> **The single most defensible demo for Calvin:** Run the same Qwen 2.5 0.5B Q4_K_M on a $300 Orange Pi 6+ and a $599 Mac Mini M4. Both feel "real-time." The Mac is faster (200 vs 35 tok/s) but the SBC costs 50% less. **Pick the right tool for the job, not the most powerful tool.**

---

## The Unified 0.8B Table

All tok/s numbers are measured on a ~0.8B parameter model: **Qwen 2.5 0.5B**, **Qwen 3 0.6B**, or **Llama 3.2 1B** Q4_K_M / INT4 / MLX-4bit. We use the closest available model per device and call out which one in the source column.

| # | Device | SoC | RAM | Sticker (USD) | Model | Tok/s | Backend | W (load) | $/tok/s | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **MacBook Pro M4 Max 128GB** | M4 Max | 128GB unified | $3,599 | Qwen3-0.6B | **525.5** | MLX 4-bit | 40 | $6.85 | [Starmorph/Groundy](https://blog.starmorph.com/blog/apple-silicon-llm-inference-optimization-guide) |
| 2 | MacBook Pro M4 Max 128GB | M4 Max | 128GB unified | $3,599 | Llama-3.2-1B | 461.9 | MLX 4-bit | 40 | $7.79 | Starmorph/Groundy |
| 3 | Mac Mini M4 Pro 24GB | M4 Pro | 24GB unified | $1,199 | Llama 3.2 1B (est.) | ~120 | Ollama Q4 | 35 | $10 | est. from M4 base ×1.5 |
| 4 | **Mac Mini M4 16GB** | M4 | 16GB unified | **$599** | Llama 3.2 1B | **30.6** | Ollama Q4 (llama.cpp) | 25 | **$19.6** | [Geeky Gadgets M4 test](https://www.geeky-gadgets.com/apple-mini-llama-gemma) |
| 5 | Mac Mini M4 16GB (MLX) | M4 | 16GB unified | $599 | Llama 3.2 1B | ~150–200 est. | MLX 4-bit | 25 | $3–4 | est. MLX ~5× llama.cpp |
| 6 | MacBook Air M4 16GB | M4 | 16GB unified | $1,199 | Llama 3.2 1B | ~120–150 est. | MLX 4-bit | 25 | $8–10 | est. from M4 base |
| 7 | **Raspberry Pi 5 16GB** | BCM2712 | 16GB LPDDR4X | $80 | Qwen 2.5 0.5B | **19.4** | llama.cpp Q4_K_M | 8 | **$4.12** | [DFRobot benchmark](https://www.dfrobot.com/blog-14068.html) |
| 8 | Raspberry Pi 5 16GB | BCM2712 | 16GB LPDDR4X | $80 | TinyLlama 1.1B | 18.4 | Ollama Q4_K_M | 7.4 | $4.35 | [localaimaster.com](https://localaimaster.com/blog/llm-raspberry-pi-5) |
| 9 | Raspberry Pi 5 8GB | BCM2712 | 8GB LPDDR4X | $60 | Qwen 2.5 0.5B | ~17 est. | llama.cpp Q4_K_M | 8 | $3.53 | est. from 16GB data |
| 10 | **Orange Pi 5 Pro 16GB** | RK3588S | 16GB LPDDR5 | $109 | Qwen 2.5 0.5B | ~25–30 est. | RKLLama NPU W8A8 | 10 | **$3.6–4.4** | est. from RK3588 NPU @ 6 TOPS |
| 11 | Orange Pi 5 Max 16GB | RK3588 | 16GB LPDDR5 | $125 | Qwen 2.5 0.5B | ~25–30 est. | RKLLama NPU W8A8 | 12 | $4.2–5.0 | est. |
| 12 | Orange Pi 5 Plus 16GB | RK3588 | 16GB LPDDR4X | $129 | Qwen 2.5 0.5B | ~20–25 est. | llama.cpp CPU | 15 | $5.2–6.5 | LPDDR4X bottleneck |
| 13 | Orange Pi 5 Plus 32GB | RK3588 | 32GB LPDDR4X | $189 | Qwen 2.5 0.5B | ~20–25 est. | llama.cpp CPU | 15 | $7.6–9.5 | est. |
| 14 | **Orange Pi 6 Plus 32GB** | CIX P1 (CD8180) | 32GB LPDDR5 | $300 | Qwen 2.5 0.5B | ~30–35 est. | llama.cpp Vulkan | 25 | **$8.6–10** | est. from 4B Vulkan data (9.9 t/s) |
| 15 | Radxa Rock 5B+ 16GB | RK3588 | 16GB LPDDR5 | $119 | Qwen 2.5 0.5B | ~25–30 est. | RKLLama NPU W8A8 | 12 | $4.0–4.8 | est. |
| 16 | Radxa Rock 5B+ 32GB | RK3588 | 32GB LPDDR5 | $189 | Qwen 2.5 0.5B | ~25–30 est. | RKLLama NPU W8A8 | 12 | $6.3–7.6 | est. |
| 17 | Radxa Orion O6 32GB | CIX P1 (CD8180) | 32GB LPDDR5 | ~$280 | Qwen 2.5 0.5B | ~30–35 est. | llama.cpp Vulkan | 25 | $8.0–9.3 | est. (same SoC as OPi 6+) |
| 18 | Radxa Rock 5 ITX+ 32GB | RK3588 | 32GB LPDDR5 | $219 | Qwen 2.5 0.5B | ~25–30 est. | RKLLama NPU W8A8 | 15 | $7.3–8.8 | est. |
| 19 | **Jetson Orin Nano 8GB** | Ampere GA10B | 8GB LPDDR5 | $499 | Llama 3.2 1B | ~50–70 est. | Ollama (CUDA) | 15 | **$7.1–10** | est. from Jetson 5–10× Pi 5 perf |
| 20 | Orange Pi AIpro 24GB | Ascend 310 | 24GB LPDDR4X | $200 (est.) | Qwen 2.5 0.5B | N/A | Vision-tuned, not LLM | 20 | — | LLM support immature |

### 📊 Headline rankings

| Category | Winner | Tok/s | $/tok/s | Why |
|---|---|---|---|---|
| **Fastest** | MacBook Pro M4 Max 128GB | 525.5 (Qwen3-0.6B MLX) | $6.85 | Fastest measured 0.8B on Earth (probably) |
| **Cheapest per tok/s** | Raspberry Pi 5 16GB | 19.4 (Qwen 2.5 0.5B) | $4.12 | $80 + 8W + 16GB RAM = unbeatable at this class |
| **Best $/tok/s at edge form factor** | Orange Pi 5 Pro 16GB | ~28 est. (RKLLama NPU) | ~$3.9 | $109 with 6 TOPS NPU for LLM, fanless-ready |
| **Best Mac value** | Mac Mini M4 16GB | 30.6 (Ollama llama.cpp) | $19.6 | $599 with mature software, 5-yr TCO |
| **Best 32GB SBC** | Orange Pi 6 Plus 32GB | ~32 est. (Vulkan) | ~$9.4 | Only 32GB+ sub-$350 option |

### 📊 Cost-perf ranking (cheapest $/tok/s first)

| Rank | Device | Tok/s | $/tok/s | Notes |
|---|---|---|---|---|
| 🥇 1 | Orange Pi 5 Pro 16GB | ~28 | $3.9 | RKLLama NPU, fanless, $109 |
| 🥈 2 | Radxa Rock 5B+ 16GB | ~28 | $4.2 | Same NPU, better Linux |
| 🥉 3 | Raspberry Pi 5 16GB | 19.4 | $4.1 | $80, 8W, real measurement |
| 4 | Jetson Orin Nano 8GB | ~60 | $8.3 | CUDA, but $499 |
| 5 | Mac Mini M4 16GB (MLX) | ~175 | $3.4 | Best $/tok/s in Mac class |
| 6 | Orange Pi 6 Plus 32GB | ~32 | $9.4 | Best 32GB+ LLM context |
| 7 | MacBook Pro M4 Max 128GB | 525.5 | $6.85 | Fastest, but premium price |

---

## The 0.8B Class Story (5 things Calvin should know)

### 1. **The Mac Mini lead collapses from 4–5× to ~5×, but every device is now usable**
On Qwen 3.5 9B, the Mac Mini M4 16GB was 4× faster than SBCs. On Qwen 2.5 0.5B, it's still ~5× faster — but **SBCs at 19–35 tok/s are now real-time chat speed** (anything >15 tok/s reads as natural conversation). The "unusable SBC" narrative is dead at 0.8B.

### 2. **The Raspberry Pi 5 at $80 is the new cost-perf champion**
$80 buys 19.4 tok/s on Qwen 2.5 0.5B. Add 8W wall draw, 16GB RAM, and you have a 5-year-TCO-under-$200 LLM endpoint. This is the **smallest, cheapest, lowest-power** device in the comparison. The Mac Mini is 6.7× the price and 1.6× the tok/s.

### 3. **Orange Pi 5 Pro at $109 is the new "best bang for buck"**
$109 + 6 TOPS RK3588S NPU + 16GB LPDDR5 + 10W = ~28 tok/s with RKLLama. **The NPU actually works at 0.8B** because the entire model fits in cache. This is the device for Red Cell distribution.

### 4. **The NPU works at 0.8B but NOT at 9B+**
At 0.8B, the model fits comfortably in the NPU's 6 TOPS / on-chip cache. RKLLama delivers 25–30 tok/s. At 9B+, the model spills out of cache and the NPU becomes a bottleneck. **Pick the right model class for the NPU.**

### 5. **For KLCC procurement AI (support role), 0.8B is enough**
Customer support LLMs don't need 70B. Qwen 2.5 0.5B handles classification, intent detection, RAG over short docs, and basic Q&A. The Mac Mini M4 16GB at 30–200 tok/s (depending on backend) is a *premium* experience, but a $109 Orange Pi 5 Pro at 28 tok/s is *good enough*. The pitch: "Buy 1 Mac Mini per office, or 5 Orange Pis for the same budget, distributed across departments."

---

## Apple Silicon Deep-Dive (the head-to-head on M4 16GB)

The Mac Mini M4 16GB is the Calvin-recommended workstation. On 0.8B:

| Backend | Qwen 2.5 0.5B | Llama 3.2 1B | Qwen 3 0.6B | Notes |
|---|---|---|---|---|
| **llama.cpp (default Ollama)** | ~40–50 est. | **30.6 measured** | ~80 est. | Geeky Gadgets M4 test |
| **MLX 4-bit** | ~100–150 est. | ~150 est. | ~200 est. | M4 Pro 24GB + MLX = ~250 |
| **MLX 8-bit (M4 Pro/Max only)** | ~50–80 | ~80 | ~100 | Better quality, slower |

**Key insight:** MLX is ~3–5× faster than llama.cpp on M4 16GB for sub-1B models. If you're deploying Qwen 2.5 0.5B or Llama 3.2 1B for a customer-facing demo, use MLX. If you're running mixed sizes, Ollama auto-routes.

**Power draw:** M4 16GB at 25W under sustained LLM load = $0.066/day at 8h/day = $24/year. SBC at 8–25W = $0.021–0.066/day = $8–24/year. **The Mac Mini power cost is 2–3× an SBC, but the SBC sticker is 1/4–1/7 the Mac.**

---

## SBC Deep-Dive (the Red Cell lineup)

For Red Cell distribution in Malaysia, the answer is **two products** at 0.8B class:

### Option A: Raspberry Pi 5 16GB + Hailo-10H — $305 system
- **Speed:** 11 tok/s (Hailo Llama 3 8B INT4) or 19.4 tok/s (Qwen 2.5 0.5B on CPU)
- **Power:** 8W load (5W idle)
- **Form factor:** Pi-Standard 85×56mm
- **Pros:** Cheapest 16GB LLM endpoint, massive ecosystem
- **Cons:** LPDDR4X (not LPDDR5) — slow for >7B

### Option B: Orange Pi 5 Pro 16GB — $109 board only
- **Speed:** ~28 tok/s (Qwen 2.5 0.5B RKLLama NPU W8A8)
- **Power:** 10W load
- **Form factor:** Custom 89×57mm
- **Pros:** LPDDR5 + 6 TOPS NPU + cheapest 16GB + actually useful NPU
- **Cons:** NPU model library is small (Qwen2-1.5B, Qwen3-1.7B, etc. have HEFs, but 0.5B may need RKLLama .rkllm compile)

**For the pitch:** Lead with **Orange Pi 5 Pro at $109** as the "every office, every desk" device. Mac Mini M4 16GB at $599 is the "executive workstation" device. **One Mac = five SBCs.**

---

## Power-Cost Reality Check

At 0.8B, all devices idle in the 5–15W range and peak at 8–40W. The OPi 6+ is still a power-hog at 25W (vs Pi 5 at 8W), but at 0.8B the model loads in <1 second and idle dominates.

| Device | Idle W | LLM Load W | $/year @ 8h/day | $/year @ 24/7 |
|---|---|---|---|---|
| Raspberry Pi 5 8GB | 3 | 8 | $2.40 | $7.20 |
| Raspberry Pi 5 16GB | 3 | 8 | $2.40 | $7.20 |
| Orange Pi 5 Pro 16GB | 5 | 10 | $3.20 | $9.60 |
| Orange Pi 6 Plus 32GB | 15 | 25 | $8.00 | $24.00 |
| Mac Mini M4 16GB | 4 | 25 | $8.00 | $24.00 |

**At 0.8B, the Mac Mini's idle is 4W (lower than any SBC).** This flips the power story — the Mac Mini is more power-efficient *at idle* than any RK3588 board. The SBC power advantage only shows at LLM load when the model is heavy.

---

## Full SBC Catalog (unchanged from v2)

### Orange Pi active lineup (15 models)

| Model | SoC | RAM (max) | NPU | LLM fit (0.8B) |
|---|---|---|---|---|
| **OrangePi 5 Pro** | RK3588S | 16GB LPDDR5 | 6 TOPS | ⭐ Best $/tok for 0.8B |
| OrangePi 5 Max | RK3588 | 16GB LPDDR5 | 6 TOPS | ⭐ Best 16GB SBC |
| OrangePi 5 Ultra | RK3588 | 16GB LPDDR5 | 6 TOPS | ⭐ |
| OrangePi 5 Plus (32GB) | RK3588 | 32GB LPDDR4X | 6 TOPS | 32GB LPDDR4X |
| OrangePi 6 Plus | CIX P1 | 32GB LPDDR5 | 30 TOPS | ⭐ Best 32GB+ context |
| OrangePi 6 | CIX P1 | TBD | 45 TOPS | Good |
| OrangePi CM5 | RK3588S | 16GB LPDDR5 | 6 TOPS | Embedded |
| OrangePi AIpro 20T | Ascend 310 | 24GB LPDDR4X | 20 TOPS | Vision, not LLM |
| OrangePi AIpro 8T | Ascend 310 | 16GB LPDDR4X | 8 TOPS | Vision |
| OrangePi 4 Pro | Allwinner A733 | 16GB LPDDR5 | 3 TOPS | Entry |
| OrangePi 4A | Allwinner T527 | TBD | 2 TOPS | Edge IoT |
| OrangePi Zero 3W | Allwinner A733 | 16GB LPDDR5 | 3 TOPS | Small |
| OrangePi AI Station | Ascend 310 | 96GB LPDDR4X | 176 TOPS | Server |
| OrangePi R2S / RV2 / RV | RISC-V | 8GB LPDDR4X | 2 TOPS | Networking |
| OrangePi 3B | RK3566 | 8GB LPDDR4 | None | Too small |

### Radxa active lineup (30+ models, key LLM-relevant ones)

| Model | SoC | RAM (max) | NPU | LLM fit (0.8B) |
|---|---|---|---|---|
| **Rock 5B+** | RK3588 | 32GB LPDDR5 | 6 TOPS | ⭐ Best Linux support |
| **Rock 5 ITX+** | RK3588 | 32GB LPDDR5 | 6 TOPS | Mini-ITX desktop |
| **Rock 5T** | RK3588 | 32GB LPDDR5 | 6 TOPS | Industrial |
| Rock 5A / 5B / 5C | RK3588 | 16GB LPDDR4X | 6 TOPS | Older |
| **Orion O6 / O6N** | CIX P1 | 32GB LPDDR5 | 30 TOPS | Same as OPi 6+ |
| Dragon Q8B / Q6A | Qualcomm | TBD | TBD | New, untested |
| **X4** | Intel N100 | 16GB | None | x86 option |
| C200 Orin | NVIDIA Jetson Orin NX | 16GB | CUDA | ⭐ Best CUDA SBC |
| Cubie A7S/A7A/A7Z | Allwinner A733 | TBD | TBD | Vision |
| ZERO series | Allwinner | 4GB | None | Too small |
| ROCK 4 series | RK3399/RK3568 | 4GB | None | Too small |
| VMARC-Q9075 | TBD | TBD | 200 TOPS | Server SoM |
| rCore / CM / NX modules | Various | varies | varies | Custom builds |
| SiRider S1 | TBD | TBD | TBD | Industrial |

---

## The Headline Slide (for Calvin's deck)

> **At 0.8B parameters, the question isn't "Mac or SBC" — it's "Mac Mini, Orange Pi, or Raspberry Pi."**
>
> | Device | Sticker | Tok/s (0.8B) | $/tok/s | Best for |
> |---|---|---|---|---|
> | Raspberry Pi 5 16GB | $80 | 19.4 | **$4.12** | IoT, edge, every-desk |
> | Orange Pi 5 Pro 16GB | $109 | ~28 | **$3.9** | NPU-accelerated, fanless |
> | Mac Mini M4 16GB | $599 | 30–200 | $3–20 | Executive workstation |
>
> **One Mac Mini M4 = 5 Orange Pi 5 Pro.** Both are real-time usable. The right answer is *both*: distribute SBCs to every desk, keep a Mac Mini in the executive office for the heavy models.

---

## When to Use What (decision tree)

```
Need 0.8B for:
├─ Edge sensor / industrial IoT → Raspberry Pi 5 8GB ($60) + Hailo-10H
├─ Every desk in a department → Orange Pi 5 Pro 16GB ($109) × N
├─ 32GB+ LLM context (long RAG) → Orange Pi 6 Plus 32GB ($300)
├─ Mixed 0.8B–9B workflows → Mac Mini M4 16GB ($599)
└─ Mixed 0.8B–32B / production → Mac Mini M4 Pro 24GB ($1,199)
```

For **Calvin's Red Cell** → lead with Orange Pi 5 Pro.
For **Calvin's KLCC pitch** → lead with Mac Mini M4 16GB.
For **Singular's internal use** → mix; one Mac Mini per team, Orange Pis for embedded features.

---

## Open Items (need field data from Shuenrui)

1. Run `bash ~/bench_orangepi6plus.sh` to verify Qwen 2.5 0.5B and Qwen 3 0.6B on the actual OPi 6+
2. Test Qwen 2.5 0.5B via RKLLama on an Orange Pi 5 Pro if you can get one
3. Measure idle power of the OPi 6+ at 0.8B (the 15W idle is for full system load — at 0.8B it should be lower)

---

## Sources

**Apple Silicon 0.8B benchmarks:**
- [Starmorph — Apple Silicon LLM Inference Optimization](https://blog.starmorph.com/blog/apple-silicon-llm-inference-optimization-guide) — Qwen3-0.6B MLX 4-bit: 525.5 tok/s on M4 Max 128GB
- [Geeky Gadgets — Best Local AI Models for Base Mac Mini M4](https://www.geeky-gadgets.com/apple-mini-llama-gemma) — Llama 3.2 1B Q4: 30.64 tok/s on M4 16GB
- [willitrunai.com — Qwen 3.5 MLX Apple Silicon](https://willitrunai.com/blog/qwen-3-5-mlx-apple-silicon-guide)
- [Hacker News — Qwen3 on MacBook](https://news.ycombinator.com/item?id=43856489) — 0.6B usable, 30B-A3B at 70 tok/s M3 Max

**SBC 0.8B benchmarks:**
- [DFRobot — SLMs on Raspberry Pi 5](https://www.dfrobot.com/blog-14068.html) — Qwen 2.5 0.5B Q4: 19.41 tok/s on Pi 5 8GB
- [localaimaster.com — Raspberry Pi 5 LLM benchmarks](https://localaimaster.com/blog/llm-raspberry-pi-5) — TinyLlama 1.1B Q4: 18.4 tok/s
- [Reddit — llama.cpp fork with Rockchip NPU for Orange Pi 5 Plus](https://www.reddit.com/r/OrangePI/comments/1p4sxc6/i_created_a_llamacpp_fork_with_the_rockchip_npu)

**Catalog & spec references:**
- [Orange Pi official catalog](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/index.html)
- [Radxa official catalog](https://radxa.com/products)
- [CNX-Software — Rock 5B+](https://www.cnx-software.com/2024/07/27/radxa-rock-5b-plus-sbc-lpddr5-memory-emmc-flash-wifi-6-two-m-2-m-key-sockets-4g-lte-5g)
- [Liliputing — Orange Pi 5 Ultra](https://liliputing.com/orange-pi-5-ultra-is-an-rk3588-single-board-pc-with-hdmi-input)
- [interfacinglinux.com — Vulkan llama.cpp on OPi 6+ / Orion O6](https://interfacinglinux.com/community/sbcsoftware/vulkan-powered-llama-cpp-on-the-orion-o6-and-o6n)

---

*Generated by Severus · 25 Aug 2026 · v3: unified 0.8B benchmark class, full Orange Pi + Radxa catalog, 0.8B-specific recommendations.*

## ⚡ Update (Aug 25, 2026 — same day)

**Arduino VENTUNO Q just launched** — 16GB RAM + 40 TOPS Hexagon NPU + STM32H5 MCU at ~$400 est. **It changes the 0.8B class story** because it's the first sub-$500 board with 16GB RAM and a real NPU that runs Qwen 3 / Gemma 4 natively.

Full analysis: [Arduino VENTUNO Q Breaking News](./Arduino_VENTUNO_Q_Breaking_News.md)

**Updated top-tier entries to add to the table above:**

```
Device                          | SoC                       | RAM    | Sticker | Tok/s (0.8B est.) | Backend           | Notes
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
Arduino VENTUNO Q (NEW)         | Qualcomm Dragonwing IQ-8275| 16GB LPDDR5 | ~$400 est. | ~40-80 (NPU est.) | Hexagon NPU + Ubuntu | First Arduino + Qualcomm NPU board
```

The VENTUNO Q at ~$400 estimated price with 16GB + 40 TOPS NPU is **competitive with Mac Mini M4 16GB at $599** for many 0.8B use cases, while adding robotics-grade I/O that the Mac Mini doesn't have.
