# Methodology

How measurements in this repo are taken. Read this before adding data or quoting numbers.

## What we measure

| Metric | Symbol | Unit | Why |
|---|---|---|---|
| Token generation speed | `tg` | tokens/sec | The user-facing speed of the model responding |
| Prompt processing speed | `pp` | tokens/sec | How fast the model eats the input prompt |
| Idle power | `P_idle` | watts | Used for cost calculations when the device is on but not loaded |
| Load power | `P_load` | watts | Sustained power under continuous inference |
| Peak power | `P_peak` | watts | Worst case (LLM + system activity) |

## What's excluded

- **Theoretical TOPS** — useless for memory-bound LLM inference. Decode is bandwidth-bound, not compute-bound.
- **"Up to X tok/s" marketing claims** — without quantization, model, prompt length, and platform disclosed, these are meaningless.
- **Estimated/synthetic numbers** — if we didn't measure it (or someone with a calibrated setup didn't), it doesn't go in.
- **First-run warm-up numbers** — first token is always slow due to model loading. We always use warm state.

## Measurement standards

### For SBCs (llama.cpp)

```bash
# Build llama.cpp with platform-appropriate flags
cmake -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DGGML_VULKAN=ON \              # if Vulkan supported
  -DGGML_CPU_ARM_ARCH=armv9-a+sve2+dotprod+i8mm+fp16+fp16fml+crypto+sha2+sha3+sm4+rcpc+lse+crc+aes+memtag+sb+ssbs+predres+pauth \
  -DGGML_NATIVE=off

# Run bench
./build/bin/llama-bench \
  -m model.gguf \
  -p 512 \                         # 512-token prompt
  -n 128 \                         # 128-token generation
  -t <thread_count> \              # match the device's big-core count
  -ngl 99                          # offload all layers to GPU/NPU if available
```

We report the **median** of 3 runs to suppress outliers. If a result is wildly different on the second run, we discard it and note the variance.

### For Apple Silicon (Ollama or MLX)

```bash
# Install Ollama
brew install ollama
ollama pull <model>

# Measure via API
curl -s http://localhost:11434/api/generate \
  -d '{"model": "<model>", "prompt": "...", "stream": false}' | jq '.eval_count, .eval_duration'

# tok/s = eval_count / (eval_duration / 1e9)
```

For MLX:

```bash
uv run --with mlx-lm mlx_lm.generate \
  --model mlx-community/<model> \
  --max-tokens 200 \
  --prompt "..." 
# Report: prompt_tokens_per_sec and generation_tokens_per_sec
```

### For Hailo accelerators

```bash
# Compile model with Hailo Dataflow Compiler → HEF file
# Run with HailoRT GenAI
# Reference: https://hailo.ai/developer-zone/
```

### Power measurement

Preferred: **wall-meter** (Tapo P110, Shelly Plug, or similar) recording 5-minute averages for 30 days. This catches idle, load, and sleep patterns.

Acceptable: **kill-a-watt** snapshot during sustained load, with idle drawn from spec sheet.

Not acceptable: spec sheet "TDP" only. TDP ≠ sustained wall draw.

## Cost-perf formula

```
tok_per_dollar_per_day = (tok/s × hours_per_day × 365) / 
                         ((device_USD / lifespan_days) + 
                          (watts / 1000 × hours_per_year × $0.11/kWh))
```

Where:
- `device_USD` = sticker + required accessories (SSD, case, accelerator)
- `lifespan_days` = 3 years for SBC, 5 years for Mac Mini
- `$0.11/kWh` = RM 0.50/kWh Malaysian commercial rate; adjust for local tariff
- `hours_per_year` = 8 × 365 (business use) or 24 × 365 (24/7 service)

## Adding data

PRs welcome. Use the [template](../benchmarks/template.md). Required fields:

1. Hardware (model, RAM, storage, accelerator if any)
2. Software (engine + version, build flags, commit SHA)
3. Model (HF repo + quantization)
4. Workload (`llama-bench` or API call, raw command)
5. Raw output (paste the actual numbers, not summaries)
6. Source URL (where the data was first published)

## Known limitations

- **Build flags matter.** llama.cpp without NEON/SIMD on aarch64 runs ~30% slower than with proper flags. If you see a number that's much lower than community reports, check the build.
- **Context length kills speed.** 8K context vs 512 context can be 5× slower. Always report context length.
- **Quantization is a speed/quality tradeoff.** Q4_K_M is the default; Q8_0 and FP16 are slower but more accurate. Always report which.
- **First generation after model load is slower.** Wait at least 1 generation before measuring.
- **Vulkan support on aarch64 is uneven.** Mali, Adreno, and Imagination all behave differently. Test CPU-only first to establish a baseline.

## When in doubt

Open an issue. We're not trying to be gatekeepers — we just want every number in here to be defensible.
