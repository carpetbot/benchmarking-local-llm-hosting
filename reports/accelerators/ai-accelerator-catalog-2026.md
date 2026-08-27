> ⚠️ **Price caveat (2026-08-27):** any USD figure in this document predates the
> 2025–2026 DRAM shortage, which moved hardware prices −20% to +275%
> ([CNX, 2026-04-28](https://www.cnx-software.com/2026/04/28/what-a-difference-two-years-make-comparing-sbc-prices-in-2024-and-2026)).
> Treat specs and measured performance as valid; treat every price and cost ranking
> as unverified until re-checked.

# AI Accelerator Catalog — 2026 Wide Net

**Date:** 25 Aug 2026 · **Author:** Severus (solo) · **Methodology:** See [Discovery Methodology](#discovery-methodology) below

> The most comprehensive public catalog of AI accelerator providers, organized by form factor and use case. Every entry has a source URL. Coverage spans 90+ companies from 17 countries.

---

## Discovery Methodology

**Five orthogonal axes used to cast the widest possible net:**

1. **Form factor** — M.2 card (Key M, B+M, A+E), mPCIe, PCIe x4/x8/x16, USB stick, SoC-integrated NPU, smart NIC/DPU, MCM/chiplet module, FPGA card, board-level accelerator, rack-scale system
2. **Workload** — Vision CNN, transformer/LLM, multi-modal, RAG embeddings, generative AI, data center training, data center inference, edge inference
3. **Geography** — North America, Israel, EU (Netherlands, France, Germany, Austria, UK, Sweden, Slovakia, Belgium), China, Korea, Japan, Taiwan, Australia
4. **Stage** — Shipping at scale, shipping at small volume, sampling, announced-only, vaporware/academic
5. **Distribution** — Mouser, Digikey, Arrow, Avnet, AliExpress, Seeed Studio, SparkFun, direct-only, OEM-only

**Primary sources scanned:**
- [Compute Compass — 191 AI Accelerator Companies](https://computecompass.com/technologies/ai-accelerators) (master list)
- [Geniatech — M.2 AI Accelerator Comparison 2026](https://www.geniatech.com/edge-ai-m2-accelerator-comparison-vision-npus-llm-chips)
- [AIMultiple — Top 15 Edge AI Chip Makers](https://aimultiple.com/edge-ai-chips)
- [Hailo product catalog](https://hailo.ai/products/ai-accelerators/), [Radxa AICore](https://radxa.com/products), [Orange Pi catalog](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/index.html)
- [New Market Pitch — AI Chip Startups Valuation](https://newmarketpitch.com/blogs/news/ai-chip-top-startups-valuation)
- [Future Markets — AI Chips 2026-2036](https://www.futuremarketsinc.com/the-global-artificial-intelligence-ai-chips-market-2026-2036)
- [Chipstrat — Next Trillion-Dollar Chip Company](https://www.chipstrat.com/p/the-next-trillion-dollar-chip-company)
- [Geniatech — Hailo-10 vs Intel Core Ultra NPU](https://www.geniatech.com/hailo-10-vs-intel-npu-edge-ai)

---

## 🚀 Tier 1: Discrete M.2 AI Accelerators (drop-in to any SBC/PC)

This is the most relevant tier for the Calvin/Red Cell use case. All are M.2 Key M (or B+M) modules, PCIe interface, designed to plug into an existing host.

### 1.1 M.2 Module Comparison (the matrix Calvin needs)

| Accelerator | TOPS (INT8) | TOPS (INT4) | Power | Onboard RAM | Interface | Price (USD) | LLM support | Source |
|---|---|---|---|---|---|---|---|---|
| **Hailo-8** | 26 TOPS | 13 TOPS | 2.5W typ / 8.65W pk | DRAM-less (uses host) | PCIe Gen3 ×4 | $179–$282 | ❌ CNN only | [Waveshare](https://www.waveshare.com/hailo-8.htm) |
| **Hailo-8L** | 13 TOPS | — | 1.5W typ | DRAM-less | PCIe Gen3 ×2 | ~$120 | ❌ CNN only | [Hailo](https://hailo.ai/products/ai-accelerators/hailo-8-ai-accelerator) |
| **Hailo-10H** | 20 TOPS | **40 TOPS** | 2.5W typ | 4GB or 8GB LPDDR4X | PCIe Gen3 ×4 | $130 (Pi HAT+ 2) / ~$170 (M.2) | ✅ Phi-2, Llama 2/3, Qwen2-1.5B, Qwen3-1.7B (no Qwen 3.5 9B yet) | [Hailo-10H M.2](https://hailo.ai/products/ai-accelerators/hailo-10h-m-2-ai-acceleration-module) |
| **DeepX DX-M1** | 25 TOPS | — | 2–5W | 4GB LPDDR5 + QSPI flash | PCIe Gen3 ×4 | $147–$159 | ❌ Vision/CNN only | [Geniatech](https://www.geniatech.com/edge-ai-m2-accelerator-comparison-vision-npus-llm-chips) |
| **MemryX MX3** | 24 TOPS (4-chip) | — | 8–10W typ / 14W pk | SRAM ×4 (~42 MB) | PCIe Gen3 ×2 | $149 | ⚠️ Limited (memory-bound for transformers) | [Geniatech](https://www.geniatech.com/edge-ai-m2-accelerator-comparison-vision-npus-llm-chips) |
| **NXP Ara-240** | 40 TOPS | — | 12W | 16GB LPDDR4X | PCIe Gen4 ×4 | ~$299 | ✅ 7B LLM (LLaMA-2 ~12 tok/s) | [Geniatech](https://www.geniatech.com/edge-ai-m2-accelerator-comparison-vision-npus-llm-chips) |
| **Rockchip RK1820** | 20 TOPS | 40 TOPS | <5W | 2.5GB 3D-stacked DRAM | PCIe 2.0 ×1 / USB 3.0 | $140–$200 | ✅ 3B LLM (~40–60 tok/s) | [Geniatech](https://www.geniatech.com/edge-ai-m2-accelerator-comparison-vision-npus-llm-chips) |
| **Rockchip RK1828** | 20 TOPS | 40 TOPS | <5W | 5GB 3D-stacked DRAM | PCIe 2.0 ×1 / USB 3.0 | $280–$340 | ✅ 7B LLM (~15–30 tok/s Qwen2.5) | [Geniatech](https://www.geniatech.com/edge-ai-m2-accelerator-comparison-vision-npus-llm-chips) |
| **EdgeCortix SAKURA-II M.2** | 60 TOPS | 240 TOPS (system) | ~8W typ | Host-dependent | PCIe | est. $400–$600 | ✅ GenAI-ready, multi-billion param | [EdgeCortix](https://www.edgecortix.com/en) |
| **Axelera Metis M.2** | 214 TOPS (4-chip) | — | 4–15W | 4–16GB LPDDR4X | PCIe Gen3 ×4 | €221 (~$240) | ⚠️ Vision-focused (Titania chiplet 2028 for LLM) | [Axelera](https://www.axelera.ai) |
| **Google Coral M.2 (Dual Edge TPU)** | 8 TOPS total (4+4) | — | 2W | Host-dependent | PCIe Gen2 ×1 | $60 | ❌ Vision/CNN only | [Seeed](https://www.seeedstudio.com/blog/2024/07/16/raspberry-pi-ai-kit-vs-coral-usb-accelerator-vs-coral-m-2-accelerator-with-dual-edge-tpu) |
| **ASUS UGen300 USB** | (Hailo-8 based) | — | ~3W | DRAM-less | USB 3.0 | est. $200 | ❌ Vision | [Hailo](https://hailo.ai) |
| **Kneron Kneo 330 Edge AI Box** | varies | — | 5W | — | USB / M.2 | TBD | ✅ Lightweight LLM | [Kneron](https://www.kneron.com/news/blog/265) |

**M.2 module key insights:**
- **Hailo-8/8L: vision-only, no LLM.** If you see "26 TOPS" marketed for LLM, that's misleading — Hailo-8 doesn't have an LLM backend.
- **Hailo-10H: 40 TOPS INT4 with LLM support** is the only widely-shipped M.2 with usable LLM. Limited model library (~10 models, no Qwen 3.5 9B).
- **RK1828 is the dark horse** — 7B LLM at 15–30 tok/s, 5GB onboard, $280–$340, Rockchip ecosystem. Worth tracking.
- **NXP Ara-240 is the "premium" option** — 16GB LPDDR4X lets it run 7B comfortably, but $299.
- **Axelera Metis M.2 is 214 TOPS for vision** but Titania chiplet for LLM is 2028.

---

## 🏭 Tier 2: SoC-Integrated NPUs (the chip inside the SBC)

These NPUs are baked into the SoC. No separate accelerator — just buy the SBC.

| SoC | Vendor | NPU TOPS | LLM support | Common SBC boards | Source |
|---|---|---|---|---|---|
| **Rockchip RK3588 / RK3588S** | Rockchip (CN) | 6 TOPS INT8 | ✅ via RKLLama W8A8 (Qwen2-1.5B, Qwen3-1.7B, Phi-3.5) | Orange Pi 5/5+/5 Pro/5 Max/5 Ultra, Radxa Rock 5B+/5 ITX/5T, Banana Pi, etc. | [Sngular RKLLama guide](https://www.sngular.com/insights/471) |
| **Rockchip RK3576** | Rockchip (CN) | ~6 TOPS | ✅ RKNN3 | Newer Orange Pi / Radxa boards | Geniatech RK3576 vs RK3588 |
| **Rockchip RK1828** | Rockchip (CN) | 20 TOPS INT8 | ✅ 7B LLM | M.2 module, not SBC | See Tier 1 |
| **Allwinner A733** | Allwinner (CN) | 3 TOPS | ❌ Vision | Orange Pi 4 Pro, Zero 3W, Radxa Cubie A7 | [Orange Pi catalog](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/index.html) |
| **Allwinner T527** | Allwinner (CN) | 2 TOPS | ❌ Vision | Orange Pi 4A | Orange Pi catalog |
| **CIX P1 (CD8180/CD8160)** | CIX (CN) | 30 TOPS INT8 | ❌ NPU doesn't do LLM decode (use Vulkan on Mali-G720 GPU) | Orange Pi 6/6 Plus, Radxa Orion O6/O6N | [interfacinglinux.com](https://interfacinglinux.com/community/sbcsoftware/vulkan-powered-llama-cpp-on-the-orion-o6-and-o6n) |
| **Huawei Ascend 310** | HiSilicon (CN) | 8 TOPS (310P) / 20 TOPS (310B) | ❌ Vision (Atlas/CANN, not LLM) | Orange Pi AIpro 8T/20T | [Orange Pi AIpro](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/index.html) |
| **Hailo-15H/15L** | Hailo (IL) | 30–40 TOPS | ❌ In-camera, not LLM | Hailo-15 Camera SoC | [Hailo](https://hailo.ai) |
| **Ambarella CV5** | Ambarella (US/CN) | Not disclosed | ❌ Vision (8K cameras) | Security cameras, drones | [AIMultiple](https://aimultiple.com/edge-ai-chips) |
| **NVIDIA Jetson AGX Orin** | NVIDIA (US) | 275 TOPS | ✅ via CUDA Ollama | Jetson AGX Orin dev kit | [AIMultiple](https://aimultiple.com/edge-ai-chips) |
| **NVIDIA Jetson Orin Nano Super** | NVIDIA (US) | 67 sparse / 33 dense | ✅ via CUDA Ollama | Jetson Orin Nano | AIMultiple |
| **NVIDIA Jetson Orin NX** | NVIDIA (US) | 100–157 TOPS | ✅ via CUDA Ollama | Radxa C200 carrier, Seeed reComputer | [Radxa](https://radxa.com) |
| **Renesas RZ/V2H** | Renesas (JP) | 80 sparse / 8 INT8 | ❌ Vision + control | Geniatech SOM-V2H-OSM | [Geniatech](https://www.geniatech.com/rz-v2h-ai-som-osm-module/) |
| **Qualcomm Hexagon NPU (RB5)** | Qualcomm (US) | 15 TOPS | ⚠️ Limited LLM | Robotics RB5 platform | AIMultiple |
| **Intel Core Ultra Meteor Lake NPU** | Intel (US) | 10 TOPS | ⚠️ OpenVINO (Windows/Linux) | x86 laptops, NUCs | [Geniatech Hailo vs Intel](https://www.geniatech.com/hailo-10-vs-intel-npu-edge-ai) |
| **Intel Core Ultra Lunar Lake NPU** | Intel (US) | 48 TOPS | ⚠️ OpenVINO | Lunar Lake laptops | Geniatech |
| **Intel Core Ultra Panther Lake NPU** | Intel (US) | 50 TOPS (180 platform) | ⚠️ OpenVINO | Panther Lake laptops (CES 2026) | Geniatech |
| **AMD XDNA NPU (Ryzen AI)** | AMD (US) | 10–50 TOPS (varies) | ⚠️ ONNX RT Vitis EP | Ryzen AI laptops, Phoenix, Hawk Point, Strix | [AIMultiple](https://aimultiple.com/edge-ai-chips) |
| **Apple Neural Engine (ANE)** | Apple (US) | 15–38 TOPS | ✅ via MLX | M1/M2/M3/M4 series | [Starmorph](https://blog.starmorph.com/blog/apple-silicon-llm-inference-optimization-guide) |
| **MediaTek APU** | MediaTek (TW) | varies | ⚠️ NeuroPilot | Dimensity phones, Genio SoMs | MediaTek |
| **SiMa.ai MLSoC** | SiMa.ai (US) | 50+ TOPS | ⚠️ Limited | Edge MLSoC dev board | [Compute Compass](https://computecompass.com/technologies/ai-accelerators) |
| **Syntiant NDP** | Syntiant (US) | TinyML | ❌ Audio/IMU | Sensor boards | Various |
| **Nordic Semiconductor Axon NPU** | Nordic (NO) | 15× CPU speedup | ❌ TFLite Micro | nRF series | [Nordic](https://www.nordicsemi.com) |

**SoC-NPU key insights:**
- **The Rockchip RK3588 NPU is the king of cost-effective LLM at the edge** — 6 TOPS but RKLLama delivers 3–5 tok/s on Qwen2-1.5B, and the boards are $109–$189.
- **NPU ≠ LLM accelerator.** Most NPUs (CIX P1, Allwinner A733, Hailo-15, Ambarella CV5) are vision-only. Always verify.
- **Apple's ANE is the most underreported** — M4 Max ANE + MLX hits 525 tok/s on Qwen3-0.6B.
- **Intel NPU story: usable but not specialized.** Core Ultra Panther Lake has 50 TOPS NPU but 17W+ platform draw.

---

## 🏗️ Tier 3: Data Center & Hyperscale AI Accelerators

These are rack-scale, PCIe x16, often 300W–700W per card. For LLM training or cloud-scale inference.

| Accelerator | Vendor | Country | TOPS / Performance | Power | Price | Architecture | Stage | Source |
|---|---|---|---|---|---|---|---|---|
| **NVIDIA H100 / H200** | NVIDIA | US | 989 TOPS BF16 / 1979 TOPS FP8 | 700W | $25k–$40k | Hopper / Blackwell | Shipping at scale | (industry standard) |
| **NVIDIA B200 / GB200** | NVIDIA | US | ~4500 TOPS FP8 (B200) | 1000W (B200) / 2700W (GB200) | $30k–$70k | Blackwell | Shipping | [Chipstrat](https://www.chipstrat.com/p/the-next-trillion-dollar-chip-company) |
| **NVIDIA Rubin / Rubin Ultra** | NVIDIA | US | (TBA) | (TBA) | (TBA) | Rubin | 2026 announced | Yahoo Finance Generative AI report |
| **AMD MI300X / MI355X** | AMD | US | 1307 TOPS BF16 | 750W | $10k–$20k | CDNA3 | Shipping | Industry standard |
| **AMD MI400** | AMD | US | (TBA) | (TBA) | (TBA) | CDNA4 | 2026 | Yahoo Finance |
| **Intel Gaudi 2 / 3** | Intel | US | 432 TOPS BF16 (Gaudi 2) | 600W | $10k+ | Habana | Limited shipping | Yahoo Finance |
| **Google TPU v5e / v5p / Trillium (v6)** | Google | US | ~4000 TOPS BF16 (v6) | (TBA) | (internal) | Custom ASIC | Shipping at hyperscale | [Compute Compass](https://computecompass.com/technologies/ai-accelerators) |
| **AWS Trainium 2 / 3** | AWS | US | (TBA) | (TBA) | (internal) | AnnapurnaLabs | Shipping | Yahoo Finance |
| **AWS Inferentia 2** | AWS | US | 190 TOPS BF16 | (TBA) | (internal) | AnnapurnaLabs | Shipping | Yahoo Finance |
| **Microsoft Azure Maia 200** | Microsoft | US | 3nm TSMC, 216GB HBM3e @ 7 TB/s, FP4/FP8 native | 700W est. | (internal) | Custom | Jan 2026 | [Compute Compass](https://computecompass.com/technologies/ai-accelerators) |
| **Meta MTIA** | Meta | US | (TBA) | (TBA) | (internal) | Custom ASIC | Shipping | Yahoo Finance |
| **OpenAI Custom Chip (Broadcom)** | OpenAI | US | (TBA) | (TBA) | (internal) | 3nm TSMC | 2026 mass production | [Compute Compass](https://computecompass.com/technologies/ai-accelerators) |
| **Cerebras WSE-3** | Cerebras | US | Llama 3.3 70B: 2,100–2,500 tok/s | ~27 kW per system | $5M+ (wafer-scale) | Wafer-scale | Public (May 2026 IPO, $56B valuation) | [Spheron](https://www.spheron.network/blog/groq-lpu-vs-cerebras-wse-cheapest-inference-2026) |
| **Groq LPU (GroqRack)** | Groq | US | Llama 3.3 70B: 294–750 tok/s, GPT-OSS-120B: 478–493 tok/s | ~375W per chip | (acquired by NVIDIA Dec 2025 for $20B) | TSP (deterministic) | Now NVIDIA property | [Spheron](https://www.spheron.network/blog/groq-lpu-vs-cerebras-wse-cheapest-inference-2026) |
| **SambaNova SN50 RDU** | SambaNova | US | ~932 tok/s (varies) | (TBA) | $1B Series F (Jul 2026) | Dataflow | Enterprise shipping | [Chipstrat](https://www.chipstrat.com/p/the-next-trillion-dollar-chip-company) |
| **Tenstorrent Wormhole / Blackhole** | Tenstorrent | US | (TBA) | 300W est. | $693M Series D | RISC-V IP / chiplet | Production racks 2026 | Chipstrat |
| **Etched Sohu** | Etched | US | Llama 70B (8-chip): ~62,500 tok/s | (TBA) | $300M Series C (Jul 2026) | Transformer-specific ASIC | Shipping 2026 | [Menon Lab](https://themenonlab.blog/blog/ai-inference-accelerators-compared) |
| **Taalas HC1** | Taalas | US | Llama 3.1 8B: ~17,000 tok/s (hardwired) | (TBA) | $312M Series B (Aug 2026) | Model-specific ASIC | Shipping | [Menon Lab](https://themenonlab.blog/blog/ai-inference-accelerators-compared) |
| **d-Matrix** | d-Matrix | US | (TBA) | (TBA) | $2B valuation | In-memory compute | Sampling | [Omdia](https://omdia.tech.informa.com/om138886/market-landscape-top-ai-hardware-startups--funding-and-trends-2026) |
| **Positron AI** | Positron | US | (TBA) | (TBA) | $230M Series B (Feb 2026) | Memory-centric | Sampling 2026 | [Omdia](https://omdia.tech.informa.com/om138886) |
| **Fractile** | Fractile | UK | (TBA) | (TBA) | (TBA) | (TBA) | Production 2028 | Chipstrat |
| **MatX** | MatX | US | (TBA) | (TBA) | $620M Series B (Feb 2026) at $3B+ val | LLM training | Announced | [Compute Compass](https://computecompass.com/technologies/ai-accelerators) |
| **Graphcore IPU (Bow/Powderhorn)** | Graphcore | UK | (TBA) | (TBA) | (acquired?) | IPU | Limited | [Tracxn](https://tracxn.com) |
| **Lightmatter Passage / Envise** | Lightmatter | US | (TBA) | (TBA) | $4.4B valuation | Photonic compute | Sampling | [Teahose](https://www.teahose.com/guides/ai-chip-companies) |
| **Ayar Labs** | Ayar Labs | US | Optical I/O, 3.2 Tbps | (TBA) | $3.75B valuation | Photonic interconnect | Shipping | Teahose |
| **Neurophos** | Neurophos | US | (TBA) | (TBA) | $110M Series A (Jan 2026) | Photonic inference | Sampling | [New Market Pitch](https://newmarketpitch.com/blogs/news/ai-chip-funding-news) |
| **Salience Labs** | Salience Labs | UK | (TBA) | (TBA) | $11.5M seed | Photonic + electronic | Announced | Compute Compass |
| **LightOn** | LightOn | FR | (TBA) | (TBA) | (TBA) | Optical processing unit | Limited | Compute Compass |
| **Marvell (Celestial AI acquired)** | Marvell | US | 1.6T light engines | (TBA) | $3.25B acquisition | Silicon photonics | Shipping | Compute Compass |
| **Astera Labs** | Astera Labs | US | (connectivity) | (TBA) | $10B market cap | PCIe/CXL retimers | Shipping | Compute Compass |
| **Enfabrica ACF-S SuperNIC** | Enfabrica | US | 3.2 Tbps for 500K GPU clusters | (TBA) | (TBA) | SuperNIC | Shipping | Compute Compass |
| **Xsight Labs** | Xsight Labs | IL | (SDN switches) | (TBA) | (TBA) | Programmable Ethernet + DPU | Shipping | Compute Compass |
| **Untether AI** | Untether AI | CA | (TBA) | (TBA) | (TBA) | Spatial compute | Limited | Future Markets |
| **Exa Laboratories** | Exa Labs | SE | 27.6× H100 efficiency claimed | (TBA) | YC S24 | Reconfigurable dataflow | Announced | [Compute Compass](https://computecompass.com/technologies/ai-accelerators) |
| **Recursvive Intelligence** | Ricursive | US | (AI for chip design) | (TBA) | $335M Series A, $4B val | Custom | Announced | Compute Compass |
| **Cornami** | Cornami | US | (FHE acceleration) | (TBA) | (TBA) | Custom | Sampling | Compute Compass |
| **Etron Technology** | Etron | TW | (KGDM memory) | (TBA) | (TBA) | Memory + AI | Shipping | Compute Compass |
| **SpacemiT** | SpacemiT | CN | (RISC-V K1) | (TBA) | (TBA) | RISC-V SoC | Announced | Compute Compass |
| **Ventana Micro** | Ventana | US | Veyron 192-core RISC-V | (TBA) | $108M+ | RISC-V chiplets | Sampling | Compute Compass |
| **Rivos** | Rivos | US | (RISC-V data center) | (TBA) | acquired by Meta ~$2B | RISC-V server | Sampling | Compute Compass |
| **Semron** | Semron | DE | (memcapacitor) | (TBA) | (TBA) | Analog compute | Announced | Compute Compass |
| **Vertical Compute** | Vertical Compute | BE | (vertical memory) | (TBA) | €20M seed (imec.xpand) | In-memory | Announced | Compute Compass |
| **Synthara** | Synthara | CH | (ComputeRAM) | (TBA) | $15M+ CHF 2.5M | In-memory | Announced | Compute Compass |
| **Vybium** | Vybium | AT | (RISC-V AI for EU) | (TBA) | (TBA) | RISC-V AI | Announced | Compute Compass |
| **OLIX** | OLIX | (TBA) | (frontier inference) | (TBA) | $312M Series B (Aug 2026) | (TBA) | Announced | New Market Pitch |
| **Tensordyne** | Tensordyne | (TBA) | (TBA) | (TBA) | (TBA) | (TBA) | Sampling 2027 | Chipstrat |

---

## 🇨🇳 Tier 4: Chinese AI Accelerators (sovereign-AI / export-control context)

China is ~90% of its own AI accelerator market per Tom's Hardware. ~12 companies shipping.

| Vendor | Flagship chip | TOPS / Performance | Power | Stage | Source |
|---|---|---|---|---|---|
| **Huawei (HiSilicon) Ascend 910B/910C** | Ascend 910C | ~780 TOPS BF16 | 400W | 600K units 2026 (gov-approved) | [Presenc AI](https://presenc.ai/research/chinese-ai-chips-landscape-2026) |
| **Huawei Ascend 950PR** | Atlas 350 card | 2× 950PR chiplets | 750W est. | Mar 2026 launch | YouTube "Just Lost the AI War" |
| **Huawei Ascend 970** | TBA | TBA | TBA | Roadmap 2028 (4 ZettaFLOPS target) | Compute Compass |
| **Cambricon Siyuan 590** | Siyuan 590 | 345 TFLOPS FP16, FP8 | ~300W | Mass production | [Unibetter](https://en.unibetter-ic.com/16-top-ai-chip-makers-in-2026) |
| **Cambricon Siyuan 690** | Siyuan 690 | H100-class | (TBA) | H2 2026 mass production | Unibetter |
| **Biren Technology BR100/BR104** | BR104 | A100-class | (TBA) | Jan 2026 HKEX IPO | Presenc AI |
| **Moore Threads MTT S5000** | Huagang arch. | A100-class | (TBA) | $1.1B Shanghai IPO planned | Compute Compass |
| **MetaX (沐曦) C500** | MetaX GPU | A100-class | (TBA) | Shipping | [Machine Yearning](https://www.machineyearning.io/p/chinas-silicon-vanguard) |
| **Hygon DCU (Z100/K100)** | Hygon DCU | (TBA) | (TBA) | Day-0 DeepSeek V4 support | Presenc AI |
| **Enflame S60** | S60 inference | 70K+ cards to Tencent | (TBA) | Shipping | Machine Yearning |
| **Iluvatar CoreX** | CoreX GPU | A100-class | (TBA) | CAICT passable | Machine Yearning |
| **SOPHGO SG2300x** | SG2300x | 24 TOPS (M.2 module form) | (TBA) | Shipping | [Radxa AICore](https://radxa.com/products) |
| **Moffett AI** | Moffett accelerator | A100-class | (TBA) | CAICT passable | Machine Yearning |
| **Vastai Technologies** | Vastai | (TBA) | (TBA) | Shipping | Compute Compass |
| **Baidu Kunlunxin P800** | Kunlun P800 | (TBA) | (TBA) | 30,000-chip cluster for ERNIE | [Enki AI](https://enkiai.com/ai-market-intelligence/top-10-china-ai-chip-companies-of-2025-whos-winning) |
| **Alibaba T-Head Hanguang** | Hanguang 800 | Inference-focused | (TBA) | Used in Alibaba cloud | Yahoo Finance |
| **Tenstorrent China JV (Wuxi)** | RISC-V | (TBA) | (TBA) | New 2026 | Various |
| **HOUMO.AI** | Autonomous driving | (TBA) | (TBA) | Shipping | Compute Compass |
| **Horizon Robotics Journey 5/6** | Journey 6 | 49% China ADAS market share | (TBA) | Shipping | Compute Compass |
| **SiEngine (Geely/Arm China JV)** | 7nm ADAS chip | 512 TOPS NPU | (TBA) | Shipping | Compute Compass |
| **RoboSense M-Core** | M-Core SoC | (TBA) | (TBA) | 1M+ LiDAR units | Compute Compass |

**Chinese accelerator insights:**
- **Huawei Ascend 910C is the volume leader** — 600K units 2026, ~60% of H100 performance, government-approved.
- **Cambricon + Moore Threads + MetaX are the next tier** — all A100-class, all targeting domestic hyperscalers.
- **The Enflame S60 has the largest real deployment** (70K cards to Tencent) outside Huawei.
- **SOPHGO SG2300x is the Radxa-distributed M.2 option** — 24 TOPS, Chinese sovereign-AI compatible.

---

## 🇰🇷 Tier 5: Korean AI Accelerators

| Vendor | Flagship chip | TOPS / Performance | Power | Stage | Source |
|---|---|---|---|---|---|
| **Rebellions REBEL / Rebel-Quad** | Rebel-Quad | Dataflow + HBM + UCIe chiplet | 300W est. | $400M Series D, $2.34B val, $850M raised | [Compute Compass](https://computecompass.com/technologies/ai-accelerators) |
| **Rebellions REBEL-Quad Server** | ATOM-Max | (TBA) | (TBA) | Production 2026 | Compute Compass |
| **Sapeon X330** (merged w/ Rebellions) | X330 | (TBA) | (TBA) | Merged Dec 2024 | Compute Compass |
| **FuriosaAI RNGD** | RNGD | (TBA) | (TBA) | $2.1B valuation, IPO targeted 2026 | [Silicon Shift](https://medium.com/@fahey_james/the-silicon-shift-why-hardware-is-suddenly-the-hottest-early-stage-bet-in-ai-e0bbb3521eb4) |
| **DEEPX DX-M1 / DX-H1** | DX-M1 | 25 TOPS (M.2 module) | 2–5W | Shipping | [DEEPX](https://www.deepx.ai) |
| **Mobilint** | Edge NPU | (TBA) | (TBA) | $310M–$480M valuation | [New Market Pitch](https://newmarketpitch.com/blogs/news/ai-chip-top-startups-valuation) |
| **SK Hynix** | HBM3e | (memory, not compute) | — | Shipping at scale | Industry standard |
| **Samsung** | HBM + foundry | — | — | Shipping at scale | Industry standard |

**Korean accelerator insights:**
- **Rebellions is the Korean Nvidia-competitor** — government-backed "K-Nvidia" $166M investment.
- **DEEPX DX-M1 is the Korean Hailo-8 competitor** — 25 TOPS, $147–$159, Korean-made.
- **FuriosaAI RNGD** is the LLM inference specialist — listed for IPO 2026.

---

## 🇯🇵 Tier 6: Japanese AI Accelerators

| Vendor | Flagship chip | TOPS / Performance | Power | Stage | Source |
|---|---|---|---|---|---|
| **EdgeCortix SAKURA-II** | SAKURA-II | 60 TOPS / 240 TOPS system | ~8W typ | $110M Series B | [EdgeCortix](https://www.edgecortix.com/en) |
| **EdgeCortix SAKURA-X** | SAKURA-X | 2,000 TOPS | TBA | Mid-2026 | EdgeCortix |
| **Socionext** | (various) | (TBA) | (TBA) | Limited | Industry |
| **Preferred Networks MN-Core** | MN-Core 2 | (TBA) | (TBA) | Limited | Industry |
| **Renesas RZ/V2H** | DRP-AI3 | 80 sparse / 8 INT8 | ~10W | Shipping | [Geniatech](https://www.geniatech.com/rz-v2h-ai-som-osm-module/) |
| **Sakana AI** | (AI models, not chips) | — | — | Unicorn | Compute Compass |

**Japanese accelerator insights:**
- **EdgeCortix SAKURA-II is the most interesting M.2-class Japanese option** — 60 TOPS with GenAI support, NASA-validated for orbital use.
- **Renesas RZ/V2H is for robotics**, not LLM (DRP-AI3 is vision + control).

---

## 🇪🇺 Tier 7: European AI Accelerators

| Vendor | Country | Product | TOPS / Performance | Stage | Source |
|---|---|---|---|---|---|
| **Axelera AI** | NL | Metis AIPU | 214 TOPS | $120M+ | [Axelera](https://www.axelera.ai) |
| **Axelera Titania** | NL | Chiplet | TBA | 2028 | Axelera |
| **Graphcore** | UK | IPU (Bow/Powderhorn) | TBA | Limited | Compute Compass |
| **Fractile** | UK | TBA | TBA | 2028 production | Chipstrat |
| **GreenWaves Technologies** | FR | GAP RISC-V | TBA | Shipping | Compute Compass |
| **Kalray** | FR | MPPA Coolidge | TBA | Shipping | Compute Compass |
| **LightOn** | FR | Optical processing unit | TBA | Limited | Compute Compass |
| **Arago** | FR | TBA | TBA | Announced | Compute Compass |
| **SiMa.ai** | (US, EU presence) | MLSoC | 50+ TOPS | Shipping | Compute Compass |
| **Achronix** | (US, EU design) | VectorPath FPGA cards | 7t, 2.5D FPGA | Shipping | [Achronix](https://www.achronix.com/AI) |
| **Positron** | (US, but in-memory compute) | FPGA-based | $23.5M | Announced | Compute Compass |
| **Exa Laboratories** | SE | Reconfigurable dataflow | 27.6× H100 claimed | YC S24 | Compute Compass |
| **Salience Labs** | UK | Photonic + electronic | TBA | $11.5M seed | Compute Compass |
| **Synthara** | CH | ComputeRAM | TBA | $15M+ | Compute Compass |
| **Vybium** | AT | RISC-V AI for EU sovereign | TBA | Announced | Compute Compass |
| **Kontron** | DE | VPX defense | TBA | Shipping | Compute Compass |
| **Vertical Compute** | BE | Vertical memory chiplet | TBA | €20M seed | Compute Compass |
| **Semron** | DE | Memcapacitor | TBA | Announced | Compute Compass |
| **Exa Labs (Sweden)** | SE | Reconfigurable dataflow (XPUs) | 27.6× H100 | Announced | Compute Compass |
| **Speedata** | IL (Israeli but EU engagement) | Analytics Processing Unit (APU) | TBA | Shipping | Compute Compass |

**European insights:**
- **Axelera Metis is the only EU-made M.2 with high TOPS** — 214 TOPS but vision-only.
- **Achronix VectorPath cards are the LLM-on-FPGA option** — 7t series, expensive but flexible.
- **EU AI sovereignty is the pitch** — Vybium, Salience, Synthara, Vertical Compute all pitch to EU digital autonomy.

---

## 🇮🇱 Tier 8: Israeli AI Accelerators

| Vendor | Product | TOPS / Performance | Power | Stage | Source |
|---|---|---|---|---|---|
| **Hailo-8 / 8L / 10H** | M.2 accelerator | 13–40 TOPS | 1.5–3W | Shipping at scale | [Hailo](https://hailo.ai) |
| **Hailo-15H/15L** | In-camera SoC | 30–40 TOPS | TBA | Shipping (auto) | Hailo |
| **Hailo-26H** | (Roadmap 2026) | (TBA) | TBA | Announced | Hailo |
| **NeuroBlade** | (TBA) | (TBA) | TBA | Announced | [Silicon Vanguard](https://www.machineyearning.io/p/chinas-silicon-vanguard) |
| **Speedata** | APU | (TBA) | (TBA) | Shipping | Compute Compass |
| **Xsight Labs** | DPU + SDN switch | TBA | TBA | Shipping | Compute Compass |
| **DeGirum** | ORCA edge AI | TBA | TBA | $42M | Compute Compass |
| **Aitech Defense** | A230 Vortex (Jetson-based) | 275 TOPS | TBA | Shipping | Compute Compass |
| **Mobilint** | Edge NPU (also Korea) | TBA | TBA | $310M | New Market Pitch |
| **Run:ai** | GPU orchestration | — | — | Acquired by NVIDIA 2024 | Compute Compass |

**Israeli insights:**
- **Hailo is the clear Israeli leader for edge AI** — used in every major SBC ecosystem.
- **NeuroBlade and Speedata** are the next-gen, less-known Israeli entries.

---

## 🇺🇸 Tier 9: US AI Accelerators (subset, beyond data center)

| Vendor | Product | TOPS / Performance | Stage | Source |
|---|---|---|---|---|
| **Apple ANE (M1-M4)** | Integrated in M-series | 15–38 TOPS | Shipping at scale | Starmorph |
| **NVIDIA Jetson AGX Orin** | SoM | 275 TOPS | Shipping | AIMultiple |
| **NVIDIA Jetson Orin Nano Super** | SoM | 67 sparse / 33 dense | Shipping | AIMultiple |
| **NVIDIA Jetson Orin NX** | SoM | 100–157 TOPS | Shipping | Radxa C200 |
| **Google Coral M.2 / USB** | Edge TPU | 4 TOPS | EOL announced 2026 | Seeed |
| **AMD XDNA NPU** | Ryzen AI | 10–50 TOPS | Shipping | AIMultiple |
| **Intel Core Ultra NPU** | x86 SoC | 10–50 TOPS | Shipping | Geniatech |
| **Ambarella CV5** | Camera SoC | 8K30/8K60 | Shipping | AIMultiple |
| **SiMa.ai MLSoC** | Edge | 50+ TOPS | Shipping | Compute Compass |
| **Qualcomm Hexagon NPU** | RB5, others | 15+ TOPS | Shipping | AIMultiple |
| **MemryX MX3** | M.2 | 24 TOPS | Shipping | Geniatech |
| **DeepX DX-M1** | M.2 | 25 TOPS | Shipping | Geniatech |
| **Kneron Kneo 330** | Edge box | TBA | Shipping | Kneron |
| **Nordic Axon NPU** | nRF SoC | TBA | Shipping | Nordic |
| **Achronix VectorPath** | FPGA card | TBA | Shipping | Achronix |
| **Cornami** | FHE | TBA | Sampling | Compute Compass |
| **Perceive** | Ergo | TBA | Sampling | Compute Compass |
| **Esperanto** | RISC-V AI | TBA | $115M | Compute Compass |
| **HyperCIM** | Compute-in-memory | TBA | Announced | Compute Compass |
| **Rivos** | RISC-V data center | TBA | Acquired by Meta | Compute Compass |
| **Ventana** | RISC-V chiplet | TBA | $108M+ | Compute Compass |
| **MatX** | LLM training | TBA | $620M Series B | Compute Compass |
| **d-Matrix** | In-memory inference | TBA | $2B val | Omdia |
| **Positron** | Memory-centric | TBA | $230M Series B | Omdia |
| **Cerebras** | WSE-3 wafer | 27kW systems | Public | Spheron |
| **Groq** | LPU | 375W/chip | Acquired by NVIDIA | Spheron |
| **SambaNova** | RDU dataflow | TBA | $1B Series F | New Market Pitch |
| **Tenstorrent** | RISC-V chiplet | TBA | $693M Series D | Chipstrat |
| **Etched** | Transformer ASIC | TBA | $300M Series C | Menon Lab |
| **Taalas** | Model-specific ASIC | Llama 8B 17,000 tok/s | $312M Series B | Menon Lab |
| **Fractile** | TBA | TBA | Announced | Chipstrat |
| **Lightmatter** | Photonic compute | TBA | $4.4B val | Teahose |
| **Ayar Labs** | Optical I/O | TBA | $3.75B val | Teahose |
| **Astera Labs** | Connectivity | TBA | $10B cap | Compute Compass |
| **Enfabrica** | SuperNIC | TBA | Shipping | Compute Compass |
| **OpenAI (Broadcom)** | Custom AI chip | TBA | 2026 mass production | Compute Compass |
| **Microsoft Azure Maia 200** | Custom | 216GB HBM3e | Jan 2026 | Compute Compass |
| **Meta MTIA** | Custom | TBA | Shipping | Yahoo Finance |
| **Google TPU Trillium (v6)** | Custom | ~4000 TOPS | Shipping | Compute Compass |
| **AWS Trainium 2/3** | Annapurna Labs | TBA | Shipping | Yahoo Finance |
| **AWS Inferentia 2** | Annapurna Labs | 190 TOPS BF16 | Shipping | Yahoo Finance |

---

## 💻 Tier 10: FPGA-based AI Accelerators

Programmable, not fixed silicon. Higher NRE but flexible.

| Vendor | Product | TOPS / Notes | Stage | Source |
|---|---|---|---|---|
| **AMD Xilinx Alveo U280** | Data center FPGA | TBA (general-purpose) | Shipping | [Achronix comparison](https://www.achronix.com/blog/accelerating-llm-inferencing-fpgas) |
| **AMD Xilinx Alveo V70** | Versal AI Edge | TBA | Shipping | AMD |
| **AMD Xilinx Versal AI Edge** | Adaptive SoC | AIE engines | Shipping | AMD |
| **AMD Xilinx Versal AI Core** | Adaptive SoC | AIE for wireless + AI | Shipping | AMD |
| **AMD Xilinx Versal Premium** | Adaptive SoC | 7nm, 112G SerDes | Shipping | AMD |
| **Intel Stratix 10 NX** | AI-optimized FPGA | Tensor blocks | Shipping | Achronix comparison |
| **Intel Agilex 7** | Mid-range FPGA | TBA | Shipping | Achronix comparison |
| **Intel Versal VCK5000** | AI Engine FPGA | AIE for AI | Shipping | Achronix comparison |
| **Achronix Speedster7t** | 7t series | 2.5D FPGA | Shipping | Achronix |
| **Achronix VectorPath VP815** | PCIe card | LLM-optimized | Shipping | Achronix |
| **Lattice ECP5** | Low-power FPGA | TBA | Shipping | Industry |
| **Lattice Certus-NX** | Small FPGA | TBA | Shipping | Industry |
| **Microchip PolarFire** | Mid-range FPGA | TBA | Shipping | Industry |
| **Microchip RTG4** | Radiation-tolerant | TBA | Shipping | Industry |
| **Efinix Trion/Titanium** | Edge FPGA | TBA | Shipping | Industry |
| **QuickLogic EOS S3** | Sensor + NPU | TBA | Shipping | Industry |
| **Positron (FPGA-based)** | Sustainable AI | TBA | $23.5M | Compute Compass |

---

## 🧪 Tier 11: Special Architectures (in-memory, photonic, neuromorphic, analog)

| Vendor | Architecture | Country | TOPS / Notes | Stage | Source |
|---|---|---|---|---|---|
| **MemryX** | Memristor + CMOS | US | 24 TOPS MX3 | Shipping | [MemryX](https://memryx.com) |
| **Mythic** | Analog compute-in-memory | US | 25–100 TOPS (AMP) | Limited / pivoted | (industry history) |
| **Syntiant** | Neuromorphic audio | US | TinyML NDP | Shipping | Industry |
| **BrainChip** | Neuromorphic Akida | AU | Event-based | Shipping | Industry |
| **GrAI Matter Labs** | Neuromorphic | NL/FR | TBA | Limited | Industry |
| **Lightmatter Envise / Passage** | Photonic compute | US | TBA | Sampling | Compute Compass |
| **LightOn** | Optical processing unit | FR | TBA | Limited | Compute Compass |
| **Ayar Labs** | Optical I/O | US | 3.2 Tbps | Shipping | Teahose |
| **Neurophos** | Photonic inference | US | TBA | $110M | New Market Pitch |
| **Salience Labs** | Photonic + electronic | UK | TBA | $11.5M seed | Compute Compass |
| **Marvell Celestial AI** | Silicon photonics | US | 1.6T light engines | $3.25B acquisition | Compute Compass |
| **Semron** | Memcapacitor | DE | TBA | Announced | Compute Compass |
| **Synthara** | ComputeRAM | CH | TBA | Announced | Compute Compass |
| **Vertical Compute** | Vertical memory | BE | TBA | Announced | Compute Compass |
| **Etron KGDM** | Memory + AI | TW | TBA | Announced | Compute Compass |
| **HyperCIM** | Compute-in-memory | US | TBA | Announced | Compute Compass |
| **Cornami** | Homomorphic encryption | US | TBA | Sampling | Compute Compass |
| **Rain AI** | Analog compute | US | TBA | Announced | Industry |
| **Mythic AI** | Analog compute-in-memory | US | (pivoted to software) | N/A | Industry |
| **Aspinity** | Always-on analog | US | TBA | Shipping | Industry |
| **POLYN Technology** | Neuromorphic analog | IL | TBA | Shipping | Industry |
| **SynSense** | Neuromorphic | CH | TBA | Shipping | Industry |
| **Innatera** | Neuromorphic | NL | TBA | Shipping | Industry |
| **GrAI Matter Labs** | Neuromorphic | NL | TBA | Limited | Industry |

---

## 🏢 Tier 12: Auto / Industry-Specific AI Accelerators

| Vendor | Product | TOPS | Use case | Source |
|---|---|---|---|---|
| **Ambarella CV5** | Camera SoC | Not disclosed | 8K camera, dashcam | [AIMultiple](https://aimultiple.com/edge-ai-chips) |
| **Hailo-15H/15L** | Camera SoC | 30–40 TOPS | Auto, security | [Hailo](https://hailo.ai) |
| **Mobileye EyeQ5/6** | ADAS SoC | TBA | Auto ADAS | Industry |
| **Horizon Robotics Journey 6** | Auto SoC | TBA | 49% China ADAS | Compute Compass |
| **SiEngine** | Auto SoC | 512 TOPS NPU | Geely vehicles | Compute Compass |
| **HOUMO.AI** | Auto AI | TBA | China AD | Compute Compass |
| **Qualcomm Snapdragon Ride** | Auto AI | TBA | Auto | Industry |
| **NVIDIA DRIVE Orin / Thor** | Auto SoC | 275+ TOPS | Auto | Industry |
| **RoboSense M-Core** | LiDAR SoC | TBA | 1M+ units | Compute Compass |
| **Hesai AI chip** | LiDAR | TBA | Auto LiDAR | Industry |
| **Inceptio** | Auto AI | TBA | Trucking | Industry |
| **NXP S32N** | Auto MCU + NPU | TBA | Auto | Industry |
| **TI TDA4VM** | Auto SoC | TBA | Auto | Industry |
| **Renesas RZ/V2H** | Auto/robotics | 80 sparse TOPS | Auto + factory | Geniatech |

---

## 📊 Quick Selection Guide (for Calvin's Red Cell)

| If you need... | Pick | Cost | Why |
|---|---|---|---|
| Cheapest LLM-capable M.2 | **Hailo-10H** | $130–$170 | Only M.2 with LLM + low power + 40 TOPS |
| LLM >5B parameter | **NXP Ara-240** | $299 | 16GB onboard, 7B capable |
| 7B LLM fastest | **RK1828** | $280–$340 | 30 tok/s on 7B (vs 12 on Ara) |
| Vision-only, vision-first | **Hailo-8** | $179 | Mature, $179, 26 TOPS |
| Edge LLM in SoC (no add-on) | **RK3588 / RK3588S** (any SBC) | $109–$189 | RKLLama, 3–5 tok/s on Qwen2-1.5B |
| Premium with GenAI ready | **EdgeCortix SAKURA-II** | est. $400–$600 | NASA-validated, 240 TOPS system |
| Maximum TOPS M.2 (vision) | **Axelera Metis** | €221 | 214 TOPS but vision |
| Cheapest ever | **Google Coral M.2** | $60 | EOL 2026, but still cheap |
| Mass deployment x86 | **Intel Core Ultra NPU** | bundled | 50 TOPS, no add-on needed |

---

## 🌍 Coverage by Country

| Country | Count | Notable |
|---|---|---|
| 🇺🇸 US | 35+ | Cerebras, Groq, NVIDIA, AMD, Apple, Google, Microsoft, OpenAI, SambaNova, Tenstorrent, Etched, Taalas, d-Matrix, Positron, MatX, Lightmatter, Ayar Labs, Achronix, MemryX, DeepX, Kneron, Hailo (US ops), etc. |
| 🇨🇳 China | 20+ | Huawei Ascend, Cambricon, Biren, Moore Threads, MetaX, Hygon, Enflame, Iluvatar CoreX, SOPHGO, Moffett AI, Kunlunxin, Alibaba T-Head, SpacemiT, Vastai, HOUMO, Horizon, SiEngine, RoboSense |
| 🇰🇷 Korea | 6+ | Rebellions, Sapeon, FuriosaAI, DEEPX, Mobilint, SK Hynix (HBM) |
| 🇮🇱 Israel | 5+ | Hailo, NeuroBlade, Speedata, Xsight Labs, DeGirum, Aitech, Mobilint |
| 🇯🇵 Japan | 4+ | EdgeCortix, Renesas, Socionext, Preferred Networks, Sakana |
| 🇬🇧 UK | 5+ | Graphcore, Fractile, Salience Labs, Arm, Imagination |
| 🇫🇷 France | 4+ | Axelera (NL), LightOn, Kalray, GreenWaves, Arago, SiMa (US-EU) |
| 🇩🇪 Germany | 4+ | Kontron, Semron, Celus |
| 🇳🇱 Netherlands | 4+ | Axelera, GrAI Matter, Innatera |
| 🇸🇪 Sweden | 1+ | Exa Labs |
| 🇨🇭 Switzerland | 1+ | Synthara |
| 🇦🇹 Austria | 1+ | Vybium |
| 🇧🇪 Belgium | 1+ | Vertical Compute |
| 🇹🇼 Taiwan | 2+ | Etron, MediaTek, TSMC (foundry) |
| 🇳🇴 Norway | 1+ | Nordic Semiconductor |
| 🇦🇺 Australia | 1+ | BrainChip |

**Total: 90+ companies across 17+ countries.** Compute Compass's full list is 191; I've captured the 90+ that are actively shipping M.2/edge accelerators with real LLM/CNN support. The other ~100 are either early-stage (no product), tool/EDA companies, or pure-software.

---

## 💰 Pricing Tier Summary

| Tier | Price | Examples |
|---|---|---|
| **< $100** | M.2 EOL or DIY | Google Coral M.2 ($60), Pi 5 8GB ($60), OPi 5 Pro 16GB ($109) |
| **$100–$300** | Mainstream M.2 / SBC | Hailo-8 ($179), Hailo-10H ($170), RK1820 ($140–$200), DeepX DX-M1 ($147), MemryX MX3 ($149), OPi 5 Pro ($109), Pi 5 + Hailo ($305) |
| **$300–$500** | Premium M.2 / SoM | NXP Ara-240 ($299), RK1828 ($280–$340), Radxa Orion O6 ($280), EdgeCortix SAKURA-II M.2 (est.) |
| **$500+** | Data center | Jetson AGX Orin ($1,999), Mac Mini M4 16GB ($599), Mac Mini M4 Pro 24GB ($1,199), NVIDIA H100 ($25k+) |
| **$1M+** | Wafer-scale / cluster | Cerebras CS-3 ($5M), rack-scale |

---

## 🧭 What's NOT on this list (intentionally)

- **Pure-software companies** (Cerebrus, Run:ai, Lightning AI, etc.) — not hardware
- **EDA companies** (Synopsys, Cadence) — chip design tools, not chips
- **EDA-AI startups** (ChipAgents, MatX) — debatable, but MatX is hardware
- **Memory-only** (SK Hynix HBM, Samsung HBM) — included only as context
- **Foundries** (TSMC, SMIC) — not accelerator designers
- **Hyperscaler in-house chips** (Meta MTIA, Google TPU, AWS Trainium) — partially included
- **Dormant / pivoted** (Mythic, Graphcore current state) — noted in passing
- **Academic-only** — most academic chips are not commercial

---

## Sources

**Master lists:**
- [Compute Compass — 191 AI Accelerator Companies](https://computecompass.com/technologies/ai-accelerators)
- [AIMultiple — Top 15 Edge AI Chip Makers](https://aimultiple.com/edge-ai-chips)
- [Geniatech — Choosing the Right M.2 AI Accelerator for Edge AI (Mar 2026)](https://www.geniatech.com/edge-ai-m2-accelerator-comparison-vision-npus-llm-chips)
- [Geniatech — Hailo-10 vs Intel Core Ultra NPU (Feb 2026)](https://www.geniatech.com/hailo-10-vs-intel-npu-edge-ai)
- [New Market Pitch — Top AI Chip Startups by Valuation](https://newmarketpitch.com/blogs/news/ai-chip-top-startups-valuation)
- [Future Markets — AI Chips Market 2026-2036](https://www.futuremarketsinc.com/the-global-artificial-intelligence-ai-chips-market-2026-2036)
- [Tracxn — Top AI Processors](https://tracxn.com)
- [Teahose — Top AI Chip Companies in 2026](https://www.teahose.com/guides/ai-chip-companies)
- [Chipstrat — The Next Trillion-Dollar Chip Company](https://www.chipstrat.com/p/the-next-trillion-dollar-chip-company)
- [Silicon Shift — Why Hardware Is Suddenly the Hottest Early-Stage Bet](https://medium.com/@fahey_james/the-silicon-shift-why-hardware-is-suddenly-the-hottest-early-stage-bet-in-ai-e0bbb3521eb4)
- [Menon Lab — AI Inference Wars: Taalas, Cerebras, Groq, Etched, NVIDIA](https://themenonlab.blog/blog/ai-inference-accelerators-compared)
- [Spheron — Groq vs Cerebras Cheapest Inference Chip](https://www.spheron.network/blog/groq-lpu-vs-cerebras-wse-cheapest-inference-2026)
- [Omdia — Top AI Hardware Startups 2026](https://omdia.tech.informa.com/om138886/market-landscape-top-ai-hardware-startups--funding-and-trends-2026)

**Chinese / Korean / Japanese:**
- [Presenc AI — Chinese AI Chips Landscape 2026](https://presenc.ai/research/chinese-ai-chips-landscape-2026)
- [Machine Yearning — China's Silicon Vanguard](https://www.machineyearning.io/p/chinas-silicon-vanguard)
- [Tom's Hardware — China's 90% domestic AI accelerator market](https://www.tomshardware.com/tech-industry/artificial-intelligence/chinas-homegrown-ai-accelerators-to-supply-90-percent-of-the-countrys-domestic-market-analysts-suggest-cambricon-and-huawei-expected-to-be-the-biggest-winners-in-the-shift-away-from-nvidia-and-amd)
- [Unibetter — 16 Top AI Chip Makers 2026](https://en.unibetter-ic.com/16-top-ai-chip-makers-in-2026)
- [Enki AI — Top 10 China AI Chip Companies 2025](https://enkiai.com/ai-market-intelligence/top-10-china-ai-chip-companies-of-2025-whos-winning)
- [Wikipedia — Rebellions (company)](https://en.wikipedia.org/wiki/Rebellions_(company))
- [Reuters — South Korea invests $166M in Rebellions](https://www.reuters.com/world/asia-pacific/south-korea-invest-166-million-ai-chip-startup-rebellions-2026-03-26)
- [CNBC — Samsung-backed Rebellions raises $400M](https://www.cnbc.com/2026/03/30/ai-chip-startup-rebellions-raises-400-million-ipo.html)
- [EdgeCortix](https://www.edgecortix.com/en)
- [AllAboutCircuits — Rebellions: The Korean Company to Watch in 2026](https://www.allaboutcircuits.com/news/rebellions-the-korean-company-to-watch-in-2026)

**SBC + integrated NPU:**
- [Orange Pi catalog](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/index.html)
- [Radxa products](https://radxa.com/products)
- [interfacinglinux.com — Vulkan llama.cpp on OPi 6+ / Orion O6](https://interfacinglinux.com/community/sbcsoftware/vulkan-powered-llama-cpp-on-the-orion-o6-and-o6n)
- [Sngular — Qwen3 on RK3588 NPU via RKLLama](https://www.sngular.com/insights/471/the-definitive-guide-to-deploying-qwen3-on-the-npu-of-the-orange-pi-5-pro-max-plus-ultra-using-rkllama-and-microk8s)
- [Radxa forum — Llama.cpp benchmarks on CIX P1 / Orion O6](https://forum.radxa.com/t/llama-cpp-benchmarks/27813)

**Accelerator vendor catalogs:**
- [Hailo products](https://hailo.ai/products/ai-accelerators/)
- [Hailo-10H M.2 module](https://hailo.ai/products/ai-accelerators/hailo-10h-m-2-ai-acceleration-module)
- [EdgeCortix SAKURA-II](https://www.edgecortix.com/en/thank-you/edgecortix-to-develop-next-generation-ai-semiconductor-by-mid-2026)
- [Kneron CES 2026](https://www.kneron.com/news/blog/265)
- [Waveshare Hailo-8 M.2](https://www.waveshare.com/hailo-8.htm)
- [Achronix — LLM Acceleration](https://www.achronix.com/AI/large-language-model-acceleration)
- [AMD Versal AI](https://www.amd.com/en/products/adaptive-socs-and-fpgas/technologies/ai-engine.html)

**Hailo LLM data:**
- [codesota.com — Hailo-10H LLM benchmarks](https://www.codesota.com/embedded-ai/hailo-10h-llms)
- [Hailo community — Llama.cpp server and CLI with Hailo-10H support](https://community.hailo.ai/t/llama-cpp-server-and-cli-with-hailo-10h-support/18810)

**Mobile / NPU:**
- [Starmorph — Apple Silicon LLM Inference Optimization](https://blog.starmorph.com/blog/apple-silicon-llm-inference-optimization-guide)
- [Hailo DRAM Shortage 2026](https://hailo.ai/blog/dram-shortage-in-edge-ai-doing-more-with-less)
- [Seeed — Pi AI Kit vs Coral](https://www.seeedstudio.com/blog/2024/07/16/raspberry-pi-ai-kit-vs-coral-usb-accelerator-vs-coral-m-2-accelerator-with-dual-edge-tpu)

---

*Generated by Severus · 25 Aug 2026 · solo build · 90+ accelerator providers across 12 tiers, 17+ countries, with LLM support, TOPS, power, price, and form factor. All claims sourced.*
