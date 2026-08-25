# Benchmark Data: Orange Pi 6 Plus

> **Field measurements for the Orange Pi 6 Plus (CIX P1 / CD8180, 32GB LPDDR5, Mali-G720).** Submit PRs to add more models.

## Hardware

- **Model:** Orange Pi 6 Plus
- **SoC:** CIX P1 (CD8180) — 12 cores (4× A720 @ 2.8 GHz + 4× A720 @ 2.4 GHz + 4× A520 @ 1.8 GHz)
- **GPU:** Mali Immortalis-G720 MC10
- **NPU:** 30 TOPS (Zhouyi Z3, ARM China) — **does NOT do LLM decode** as of Aug 2026
- **RAM:** 32GB LPDDR5
- **Memory bandwidth:** 40.1 GB/s measured (8 threads, large buffers)
- **Storage:** 1TB NVMe (M.2)
- **Cooling:** Active fan recommended under LLM load

## Software

- **Engine:** llama.cpp (build flags below)
- **Recommended build:**
  ```bash
  cmake -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DGGML_VULKAN=ON \
    -DGGML_CPU_ARM_ARCH=armv9-a+sve2+dotprod+i8mm+fp16+fp16fml+crypto+sha2+sha3+sm4+rcpc+lse+crc+aes+memtag+sb+ssbs+predres+pauth \
    -DGGML_NATIVE=off
  cmake --build build --config Release -j 6
  ```
- ⚠️ The build flags matter. Without `GGML_CPU_ARM_ARCH`, llama.cpp misses NEON/SIMD detection on the Radxa Debian image and runs ~30% slower.

## Power (measured)

| State | Watts | Source |
|---|---|---|
| Idle (board only) | 15.0 W | [Tao of Mac 30-day measurement](https://taoofmac.com/space/reviews/2026/04/11/1900) |
| Daily cycle (mixed use) | 20–27 W | Tao of Mac |
| LLM load (Vulkan, sustained) | 25–30 W | interfacinglinux.com hands-on |
| Peak (CPU + GPU + NPU + NVMe) | 30 W | Tao of Mac |

⚠️ **The "5–15W" idle figures from some vendor blogs are wrong.** The CIX P1 reference design runs hot. Plan for 15W minimum even when "idle."

## Benchmark results

### Qwen2.5-3B-Instruct Q5_K_M

**Model:** `bartowski/Qwen2.5-3B-Instruct-GGUF:Q5_K_M`
**Backend:** llama.cpp Vulkan
**Source:** [interfacinglinux.com — Vulkan-Powered llama.cpp on Orion O6](https://interfacinglinux.com/community/sbcsoftware/vulkan-powered-llama-cpp-on-the-orion-o6-and-o6n)

| Backend | tg (tok/s) | pp (tok/s) | Notes |
|---|---|---|---|
| CPU only (8 threads) | 4.3 | — | Memory-bandwidth bound |
| Vulkan (`-ngl 60`) | 9.9 | — | **2.3× speedup over CPU** |

### Qwen3.5-4B Q4_K_M (Shuenrui's board)

**Model:** Qwen 3.5 4B Q4_K_M
**Backend:** llama.cpp Vulkan
**Measured by:** Shuenrui, on actual hardware

| Backend | tg (tok/s) |
|---|---|
| Vulkan | **9.7** (matches the 9.9 number above) |

### Qwen3-30B-A3B Q4_K_M (Orion O6 — same SoC, different board)

**Model:** `Qwen/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M`
**Backend:** llama.cpp CPU 7 threads
**Source:** [Radxa forum — Llama.cpp benchmarks on Orion O6](https://forum.radxa.com/t/llama-cpp-benchmarks/27813)

| Build | tg (tok/s) | pp (tok/s) |
|---|---|---|
| With NEON/SIMD (correct build) | 16.13 | 23.31 |
| Without NEON/SIMD | 12.41 | 14.85 |

### Qwen3-32B Q4_K_M (Orion O6)

| Backend | tg (tok/s) | pp (tok/s) |
|---|---|---|
| CPU 7 threads | 1.95 | 3.90 |
| Vulkan | 1.1 | 2.0 |

## Notes

- The Orange Pi 6+ and the Radxa Orion O6 use the same CIX P1 SoC. Benchmarks transfer between the two boards.
- **Vulkan > CPU on small models** (because GPU has its own cache), but the gap closes on larger models where memory bandwidth dominates.
- **The 30 TOPS NPU does not accelerate LLM decode.** Don't promise customers NPU-boosted LLM inference. The NPU is for vision (YOLO, CLIP) and embeddings.
- **Idle power is 15W, not 5W.** This is a board-level finding, not a workload finding. Plan for it.
