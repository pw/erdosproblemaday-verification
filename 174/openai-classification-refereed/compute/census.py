#!/usr/bin/env python3
"""Census: which k-point subsets of the three-squares set X (Prop 7.7, F = Q(t)) satisfy the field criterion, i.e.
are Ramsey by Theorem 1.1? Orbits under the symmetry group of X (rotation by 90 deg, reflection y -> -y, order 8).
Usage: census.py k [limit]"""
import sys, time, itertools, sympy as sp
from criterion import criterion, tau
t = tau; u, v = (1 - t**2)/(1 + t**2), 2*t/(1 + t**2)
Q0 = [(1, 0), (0, 1), (-1, 0), (0, -1)]          # q_j = J^j e1
X = []
for eps in ('+', '-', '0'):
    for a, b in Q0:
        if eps == '+': X.append((sp.sympify(u*a - v*b), sp.sympify(v*a + u*b)))
        elif eps == '-': X.append((sp.sympify(u*a + v*b), sp.sympify(-v*a + u*b)))
        else: X.append((sp.Integer(a), sp.Integer(b)))
# label = (square s in {0:+,1:-,2:0}, j in Z/4); rot90: j -> j+1 ; reflection y->-y: + <-> -, j -> -j
def act(g, lab):
    s, j = divmod(lab, 4); r, f = g
    if f: s = {0: 1, 1: 0, 2: 2}[s]; j = (-j) % 4
    return s*4 + (j + r) % 4
G = [(r, f) for r in range(4) for f in (0, 1)]
k = int(sys.argv[1]); lim = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
seen = set(); reps = []
for S in itertools.combinations(range(12), k):
    c = min(tuple(sorted(act(g, i) for i in S)) for g in G)
    if c not in seen: seen.add(c); reps.append(c)
print(f"k={k}: {len(reps)} orbits", flush=True)
nh = nf = 0
for S in reps[:lim]:
    t0 = time.time()
    ok = criterion([X[i] for i in S], name=f"k={k} {S}")
    nh += ok; nf += (not ok)
    print(f"   {time.time()-t0:.1f}s", flush=True)
print(f"SUMMARY k={k}: HOLDS {nh} FAILS {nf} (of {min(lim,len(reps))} orbits)")
