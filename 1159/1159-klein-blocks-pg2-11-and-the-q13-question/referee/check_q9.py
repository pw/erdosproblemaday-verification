"""Referee: verify the author's q=9 type-(1,3,4) witness in the author's ENCODING (galois integer repr of GF(9):
k = a0 + 3*a1 <-> a0 + a1*x, modulus = galois' default irreducible poly), with our own arithmetic; then test
(by nauty, coloured Levi graphs) whether it is collineation-equivalent to Klein's configuration built from
Seceleanu's explicit coordinates over the same field."""
import json, os, sys, itertools
from collections import Counter
import galois, pynauty
HERE = os.path.dirname(os.path.abspath(__file__))
poly = galois.GF(9).irreducible_poly
c = [int(x) for x in poly.coeffs]  # [1, b, a] for x^2 + b x + a
print("galois GF(9) modulus:", poly)
assert c[0] == 1 and len(c) == 3
def dec(k): return k % 3, k // 3
def enc(a0, a1): return a0 % 3 + 3 * (a1 % 3)
def add(u, v): a, b = dec(u); x, y = dec(v); return enc(a + x, b + y)
def mul(u, v):
    a, b = dec(u); x, y = dec(v)
    c0, c1, c2 = a * x, a * y + b * x, b * y          # c2 x^2 = c2 * (-(b' x + a'))
    return enc(c0 - c2 * c[2], c1 - c2 * c[1])
GF = galois.GF(9)
for u, v in itertools.product(range(9), repeat=2):   # cross-check our arithmetic against galois on all 81 pairs
    assert mul(u, v) == int(GF(u) * GF(v)) and add(u, v) == int(GF(u) + GF(v))
inv = [None] + [next(y for y in range(9) if mul(x, y) == 1) for x in range(1, 9)]
neg = [next(y for y in range(9) if add(x, y) == 0) for x in range(9)]
def norm(v):
    for x in v:
        if x: i = inv[x]; return tuple(mul(i, y) for y in v)
def dot(u, v):
    s = 0
    for a, b in zip(u, v): s = add(s, mul(a, b))
    return s
pts = sorted({norm(v) for v in itertools.product(range(9), repeat=3) if any(v)}); idx = {P: i for i, P in enumerate(pts)}
inc = [frozenset(i for i, P in enumerate(pts) if dot(P, L) == 0) for L in pts]
assert len(pts) == 91 and all(len(l) == 10 for l in inc) and all(len(a & b) == 1 for a, b in itertools.combinations(inc, 2))
W = json.load(open(os.path.join(HERE, '..', 'runs', 'witness_q9_type134_n21.json')))
S = {idx[norm(tuple(P))] for P in W}
print("author q=9 witness: |S| =", len(S), "spectrum", dict(sorted(Counter(len(S & l) for l in inc).items())))
# Klein over this field
roots = [t for t in range(9) if add(add(mul(t, t), t), 2) == 0]
def perms(vs):
    out = set()
    for v in vs:
        for pm in itertools.permutations(v): out.add(norm(pm))
    return out
def levi(Sset):
    n = len(pts); adj = {i: [] for i in range(2 * n)}
    for li, l in enumerate(inc):
        for j in l: adj[j].append(n + li); adj[n + li].append(j)
    return pynauty.Graph(2 * n, adjacency_dict=adj, vertex_coloring=[set(Sset), set(range(n)) - set(Sset), set(range(n, 2 * n))])
for cc in roots:
    cb = add(neg[cc], neg[1]); sg = [1, neg[1]]
    Q = perms([(1, 0, 0)] + [(1, s, 0) for s in sg] + [(1, s, mul(t, cb)) for s in sg for t in sg])
    Qi = {idx[P] for P in Q}
    print(f"Klein (c={cc}) over this GF(9): |Q|={len(Qi)} spectrum", dict(sorted(Counter(len(Qi & l) for l in inc).items())),
          "| collineation-equivalent to author's q=9 witness:", pynauty.certificate(levi(Qi)) == pynauty.certificate(levi(S)))
_, a1, a2, _, _ = pynauty.autgrp(levi(S)); print("|PGammaL(3,9)-stabilizer of author's q=9 witness| =", round(a1 * 10 ** a2))
