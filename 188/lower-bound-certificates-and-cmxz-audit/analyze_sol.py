#!/usr/bin/env python3
"""Read a cadical solution for a config188 instance and describe the colouring on the BASE lattice copy:
ASCII picture in lattice coordinates + period detection along the three unit directions."""
import sys, json
base = sys.argv[1]
meta = json.load(open(base + ".json"))
vals = {}
for line in open(base + ".sol"):
    if line.startswith("v "):
        for t in line.split()[1:]:
            v = int(t)
            if v != 0: vals[abs(v)] = v > 0
isos = meta["isos"]
ident = [gi for gi, g in enumerate(isos) if abs(g[0]-1) < 1e-12 and abs(g[1]) < 1e-12 and abs(g[2]) < 1e-12 and abs(g[3]) < 1e-12][0]
col = {}
for i, (gi, a, b) in enumerate(meta["tags"]):
    if gi == ident: col[(a, b)] = vals[i+1]
A = max(abs(a) for a, b in col); B = max(abs(b) for a, b in col)
print(f"base lattice: {len(col)} points, red = {sum(col.values())}")
for b in range(B, -B-1, -1):
    row = " " * (b + B)
    for a in range(-A, A+1):
        row += ("R" if col[(a, b)] else ".") + " " if (a, b) in col else "  "
    print(f"{b:3d} {row}")
# periods along the three directions: (1,0), (0,1), (1,1) in (a,b) coords -> is col(p + t*u) == col(p) for all p?
for u in [(1, 0), (0, 1), (1, 1)]:
    per = []
    for t in range(1, 13):
        ok = all(col[(a + t*u[0], b + t*u[1])] == c for (a, b), c in col.items() if (a + t*u[0], b + t*u[1]) in col)
        if ok: per.append(t)
    print("direction", u, "periods observed:", per)
# red-red distances: min, and multiset of distances <= 3 among red lattice points
import math
reds = [(a - b/2, b*math.sqrt(3)/2) for (a, b), c in col.items() if c]
ds = sorted(set(round(math.dist(p, q), 4) for p in reds for q in reds if p < q))
print("red-red distances <= 4:", [d for d in ds if d <= 4][:12])
