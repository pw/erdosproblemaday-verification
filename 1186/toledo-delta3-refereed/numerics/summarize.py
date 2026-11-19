import json, sys, collections
QSTAR = -5 / 137
for fn in sys.argv[1:]:
    rs = [json.loads(l) for l in open(fn)]
    print(f"== {fn}: {len(rs)} runs")
    by = collections.defaultdict(list)
    for r in rs: by[r["method"]].append(r)
    for m, L in sorted(by.items()):
        b = min(L, key=lambda r: r["Q"])
        rec = sum(r["ham"] == 0 for r in L); near = sum(r["ham"] <= 20 for r in L)
        below = sum(r["gap"] < -1e-12 for r in L)
        print(f"  {m:5s} runs={len(L):5d} bestQ={b['Q']:.13f} gap={b['gap']:+.3e} (ham {b['ham']}, {b['nblocks']} blocks) "
              f"exact±phi*={rec} ({100*rec/len(L):.1f}%) within-20-cells={near} ({100*near/len(L):.1f}%) below-5/137={below}")
        fam = collections.defaultdict(list)
        for r in L: fam[r["fam"]].append(r)
        print("        per start family: " + "; ".join(f"{f}: {sum(r['ham']==0 for r in v)}/{len(v)} exact, best gap {min(r['gap'] for r in v):+.2e}" for f, v in sorted(fam.items())))
    far = [r for r in rs if r["ham"] > 20]
    if far:
        b = min(far, key=lambda r: r["Q"])
        print(f"  best run NOT near ±phi* (ham>20): Q={b['Q']:.10f} gap={b['gap']:+.3e} ham={b['ham']} blocks={b['nblocks']} {b['method']}/{b['fam']}; such runs: {len(far)}")
        if b["blocks"]: print("     its blocks (sign, length in 1/548 units):", b["blocks"])
