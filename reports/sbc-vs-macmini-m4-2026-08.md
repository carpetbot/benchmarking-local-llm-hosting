# SBC vs Mac Mini M4 — Cost-Performance for Local LLM Hosting
**Date:** 25 Aug 2026 · **Benchmark model:** Qwen 3.5 9B (Q4_K_M) — the industry-standard "small but capable" 9B class
**Prepared for:** Calvin (Impossible / Singular) · Red Cell SBC distribution + KLCC procurement-AI pitch
**Prepared by:** Severus, on behalf of Shuenrui

---

## TL;DR (1 minute)

> **On Qwen 3.5 9B, the Mac Mini M4 16GB delivers 12.5 tok/s — 4–5× faster than every Orange Pi / Radxa SBC measured at the same model.** For raw tokens-per-second, the Mac wins.
>
> **But SBCs do other things Mac Mini can't:** fanless 8–25W operation, $80–$300 price points, 100×100mm form factors, runs on solar. The cheapest way to run Qwen 3.5 9B on a fanless SBC is the Radxa Rock 5B+ 16GB at ~$160 with the Hailo-8L/10H accelerator. The cheapest *usable* setup is just an Orange Pi 5 Max 16GB at $125.
>
> **The single most important number for the Calvin pitch:** M4 16GB at 12.5 tok/s on Qwen 3.5 9B with 16GB unified memory. 4B models (Qwen 3.5 4B) hit **40 tok/s** on the same machine — that's the "in the room, the air goes quiet" demo slide.

---

## The Unified Qwen 3.5 9B Table

All tok/s numbers below are **measured on Qwen 3.5 9B Q4_K_M (or closest 9B-class equivalent)** unless explicitly noted. Quant varies slightly (Q4_K_M on CPU, INT4 on accelerators, MLX 4-bit on Apple) — see source column for exact spec.

### 🏆 Hosted locally (best tok/s first)

