#!/bin/bash
# OrangePi 6+ LLM Benchmark Script
# Run this on the actual device to get measured tok/s for the Calvin deck
# Outputs a JSON file Shuenrui sends back to Severus

set -e
OUT="orangepi6plus_bench_$(date +%Y%m%d_%H%M%S).json"

echo "=== OrangePi 6+ LLM Benchmark ===" | tee "$OUT"
echo "Device: $(uname -a)" >> "$OUT"
echo "Date: $(date -Iseconds)" >> "$OUT"

# CPU info
echo "" >> "$OUT"
echo "=== CPU ===" >> "$OUT"
lscpu 2>/dev/null | grep -E "Model name|Architecture|CPU\(s\)|Thread|Core" >> "$OUT" || \
  cat /proc/cpuinfo | grep -E "model name|architecture|cpu cores" | head -5 >> "$OUT"

# RAM
echo "" >> "$OUT"
echo "=== RAM ===" >> "$OUT"
free -h >> "$OUT"

# Vulkan device
echo "" >> "$OUT"
echo "=== Vulkan ===" >> "$OUT"
if command -v vulkaninfo >/dev/null 2>&1; then
  vulkaninfo 2>/dev/null | grep -E "deviceName|apiVersion|driverVersion|deviceType" | head -8 >> "$OUT"
else
  echo "vulkaninfo not installed (apt install vulkan-tools mesa-vulkan-drivers)" >> "$OUT"
fi

# llama.cpp
echo "" >> "$OUT"
echo "=== llama.cpp ===" >> "$OUT"
if command -v llama-bench >/dev/null 2>&1; then
  llama-bench --version 2>&1 | head -3 >> "$OUT"
else
  echo "llama-bench not on PATH. Install: https://github.com/ggerganov/llama.cpp" >> "$OUT"
  echo "Pre-built: https://github.com/ggerganov/llama.cpp/releases" >> "$OUT"
fi

# Check for models already downloaded
echo "" >> "$OUT"
echo "=== Models on disk ===" >> "$OUT"
find ~/models ~/.cache/llama.cpp /opt/models -name "*.gguf" 2>/dev/null | head -20 >> "$OUT" || echo "No models found yet" >> "$OUT"

# Benchmark matrix — only run if llama-bench + models present
if command -v llama-bench >/dev/null 2>&1; then
  echo "" >> "$OUT"
  echo "=== Bench Results ===" >> "$OUT"

  # Common Qwen2.5 / Qwen3.5 GGUF paths
  declare -A MODELS=(
    ["qwen2.5-0.5b"]="Qwen2.5-0.5B-Instruct-Q4_K_M.gguf"
    ["qwen2.5-1.5b"]="Qwen2.5-1.5B-Instruct-Q4_K_M.gguf"
    ["qwen2.5-3b"]="Qwen2.5-3B-Instruct-Q4_K_M.gguf"
    ["qwen3.5-4b"]="Qwen3.5-4B-Instruct-Q4_K_M.gguf"
    ["qwen2.5-7b"]="Qwen2.5-7B-Instruct-Q4_K_M.gguf"
    ["llama3.1-8b"]="Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
  )

  for nick in "${!MODELS[@]}"; do
    file="${MODELS[$nick]}"
    # Search common locations
    found=$(find ~/models ~/.cache/huggingface /root/models /opt/models . -name "$file" 2>/dev/null | head -1)
    if [ -n "$found" ]; then
      echo "" >> "$OUT"
      echo "--- $nick ($found) ---" >> "$OUT"
      # Vulkan first, then CPU fallback
      echo "[Vulkan]" >> "$OUT"
      llama-bench -m "$found" -ngl 99 -p 512 -n 128 -t 1 2>&1 | grep -E "model size|total time|tokens per second" >> "$OUT" || echo "  vulkan failed" >> "$OUT"
      echo "[CPU 4 threads]" >> "$OUT"
      llama-bench -m "$found" -ngl 0 -p 512 -n 128 -t 4 2>&1 | grep -E "model size|total time|tokens per second" >> "$OUT" || echo "  cpu 4t failed" >> "$OUT"
    else
      echo "  $nick: model $file not found, skipping" >> "$OUT"
    fi
  done
fi

echo "" >> "$OUT"
echo "=== End of report ===" >> "$OUT"
echo ""
echo "Report saved to: $OUT"
echo "Send this file back to Severus for analysis."
cat "$OUT"
