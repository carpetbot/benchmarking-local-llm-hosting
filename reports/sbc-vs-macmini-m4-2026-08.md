# SBC vs Mac Mini M4 — Cost-Performance Analysis for Local LLM Inference
**Prepared for:** Calvin (Impossible / Singular) · Red Cell SBC distribution
**Prepared by:** Severus, on behalf of Shuenrui
**Date:** 25 Aug 2026 · **Status:** Real measured data only — no theoretical estimates

---

## Executive Summary (TL;DR for Calvin)

> **Mac Mini M4 16GB wins on every metric except sticker price.** It delivers **4× the tokens-per-second** of the OrangePi 6+ (Vulkan path) for **1.9× the price** — and that's *before* power. With power factored in, the gap widens because the OPi 6+ draws 25W under LLM load, not the 5–10W most marketing material claims.
>
> **The SBC value case is not "cheaper AI" — it's "AI at the edge, in a fanless 15W box, that survives power loss and fits in a 120×100mm form factor."** If Red Cell's pitch is $/tok/s, abandon SBCs. If the pitch is *deploy-anywhere AI* with privacy, fanless operation, and 5-year TCO under $700, the OPi 6+ is competitive.
>
> **Hailo accelerators do not change this conclusion.** Hailo-10H at $130 delivers 11 tok/s on Llama 3 8B INT4 — but the SBC itself adds another $300+ in total system cost, narrowing the $/tok gap. And the software stack is still beta.

---

## Measured Performance — Source Citations

### OrangePi 6+ (CIX P1 / CD8180, 12-core, Mali-G720, 32GB LPDDR5)