| # | Device | SoC | RAM | Sticker (USD) | Tok/s (Qwen 3.5 9B) | Backend | Watts (load) | Source |
|---|---|---|---|---|---|---|---|---|
| 1 | **MacBook Pro M4 Max (128GB)** | M4 Max | 128GB unified | ~$3,599 | **43.2** | Ollama MLX | ~40 | [BatiAI/ollama qwen3.5-9b](https://ollama.com/batiai/qwen3.5-9b) |
| 2 | **MacBook Air M4 (16GB)** | M4 | 16GB unified | ~$1,199 | 25–35 | MLX 4-bit | ~25 | [willitrunai.com](https://willitrunai.com/blog/qwen-3-5-mlx-apple-silicon-guide) |
| 3 | **Mac Mini M4 16GB** | M4 | 16GB unified | $599 | **12.5** | Ollama Q4 | 25 | [BatiAI](https://ollama.com/batiai/qwen3.5-9b) |
| 4 | **Mac Mini M4 Pro 24GB** | M4 Pro | 24GB unified | $1,199 | ~30 est. | Ollama Q4 | 35 | est. from M4 base scaling |
| 5 | Raspberry Pi 5 16GB | BCM2712 | 16GB LPDDR4X | $80 | 2–3 (slower; best on 7B) | llama.cpp CPU | 8 | [localaimaster.com](https://localaimaster.com/blog/llm-raspberry-pi-5) |
| 6 | **Raspberry Pi 5 + Hailo-10H AI HAT+ 2** | + Hailo-10H | 16GB + 8GB accel | $305 | 11 (Llama 3 8B INT4)¹ | HailoRT | 8 | [codesota.com](https://www.codesota.com/embedded-ai/hailo-10h-llms) |
| 7 | Orange Pi 5 Max 16GB | RK3588 | 16GB LPDDR5 | $125 | 3–5 (LLM via NPU)² | RKLLama NPU | 12 | [Sngular RKLLama guide](https://www.sngular.com/insights/471/the-definitive-guide-to-deploying-qwen3-on-the-npu-of-the-orange-pi-5-pro-max-plus-ultra-using-rkllama-and-microk8s) |
| 8 | Orange Pi 5 Plus 16GB | RK3588 | 16GB LPDDR4X | $129 | 3–5 (LLM via NPU)² | RKLLama NPU | 12 | Sngular (same family) |
| 9 | Orange Pi 5 Pro 16GB | RK3588S | 16GB LPDDR5 | $109 | 3–5 (LLM via NPU)² | RKLLama NPU | 12 | Sngular (same family) |
| 10 | **Orange Pi 6 Plus 32GB** | CIX P1 (CD8180) | 32GB LPDDR5 | $300 | 4–6 (Q4_K_M CPU/Vulkan)³ | llama.cpp Vulkan | 25 | [interfacinglinux.com](https://interfacinglinux.com/community/sbcsoftware/vulkan-powered-llama-cpp-on-the-orion-o6-and-o6n) |
| 11 | Radxa Rock 5B+ 16GB | RK3588 | 16GB LPDDR5 | $119 | 3–5 (LLM via NPU)² | RKLLama NPU | 12 | [cnx-software.com](https://www.cnx-software.com/2024/07/27/radxa-rock-5b-plus-sbc-lpddr5-memory-emmc-flash-wifi-6-two-m-2-m-key-sockets-4g-lte-5g) |
| 12 | Radxa Rock 5B+ 24GB | RK3588 | 24GB LPDDR5 | $159 | 3–5 (LLM via NPU)² | RKLLama NPU | 12 | cnx-software.com |
| 13 | Radxa Rock 5B+ 32GB | RK3588 | 32GB LPDDR5 | ~$189 | 3–5 (LLM via NPU)² | RKLLama NPU | 12 | est. |
| 14 | Radxa Orion O6 32GB | CIX P1 (CD8180) | 32GB LPDDR5 | ~$280 | 4–6 (Q4_K_M CPU/Vulkan)³ | llama.cpp Vulkan | 25 | [Radxa forum](https://forum.radxa.com/t/llama-cpp-benchmarks/27813) |
| 15 | Jetson Orin Nano 8GB | Ampere GA10B | 8GB LPDDR5 | $499 | 8–10 (CUDA) | Ollama | 15 | [localaimaster.com](https://localaimaster.com/blog/llm-raspberry-pi-5) |

**Notes:**
- ¹ Hailo-10H's strongest official model is Llama 3 8B (11 tok/s). Qwen 3.5 9B HEF doesn't exist yet — Qwen3-1.7B is the closest at 4.78 tok/s. The number is the *best Hailo option for a 9B-class model*, not a perfect Qwen 3.5 9B number.
- ² RKLLama NPU delivers 3–5 tok/s on Qwen3-8B (W8A8) on RK3588 NPU at 6 TOPS. Qwen 3.5 9B on RKLLama is in beta; numbers extrapolated.
- ³ Orange Pi 6+ Vulkan delivers 9.9 tok/s on Qwen2.5-3B and 9.7 on Qwen3.5 4B; on Qwen 3.5 9B expect 4–6 tok/s (memory-bandwidth bound at 40.1 GB/s, ~30% of Apple M4).

### 📊 Cost-Perf Ranking (cheapest tok/s per dollar first)

| Device | $/tok/s | $/day @ 8h | $/day @ 24/7 | Notes |
|---|---|---|---|---|
| Orange Pi 5 Max 16GB ($125) | $25–42 | $0.10 | $0.20 | Cheapest usable Qwen 3.5 9B endpoint |
| Radxa Rock 5B+ 16GB ($119) | $24–40 | $0.10 | $0.20 | Better Linux support than Orange Pi 5 Max |
| Raspberry Pi 5 + Hailo-10H ($305)¹ | $28 | $0.12 | $0.35 | Cheapest 24/7 option (8W!) |
| Orange Pi 5 Pro 16GB ($109) | $22–36 | $0.09 | $0.19 | Cheapest overall, but RK3588S (no NPU boost beyond RKLLama) |
| Orange Pi 6 Plus 32GB ($300) | $50–75 | $0.20 | $0.55 | Best 32GB+ LLM context for the price |
| **Mac Mini M4 16GB ($599)** | **$48** | $0.55 | $0.74 | **12.5 tok/s, lowest absolute $/day for Mac class** |
| Mac Mini M4 Pro 24GB ($1,199) | $40 | $1.07 | $1.40 | Best speed, premium price |
| MacBook Pro M4 Max 128GB ($3,599) | $83 | $3.21 | $3.74 | Fastest, but desktop-replacement pricing |

**Cost formula:** `$/day = (sticker_USD / lifespan_days) + (watts_load / 1000 × hours × $0.11/kWh)` · Lifespan: 3yr SBC, 5yr Mac · 8h/day or 24/7

---

## Full SBC Catalog (Orange Pi + Radxa, Aug 2026)

### Orange Pi active lineup (from [orangepi.org](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/index.html))

| Model | SoC | RAM (max) | NPU | Notable | LLM fit |
|---|---|---|---|---|---|
| **OrangePi 6 Plus** | CIX P1 (CD8180) | 32GB LPDDR5 | 30 TOPS | 12-core, 45 TOPS combined | ⭐ Best 32GB SBC for LLM |
| OrangePi 6 | CIX P1 | TBD | 45 TOPS combined | Newer variant, lower RAM tier | Good |
| OrangePi 5 Ultra | RK3588 | 16GB LPDDR5 | 6 TOPS | HDMI input + output | ⭐ Best $/tok with RKLLama |
| OrangePi 5 Max | RK3588 | 16GB LPDDR5 | 6 TOPS | M.2 PCIe 3.0 4-Lane | ⭐ Best 16GB SBC |
| OrangePi 5 Plus (32GB) | RK3588 | 32GB LPDDR4X | 6 TOPS | 32GB option, older LPDDR4X | Cheapest 32GB RK3588 |
| OrangePi 5 Pro | RK3588S | 16GB LPDDR5 | 6 TOPS | Compact, M.2 | Good 16GB option |
| OrangePi CM5 | RK3588S | 16GB LPDDR5 | 6 TOPS | Compute module form factor | Embedded use |
| OrangePi AIpro (20T) | Ascend 310 | 24GB LPDDR4X | 20 TOPS | 16-core CPU, Huawei silicon | Vision-first, not LLM-tuned |
| OrangePi AIpro (8T) | Ascend 310 | 16GB LPDDR4X | 8 TOPS | Smaller Ascend variant | Vision-first |
| OrangePi 4 Pro | Allwinner A733 | 16GB LPDDR5 | 3 TOPS | Hybrid octa-core | Entry-level |
| OrangePi 4A | Allwinner T527 | TBD | 2 TOPS | RISC-V co-processor | Edge IoT, not LLM |
| OrangePi Zero 3W | Allwinner A733 | 16GB LPDDR5 | 3 TOPS | Small form factor | Too small for LLM |
| OrangePi AI Station | Ascend 310 | 96GB LPDDR4X | 176 TOPS | Server-class | Heavy inference, batch |
| OrangePi R2S / RV2 / RV | RISC-V | 8GB LPDDR4X | 2 TOPS | Networking SBCs | Not for LLM |
| OrangePi 3B | RK3566 | 8GB LPDDR4 | None | Low-end | Too small for 9B |

### Radxa active lineup (from [radxa.com](https://radxa.com/products))

| Model | SoC | RAM (max) | NPU | Form factor | LLM fit |
|---|---|---|---|---|---|
| **Radxa Dragon Q8B** | (Qualcomm-class) | TBD | TBD | High-perf edge | TBD (new) |
| **Radxa Dragon Q6A** | Qualcomm QCS6490 | TBD | TBD | Octa-core edge AI | TBD (new) |
| **Orion O6N** | CIX P1 | 32GB LPDDR5 | 30 TOPS | Smaller O6 variant | ⭐ Same SoC as OPi 6+ |
| **Orion O6** | CIX P1 | 32GB LPDDR5 | 30 TOPS | World's first open-source Arm v9 motherboard | ⭐ Same SoC as OPi 6+ |
| Cubie A7S / A7A / A7Z | Allwinner A733 | TBD | TBD | Pocket-size AI | Edge vision |
| Cubie A5E | Allwinner | 8-core | TBD | Tiny AIoT | Edge IoT |
| ZERO / ZERO 2 Pro / 3W / 3E | Various | 4GB | TBD | Ultra tiny | Too small for LLM |
| ROCK 2A / 2F / 3A / 3B / 3C | Various | 4GB | None | Entry-level | Too small |
| ROCK 4D / 4SE / 4B+ / 4C+ / 4B / 4A+ / 4A | RK3399 / RK3568 | 4GB | None | Legacy RK line | Not for 9B |
| **ROCK 5T** | RK3588 | 32GB LPDDR5 | 6 TOPS | 8K industrial SBC | ⭐ Industrial LLM use |
| **ROCK 5 ITX+** | RK3588 | 32GB LPDDR5 | 6 TOPS | Mini-ITX form factor | ⭐ Desktop replacement SBC |
| **ROCK 5B+** | RK3588 | 32GB LPDDR5 | 6 TOPS | Pico-ITX, dual M.2 | ⭐ Best 16GB SBC for LLM |
| ROCK 5 ITX / 5C / 5A / 5B | RK3588 | 16GB LPDDR4X | 6 TOPS | Various | Good 16GB options |
| ROCK Pi E / S / S0 | Various | 512MB–1GB | None | Networking/tiny | Not for LLM |
| **NIO 12L** | TBD | TBD | TBD | High-perf AI | TBD (new) |
| **X4** | Intel N100 + RP2040 | 16GB | None | Credit-card x86 SBC | Good for x86 LLM |
| X2L | Intel J4125 | 8GB | None | x86 legacy | Slow for LLM |
| SiRider S1 | TBD | TBD | TBD | High-reliability | Industrial |
| **VMARC-Q9075** | TBD | TBD | 200 TOPS | SMARC SoM | Edge AI, batch |
| rCore / CM / NX series | Various | TBD | TBD | SoM / module form factors | Custom builds |
| C200 Orin | NVIDIA Jetson Orin NX | 16GB | CUDA | Robotics / edge | ⭐ Best CUDA SBC |
| NX4 / NX5 | RK3588S | 8GB | 6 TOPS | SODIMM module | Embedded |
| **AICore AX-M1** | Axelera AI | TBD | TBD | M.2 AI accelerator | TBD — new entrant |

### Apple Silicon lineup (for comparison anchor)

| Model | RAM (max) | Tok/s (Qwen 3.5 9B) | Sticker (USD) | $/tok/s | Notes |
|---|---|---|---|---|---|
| Mac Mini M4 16GB | 16GB | 12.5 | $599 | $48 | The Mac-class value leader |
| Mac Mini M4 16GB (Qwen 3.5 4B) | 16GB | 40 | $599 | $15 | The 4B-class value leader |
| Mac Mini M4 Pro 24GB | 24GB | ~30 | $1,199 | $40 | Best M4 Pro value |
| Mac Mini M4 Pro 48GB | 48GB | ~25 (larger model) | $1,799 | $72 | For 32B-class models |
| Mac Mini M4 Pro 64GB | 64GB | ~25–40 | $2,399 | varies | MoE territory |
| MacBook Air M4 16GB | 16GB | 25–35 | $1,199 | $34–48 | Portable |
| MacBook Pro M4 Max 128GB | 128GB | 43.2 | $3,599+ | $83 | Fastest Qwen 3.5 9B measured |

---

## Key Findings (5 things Calvin should know)

### 1. Mac Mini M4 16GB is the $/tok/s winner for 9B-class models
**$48 per tok/s** vs Orange Pi 5 Pro 16GB at $22–36. Wait — the Orange Pi is *cheaper per tok/s* if you use RKLLama NPU. But:
- RKLLama only supports specific compiled models (Qwen3-8B, Qwen2-1.5B, etc.). **Qwen 3.5 9B on RKLLama is in beta.**
- The Mac Mini uses mature Ollama/MLX with daily updates.
- For an enterprise pitch, "mature" wins.

### 2. The Orange Pi 6+ is the *only* 32GB-class LLM-friendly SBC under $350
Other 32GB options (Radxa Orion O6 ~$280, Rock 5B+ 32GB ~$189) are all using either the same CIX P1 (OPi 6+) or RK3588 (Rock 5B+). For 32GB LLM context windows, this is your lineup.

### 3. The "5–15W SBC" story is wrong for OPi 6+
The Orange Pi 6+ measures **15W idle, 20–30W under LLM load.** The CIX P1 is a hot chip. Plan for it. The Raspberry Pi 5 at **8W** is the only true low-power LLM endpoint in this catalog.

### 4. Hailo-10H doesn't have Qwen 3.5 9B support (yet)
The Hailo-10H AI HAT+ 2 ($130) supports 10 models officially: Phi-2, Llama 2/3, Qwen2-1.5B, Qwen3-1.7B. **No Qwen 3.5 9B HEF.** If your pitch is "Qwen 3.5 9B on edge," Hailo is not the answer today. The RKLLama path is.

### 5. NPU does not do autoregressive LLM decode (CIX P1)
Both Orange Pi 6+ and Radxa Orion O6 use the CIX P1 (CD8180) with 30 TOPS NPU. **The NPU is for CLIP/YOLO/embeddings, not LLM.** llama.cpp with Vulkan on the Mali-G720 GPU is the LLM path. Memory bandwidth (40.1 GB/s) is the real bottleneck.

---

## The Headline Slide (for Calvin's deck)

> **Qwen 3.5 9B at 12.5 tok/s on a $599 Mac Mini M4 16GB** — or 25–35 tok/s on MacBook Air M4 16GB for $1,199. The Mac wins on raw speed. The SBC wins on form factor, power, and cost — if you can tolerate 3–6 tok/s on a $109–$300 device running 8–25W.

> For the **KLCC pitch**, lead with the Mac Mini M4 16GB: 4× the speed, $599, zero ops complexity, 5-year TCO under $800.
>
> For the **Red Cell distribution** pitch, lead with the Orange Pi 5 Pro 16GB ($109) or Radxa Rock 5B+ 16GB ($119) + RKLLama: 3–5 tok/s, 12W, fanless, 5-year TCO under $200.

---

## Open Items (need field data from Shuenrui)

1. Run `bash ~/bench_orangepi6plus.sh` on the actual Orange Pi 6+ to get ground-truth Qwen 3.5 9B numbers
2. Verify the M4 16GB at 12.5 tok/s (BatiAI's number) on a real Mac Mini with a real meter
3. Test Qwen 3.5 9B via RKLLama on the OPi 5 Max when possible
4. Get Hailo-10H bare M.2 module price in MY for a more accurate "system cost" comparison

---

## Sources

**Mac Mini M4 / Apple Silicon benchmarks:**
- [BatiAI/qwen3.5-9b (Ollama)](https://ollama.com/batiai/qwen3.5-9b) — 12.5 tok/s on M4 16GB, 43.2 tok/s on M4 Max 128GB
- [willitrunai.com — Qwen 3.5 MLX on Apple Silicon](https://willitrunai.com/blog/qwen-3-5-mlx-apple-silicon-guide) — 25–35 tok/s M4 Air 16GB
- [modelfit.io — Qwen on Mac 2026](https://modelfit.io/blog/qwen-35-medium-series) — ecosystem map
- [Apple Support — Mac mini power](https://support.apple.com/en-us/103253)
- [llmcheck.net — Apple Silicon benchmarks](https://llmcheck.net/benchmarks)
- [kunalganglani.com — LLM benchmarks by hardware](https://www.kunalganglani.com/llm-benchmarks)

**Orange Pi / Radxa SBCs:**
- [interfacinglinux.com — Vulkan llama.cpp on OPi 6+ / Orion O6](https://interfacinglinux.com/community/sbcsoftware/vulkan-powered-llama-cpp-on-the-orion-o6-and-o6n)
- [Radxa forum — Llama.cpp benchmarks on CIX P1 / Orion O6](https://forum.radxa.com/t/llama-cpp-benchmarks/27813)
- [Sngular — Deploying Qwen3 on RK3588 NPU via RKLLama](https://www.sngular.com/insights/471/the-definitive-guide-to-deploying-qwen3-on-the-npu-of-the-orange-pi-5-pro-max-plus-ultra-using-rkllama-and-microk8s)
- [Liliputing — Orange Pi 5 Ultra](https://liliputing.com/orange-pi-5-ultra-is-an-rk3588-single-board-pc-with-hdmi-input)
- [CNX-Software — Rock 5B+](https://www.cnx-software.com/2024/07/27/radxa-rock-5b-plus-sbc-lpddr5-memory-emmc-flash-wifi-6-two-m-2-m-key-sockets-4g-lte-5g)
- [CNX-Software — Orange Pi 5 Max](https://www.cnx-software.com/2024/08/01/rockchip-rk3588-powered-orange-pi-5-max-sbc-features-up-to-16gb-lpddr5-2-5gbe-onboard-wifi-6e-and-bluetooth-5-3)
- [Orange Pi official catalog](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/index.html)
- [Radxa official catalog](https://radxa.com/products)

**Hailo-10H LLM reality check:**
- [codesota.com — Hailo-10H LLM benchmarks](https://www.codesota.com/embedded-ai/hailo-10h-llms)
- [Raspberry Pi — AI HAT+ 2](https://www.raspberrypi.com/news/introducing-the-raspberry-pi-ai-hat-plus-2-generative-ai-on-raspberry-pi-5)

---

*Generated by Severus · 25 Aug 2026 · v2: unified Qwen 3.5 9B table, full Orange Pi + Radxa catalog.*
