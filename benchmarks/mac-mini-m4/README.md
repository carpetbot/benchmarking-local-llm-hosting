# Benchmark Data: Mac Mini M4

> **Field measurements for the Mac Mini M4 (16/24/32/48/64GB unified memory).** Submit PRs to add more models.

## Hardware

- **Model:** Mac Mini M4 (2024)
- **SoC:** Apple M4 / M4 Pro
- **Memory:** Unified memory (16/24/32/48/64GB depending on config)
- **Memory bandwidth:** ~100 GB/s (M4) / ~200 GB/s (M4 Pro)
- **Storage:** Apple SSD (256GB to 8TB)

## Software

- **Engine options:** Ollama (most common, uses MLX since v0.19 Mar 2026), llama.cpp, MLX
- **Ollama MLX backend** is 1.5–3× faster than llama.cpp Metal for short contexts (<40K tokens)
- **llama.cpp `--mmap` trick** lets models larger than RAM run on M4 16GB (Qwen3.5-35B-A3B at 17.3 tok/s)

## Power (measured)

| State | M4 | M4 Pro | Source |
|---|---|---|---|
| Idle | 4 W | 5 W | [Apple spec](https://support.apple.com/en-us/103253) |
| Typical load | 25 W | 35 W | ServeTheHome review |
| Peak | 65 W | 140 W | Apple spec |
| Max rated PSU | 110 W | 155 W | Apple spec |

**Important:** the M4 Pro draws significantly more than the base M4. If your pitch is "low power," stick with base M4.

## Benchmark results

### Qwen 3.5 4B Q4_K_M

**Model:** `qwen3.5:4b` (Ollama) or `Qwen/Qwen3.5-4B-Instruct-GGUF:Q4_K_M`
**Backend:** Ollama MLX (recommended) or llama.cpp

| Device | tok/s (gen) | Source |
|---|---|---|
| M4 16GB | **40** | [llmcheck.net](https://llmcheck.net/benchmarks) |
| M4 Pro 24GB (MLX) | **84** | [llmcheck.net](https://llmcheck.net/benchmarks) |
| M4 Pro 48GB | 40+ | estimated from M4 scaling |

### Llama 3.1 8B Q4_K_M

| Device | tok/s (gen) | Source |
|---|---|---|
| M4 16GB (Ollama) | 23 | [kunalganglani.com](https://www.kunalganglani.com/llm-benchmarks) |
| M4 Pro 24GB (Ollama) | 34 | kunalganglani.com |
| M4 Pro 24GB (MLX) | 56% faster than Ollama | [Ajit Singh benchmarks](https://singhajit.com/llm-inference-speed-comparison) |
| M3 Pro 18GB (Ollama) | 22 | kunalganglani.com (for reference) |
| M3 Max 36GB (Ollama) | 46 | kunalganglani.com (for reference) |

### Qwen 2.5 14B Q4_K_M

| Device | tok/s (gen) | Source |
|---|---|---|
| M4 24GB (Ollama) | 12 | kunalganglani.com |
| M3 Pro 36GB (Ollama) | 11 | kunalganglani.com |
| M3 Max 36GB (Ollama) | 28 | kunalganglani.com |

### Qwen 2.5 32B Q4_K_M

| Device | tok/s (gen) | Source |
|---|---|---|
| M4 Pro 48GB | 11 | kunalganglani.com |
| M4 Max 48GB | 22 | kunalganglani.com |
| M3 Max 64GB | 14 | kunalganglani.com |

### Qwen 3-30B-A3B (MoE)

**This is the moat.** The 30B model with only 3B active per token is the best large-model-on-M4 story.

| Device | tok/s (gen) | Source |
|---|---|---|
| M4 Pro 64GB (MLX) | 42 | [llmcheck.net](https://llmcheck.net/benchmarks) |
| M4 Max 48GB (Ollama) | 42 | llmcheck.net |
| M3 Max 128GB (Ollama) | 9 (Llama 3.1 70B) | kunalganglani.com (different model) |

### Qwen3.5-35B-A3B (MoE, on M4 16GB)

| Device | tok/s (gen) | RAM free | Source |
|---|---|---|---|
| M4 16GB (llama.cpp mmap) | 17.3 | 81% | [modelfit.io Apr 2026](https://modelfit.io/blog/run-35b-llm-mac-mini-m4-16gb-mmap) |

The "you don't need 32GB" trick. Works because MoE only activates a few experts per token, and the rest can be paged from SSD.

## Notes

- **MLX > Ollama > llama.cpp Metal for short contexts.** Switch to MLX if you're CPU-bound.
- **For 24/7 deployment, base M4 16GB draws ~25W.** That's similar to the Orange Pi 6+ under LLM load.
- **M4 Pro's 200 GB/s memory bandwidth is the real differentiator** vs SBC's 40 GB/s. This is why the M4 Pro 24GB hits 84 tok/s on a 4B model while the OPi 6+ hits 9.9.
- **Don't trust "Qwen 3.8 27B at 21 tok/s on M4 Pro 24GB" YouTube benchmarks.** Those are first-run numbers. Warm runs hit 28–30 tok/s.