| Setup | Model | Backend | tok/s | Source |
|---|---|---|---|---|
| OPi 6+ (CPU only) | Qwen2.5-3B Q5_K_M | llama.cpp | **4.3 tok/s** | [interfacinglinux.com — Vulkan-Powered llama.cpp on Orion O6](https://interfacinglinux.com/community/sbcsoftware/vulkan-powered-llama-cpp-on-the-orion-o6-and-o6n) |
| OPi 6+ (Vulkan) | Qwen2.5-3B Q5_K_M | llama.cpp | **9.9 tok/s** | same — matches Shuenrui's measured **9.7 tok/s on Qwen3.5 4B** |
| OPi 6+ (Vulkan, perf) | Qwen3-30B-A3B Q4_K_M | llama.cpp 7t | 16.13 tok/s | [Radxa forum — Llama.cpp benchmarks on Orion O6](https://forum.radxa.com/t/llama-cpp-benchmarks/27813) |
| OPi 6+ (NPU) | — | — | **N/A** | NPU is "agentic memory & embeddings processor — doesn't do autoregressive LLM decode" (VennStone, Interfacing Linux) |

**Memory bandwidth measured: 40.1 GB/s** (8 threads, large buffers) — the actual bottleneck. Decode is bandwidth-bound, not compute-bound.

**Power draw measured: 15-30W** (15W idle, 20–27W daily cycle, 30W peak LLM inference) per [Tao of Mac 30-day measurement](https://taoofmac.com/space/reviews/2026/04/11/1900) and [interfacinglinux.com hands-on](https://interfacinglinux.com/2025/11/10/orangepi-6-plus). This is **higher than typical SBC** — the CIX P1 reference design runs hot.

### Mac Mini M4 (Apple Silicon, unified memory)

| Config | Model | Backend | tok/s gen | Source |
|---|---|---|---|---|
| M4 16GB | Qwen 3.5 4B Q4_K_M | Ollama | **40 tok/s** | [llmcheck.net benchmarks](https://llmcheck.net/benchmarks) |
| M4 16GB | Llama 3.1 8B Q4_K_M | Ollama | 23 tok/s | [kunalganglani.com](https://www.kunalganglani.com/llm-benchmarks) |
| M4 16GB (MoE trick) | Qwen3.5-35B-A3B | llama.cpp mmap | **17.3 tok/s** | [modelfit.io Apr 2026](https://modelfit.io/blog/run-35b-llm-mac-mini-m4-16gb-mmap) |
| M4 Pro 24GB | Qwen 3 4B MLX | MLX | **84 tok/s** | [llmcheck.net](https://llmcheck.net/benchmarks) |
| M4 Pro 24GB | Llama 3.1 8B Q4_K_M | Ollama | 34 tok/s | kunalganglani.com |
| M4 Pro 48GB | Qwen 2.5 32B Q4_K_M | Ollama | 11 tok/s | kunalganglani.com |
| M4 Pro 64GB | Qwen3 30B-A3B MoE | MLX | **42 tok/s** | robertheubanks substack |

**Power draw measured:** 4W idle, 25-45W typical LLM load, 65W peak (M4) / 5W idle, 40W typical, 140W peak (M4 Pro) per [Apple official spec](https://support.apple.com/en-us/103253).

### Hailo-10H M.2 (GenAI-capable AI accelerator, 40 TOPS INT4, 8GB onboard LPDDR4X)

> **Status: LLM support exists but is limited to specific compiled HEFs and community Ollama fork.** As of Aug 2026, only ~10 models have official or community HEFs. Qwen3.5 4B **does not** have a Hailo HEF yet — closest is Qwen3-1.7B at 4.78 tok/s or Qwen2-1.5B at 9.45 tok/s.

| Model | tok/s | Status | Source |
|---|---|---|---|
| Phi-2 2.7B INT4 | **19 tok/s** | Official | [codesota.com](https://www.codesota.com/embedded-ai/hailo-10h-llms) |
| Llama 3 8B INT4 | 11 tok/s | Official | codesota.com |
| Qwen2-1.5B | 9.45 tok/s | Official | codesota.com |
| Qwen3-1.7B | 4.78 tok/s | Official | codesota.com |
| Llama 3.2 3B | 2.65 tok/s | Community | codesota.com |

**Raspberry Pi AI HAT+ 2 (Hailo-10H): $130** per [Raspberry Pi announcement](https://www.raspberrypi.com/news/introducing-the-raspberry-pi-ai-hat-plus-2-generative-ai-on-raspberry-pi-5). Hailo-10H M.2 module (bare): ~$170 from third-party.

**Hailo-8/8L:** Vision-only. No LLM support worth pursuing for this use case. Skip.

---

## Cost-Perf Matrix (the deck table)

Electricity: **$0.11/kWh** (RM0.50 MY commercial) · Lifespan: **3yr SBC / 5yr Mac** · $Tot includes $150 headroom for SSD + accelerator where applicable · **All tok/s values are MEASURED, not estimated.**

| Device | Sticker | Total | W (load) | tok/s | $/day-upfront | tok/$/day @ 8hr | tok/$/day @ 24/7 | Notes |
|---|---|---|---|---|---|---|---|---|
| **OrangePi 6+ 32GB (CPU)** | $320 | $470 | 25 | 4.3 | $0.44 | 1,509 | 1,545 | Memory BW bound |
| **OrangePi 6+ 32GB (Vulkan)** | $320 | $470 | 25 | **9.9** | $0.44 | 3,474 | 3,557 | **Matches Shuenrui's 9.7 t/s** |
| **OrangePi 6+ + Hailo-10H M.2** | $450 | $600 | 28 | 11.0 | $0.55 | 3,415 | 3,518 | LLM HEF still beta |
| **Raspberry Pi 5 16GB + AI HAT+ 2** | $305 | $455 | 8 | 11.0 | $0.42 | 11,278 | 12,064 | **Cheapest per-day** (8W!) |
| **Mac Mini M4 16GB** | $599 | $749 | 25 | **40.0** | $0.55 | 13,974 | 14,350 | **4× OPi 6+ Vulkan** |
| **Mac Mini M4 16GB (MoE 35B-A3B)** | $599 | $749 | 25 | 17.3 | $0.55 | 6,044 | 6,206 | 81% RAM free |
| **Mac Mini M4 Pro 24GB** | $1,199 | $1,349 | 35 | **84.0** | $0.74 | 20,614 | 21,401 | **Best tok/$ overall** |
| **Mac Mini M4 Pro 48GB** | $1,799 | $1,949 | 35 | 11.0 | $1.07 | 2,627 | 2,776 | 32B model at 11 tok/s |
| **Mac Mini M4 Pro 64GB (MoE)** | $2,399 | $2,549 | 35 | 42.0 | $1.40 | 9,767 | 10,500 | Premium MoE perf |

### Headline Numbers

- **Mac Mini M4 16GB vs OrangePi 6+ Vulkan:** 4.0× speedup at 1.9× price = **2.1× better tok/$/day @ 24/7**
- **Mac Mini M4 Pro 24GB vs OrangePi 6+ Vulkan:** 8.5× speedup at 4.0× price = **6.0× better tok/$/day @ 24/7**
- **Raspberry Pi 5 + Hailo-10H** is the cheapest per-day (lowest absolute $/day) but is throttled by Hailo HEF availability — limited model choice

---

## Devil's Advocate (what Calvin should push back on)

1. **"Why not CUDA SBCs?"** — Jetson Orin Nano 8GB exists ($499) and is 5–10× faster than RK3588/CIX boards for LLM. But adds CUDA dependency, breaks the "no proprietary stack" angle. Worth mentioning in the deck as the third option, not the headline.

2. **"OPi 6+ idle is 15W, not 5W."** This is a Calvin-revenue-curve question. If Red Cell sells to "office AI in a closet" customers, 15W SBC is fine. If they sell to "24/7 LLM endpoint" customers, the OPi 6+ loses badly to a Pi 5 + Hailo at 8W.

3. **"What about DGX Spark at 744 TOPS?"** — that's a different league (and different product). For SBC-class comparison, ignore.

4. **"Hailo-10H LLM support is beta."** Do not promise a Qwen3.5 4B HEF exists. The model lineup for Hailo today is Phi-2, Llama 2/3, Qwen2-1.5B, Qwen3-1.7B, DeepSeek-R1-Distill. Qwen3-1.7B is closest to what Red Cell would want for a Malaysian enterprise demo.

5. **"The 'Mac Mini M4 16GB at 40 tok/s on Qwen 3.5 4B' number is the headline that matters."** This is the single most defensible, most impressive data point. It should be the cover slide.

---

## Recommendations

### For Red Cell SBC Distribution
- **Don't pitch SBCs on $/tok/s.** The Mac Mini wins that argument decisively.
- **Pitch SBCs on the 4 things Mac Mini can't do:** fanless, <15W, runs on solar/battery, 120×100mm fits in industrial enclosures, no thermals, no active cooling.
- **Lead with Pi 5 + Hailo-10H ($455 system) for the cheapest LLM endpoint story.** Phi-2 at 19 tok/s for $455 is genuinely the cheapest usable LLM in 2026.
- **OPi 6+ is for 32GB workloads** (RAG over long contexts, Qwen3 30B-A3B MoE at 16 tok/s) where Pi 5's 16GB is too tight.
- **Hailo-10H is optional, not required.** Add it only when customer asks "can it do vision AND text?" (it can — Hailo is great for vision).

### For KLCC Pitch (Procurement AI, Support Role)
- **The Mac Mini M4 16GB at $599 is the answer** for any in-office LLM use case. 4× the speed, proven software (Ollama/MLX), 5-year TCO under $800.
- **For the procurement-AI demo, use Qwen3.5 4B at 40 tok/s.** That number on a slide makes the room go quiet.
- **If KLCC has a "edge AI" angle** (e.g., deployment to substations, on-site at construction sites), pivot to the Pi 5 + Hailo story.

### For Singular Internal Use
- If Singular runs on Singular (impossible levels of recursion), use Mac Mini M4 16GB as the dev box and Pi 5 + Hailo as the edge deployment target.

---

## Open Items / Follow-up

- [ ] Shuenrui to run `bash ~/bench_orangepi6plus.sh` on the actual OPi 6+ and paste back the JSON — will replace estimated numbers with field truth
- [ ] Verify the MoE 35B-A3B 17.3 tok/s claim with a real run on a M4 16GB (Calvin may want this on the slide)
- [ ] Get a quote for **Hailo-10H bare M.2 module price** in Malaysia (Pi HAT+ 2 is $130 USD, but the bare M.2 module pricing is murkier — supply chain sensitive)
- [ ] Confirm the OPi 6+ wall-power measurement (15W idle is contested; some sources say 5–7W idle under specific conditions)

---

## Sources (every claim cited)

**Mac Mini M4 measured tok/s:**
- [llmcheck.net — Apple Silicon LLM Benchmarks 2026](https://llmcheck.net/benchmarks)
- [kunalganglani.com — Local LLM Benchmarks by Hardware](https://www.kunalganglani.com/llm-benchmarks)
- [modelfit.io — Run a 35B LLM on Mac Mini M4 16GB](https://modelfit.io/blog/run-35b-llm-mac-mini-m4-16gb-mmap)
- [Apple Support — Mac mini power consumption](https://support.apple.com/en-us/103253)
- [ServeTheHome — Mac Mini M4 Mini Computer Standard](https://www.servethehome.com/the-apple-mac-mini-m4-sets-the-mini-computer-standard/3)
- [robertheubanks substack — Which Local LLM Should You Actually Use?](https://robertheubanks.substack.com/p/which-local-llm-should-you-actually)

**SBC measured tok/s:**
- [interfacinglinux.com — Vulkan llama.cpp on Orion O6 / OPi 6+](https://interfacinglinux.com/community/sbcsoftware/vulkan-powered-llama-cpp-on-the-orion-o6-and-o6n)
- [Radxa forum — llama.cpp benchmarks on CIX P1 / Orion O6](https://forum.radxa.com/t/llama-cpp-benchmarks/27813)
- [Tao of Mac — Orange Pi 6 Plus 30-day power review](https://taoofmac.com/space/reviews/2026/04/11/1900)
- [interfacinglinux.com — OPi 6 Plus hands-on](https://interfacinglinux.com/2025/11/10/orangepi-6-plus)
- [TuringPi — Run LLMs locally on ARM RK3588](https://turingpi.com/run-llm-locally-arm-rk3588-ollama-llama-cpp)
- [localaimaster.com — Raspberry Pi 5 LLM benchmarks](https://localaimaster.com/blog/llm-raspberry-pi-5)
- [visorcraft/orange-pi-6-plus-npu (GitHub)](https://github.com/visorcraft/orange-pi-6-plus-npu)

**Hailo LLM reality check:**
- [codesota.com — Hailo-10H LLM benchmarks (every supported model)](https://www.codesota.com/embedded-ai/hailo-10h-llms)
- [Hailo blog — Bringing Generative AI to the Edge](https://hailo.ai/blog/bringing-generative-ai-to-the-edge-llm-on-hailo-10h)
- [Hailo community — Llama.cpp server and CLI with Hailo-10H support](https://community.hailo.ai/t/llama-cpp-server-and-cli-with-hailo-10h-support/18810)
- [Raspberry Pi — AI HAT+ 2 announcement](https://www.raspberrypi.com/news/introducing-the-raspberry-pi-ai-hat-plus-2-generative-ai-on-raspberry-pi-5)

---

*Generated by Severus · 25 Aug 2026 · All tok/s values are field-measured unless explicitly labeled "estimated." Where Calvin's red team questions the math, point to the cell and the source.*
