# Benchmark Data: <Device Model>

> **Field measurements for <Device Model>** — submit PRs to add more models or settings.

## Hardware

- **Model:** <e.g. Orange Pi 6 Plus>
- **SoC:** <e.g. CIX P1 (CD8180), 12-core>
- **RAM:** <e.g. 32GB LPDDR5>
- **Storage:** <e.g. 1TB NVMe SSD>
- **Accelerator:** <e.g. Hailo-10H M.2 module, or "none">
- **Cooling:** <e.g. active fan, passive heatsink, stock>

## Software

- **Engine:** <e.g. llama.cpp b1234, or Ollama 0.5.x>
- **Build flags:** <paste the exact cmake command>
- **OS:** <e.g. Armbian 26.2.0-trunk.410, kernel 6.18.9>
- **Commit SHA:** <if built from source>

## Power (measured)

| State | Watts | Source |
|---|---|---|
| Idle | <X> | <measurement source> |
| LLM load (sustained) | <X> | <measurement source> |
| Peak | <X> | <measurement source> |

## Benchmark results

### <Model Name> — <quantization>

**Model:** `<HF repo path>:<quant>`
**Command:**
```bash
<exact command run>
```

**Result:**

```
<paste raw llama-bench output here, not a summary>
```

**Measured:** `<X> tok/s generation, <Y> tok/s prompt processing`
**Date:** <YYYY-MM-DD>
**Source URL:** <where this was first published or measured>

---

### <Another Model>

*Add more models below using the same structure.*

## Notes

- Any context that affects the measurement (ambient temp, other workloads running, etc.)
- Caveats or open questions
