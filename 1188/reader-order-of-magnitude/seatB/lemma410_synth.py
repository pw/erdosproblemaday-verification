#!/usr/bin/env python3
"""Bookkeeping of the proof of Lemma 4.10 at depth up to 5, with synthetic pool sizes:
a_e, b_e, L_e as defined in the paper; the trees are then grown from the a_e and checked:
labels decrease along paths, node counts, leaf counts L_e, |P_d| - l(d) < L_d <= |P_d| for d in D,
each nontrivial tree's leaves partition its fibre (sum of 1/e = 1), and N_1 = sum_e L_e/e exactly."""
import random, itertools
from fractions import Fraction
from math import prod

rng = random.Random(410)
for trial in range(200):
    I = sorted(rng.sample([11, 13, 17, 19, 23, 29, 31], rng.randint(2, 6)))
    allI = [prod(c) for k in range(1, len(I) + 1) for c in itertools.combinations(I, k)]
    D = set(rng.sample(allI, rng.randint(1, len(allI))))
    pf = {e: sorted(c for c in I if e % c == 0) for e in allI}
    ell = {e: pf[e][0] for e in allI}
    N = set()
    for d in D:
        ps = pf[d][::-1]
        for i in range(1, len(ps) + 1): N.add(prod(ps[:i]))
    pool = {e: rng.randint(ell[e] + 1, 12 * ell[e]) for e in N}       # |P_{p,e}| > l(e) as in the paper
    succ = {e: [e2 for e2 in N if e2 % e == 0 and e2 // e in I and e2 // e < ell[e]] for e in N}
    a, L = {}, {}
    for e in sorted(N, reverse=True):
        b = sum(a[e2] for e2 in succ[e])
        a[e] = (pool[e] + b) // ell[e] if e in D else -(-b // ell[e])
        L[e] = ell[e] * a[e] - b
        assert 0 <= L[e] <= pool[e]
        if e in D: assert pool[e] - ell[e] < L[e] <= pool[e]
        else: assert L[e] < ell[e]
    N1 = sum(a[e] for e in N if e in I)
    assert Fraction(N1) == sum(Fraction(L[e], e) for e in N)
    # grow the trees
    nodes = {}; fib = 0; trees = {}
    for c in sorted(e for e in N if e in I):
        for _ in range(a[c]):
            fib += 1; nodes.setdefault(c, []).extend((fib, ((c, v),)) for v in range(c))
    leaves = []
    for e in sorted(N, key=lambda e: (len(pf[e]), e)):
        lst = nodes.get(e, [])
        assert len(lst) == ell[e] * a[e]
        k = 0
        for e2 in sorted(succ[e], reverse=True):
            c = e2 // e
            for _ in range(a[e2]):
                u, path = lst[k]; k += 1
                nodes.setdefault(e2, []).extend((u, path + ((c, v),)) for v in range(c))
        assert len(lst) - k == L[e]
        leaves += lst[k:]
    per = {}
    for u, path in leaves:
        assert all(path[i][0] > path[i + 1][0] for i in range(len(path) - 1))
        per[u] = per.get(u, 0) + Fraction(1, prod(c for c, v in path))
    assert len(per) == N1 and all(v == 1 for v in per.values())
    # exact partition check on each tree: leaves' (e, residue) cover Z/(prod I) exactly once
    E = prod(I)
    if E <= 3_000_000 and trial % 20 == 0:
        import numpy as np
        for u in list(per)[:5]:
            cnt = np.zeros(E, dtype=np.int8)
            for uu, path in leaves:
                if uu != u: continue
                e = prod(c for c, v in path)
                r = next(x for x in range(e) if all(x % c == v for c, v in path))
                cnt[r::e] += 1
            assert (cnt == 1).all()
    if trial < 5 or trial % 50 == 0:
        print(f"trial {trial}: I={I} |D|={len(D)} |N|={len(N)} N_1={N1} leaves={len(leaves)} "
              f"max depth={max(len(p) for _, p in leaves)}")
print("Lemma 4.10 bookkeeping: 200 synthetic trials passed (identity, bounds, decreasing labels, partition)")
