#!/usr/bin/env python3
"""Third instrument for the 11-line cover: 10^7 random lines (+ the float hull's deep holes) must all satisfy
max_i <x,c_i>^2 >= 1/(2M) (the exact certificate's bound); prints the empirical minimum. Uses the RATIONAL centres from the .cert.json."""
import json, sys, numpy as np
from fractions import Fraction as Fr
d = json.load(open(sys.argv[1])); C = np.array([[float(Fr(a)) for a in c] for c in d['centres_rational']]); M = Fr(d['M'])
bound = float(1 / (2 * M)); rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
worst = 1.0
for _ in range(100):
    X = rng.standard_normal((100000, 4)); X /= np.linalg.norm(X, axis=1, keepdims=True)
    worst = min(worst, float(((X @ C.T) ** 2).max(1).min()))
from scipy.spatial import ConvexHull
H = ConvexHull(np.vstack([C, -C])); U = H.equations[:, :4]
hole = float(((U @ C.T) ** 2).max(1).min())
print(f'certified bound 1/(2M) = {bound:.10f}; sampled min over 1e7 lines = {worst:.10f}; min over hull deep holes = {hole:.10f}')
ok = worst >= bound - 1e-12 and hole >= bound - 1e-9 and abs(hole - bound) < 1e-6
print('AGREES' if ok else 'DISAGREES'); sys.exit(0 if ok else 1)
