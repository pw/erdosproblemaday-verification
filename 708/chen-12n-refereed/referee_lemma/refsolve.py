#!/usr/bin/env python3
"""Referee B's own exact solver for Erdos #708 instances (does NOT import exact.py).

min |B|, B subset of {x+1..x+m}, m = max A, prod(A) | prod(B).

Route 1 (dp_types): group window elements by their capped valuation vector over the demanded primes
  (elements with equal vectors are interchangeable), then a bounded-multiplicity DP over capped states,
  type by type.  Generic: assumes nothing about F1-F3.
Route 2 (ilp_types): the same type-count model solved as an integer programme by HiGHS (scipy.milp),
  with UNCAPPED valuations as coefficients; optimality certified by HiGHS (status 0, gap 0).
Route 3 (brute): plain subset enumeration, small windows only.
"""
import itertools
from math import prod
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from sympy import factorint


def demand(A):
    e = {}
    for a in A:
        for p, k in factorint(a).items():
            e[p] = e.get(p, 0) + k
    return e


def val(b, p):
    k = 0
    while b % p == 0:
        b //= p
        k += 1
    return k


def window_types(A, x):
    A = sorted(set(A))
    m = A[-1]
    e = demand(A)
    P = sorted(e)
    types = {}          # uncapped valuation vector -> list of window elements
    for b in range(x + 1, x + m + 1):
        v = tuple(val(b, p) for p in P)
        if any(v):
            types.setdefault(v, []).append(b)
    return A, m, e, P, types


def dp_types(A, x):
    A, m, e, P, types = window_types(A, x)
    E = tuple(e[p] for p in P)
    # merge types after capping
    capped = {}
    for v, bs in types.items():
        cv = tuple(min(v[i], E[i]) for i in range(len(P)))
        capped.setdefault(cv, []).extend(bs)
    best = {tuple(0 for _ in P): (0, ())}   # state -> (cost, list of (type, count))
    for cv, bs in capped.items():
        useful = max(-(-E[i] // cv[i]) for i in range(len(P)) if cv[i] > 0)
        cmax = min(len(bs), useful)
        new = dict(best)
        for s, (c, hist) in best.items():
            for j in range(1, cmax + 1):
                t = tuple(min(E[i], s[i] + j * cv[i]) for i in range(len(P)))
                if t not in new or new[t][0] > c + j:
                    new[t] = (c + j, hist + ((cv, j),))
        best = new
    c, hist = best[E]
    wit = []
    for cv, j in hist:
        wit += capped[cv][:j]
    assert len(wit) == c == len(set(wit))
    assert all(x < b <= x + m for b in wit)
    assert prod(wit) % prod(A) == 0, 'witness does not cover'
    return c, sorted(wit)


def ilp_types(A, x):
    A, m, e, P, types = window_types(A, x)
    keys = list(types)
    nv = len(keys)
    M = np.array([[keys[j][i] for j in range(nv)] for i in range(len(P))], dtype=float)
    lb = np.array([e[p] for p in P], dtype=float)
    res = milp(c=np.ones(nv), constraints=LinearConstraint(M, lb, np.inf),
               integrality=np.ones(nv), bounds=Bounds(np.zeros(nv), np.array([len(types[k]) for k in keys], float)),
               options={'mip_rel_gap': 0.0})
    assert res.status == 0, res.message
    cnt = [int(round(z)) for z in res.x]
    wit = [b for j, k in enumerate(keys) for b in types[k][:cnt[j]]]
    assert prod(wit) % prod(A) == 0
    return int(round(res.fun)), len(keys), getattr(res, 'mip_gap', None)


def brute(A, x, limit=8):
    A = sorted(set(A)); m = A[-1]; PA = prod(A)
    I = range(x + 1, x + m + 1)
    for k in range(0, limit + 1):
        for S in itertools.combinations(I, k):
            if prod(S) % PA == 0:
                return k
    return None


if __name__ == '__main__':
    import random, sys
    random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    bad = 0; N = 600
    for trial in range(N):
        n = random.choice([1, 2, 3, 4])
        A = sorted(random.sample(range(2, 25), n)); x = random.randrange(0, 20000)
        g1, _ = dp_types(A, x); g2, _, _ = ilp_types(A, x); g3 = brute(A, x, limit=max(g1, g2))
        if not (g1 == g2 == g3):
            bad += 1; print('MISMATCH', A, x, g1, g2, g3)
    print(f'self-test: {bad} mismatches of {N} (dp vs ilp vs brute)')
