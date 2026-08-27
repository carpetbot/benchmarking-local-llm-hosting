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

## ⚠️ MANDATORY: cold prefill (the KV-cache trap)

**Read this before submitting any prefill / prompt-processing number.**

llama.cpp and ollama reuse the KV cache when a prompt repeats. `prompt_eval_duration`
then measures a **cache hit**, not prefill compute. Measured on our CIX P1 CD8160,
qwen3:8b, 2,232-token prompt:

| condition | reported prefill |
|---|---|
| Cache hit (identical prompt, 2nd run) | **7,962.74 tok/s** |
| Median of 2 repeats | 2,899.71 tok/s |
| **Cold, unique prefix** | **8.13 tok/s** |

A **979× overstatement**.

**The trap is counterintuitive:** *running repeats for statistical rigor is what
introduces it.* Our single-run measurements were cold and correct; adding repeats
made the numbers worse while looking more rigorous.

**Required practice:**
1. Prepend a unique token (timestamp, counter) to every run so no two prompts match.
2. Or restart the server between runs.
3. **Sanity check before believing any number:** on CPU inference, if prefill exceeds
   roughly **20× your measured decode rate**, you are timing a cache, not the model.

Reference implementation: [`scripts/bench_cix_p1_v2.py`](../scripts/bench_cix_p1_v2.py).
Isolation probe: [`scripts/probe_prefill.py`](../scripts/probe_prefill.py).

## MANDATORY: report prefill and decode separately

They are different physics and they are the axis vendors deliberately merge.

- **Prefill** (prompt processing / `pp`) scales with compute. It is the wait before the
  first token. On our board an 8B model with a 2.2k system prompt takes **4 min 37 s**
  before emitting anything.
- **Decode** (token generation / `tg`) scales with memory bandwidth and **active**
  parameters. It is what "tok/s" usually means.

A single number that does not say which one it is, at what context length, is not a
benchmark. **Always report context length alongside both.**

## MANDATORY: state which engine actually ran

Never assume the accelerator engaged. Our repo listed this board as "llama.cpp Vulkan"
for months; the ollama logs said `offloaded 0/49 layers to GPU` — 100% CPU.

Paste the offload line from your runtime's own log. If you cannot produce it, label the
backend `unverified`.

Related: vendor TOPS figures are frequently unreachable for LLM work. The CIX P1
advertises 45 TOPS combined, but the Zhouyi NPU does not perform autoregressive decode
at all, and no mainstream runtime routes to NPUs. **Never record a TOPS number as an
LLM performance claim.**

## Evidence labelling

Every row in `data/*.csv` must carry an `evidence` value:

| label | meaning |
|---|---|
| `MEASURED-FIRST-PARTY` | we ran it, on hardware we own, harness in this repo |
| `MEASURED` | third party ran it, named source URL, reproducible method |
| `ESTIMATED` | inferred or scaled — **must be visibly labelled wherever displayed** |
| `ESTIMATED-DISPUTED` | estimate that conflicts with a measurement |
| `RETRACTED` | previously published, now disproven — **kept visible, not deleted** |

An unsourced row is a liability, not a data point. Either measure it, cite it, or delete
it. Copying an estimate from an older revision and dropping the label is fabrication.

## Corrections policy

When a number here is disproven, we publish a corrected row and **leave the retraction
visible**. We do not silently edit. See the
[Orange Pi 6 Plus correction log](../benchmarks/orangepi-6-plus/README.md#-corrections-issued-2026-08-27)
for the format — four wrong attributes on a board we now own, published in full.

## MANDATORY: date every price, and treat prices as perishable

Performance numbers age slowly. **Prices age in weeks.**

Between late 2025 and April 2026 the DRAM shortage moved this market by −20% to
**+275%**. The Raspberry Pi 5 16GB went $80 → $299.99. The Radxa X4 went $79.96 →
$265.99. The $599 Mac Mini M4 SKU was discontinued. Every cost-perf ranking this
repo published before 2026-08-27 was void as a result — not because any measurement
was wrong, but because the denominator moved.

**Required for any row carrying a price:**

| column | rule |
|---|---|
| `sticker_usd` | leave **empty** rather than guess. An unsourced price is worse than none. |
| `price_source` | URL. Vendor page, or a dated article that quotes the vendor. |
| `price_date` | when that price was observed. Not when you wrote the row. |
| `price_status` | `SOURCED` / `REPRICED from $X` / `STALE` / `UNPRICED` |

**Never bundle a price you did not source.** While repricing this repo we nearly
published a "$524.99" Pi 5 + Hailo-10H bundle built from a real Pi price and an
*invented* $225 accelerator price. It was caught and the row is now `UNPRICED`.
A fabricated component price inside a plausible total is the hardest error to spot
downstream.

**Re-check cadence:** any cost conclusion older than ~3 months should be treated as
unverified. State a re-check date next to every ranking.

## Known limitations

- **Build flags matter.** llama.cpp without NEON/SIMD on aarch64 runs ~30% slower than with proper flags. If you see a number that's much lower than community reports, check the build.
- **Context length kills speed.** 8K context vs 512 context can be 5× slower. Always report context length.
- **Quantization is a speed/quality tradeoff.** Q4_K_M is the default; Q8_0 and FP16 are slower but more accurate. Always report which.
- **First generation after model load is slower.** Wait at least 1 generation before measuring.
- **Vulkan support on aarch64 is uneven.** Mali, Adreno, and Imagination all behave differently. Test CPU-only first to establish a baseline.

## When in doubt

Open an issue. We're not trying to be gatekeepers — we just want every number in here to be defensible.
