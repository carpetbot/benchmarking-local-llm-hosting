#!/usr/bin/env python3
"""Cost-perf matrix calculator. Now supports both 0.8B and 9B class."""
ELECTRICITY = 0.11  # USD/kWh (RM0.50/kWh MY)
HRS_24_7 = 24 * 365
HRS_8HR = 8 * 365
DAYS_3YR = 365 * 3
DAYS_5YR = 365 * 5

# (name, sticker_usd, watts, tok/s, is_mac, model)
rows_08b = [
    ("MacBook Pro M4 Max 128GB",   3599, 40, 525.5, True,  "Qwen3-0.6B"),
    ("Mac Mini M4 Pro 24GB (MLX)", 1199, 35, 300,   True,  "Llama 3.2 1B est"),
    ("Mac Mini M4 16GB (MLX)",      599, 25, 175,   True,  "Llama 3.2 1B est"),
    ("Jetson Orin Nano 8GB",        499, 15, 60,    False, "Llama 3.2 1B est"),
    ("Mac Mini M4 16GB (Ollama)",   599, 25, 30.6,  True,  "Llama 3.2 1B"),
    ("Radxa Rock 5 ITX+ 32GB",      219, 15, 28,    False, "Qwen 2.5 0.5B est"),
    ("Orange Pi 5 Pro 16GB",        109, 10, 28,    False, "Qwen 2.5 0.5B est"),
    ("Radxa Rock 5B+ 16GB",         119, 12, 28,    False, "Qwen 2.5 0.5B est"),
    ("Orange Pi 5 Max 16GB",        125, 12, 28,    False, "Qwen 2.5 0.5B est"),
    ("Orange Pi 5 Plus 16GB",       129, 15, 22,    False, "Qwen 2.5 0.5B est"),
    ("Radxa X4 (Intel N100)",        80, 15, 30,    False, "Qwen 2.5 0.5B est"),
    ("Orange Pi 6 Plus 32GB",       300, 25, 32,    False, "Qwen 2.5 0.5B est"),
    ("Radxa Orion O6 32GB",         280, 25, 32,    False, "Qwen 2.5 0.5B est"),
    ("Raspberry Pi 5 16GB",          80,  8, 19.4,  False, "Qwen 2.5 0.5B"),
]

def cost_perf_table(rows, header):
    print("=" * 110)
    print(header)
    print(f"Electricity: ${ELECTRICITY}/kWh (RM0.50/kWh MY) | Lifespan: 3yr SBC / 5yr Mac")
    print("=" * 110)
    print(f"{'Device':<32} {'Stk':>5} {'W':>3} {'t/s':>7} {'$/tok/s':>10} {'$/d-8h':>9} {'$/d-24h':>9}  Model")
    print("-" * 110)
    results = []
    for name, usd, watts, tps, is_mac, model in rows:
        lifespan = DAYS_5YR if is_mac else DAYS_3YR
        depr = usd / lifespan
        per_day_8h = depr + (watts/1000) * HRS_8HR * ELECTRICITY
        per_day_24h = depr + (watts/1000) * HRS_24_7 * ELECTRICITY
        per_tok_s = usd / tps
        results.append({"name": name, "usd": usd, "watts": watts, "tps": tps,
                        "per_tok_s": per_tok_s, "per_day_8h": per_day_8h,
                        "per_day_24h": per_day_24h, "model": model})
        print(f"{name:<32} ${usd:>4} {watts:>3} {tps:>7.1f} ${per_tok_s:>9.2f} ${per_day_8h:>8.3f} ${per_day_24h:>8.3f}  {model}")
    print()
    print("** WINNERS **")
    print(f"Cheapest per tok/s:   {min(results, key=lambda r: r['per_tok_s'])['name']} (${min(results, key=lambda r: r['per_tok_s'])['per_tok_s']:.2f})")
    print(f"Fastest:              {max(results, key=lambda r: r['tps'])['name']} ({max(results, key=lambda r: r['tps'])['tps']:.1f} tok/s)")
    print(f"Cheapest per-day 24/7:{min(results, key=lambda r: r['per_day_24h'])['name']} (${min(results, key=lambda r: r['per_day_24h'])['per_day_24h']:.3f}/day)")
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "9b":
        # legacy 9B class (v2)
        rows_9b = [
            ("MacBook Pro M4 Max 128GB",  3599, 40, 43.2, True,  "Qwen 3.5 9B"),
            ("MacBook Air M4 16GB",       1199, 25, 30,   True,  "Qwen 3.5 9B est"),
            ("Mac Mini M4 Pro 24GB",      1199, 35, 30,   True,  "Qwen 3.5 9B est"),
            ("Mac Mini M4 16GB",           599, 25, 12.5, True,  "Qwen 3.5 9B"),
            ("Raspberry Pi 5 + Hailo",     305,  8, 11,   False, "Llama 3 8B (Hailo)"),
            ("Radxa Rock 5B+ 16GB",        119, 12, 4,    False, "Qwen3-8B RKLLama"),
            ("Orange Pi 5 Pro 16GB",      109, 10, 3.5,  False, "Qwen3-8B RKLLama"),
            ("Orange Pi 6 Plus 32GB",      300, 25, 5,    False, "Qwen 3.5 9B Vulkan est"),
        ]
        cost_perf_table(rows_9b, "COST-PERF — Qwen 3.5 9B class")
    else:
        cost_perf_table(rows_08b, "COST-PERF — 0.8B class (Qwen 2.5 0.5B / Qwen 3 0.6B / Llama 3.2 1B)")
