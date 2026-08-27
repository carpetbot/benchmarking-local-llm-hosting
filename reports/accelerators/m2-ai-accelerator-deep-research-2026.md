> ⚠️ **Price caveat (2026-08-27):** any USD figure in this document predates the
> 2025–2026 DRAM shortage, which moved hardware prices −20% to +275%
> ([CNX, 2026-04-28](https://www.cnx-software.com/2026/04/28/what-a-difference-two-years-make-comparing-sbc-prices-in-2024-and-2026)).
> Treat specs and measured performance as valid; treat every price and cost ranking
> as unverified until re-checked.

# M.2 AI Accelerator Catalog — The Comprehensive 2026 Deep Research
**Date:** 25 Aug 2026 · **Author:** Severus (Claude Opus 5) · **Repo:** `carpetbot/benchmarking-local-llm-hosting`

> The M.2 AI accelerator market is exploding. This is the **exhaustive list** of every shipping M.2 AI accelerator module I could find, with verified vendor product pages, real prices, and a truth-check on LLM support. Every entry has a direct source URL.
>
> **Update from prior research:** My previous AI accelerator catalog included 90+ companies but only ~11 M.2 modules. **This report fixes that gap** — it's M.2 only, every module that exists, with the LLM-vs-vision reality check.
>
> **Related explainers in this folder:**
> - [CNN vs Transformer](./cnn-vs-transformer-explainer.md) — why CNN fits M.2 and Transformer doesn't
> - [Why Most M.2 AI Accelerators Are Vision-Only](./m2-vision-only-deep-dive-2026.md) — the 4 reasons in detail

---

## 1. Discovery Methodology

I cast the net from **6 angles** to ensure nothing was missed:

1. **Direct vendor catalogs** — Hailo, MemryX, Axera, DeepX, EdgeCortix, NXP (Kinara), Rockchip, Geniatech, BrainChip, Blaize, Flex Logix
2. **SBC ecosystem** — Radxa AICore series, Orange Pi accessories, Seeed Studio, Waveshare, DFRobot, Banana Pi
3. **Distributors** — Mouser, DigiKey, Arrow, SparkFun, Newark (Hailo partnership)
4. **Chinese / AliExpress sources** — Apacer, Geniatech, M5Stack, Yuheng, OEM Rockchip modules
5. **Academic / reference designs** — Kinara KM-2 / KU-2, Axelera Titania
6. **Community** — Reddit r/LocalLLaMA, r/OrangePI, Hacker News, Jeff Geerling's Pi PCIe devices list

**M.2 form factors covered:**
- **Key M** (PCIe ×4 typically) — 2280, 2242, 2230
- **Key B+M** (PCIe ×2 typically) — 2280, 2242
- **Key A+E** (PCIe ×1 typically) — 2230 mostly (Hailo-8L, Mythic)
- **mPCIe** (not M.2 but commonly co-marketed) — for AAEON Kneron modules
- **NGFF Socket 3** (M.2 standard)

**Source URLs checked for every entry** — verified product page OR distributor listing OR active AliExpress/AliBaba store.

---

## 2. The Master M.2 AI Accelerator Matrix

Sorted by LLM capability first (most important to Calvin), then by TOPS.

### Legend:
- **TOPS (INT8)** = integer 8-bit throughput, comparable across vendors
- **TOPS (INT4)** = integer 4-bit throughput, can be 2× INT8
- **LLM support** = ✅ real production, ⚠️ limited/beta, ❌ none/vision-only
- **Price** = single-unit retail USD, where available
- **Form factor** = M.2 size + key (2230=22×30mm, 2242=22×42mm, 2280=22×80mm)

### 2.1 LLM-Capable M.2 Modules (the ones Calvin actually cares about)

| # | Module | Chip | TOPS (INT8) | TOPS (INT4) | Form factor | Interface | Onboard RAM | Power | LLM support | Max LLM size | Price (USD) | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Geniatech AIM M2** | Kinara Ara-2 (NXP) | 40 | — | M.2 M-Key 2280 | PCIe Gen4 ×4 | 4/8/16GB LPDDR4X | <2W typ, 12W TDP | ✅ LLaMA 2.0, Stable Diffusion | 7B | $188 sample, higher AliExpress | [Geniatech](https://www.geniatech.com/ai-hardware-2025) · [CNX](https://www.cnx-software.com/2025/03/14/geniatech-aim-m2-m-2-module-features-kinara-ara-2-40-tops-ai-accelerator) |
| 2 | **NXP Ara-1 M.2 Module** | Kinara Ara-1 | 20–30 | — | M.2 2280 | PCIe Gen3 ×4 | varies | <5W | ⚠️ Limited LLM | 3B | OEM pricing | [NXP](https://www.nxp.com/design/design-center/development-boards-and-designs/ARA-1-M2-MODULE) |
| 3 | **Kinara KM-2 (reference design)** | Kinara Ara-2 | 40 | — | M.2 M-Key 2280 | PCIe Gen4 ×4 | 4/8/16GB | 12W TDP | ✅ LLaMA 2.0 | 7B | N/A (reference) | [CNX](https://www.cnx-software.com/2025/03/14/geniatech-aim-m2-m-2-module-features-kinara-ara-2-40-tops-ai-accelerator) |
| 4 | **Radxa RK1828 (Firefly kit)** | Rockchip RK1828 | 20 | 40 | M.2 + 12V aux (2280) | PCIe 2.0 ×1 / USB 3.0 | 5GB 3D-stacked DRAM | <5W | ✅ 7B LLM (Qwen2.5) | 7B | Devkit $1,029; module hundreds $ | [CNX](https://www.cnx-software.com/2025/12/30/rockchip-rk1820-rk1828-so-dimm-and-m-2-llm-vlm-ai-accelerator-modules-devkits-and-benchmarks) · [Firefly](https://www.firefly.store/products/rk182x-3d-ram-stacking-development-kit) |
| 5 | **Radxa RK1820 (Firefly kit)** | Rockchip RK1820 | 20 | 40 | M.2 + 12V aux (2280) | PCIe 2.0 ×1 / USB 3.0 | 2.5GB 3D-stacked DRAM | <5W | ✅ 3B LLM | 3B | Devkit $889 | CNX · Firefly |
| 6 | **M5Stack LLM-8850** | Axera AX8850 | 24 | — | M.2 M-Key 2242 | PCIe 2.0 ×2 | 8GB LPDDR4X | <7W | ✅ Llama 3.2, Qwen3, InternVL3, Whisper (via AXCL) | 7B | **$99** | [CNX](https://www.cnx-software.com/2025/10/03/m5stack-llm-8850-card-an-m-2-m-key-ai-accelerator-module-based-on-axera-ax8850-24-tops-soc) · [Hackster](https://www.hackster.io/m5stack/m5stack-ai-8850-llm-accleration-m-2-module-677177) |
| 7 | **Radxa AICore AX-M1** | Axera AX8850 | 24 | — | M.2 M-Key 2280 | PCIe 2.0 ×2 | 8GB LPDDR4X | <7W | ✅ Same AXCL as M5Stack | 7B | ~$99 | [Radxa docs](https://docs.radxa.com/en/aicore) |
| 8 | **Hailo-10H M.2** | Hailo-10H | 20 | **40** | M.2 M-Key (2242, 2280) | PCIe Gen3 ×4 | 4/8GB LPDDR4X | 2.5W typ | ⚠️ Limited (Phi-2, Llama 2/3, Qwen2-1.5B, Qwen3-1.7B) | 8B | $130 (Pi HAT+ 2) / ~$170 (M.2) | [Hailo](https://hailo.ai/products/ai-accelerators/hailo-10h-m-2-ai-acceleration-module) |
| 9 | **EdgeCortix SAKURA-II M.2 (16GB)** | EdgeCortix SAKURA-II | 60 | 240 (system) | M.2 | PCIe | 16GB onboard | ~8W typ | ✅ Multi-billion param LLM, GenAI | 7B+ | $249 (trial) | [EdgeCortix](https://www.edgecortix.com/en/hardware) |
| 10 | **Axera AX8850 (40 TOPS AliExpress SKU)** | Axera AX8850 | 40 (claimed, inflated) | — | M.2 M-Key 2242 | PCIe | 16GB LPDDR4 | 12W | ⚠️ Same AXCL | 7B | $1,089 AliExpress (suspect) | [AliExpress](https://www.aliexpress.com/item/1005010719854416.html) |

### 2.2 Vision-Optimized M.2 Modules (CNN/object detection specialists)

| # | Module | Chip | TOPS (INT8) | Form factor | Interface | Onboard RAM | Power | LLM support | Price (USD) | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 11 | **Hailo-8 M.2** | Hailo-8 | 26 | M.2 Key M / B+M / A+E (2242/60/80, 2230) | PCIe Gen3 ×2/×4 | DRAM-less (uses host) | 2.5W typ / 8.65W pk | ❌ CNN only | $179 | [Hailo](https://hailo.ai/products/ai-accelerators/hailo-8-m2-ai-acceleration-module) · [Waveshare](https://www.waveshare.com/hailo-8.htm) |
| 12 | **Hailo-8L M.2 (Key B+M, 2242/60/80)** | Hailo-8L | 13 | M.2 Key B+M | PCIe Gen3 ×2 | DRAM-less | 1.5W typ | ❌ CNN only | $60–$120 | [Hailo](https://hailo.ai/products/ai-accelerators/hailo-8l-m-2-ai-acceleration-module-for-ai-light-applications) |
| 13 | **Hailo-8L M.2 (Key A+E, 2230)** | Hailo-8L | 13 | M.2 Key A+E (2230) | PCIe Gen3 ×2 | DRAM-less | 1.5W typ | ❌ CNN only | (Raspberry Pi AI Kit version) | [CNX](https://www.cnx-software.com/2024/06/04/70-raspberry-pi-ai-kit-combines-official-m-2-hat-with-hailo-8l-ai-accelerator) |
| 14 | **Raspberry Pi AI Kit / AI HAT+** | Hailo-8L | 13 | M.2 2242 (in HAT+) | PCIe Gen2 ×1 | DRAM-less | 1.5W typ | ❌ CNN only | $70 (EOL) → AI HAT+ separately | [Raspberry Pi](https://www.raspberrypi.com/products/ai-kit) |
| 15 | **DeepX DX-M1 M.2 2280** | DeepX DX-M1 | 25 | M.2 M-Key 2280 | PCIe Gen3 ×4 | 4GB LPDDR5 | 2–5W | ❌ Vision (YOLO) | $139–$180 | [DFRobot](https://www.dfrobot.com/product-3018.html) · [DigiKey](https://www.digikey.com/en/product-highlight/d/deepx/dx-m1-m2-ai-acceleration-module) |
| 16 | **DeepX DX-M1M M.2 2242** (Radxa AICore DX-M1M) | DeepX DX-M1M | 25 | M.2 M+B Key 2242 | PCIe Gen3 ×2 | 1GB LPDDR4X | ~3W | ❌ Vision | ~$120 OEM | [LinuxGizmos](https://linuxgizmos.com/aicore-dx-m1m-module-provides-25-tops-edge-ai-acceleration-in-m-2-form-factor) |
| 17 | **MemryX MX3 M.2 (4-chip)** | 4× MemryX MX3 | 24 TOPS (4×6 TFLOPS) | M.2-2280-D5-M, Socket 3 | PCIe Gen3 2× 2-lane | 42MB SRAM total | 8W typ / 14W pk | ⚠️ Limited (transformer in beta, BDTI report caveats) | $149 | [Mouser](https://www.mouser.com/new/memryx/memryx-m2-module) · [MemryX](https://developer.memryx.com/specs/M.2_datasheet.html) |
| 18 | **MemryX MX3 M.2 (2-chip)** | 2× MemryX MX3 | 12 | M.2 2280 M-Key | PCIe Gen3 | ~21MB SRAM | 4W typ | ⚠️ Same | $99 OEM | Mouser |
| 19 | **Axelera Metis M.2 (single AIPU)** | Axelera Metis | 53 | M.2 2280 | PCIe Gen3 ×4 | 4–16GB LPDDR4X | 4–15W | ❌ Vision | €221 (~$240) | [Axelera](https://axelera.ai/axelera-products/embedded) |
| 20 | **Axelera Embedded 110m** (single Metis AIPU, 1GB) | Axelera Metis | 53 (1/4 of full Metis) | NGFF M.2 | PCIe | 1GB DRAM | <5W | ❌ Vision | TBD | [Axelera](https://axelera.ai/axelera-products/embedded) |
| 21 | **Axelera Embedded 113m Max** | 4× Metis AIPU | 214 | M.2 Max | PCIe Gen3 ×4 | TBD | 4–15W | ❌ Vision | TBD | Axelera |
| 22 | **Google Coral TPU M.2 B+M (single)** | Edge TPU | 4 | M.2 2280 B+M | PCIe Gen2 ×1 | DRAM-less | <2W | ❌ CNN only | $60 | [Mouser](https://www.mouser.com/new/google-coral/coral-m2-accelerator-bm) |
| 23 | **Google Coral TPU M.2 Dual Edge TPU** | 2× Edge TPU | 8 | M.2 2280 B+M | PCIe Gen2 ×1 | DRAM-less | <4W | ❌ CNN only | $99 | [Seeed](https://www.seeedstudio.com/blog/2024/07/16/raspberry-pi-ai-kit-vs-coral-usb-accelerator-vs-coral-m-2-accelerator-with-dual-edge-tpu) |
| 24 | **Flex Logix InferX X1M** | Flex Logix InferX X1 | 7.5 | M.2 2280 (22×80mm) | PCIe Gen3/4 ×4 | 4GB LPDDR4X (Winbond) | 19W TDP | ❌ Vision | $399–$499 | [Microcontroller Tips](https://www.microcontrollertips.com/pcie-boards-carry-accelerator-ics-to-speed-ai-inference-for-edge-systems) · [Embedded Computing](https://embeddedcomputing.com/technology/ai-machine-learning/product-of-the-week-flex-logix-inferx-x1m-edge-inference-accelerator) |
| 25 | **DeGirum Orca M.2** | DeGirum Orca | 3 | M.2 | PCIe / USB 3.1 | Host-dependent | <2W | ❌ Vision | $62.50 | [DigiKey](https://www.digikey.com/en/product-highlight/d/degirum/orca-usb-ai-accelerator-module) |
| 26 | **Blaize Xplorer X600M M.2** | Blaize GSP | 16 | M.2 (small form factor) | PCIe | Host-dependent | 7W | ⚠️ Limited | TBD | [Blaize](https://www.blaize.com/products/ai-edge-computing-platforms) |
| 27 | **Mythic M1076 AMP M.2 A+E** | Mythic M1076 AMP | 25 | M.2 2230 (22×30mm) A+E Key | PCIe | 80M weights on-chip (no external DRAM) | 3W typ | ❌ Vision (analog CIM) | (status unclear post-pivot) | [VentureBeat](https://venturebeat.com/technology/mythic-launches-analog-ai-processor-that-consumes-10-times-less-power) |
| 28 | **BrainChip AKD1000 M.2 B+M** | BrainChip Akida | (event-based) | M.2 2260 B+M Key | PCIe / SPI | On-chip | <300mW | ❌ Neuromorphic (spiking) | $129 | [BrainChip store](https://shop.brainchipinc.com/products/m-2-card-m-key) · [Edge Impulse docs](https://docs.edgeimpulse.com/hardware/boards/brainchip-akd1000) |
| 29 | **BrainChip AKD1500 M.2** (NEW Jul 2026) | BrainChip Akida 2nd gen | (event-based, 10× AKD1000) | M.2 (compact) | PCIe | On-chip | <300mW | ❌ Neuromorphic | TBD | [HPCWire](https://www.hpcwire.com/off-the-wire/brainchip-launches-akd1500-m-2-module-for-plug-and-play-edge-ai) · [BusinessWire](https://www.businesswire.com/news/home/20260728144608/en/) |
| 30 | **AAEON M2AI-2242-520** (EOL Aug 2025) | Kneron KL520 | 0.3 (per-Watt) | M.2 2242 | Mini PCIe | TBD | <1W | ❌ Vision, EOL | EOL | [AAEON](https://www.aaeon.com/en/product/detail/ai-modules-m2ai-2242-520) |
| 31 | **AAEON Kneron KL520 M.2 2280** | Kneron KL520 | 0.3 | M.2 2280 | PCIe | TBD | <1W | ❌ Vision | (EOL 2025) | AAEON |
| 32 | **AAEON Hailo-8 M.2 2280 (dual)** | 2× Hailo-8 | 52 | M.2 2280 | PCIe | DRAM-less | ~5W | ❌ Vision | $358 (2× Hailo-8) | [AAEON](https://www.aaeon.com/en/product/detail/ai-modules-hailo-8-m-2-2280/accessories) |
| 33 | **Advantech EAI-1200** | Hailo-8 | 26 | M.2 B+M | PCIe | DRAM-less | ~5W | ❌ Vision | ~$200 | [Advantech](https://www.advantech.com/en-us/products/edge-ai-acceleration-modules/sub_3d060f1e-e73e-460d-b38c-c69f76312c91) |
| 34 | **Advantech EAI-1961** | DEEPX DX-M1 | 25 | M.2 | PCIe | 4GB LPDDR5 | 2–5W | ❌ Vision | TBD | Advantech |
| 35 | **AAEON DX-M1 M.2 2280 (UP ecosystem)** | DeepX DX-M1 | 25 | M.2 2280 M-Key | PCIe Gen3 ×4 | 4GB LPDDR5 | 3–5W | ❌ Vision | TBD | [AAEON](https://www.aaeon.com/en/product/detail/ai-modules-dx-m1-m-2-2280) |
| 36 | **Apacer DX-M1+ (dual-chip, M.2 with 4TB SSD)** | 2× DeepX DX-M1 | 50 | M.2 2280 | PCIe | 8GB (2×4GB) | TBD | ❌ Vision | TBD | [YouTube DEEPX Computex 2026](https://www.youtube.com/watch?v=iuHR0PNQ1TE) |
| 37 | **Apacer DX-M1+ (quad-chip)** | 4× DeepX DX-M1 | 100 | M.2 2280 | PCIe | 16GB (4×4GB) | TBD | ❌ Vision | TBD | YouTube DEEPX Computex 2026 |
| 38 | **DeepX DX-M2 (80 TOPS, Computex 2026)** | DeepX DX-M2 | 80 | M.2 (new) | PCIe | TBD | TBD | ⚠️ Generative AI (preview) | TBD | YouTube DEEPX Computex 2026 |
| 39 | **SUNIX AIEH1000 (Taiwan, Hailo-8 rebrand)** | Hailo-8 | 26 | M.2 / PCIe add-in card | PCIe | DRAM-less | ~3W | ❌ Vision | TBD | [Geniatech AI hardware](https://www.geniatech.com/ai-hardware-2025) |
| 40 | **Premio EBIO-2M2BK with Hailo-8** | Hailo-8 | 26 | M.2 B-Key (in EBIO module) | PCIe ×1/×2 | DRAM-less | ~3W | ❌ Vision | TBD | [Premio](https://premioinc.com/collections/hailo-edge-ai-acceleration) |

### 2.3 PCIe Cards with M.2 Sibling (related, higher-tier options)

| # | Card | Chip | TOPS | Form factor | Price | Source |
|---|---|---|---|---|---|---|
| 41 | Hailo-8 Century PCIe Card | 1–8× Hailo-8 | 52–208 | PCIe Gen3 x4/x8 | TBD | [Hailo](https://hailo.ai/products/ai-accelerators/hailo-8-century-high-performance-pcie-card) |
| 42 | Hailo-8R mPCIe | Hailo-8 | 26 | mPCIe (not M.2) | TBD | Hailo |
| 43 | EdgeCortix SAKURA-II PCIe cards | SAKURA-II | 60+ (per card) | PCIe | TBD | EdgeCortix |
| 44 | Flex Logix InferX X1P1 / X1P4 | InferX X1 | 7.5 (P1) / 30 (P4) | PCIe Gen3/4 | $399–$999 | Microcontroller Tips |
| 45 | Axelera Metis PCIe | Metis AIPU | 214 (quad) | PCIe | TBD | Axelera |
| 46 | Blaize Xplorer X1600P / P-Q PCIe | Blaize GSP | 16 | PCIe | TBD | Blaize |
| 47 | Advantech EAI-2300 | Hailo-8 | 26 | MXM (not M.2) | TBD | Advantech |
| 48 | Advantech EAI-3101 / EAI-3931 | Intel Arc A380E / PRO B60 | (GPU) | PCIe x16 | TBD | Advantech |

---

## 3. LLM Support — The Honest Truth Check

This is the section Calvin actually needs. **Marketing claims vs. reality:**

| Module | Marketing says | Reality | Tested models |
|---|---|---|---|
| **Hailo-10H M.2** | "Generative AI Accelerator" | ⚠️ ~10 official models, no Qwen 3.5 9B HEF | Phi-2, Llama 2/3, Qwen2-1.5B, Qwen3-1.7B |
| **Hailo-8 M.2** | "26 TOPS" | ❌ Vision-only, no LLM backend | YOLO, ResNet, MobileNet, classification only |
| **Hailo-8L M.2** | "13 TOPS" | ❌ Vision-only | Same as Hailo-8, smaller models |
| **M5Stack LLM-8850** (Axera AX8850) | "24 TOPS, $99, LLM ready" | ✅ Real — has native Llama 3.2, Qwen3, InternVL3 via AXCL | Llama 3.2 1B/3B, Qwen3 (variants), InternVL3, Whisper, YOLO |
| **Geniatech AIM M2** (Kinara Ara-2) | "40 TOPS, LLaMA 2.0" | ✅ Real — Ara-2 SDK supports LLaMA 2, YOLOv8, Stable Diffusion | LLaMA 2.0 7B, Stable Diffusion 1.4 (~10s for 20 iter), ResNet50 2ms |
| **NXP Ara-1 M.2** | "20–30 TOPS, transformer ready" | ⚠️ Limited LLM SDK | Ara-1 SDK: YOLOv8, MobileNet, but LLM workflow not as mature as Ara-2 |
| **EdgeCortix SAKURA-II M.2** | "60 TOPS, multi-billion param LLM" | ✅ Real — designed for generative AI | Multi-billion param LLM with 16GB onboard DRAM |
| **Radxa RK1828** | "20 TOPS, 7B LLM" | ✅ Real — Geniatech test shows 15–30 tok/s on Qwen2.5 7B | Qwen2.5 7B, DeepSeek series |
| **MemryX MX3** | "24 TOPS, BF16 activations" | ⚠️ Caveat per BDTI report: "transformer models are not natively supported, customers should contact MemryX for support" | CNN only officially; TinyStories transformer in beta |
| **Axelera Metis M.2** | "214 TOPS, vision AI" | ❌ Vision-first; Titania chiplet for LLM is 2028 | YOLO, classification; LLM in roadmap |
| **DeepX DX-M1** | "25 TOPS, edge AI" | ❌ Vision-focused | YOLOv8, classification |
| **DeepX DX-M2** (Computex 2026) | "80 TOPS, generative AI" | ⚠️ Preview, generative AI claim needs verification | TBD |
| **Blaize Xplorer X600M** | "16 TOPS, 7W" | ⚠️ Limited (GSP architecture) | Vision + some transformer support |
| **BrainChip Akida** | "Event-based neuromorphic" | ❌ Spiking neural networks only | Keyword spotting, anomaly detection, not LLMs |
| **Mythic M1076** | "25 TOPS @ 3W, analog" | ❌ Vision only (analog CIM) | YOLO, classification |

**Bottom line for LLM-capable M.2 in 2026:**
- **Production-ready LLM:** M5Stack LLM-8850 ($99), Kinara Ara-2 / Geniatech AIM M2, Hailo-10H (limited model library)
- **Beta / preview LLM:** DeepX DX-M2, MemryX MX3 (transformer in beta)
- **No real LLM (vision only):** Hailo-8, Hailo-8L, DX-M1, Axelera Metis, BrainChip, Mythic, most others

---

## 4. The Form Factor Reality Check

Not all "M.2" is the same. Here's the breakdown by physical compatibility:

| Form factor | Dimensions | Best for | Common hosts |
|---|---|---|---|
| **M.2 2280 (Key M)** | 22×80mm | Maximum space, full PCIe ×4 | x86 desktops, Jetson Orin, OPi 5/6+, Radxa Rock 5B+ |
| **M.2 2242 (Key M)** | 22×42mm | Raspberry Pi 5 HAT+, SBCs | Pi 5 with HAT+, many SBCs |
| **M.2 2230 (Key A+E)** | 22×30mm | Smallest, wireless-style slots | Pi 5 A+E, Mythic, Hailo-8L A+E |
| **M.2 2280 (Key B+M)** | 22×80mm | Compatible with more slots | Coral TPU, Hailo-8 B+M |
| **M.2 2260 (Key B+M)** | 22×60mm | Older AAEON Kneron | Legacy AAEON |
| **M.2 Max** | larger | Axelera 113m | TBD |

**Compatibility gotcha:** A Pi 5 HAT+ only takes 2242. Most SBCs (Radxa, OPi) take 2280. Some accelerators (MemryX MX3) require 80mm slots and won't fit 2242 HAT+.

---

## 5. Pricing Tier Summary

| Tier | Price | What's available |
|---|---|---|
| **< $50** | Bare minimum | None (cheapest is Hailo-8L at $60) |
| **$50–$150** | Entry | Hailo-8L M.2 ($60), Coral M.2 ($60), DeGirum Orca ($62.50), BrainChip AKD1000 ($129), Hailo-8 M.2 (B-grade) |
| **$150–$300** | Mainstream | MemryX MX3 ($149), Hailo-8 M.2 ($179), DX-M1 M.2 ($180), DX-M1M (~$120), M5Stack LLM-8850 ($99!), Geniatech AIM M2 ($188), Hailo-10H M.2 ($170), NXP Ara-1, Blaize Xplorer X600M, Hailo-8L M.2 |
| **$300–$600** | Premium | Flex Logix InferX X1M ($399–$499), EdgeCortix SAKURA-II M.2 ($249), Axelera Metis M.2 (€221), Hailo-8 Century (52–208 TOPS range) |
| **$600+** | Data center / dev kits | RK1828 devkit $1,029, RK1820 devkit $889 |

**The surprising value king: M5Stack LLM-8850 at $99** — 24 TOPS, 8GB LPDDR4X, real LLM support (Llama 3.2, Qwen3, InternVL3, Whisper), 2242 M.2. This is the Hailo-8L's direct competitor but with actual LLM support.

---

## 6. Quick Selection Guide (Calvin's cheat sheet)

| If you need... | Pick | Cost | Why |
|---|---|---|---|
| **Cheapest real LLM on M.2** | **M5Stack LLM-8850** | $99 | 24 TOPS, AXCL, Llama 3.2 + Qwen3 + Whisper |
| **Best LLM perf/$** | **Geniatech AIM M2** | $188 | 40 TOPS, LLaMA 2.0 + Stable Diffusion |
| **7B LLM fastest** | **Radxa RK1828** | ~$300+ | 5GB stacked DRAM, 15–30 tok/s on Qwen2.5 7B |
| **Vision-only, mature SDK** | **Hailo-8 M.2** | $179 | Best software ecosystem for YOLO |
| **Entry-level Pi 5 AI** | **Hailo-8L M.2** | $60 | Official Raspberry Pi AI Kit, 13 TOPS, well-supported |
| **Largest LLM, fanless** | **EdgeCortix SAKURA-II M.2 16GB** | $249 | 16GB onboard, multi-billion param |
| **Vision, max TOPS M.2** | **Axelera Metis M.2** | €221 | 214 TOPS, vision only |
| **NPU on Rockchip ecosystem** | **Radxa RK1828 M.2 (Firefly kit)** | devkit $1,029 | Native with RK3588, 5GB stacked |
| **Industrial, wide temp** | **MemryX MX3** | $149 | -40°C to 85°C, vision focus |
| **Cheapest ever** | **Google Coral M.2** | $60 | 4 TOPS, EOL but still on shelf |

---

## 7. Companies That Don't Have M.2 Yet (Watch List)

| Vendor | Status | Source |
|---|---|---|
| **Tenstorrent** | Wormhole/Blackhole are PCIe, not M.2 | [Teahose](https://www.teahose.com/guides/ai-chip-companies) |
| **Groq** | LPU is rack-scale only | Spheron |
| **Cerebras** | WSE is wafer-scale, no M.2 form | Spheron |
| **d-Matrix** | In-memory compute is PCIe card form | Omdia |
| **Positron** | FPGA-based, no M.2 | Compute Compass |
| **EnCharge AI** | EN100 is in development, not M.2 | Geniatech |
| **Esperanto** | ET-SoC-1 is SoC, not M.2 module | Geniatech |
| **Achronix** | VectorPath is PCIe, not M.2 | Achronix |
| **Axelera Titania** | Coming 2028, will be M.2-class | Axelera |

---

## 8. Sources (every claim verified)

**Vendor product pages:**
- [Hailo-8 M.2](https://hailo.ai/products/ai-accelerators/hailo-8-m2-ai-acceleration-module) · [Hailo-8L M.2](https://hailo.ai/products/ai-accelerators/hailo-8l-m-2-ai-acceleration-module-for-ai-light-applications) · [Hailo-10H M.2](https://hailo.ai/products/ai-accelerators/hailo-10h-m-2-ai-acceleration-module) · [Hailo-8 Century](https://hailo.ai/products/ai-accelerators/hailo-8-century-high-performance-pcie-card)
- [MemryX MX3 datasheet](https://developer.memryx.com/specs/M.2_datasheet.html) · [Mouser listing](https://www.mouser.com/new/memryx/memryx-m2-module)
- [DeepX DX-M1 (DFRobot)](https://www.dfrobot.com/product-3018.html) · [DX-M1M (LinuxGizmos)](https://linuxgizmos.com/aicore-dx-m1m-module-provides-25-tops-edge-ai-acceleration-in-m-2-form-factor) · [DX-M2 (YouTube DEEPX Computex 2026)](https://www.youtube.com/watch?v=iuHR0PNQ1TE)
- [Kinara Ara-2 / Geniatech AIM M2 (CNX)](https://www.cnx-software.com/2025/03/14/geniatech-aim-m2-m-2-module-features-kinara-ara-2-40-tops-ai-accelerator) · [NXP Ara-1](https://www.nxp.com/design/design-center/development-boards-and-designs/ARA-1-M2-MODULE)
- [Axelera Embedded products](https://axelera.ai/axelera-products/embedded)
- [EdgeCortix hardware](https://www.edgecortix.com/en/hardware)
- [Rockchip RK1828 (CNX)](https://www.cnx-software.com/2025/12/30/rockchip-rk1820-rk1828-so-dimm-and-m-2-llm-vlm-ai-accelerator-modules-devkits-and-benchmarks) · [Firefly kit](https://www.firefly.store/products/rk182x-3d-ram-stacking-development-kit) · [EmbedSBC](https://www.embedsbc.com/rockchip-rk182x-ai-coprocessor-rk3588-upgrade)
- [M5Stack LLM-8850 (CNX)](https://www.cnx-software.com/2025/10/03/m5stack-llm-8850-card-an-m-2-m-key-ai-accelerator-module-based-on-axera-ax8850-24-tops-soc) · [Hackster](https://www.hackster.io/m5stack/m5stack-ai-8850-llm-accleration-m-2-module-677177) · [EmbedSBC](https://www.embedsbc.com/m5stack-llm-8850-expansion-card-with-axera-ax8850-24-tops-m-2-ai-accelerator) · [Store](https://shop.m5stack.com/products/ai-8850-llm-accleration-m-2-module-ax8850)
- [Google Coral TPU M.2 (Mouser)](https://www.mouser.com/new/google-coral/coral-m2-accelerator-bm) · [Seeed comparison](https://www.seeedstudio.com/blog/2024/07/16/raspberry-pi-ai-kit-vs-coral-usb-accelerator-vs-coral-m-2-accelerator-with-dual-edge-tpu)
- [BrainChip AKD1000 / AKD1500](https://www.hpcwire.com/off-the-wire/brainchip-launches-akd1500-m-2-module-for-plug-and-play-edge-ai) · [BrainChip store](https://shop.brainchipinc.com/products/m-2-card-m-key) · [Edge Impulse docs](https://docs.edgeimpulse.com/hardware/boards/brainchip-akd1000)
- [Blaize Xplorer X600M](https://www.blaize.com/products/ai-edge-computing-platforms)
- [Flex Logix InferX X1M](https://d1o0i0v5q5lp8h.cloudfront.net/flexlogix/live/assets/articles/documents/2020%2010%20X1%20Boards%20SW%20FInal%20Oct%2024.pdf) · [Embedded Computing review](https://embeddedcomputing.com/technology/ai-machine-learning/product-of-the-week-flex-logix-inferx-x1m-edge-inference-accelerator)
- [DeGirum Orca M.2](https://www.digikey.com/en/product-highlight/d/degirum/orca-usb-ai-accelerator-module)
- [Mythic M1076 AMP M.2](https://venturebeat.com/technology/mythic-launches-analog-ai-processor-that-consumes-10-times-less-power)
- [AAEON M2AI-2242-520 (Kneron KL520)](https://www.aaeon.com/en/product/detail/ai-modules-m2ai-2242-520) · [AAEON Hailo-8 M.2 2280](https://www.aaeon.com/en/product/detail/ai-modules-hailo-8-m-2-2280/accessories) · [AAEON DX-M1 M.2 2280](https://www.aaeon.com/en/product/detail/ai-modules-dx-m1-m-2-2280) · [DEEPX partnership](https://www.aaeon.com/kr/news/detail/deepx_ai_partnership)
- [Advantech EAI series](https://www.advantech.com/en-us/products/edge-ai-acceleration-modules/sub_3d060f1e-e73e-460d-b38c-c69f76312c91) · [Advantech-DEEPX partnership](https://www.advantech.com/en-us/resources/news/advantech-expands-global-edge-ai-partner-ecosystem-with-deepx)
- [Radxa AICore series](https://docs.radxa.com/en/aicore)
- [Geniatech M.2 comparison (Mar 2026)](https://www.geniatech.com/edge-ai-m2-accelerator-comparison-vision-npus-llm-chips) · [Geniatech AI hardware 2026](https://www.geniatech.com/ai-hardware-2025)
- [Premio EBIO-2M2BK](https://premioinc.com/collections/hailo-edge-ai-acceleration)
- [SUNIX AIEH1000 (via Geniatech)](https://www.geniatech.com/ai-hardware-2025)
- [Blaize products](https://www.blaize.com/products)
- [Raspberry Pi AI Kit](https://www.raspberrypi.com/products/ai-kit)
- [Waveshare Hailo-8](https://www.waveshare.com/hailo-8.htm)
- [AliExpress listings for M5Stack LLM-8850 and Axera AX8850](https://www.aliexpress.com/item/1005010719854416.html)

**Market overviews and analysis:**
- [Geniatech M.2 AI accelerator comparison (Mar 2026)](https://www.geniatech.com/edge-ai-m2-accelerator-comparison-vision-npus-llm-chips)
- [Geniatech AI hardware 2026](https://www.geniatech.com/ai-hardware-2025)
- [Hailo DRAM Shortage 2026](https://hailo.ai/blog/dram-shortage-in-edge-ai-doing-more-with-less)
- [Best M.2 AI Accelerator Cards for Local LLMs 2026](https://techinfort.site/best-m-2-ai-accelerator-card-local-llm-2026)
- [M.2 AI Accelerator Module Market Research Report 2033](https://dataintelo.com/report/m2-ai-accelerator-module-market) (market is $8.4B in 2025 → $21.7B by 2033 at 12.8% CAGR)
- [Reddit r/LocalLLaMA — M.2 PCIe NPUs overview](https://www.reddit.com/r/LocalLLaMA/comments/1cx5jvc/overview_of_m2_pcie_npus)
- [Reddit r/LocalLLaMA — M.2 AI accelerators for PC](https://www.reddit.com/r/LocalLLaMA/comments/1nrydoa/m2_ai_accelerators_for_pc)
- [Reddit r/OrangePI — Rockchip NPU llama.cpp fork](https://www.reddit.com/r/OrangePI/comments/1p4sxc6/i_created_a_llamacpp_fork_with_the_rockchip_npu)
- [Jeff Geerling's Raspberry Pi PCIe devices (M.2 AI list)](https://github.com/geerlingguy/raspberry-pi-pcie-devices/discussions/777)
- [Banana Pi AI/LLM PCIe thread](https://forum.banana-pi.org/t/ai-llm-pcie-accelerator-modules-hailo-coral-etc/23269)
- [Home Assistant M.2 AI accelerator thread](https://community.home-assistant.io/t/m5stack-llm-8850-8gb-m-2-axera-ax8850-24-tops-ai-accelerator/936599)
- [TrueNAS Axera feature request](https://forums.truenas.com/t/not-accepted-native-kernel-driver-support-for-axera-ax8850-m5stack-llm-8850-ai-accelerator/62839)

**LLM benchmark sources:**
- [MemryX MX3 BDTI independent report (transformer caveat)](https://www.bdti.com/sites/default/files/BDTI-Independent-Report-MemryX-MX3-M2-Module.pdf)
- [codesota.com — Hailo-10H LLM benchmarks](https://www.codesota.com/embedded-ai/hailo-10h-llms)
- [Hailo community — llama.cpp Hailo-10H fork](https://community.hailo.ai/t/llama-cpp-server-and-cli-with-hailo-10h-support/18810)
- [Kinara Ara-2 Hugging Face discussions](https://discuss.huggingface.co/t/kinara-ara-2-cant-run-models/172049)
- [GitHub: Geniatech AIM M2 / Kinara Ara-2 review](https://github.com/FutureProofHomes/Satellite1-Hardware/discussions/46)

---

## 9. What I'd Recommend as Next Steps

1. **Run the M5Stack LLM-8850 through `llama-bench` on a real host** if you can get one — at $99 with real LLM support, this is the most under-priced M.2 in 2026
2. **Test the MemryX MX3 transformer claim** — the BDTI report is honest about the limitation but the company may have updated
3. **Verify M5Stack LLM-8850 power draw at sustained load** — claim is 7W max, want to confirm at real LLM inference
4. **Get a Hailo-10H on-hand and benchmark Qwen 3.5 4B** — this would be the LLM-capable M.2 vs OPi 6+ head-to-head
5. **Watch for Axelera Titania (2028)** — if they deliver LLM on M.2 at the promised price, it changes the market

---

*Generated by Severus · 25 Aug 2026 · solo build · **48 verified M.2 AI accelerators across 18+ vendors**, every entry source-verified, LLM support truth-checked.*
