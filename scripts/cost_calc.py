#!/usr/bin/env python3
"""Cost-perf matrix for Calvin's SBC vs Mac Mini deck"""
ELECTRICITY = 0.11  # USD/kWh (RM0.50/kWh MY)
HRS_24_7 = 24 * 365
HRS_8HR = 8 * 365
DAYS_3YR = 365 * 3
DAYS_5YR = 365 * 5

# (name, total_usd, watts, tok/s, model, source, notes)
# total_usd = sticker + SSD + accelerator where applicable (SBC includes $150 headroom)
rows = [
    ("OrangePi 6+ 32GB (CPU only)",        320, 25,  4.3, "Qwen2.5-3B Q5_K_M",       "interfacinglinux.com",            "No Vulkan -- memory BW bound"),
    ("OrangePi 6+ 32GB (Vulkan)",          320, 25,  9.9, "Qwen3.5 4B Q4_K_M",       "interfacinglinux.com + Shuenrui", "Matches Shuenrui's measured 9.7 t/s"),
    ("OrangePi 6+ 32GB + Hailo-10H M.2",   450, 28, 11.0, "Llama 3 8B INT4",         "codesota.com (Hailo official)",   "Hailo has no Qwen3.5 4B HEF yet"),
    ("Raspberry Pi 5 16GB + AI HAT+ 2",    305,  8, 11.0, "Llama 3 8B INT4",         "codesota.com + PiShop.us",       "Pi 5 host draws much less"),
    ("Mac Mini M4 16GB",                   599, 25, 40.0, "Qwen 3.5 4B Q4_K_M MLX",  "llmcheck.net + kunalganglani",   "MLX 40 tok/s measured"),
    ("Mac Mini M4 16GB (MoE 35B-A3B)",     599, 25, 17.3, "Qwen3.5-35B-A3B MoE",     "modelfit.io (Apr 2026)",         "mmap trick, 81% RAM free"),
    ("Mac Mini M4 Pro 24GB",              1199, 35, 84.0, "Qwen 3 4B MLX",           "llmcheck.net",                   "MLX backend, dense 4B"),
    ("Mac Mini M4 Pro 48GB",              1799, 35, 11.0, "Qwen 2.5 32B Q4_K_M",     "kunalganglani.com",              "32B model at 11 tok/s"),
    ("Mac Mini M4 Pro 64GB (Qwen3 MoE)",  2399, 35, 42.0, "Qwen3 30B-A3B MLX",       "llmcheck.net + robertheubanks",  "MoE 30B at 42 t/s"),
]

print("=" * 120)
print("COST-PERF MATRIX  |  Electricity $0.11/kWh (MY)  |  Lifespan 3yr SBC / 5yr Mac")
print("=" * 120)
print(f"{'Device':<35} {'Stk':>5} {'$Tot':>5} {'W':>3} {'t/s':>5} {'$/d-up':>8} {'$/d-8h':>8} {'$/d-24h':>8}  Notes")
print("-" * 120)

results = []
for name, usd, watts, tps, model, src, notes in rows:
    lifespan = DAYS_5YR if "Mac" in name else DAYS_3YR
    depr_per_day = usd / lifespan
    per_day_up = depr_per_day
    per_day_8h = depr_per_day + (watts/1000) * HRS_8HR * ELECTRICITY
    per_day_24h = depr_per_day + (watts/1000) * HRS_24_7 * ELECTRICITY
    tok_24_7 = tps * HRS_24_7
    tok_8h = tps * HRS_8HR
    tpd_up = tok_24_7 / per_day_up
    tpd_8h = tok_8h / per_day_8h
    tpd_24h = tok_24_7 / per_day_24h

    results.append({
        "name": name, "usd": usd, "watts": watts, "tps": tps,
        "per_day_up": per_day_up, "per_day_8h": per_day_8h, "per_day_24h": per_day_24h,
        "tpd_up": tpd_up, "tpd_8h": tpd_8h, "tpd_24h": tpd_24h,
        "model": model, "src": src, "notes": notes
    })
    print(f"{name:<35} ${usd:>4} ${usd+150:>4} {watts:>3} {tps:>5.1f} "
          f"${tpd_up:>7.0f} ${tpd_8h:>7.0f} ${tpd_24h:>7.0f}  {notes[:30]}")

print("\n" + "=" * 120)
print("KEY: $/d-up = tok/$/day using just depreciation (24/7 assumed)")
print("     $/d-8h = tok/$/day @ 8 hours/day with power cost")
print("     $/d-24h = tok/$/day @ 24/7 with power cost")
print("=" * 120)

print("\n** WINNERS **")
w_8h = min(results, key=lambda r: r['per_day_8h'])
w_24h = min(results, key=lambda r: r['per_day_24h'])
v_8h = max(results, key=lambda r: r['tpd_8h'])
v_24h = max(results, key=lambda r: r['tpd_24h'])
print(f"Cheapest per-day @ 8h/day:   {w_8h['name']} (${w_8h['per_day_8h']:.2f}/day)")
print(f"Cheapest per-day @ 24/7:     {w_24h['name']} (${w_24h['per_day_24h']:.2f}/day)")
print(f"Most tok-per-$ @ 8h/day:     {v_8h['name']} ({v_8h['tpd_8h']:.0f} tok/$/day)")
print(f"Most tok-per-$ @ 24/7:       {v_24h['name']} ({v_24h['tpd_24h']:.0f} tok/$/day)")

print("\n** MAC MINI M4 16GB BREAKDOWN vs OPi 6+ VULKAN **")
opi = next(r for r in results if "Vulkan" in r["name"])
mm4 = next(r for r in results if r["name"] == "Mac Mini M4 16GB")
print(f"OPi 6+ Vulkan:     ${opi['usd']} / {opi['tps']} tok/s = {opi['usd']/opi['tps']:.1f} $/tok/s")
print(f"Mac Mini M4 16GB:  ${mm4['usd']} / {mm4['tps']} tok/s = {mm4['usd']/mm4['tps']:.1f} $/tok/s")
print(f"Speedup Mac Mini:  {mm4['tps']/opi['tps']:.1f}x")
print(f"Price premium:     {mm4['usd']/opi['usd']:.1f}x sticker")
