#!/usr/bin/env python3
"""Lemma-2.6 branch of Tsaturian's proof as a lattice-only SAT instance: the unit triangular lattice within radius R,
origin red, (5,0) blue, no red l_2, no blue l_5, and NO red T_3 (three red points pairwise at distance sqrt3).
UNSAT for R = 8, 10, 12 -- i.e. with no red T_3 the lattice alone forces a contradiction, as Lemma 2.6 says."""
import sys, math, subprocess
import numpy as np
from scipy.spatial import cKDTree
sys.argv = ['x']
exec(open('config188.py').read().split('if __name__')[0])
for R in (8, 10, 12):
    P, T, isos = build(R, [(0.0, 0.0)], [], words=0)
    pairs = unit_pairs(P); kr = runs(P, pairs, 5)
    arr = np.array(P); tree = cKDTree(arr)
    s3 = [(i, j) for i, j in tree.query_pairs(math.sqrt(3) + 1e-9) if abs(((arr[i]-arr[j])**2).sum() - 3) < 1e-9]
    nb = {}
    for i, j in s3: nb.setdefault(i, set()).add(j); nb.setdefault(j, set()).add(i)
    t3 = {tuple(sorted((i, j, k))) for i, j in s3 for k in nb.get(i, set()) & nb.get(j, set())}
    o = [i for i, p in enumerate(P) if abs(p[0]) < 1e-9 and abs(p[1]) < 1e-9][0]
    b = [i for i, p in enumerate(P) if abs(p[0]-5) < 1e-9 and abs(p[1]) < 1e-9][0]
    cl = [[-(i+1), -(j+1)] for i, j in pairs] + [[v+1 for v in ch] for ch in kr] + [[-(a+1), -(b_+1), -(c+1)] for a, b_, c in t3] + [[o+1], [-(b+1)]]
    fn = f"runs/noT3_R{R}.cnf"
    with open(fn, 'w') as f:
        f.write(f"p cnf {len(P)} {len(cl)}\n"); f.writelines(" ".join(map(str, c)) + " 0\n" for c in cl)
    r = subprocess.run(["timeout", "300", "nice", "-n", "19", "cadical", "-q", fn], capture_output=True, text=True).stdout
    print(f"noT3 R={R}: points={len(P)} unit_pairs={len(pairs)} l5_runs={len(kr)} T3={len(t3)} ->", [l for l in r.splitlines() if l.startswith('s ')][0])
