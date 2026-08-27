> ⚠️ **Price caveat (2026-08-27):** any USD figure in this document predates the
> 2025–2026 DRAM shortage, which moved hardware prices −20% to +275%
> ([CNX, 2026-04-28](https://www.cnx-software.com/2026/04/28/what-a-difference-two-years-make-comparing-sbc-prices-in-2024-and-2026)).
> Treat specs and measured performance as valid; treat every price and cost ranking
> as unverified until re-checked.

# CNN vs Transformer — Plain English Architecture Explainer
**Date:** 25 Aug 2026 · **Author:** Severus (Claude Opus 5) · **Audience:** anyone who needs to understand why certain hardware choices make sense

> Both are types of **neural network architectures** — the fundamental design patterns that determine how an AI model processes data. The difference between them is the single most important thing to understand when choosing AI hardware.

---

## TL;DR

```
CNN      = Camera / eyes    (look at one image, give one answer)
Transformer = Reader / brain (read a book, write a response)
```

CNN says "**what do I see?**"
Transformer says "**what should I say next?**"

That's it. Everything else flows from this distinction.

---

## 1. CNN — Convolutional Neural Network

**Specialized for: images, video, audio spectrograms, time-series sensor data**

The "convolution" is a **sliding window** that scans across the input and looks for patterns. Think of it like a flashlight sweeping across a photo, checking for edges, shapes, textures as it goes.

### How it works (visual)

```
Image of a cat (300×300 pixels = 90,000 values)
┌──────────────┐
│  🐱          │  →  Filter 1: "edge detector" → finds cat outline
│              │  →  Filter 2: "color detector" → finds fur color
│   (pixels)   │  →  Filter 3: "shape detector" → finds ears, eyes
└──────────────┘
       ↓
   Combined features
       ↓
   "Cat: 97% confidence"
```

Each filter is **small** (e.g., 3×3 pixels) but gets **applied across the entire image**. This is the "convolution" — a tiny pattern detector sweeping everywhere.

### Key properties

| Property | Value | Why it matters |
|---|---|---|
| **One-shot inference** | Single forward pass | Fast (milliseconds per image) |
| **Memory footprint** | 5–50 MB weights | Fits in chip SRAM, no DRAM needed |
| **Compute pattern** | Dense MAC arrays | Loves high TOPS, hates memory bandwidth |
| **Deterministic output** | Same image → same answer | Good for real-time control |
| **No "memory" between frames** | Each frame independent | Perfect for video streams |

### Famous CNNs

- **ResNet** (2015) — the foundational image classifier
- **YOLO** (2016+) — real-time object detection ("you only look once")
- **MobileNet** (2017+) — efficient CNN for phones
- **EfficientNet** (2019+) — Google's scaled-down CNN family

### Where CNNs live in 2026

- Security cameras, IP cameras, NVRs
- Self-driving cars (Tesla FSD, Waymo)
- Medical imaging (X-ray, CT, MRI analysis)
- Factory quality control
- Face unlock on your phone
- Frigate NVR / Home Assistant
- Smart doorbells

---

## 2. Transformer — Attention-Based Neural Network

**Specialized for: language, code, sequences, any context where you need long-range understanding**

The "attention" mechanism lets the model look at **all the words at once** and figure out which words relate to which other words. This is how it understands that "bank" means money vs. river vs. airplane in different sentences.

### How it works (visual)

```
Sentence: "The cat sat on the mat because it was tired"
                    ↓
Transformer reads ALL words at once
                    ↓
For each word, compute attention scores to every other word:

       The  cat  sat  on  the  mat  because  it  was  tired
The  [  --  .05  .02  .01  .10  .01   .02   .03  .02  .01 ]
cat  [ .05  --  .20  .15  .10  .15   .05   .25  .10  .20 ]
sat  [ .02  .20  --  .15  .05  .10   .03   .10  .08  .10 ]
on   [ ...                          ]
it   [ .03  .25  .10  ...                         .10 ]
     (Each row: where does this word "attend"?)
                    ↓
Question: What does 'it' refer to?
                    ↓
Looking at 'it' row: cat=0.25, mat=0.10, tired=0.05
                    ↓
Answer: 'it' = the cat (highest attention weight)
```

### Key properties

| Property | Value | Why it matters |
|---|---|---|
| **Autoregressive generation** | One token at a time, repeat | Slow (50ms+ per token) |
| **Memory footprint** | 1–16 GB weights + KV cache | Requires external DRAM |
| **Compute pattern** | Memory-bandwidth bound | Needs GB/s, not TOPS |
| **Context-sensitive** | All tokens "see" each other | Great at nuance, references, long docs |
| **Stateful between calls** | KV cache carries forward | High memory pressure |

### Famous Transformers

- **GPT-4 / Claude / Gemini** — large language models
- **Qwen, Llama, Mistral** — open-source LLMs
- **BERT, RoBERTa** — early encoder-only transformers (understanding, not generation)
- **T5, FLAN** — encoder-decoder transformers
- **Vision Transformer (ViT)** — transformer for images (yes, CNN isn't the only way!)

### Where Transformers live in 2026

- Chatbots and assistants
- Code generation (Claude Code, Cursor, GitHub Copilot)
- Search and ranking
- Translation
- Summarization
- RAG (Retrieval-Augmented Generation)
- Document Q&A
- Voice assistants (Whisper is transformer-based)

---

## 3. Side-by-side comparison

```
CNN (Convolutional):
─────────────────────
Input:  A whole image at once
Process: Slide filters across the image
Output: One answer (e.g., "cat", "no cat")
Time:   Fast (milliseconds)
Memory: Low (doesn't need to remember)
Steps:  ONE forward pass

Transformer (Attention):
─────────────────────
Input:  A sequence of tokens (words, code, etc.)
Process: Look at ALL tokens, find relationships
Output: One token at a time, then loop
Time:   Slow (seconds, generates token-by-token)
Memory: High (must remember all previous tokens)
Steps:  MANY forward passes (one per token generated)
```

### Quantitative comparison

| Metric | CNN (typical) | Transformer (typical) | Ratio |
|---|---|---|---|
| Weights | 5–50 MB | 1–16 GB | **200× heavier** |
| Input size | 1 image | up to 1M tokens | Different unit |
| Output | 1 prediction | up to 100K tokens | Different unit |
| Latency | 5–50 ms | 50–500 ms/token | 10× slower |
| Memory bandwidth | 4 GB/s (M.2 PCIe) | 50+ GB/s (HBM) | **12× more BW** |
| Power at idle | 2.5W (Hailo-8) | 25W+ (M.2 LLM modules) | 10× more power |
| Power at load | 8W (Hailo-8) | 100W+ (Mac Mini MLX) | 12× more |

---

## 4. The crucial memory-bandwidth math

This is **the** number that determines whether a model will run well on given hardware.

### For CNNs (vision)

```
YOLOv8n example:
- 3.2M weights × 4 bytes (FP32) = 12.8 MB total weights
- One forward pass needs to read those weights once
- Total memory traffic per inference: ~12.8 MB
- At 4 GB/s M.2 PCIe bandwidth: 3.2 ms per inference
```

CNN inference is **compute-bound**, not memory-bound. Adding more TOPS speeds it up.

### For Transformers (LLMs)

```
Qwen 2.5 7B example:
- 7B weights × 2 bytes (FP16) = 14 GB total weights (lol too big for M.2)
- For Qwen 2.5 0.5B: 0.5B × 2 bytes = 1 GB total weights
- Each generated token reads ALL weights once + KV cache
- Per-token memory traffic: ~1 GB for 0.5B model
- At 50 GB/s Apple M4 memory bandwidth: 20 ms per token = 50 tok/s
- At 4 GB/s M.2 PCIe bandwidth: 250 ms per token = 4 tok/s (painful)
- At 100 GB/s Apple M4 Pro / H100: 10 ms per token = 100+ tok/s
```

**Transformer inference is memory-bandwidth-bound, not compute-bound.** Adding more TOPS doesn't help — you need more GB/s.

### The decoder loop problem

A transformer that generates 100 tokens reads its weights **100 times**. This is why generation is slow.

```
To generate "Hello, how are you?" (5 words):
┌─────────────┐
│ "Hello,"    │  → Read 1 GB of weights once
└─────────────┘
┌──────────────────┐
│ "Hello, how"     │  → Read 1 GB of weights once
└──────────────────┘
┌───────────────────────┐
│ "Hello, how are"      │  → Read 1 GB of weights once
└───────────────────────┘
┌────────────────────────────┐
│ "Hello, how are you?"      │  → Read 1 GB of weights once
└────────────────────────────┘

Total memory traffic: 4 × 1 GB = 4 GB just to generate 5 tokens.
```

For comparison, a CNN does the **same amount of memory traffic** to classify 4 different images.

---

## 5. Why this matters for the M.2 accelerator question

A "26 TOPS Hailo-8 M.2" accelerator is **physically incapable** of running a 7B LLM, not because of TOPS, but because:

| Resource | CNN need | LLM need | M.2 supply | Result |
|---|---|---|---|---|
| TOPS | 10–50 | 10–50 (modest) | ✅ 13–60 | Both fine |
| On-chip SRAM | 64 MB (fits CNN) | 256 MB+ (fits KV cache) | ⚠️ 0–64 MB | CNN ✅, LLM ❌ |
| External DRAM | 0 (CNN fits) | 8–16 GB | ⚠️ 0–16 GB (rare) | CNN ✅, LLM ⚠️ |
| Memory bandwidth | 4 GB/s (PCIe) | 50+ GB/s | ❌ 4 GB/s | CNN ✅, LLM ❌ |
| Power | 2.5W (CNN) | 25W+ (LLM at usable speed) | ⚠️ 25W max | CNN ✅, LLM ⚠️ |
| Thermal | 25W | 100W+ for data center | ❌ 25W | CNN ✅, LLM ❌ |

**CNN hits all green. LLM hits mostly red.** This is why M.2 AI accelerators were vision-only for years.

### The vendors that solved it (2024–2026)

These vendors specifically engineered M.2 to handle the LLM workload:

| Vendor | How they solved the bottleneck |
|---|---|
| **Hailo-10H** | Added transformer-specific ISA, 8GB LPDDR4X on module |
| **Kinara Ara-2** (Geniatech AIM M2) | 16GB LPDDR4X, transformer-optimized NPU |
| **Axera AX8850** (M5Stack LLM-8850) | 8GB LPDDR4X, AXCL runtime, native Llama 3.2 + Qwen3 |
| **Rockchip RK1828** | 5GB 3D-stacked DRAM with 1 TB/s bandwidth |
| **EdgeCortix SAKURA-II** | 16GB onboard DRAM, multi-billion param LLM |
| **BrainChip Akida** | (different approach — event-based, not for LLMs) |

Each one traded off something to fit LLM into M.2 form factor:
- **Hailo-10H**: smaller model library (~10 models)
- **M5Stack LLM-8850**: $99 but only up to 7B models, ~15–20 tok/s
- **RK1828**: needs 12V aux power + heatsink (not pure M.2 anymore)

---

## 6. Quick mental models

### The CNN mental model

CNN = "spotting pattern X in a fixed image"

```
YOLOv8n: "Is there a person in this camera frame?"
- Look at image once
- Output: person @ (x=320, y=240, w=80, h=160), confidence 0.95
- Time: 8 ms
- Memory needed: 12 MB
```

### The Transformer mental model

Transformer = "reading a book and writing a thoughtful response"

```
Qwen 0.5B: "Explain photosynthesis in 3 sentences"
- Read the prompt (1 GB weights, read once)
- Generate "Photosynthesis" (1 GB weights, read again)
- Generate " is" (1 GB weights, read again)
- Generate " the" (1 GB weights, read again)
- ... 50 more ...
- Total memory traffic: ~3 GB
- Time: ~600 ms
- Memory needed: 1 GB minimum
```

### The mental model for the difference

```
CNN:       I see cat      → Cat
Transformer: I read sentence → Generate word 1, word 2, word 3...
```

---

## 7. Hybrid architectures (the new frontier)

The cleanest dichotomy is breaking down in 2025–2026:

### Vision Transformers (ViT)

- Image patches become "tokens" → transformer attention applied
- Used in: SAM (Segment Anything), CLIP, DINOv2, InternVL3
- Hybrid: CNN extracts features, transformer reasons about them

### Multimodal models

- Image encoder (CNN or ViT) + text decoder (transformer)
- InternVL3, LLaVA, Qwen-VL, Llama 3.2 Vision
- The LLM side still has all the transformer memory problems

### Small transformers for edge

- **Qwen 3 0.6B** is small enough that 19 tok/s on Raspberry Pi 5 works
- **Llama 3.2 1B** fits in 16GB M.2 LLM modules
- **Phi-2 2.7B** runs on Hailo-10H at 19 tok/s

### Speculative decoding

- Small model generates candidates fast
- Large model verifies
- Reduces effective memory bandwidth needs

---

## 8. What this means for your hardware choices

### If you need vision AI

✅ Use M.2 AI accelerators — they're mature, cheap, power-efficient
- **Hailo-8 M.2 ($179)** — best software, 26 TOPS, vision-only
- **MemryX MX3 ($149)** — developer-friendly, vision-only
- **DeepX DX-M1 ($139–$180)** — vision-focused, good Linux support

### If you need LLM inference

✅ Use systems with high memory bandwidth
- **Mac Mini M4 ($599)** — 100 GB/s, 30–200 tok/s depending on model size
- **Apple Silicon with 32GB+** — unified memory architecture wins
- **Workstation GPUs (H100, MI300X)** — for serious production

❌ Don't expect M.2 LLM accelerators to feel "fast"
- **M5Stack LLM-8850 at $99** — 15–20 tok/s on Qwen 0.5B is real but not blazing
- **Hailo-10H** — 11 tok/s on Llama 3 8B INT4 (workable for offline tasks, not chat)

### If you need both

Hybrid is the future:
- **M.2 vision accelerator** for camera/video processing
- **Host system (Pi 5, Mac Mini)** for the LLM that interprets results
- Example: Frigate NVR with Hailo-8 for detection + LLM on host for description

---

## 9. References & Sources

**CNN:**
- [Stanford CS231n — Convolutional Neural Networks for Visual Recognition](http://cs231n.stanford.edu/)
- [YOLO original paper (Redmon et al., 2016)](https://arxiv.org/abs/1506.02640)
- [ResNet original paper (He et al., 2015)](https://arxiv.org/abs/1512.03385)

**Transformer:**
- ["Attention Is All You Need" (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762)
- [The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/)
- [Andrej Karpathy — Let's build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY)

**Edge AI benchmarks:**
- [Hailo-10H LLM benchmarks — codesota.com](https://www.codesota.com/embedded-ai/hailo-10h-llms)
- [M5Stack LLM-8850 AXCL documentation](https://www.cnx-software.com/2025/10/03/m5stack-llm-8850-card-an-m-2-m-key-ai-accelerator-module-based-on-axera-ax8850-24-tops-soc)
- [EdgeCortix SAKURA-II M.2 specifications](https://www.edgecortix.com/en/hardware)

**Architecture deep-dives:**
- [MemryX MX3 BDTI independent report](https://www.bdti.com/sites/default/files/BDTI-Independent-Report-MemryX-MX3-M2-Module.pdf)
- [Rockchip RK1828 3D-stacked DRAM analysis](https://www.cnx-software.com/2025/12/30/rockchip-rk1820-rk1828-so-dimm-and-m-2-llm-vlm-ai-accelerator-modules-devkits-and-benchmarks)

**Related reports in this repo:**
- [Why Most M.2 AI Accelerators Are Vision-Only](./m2-vision-only-deep-dive-2026.md) — the follow-up deep-dive explaining the market
- [M.2 AI Accelerator Deep Research](./m2-ai-accelerator-deep-research-2026.md) — full 48-module catalog
- [SBC vs Mac Mini M4 Cost-Performance](../sbc-vs-macmini-m4-2026-08.md) — host system comparison
- [AI Accelerator Wide-Net Catalog](./ai-accelerator-catalog-2026.md) — 90+ companies across 12 tiers

---

*Generated by Severus (Claude Opus 5) · 25 Aug 2026 · Written for Shuenrui's daily secretary workflow · Use it to make better hardware decisions, not just to understand theory.*