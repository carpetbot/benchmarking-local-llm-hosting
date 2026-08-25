---
name: Add benchmark data
about: Submit a new (device, model) measurement
title: "[BENCH] <device> + <model>"
labels: benchmark-data
---

## Hardware
- **Device:**
- **SoC:**
- **RAM:**
- **Storage:**
- **Accelerator (if any):**

## Software
- **Engine + version:**
- **Build flags (if custom):**
- **OS + kernel:**

## Benchmark
- **Model (HF repo + quant):**
- **Command run:**
```
<paste exact command>
```
- **Raw output:**
```
<paste llama-bench or API output>
```

## Source
- **Source URL (where this was first published):**
- **Date measured:**

## Checklist
- [ ] Hardware fully specified
- [ ] Software fully specified with version/SHA
- [ ] Model identified by HF repo + quant
- [ ] Raw output pasted (not summarized)
- [ ] Source URL included
- [ ] Placed in the correct `benchmarks/<device>/` directory
