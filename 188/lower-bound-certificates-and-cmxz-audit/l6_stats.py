#!/usr/bin/env python3
"""Statistics of an l_6-free satisfying patch on the BASE lattice copy (correct Eisenstein norm a^2 - ab + b^2;
each red sqrt3-triangle counted once)."""
import sys, json, collections
base = sys.argv[1]
meta = json.load(open(base + ".json"))
vals = {}
for line in open(base + ".sol"):
    if line.startswith("v "):
        for t in line.split()[1:]:
            v = int(t)
            if v: vals[abs(v)] = v > 0
isos = meta["isos"]
ident = [gi for gi, g in enumerate(isos) if abs(g[0]-1) < 1e-12 and abs(g[1]) < 1e-12 and abs(g[2]) < 1e-12 and abs(g[3]) < 1e-12][0]
col = {(a, b): vals[i+1] for i, (gi, a, b) in enumerate(meta["tags"]) if gi == ident}
n = len(col); red = sum(col.values())
def norm(a, b): return a*a - a*b + b*b
longest = {}
for u in [(1, 0), (0, 1), (1, 1)]:
    L = 0
    for (a, b), c in col.items():
        if c or ((a-u[0], b-u[1]) in col and not col[(a-u[0], b-u[1])]): continue
        x, k = (a, b), 0
        while x in col and not col[x]: k += 1; x = (x[0]+u[0], x[1]+u[1])
        L = max(L, k)
    longest[u] = L
reds = {p for p, c in col.items() if c}
V3 = [(1, 2), (-1, 1), (-2, -1), (-1, -2), (1, -1), (2, 1)]      # the six vectors of norm 3
assert all(norm(*v) == 3 for v in V3)
tri = set()
for (a, b) in reds:
    for (da, db) in V3:
        p2 = (a+da, b+db)
        if p2 not in reds: continue
        for (ea, eb) in V3:
            p3 = (a+ea, b+eb)
            if p3 in reds and norm(p3[0]-p2[0], p3[1]-p2[1]) == 3:
                tri.add(frozenset([(a, b), p2, p3]))
periods = []
for u in [(1, 0), (0, 1), (1, 1)]:
    for t in range(1, 13):
        if all(col[(a+t*u[0], b+t*u[1])] == c for (a, b), c in col.items() if (a+t*u[0], b+t*u[1]) in col):
            periods.append((u, t))
print(f"{base}: base-lattice points {n}, red {red} (density {red/n:.3f}), longest blue run per direction {longest}, "
      f"red sqrt3-triangles (distinct) {len(tri)}, lattice periods <= 12 observed: {periods or 'none'}")
