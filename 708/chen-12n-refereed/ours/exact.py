#!/usr/bin/env python3
"""Exact min |B| for Erdős #708 instances — independent implementation (does not use chy4pro's gn_dp.py).

g(A,x) = min |B|, B ⊆ {x+1..x+m}, m = max A, prod(A) | prod(B).
Method: capped valuation vectors; 'special' positions (>= 2 capped units) handled by an exact DP over
capped demand states; 'single' positions (exactly one unit, of one prime) are interchangeable per prime,
so a deficit d_p is filled by d_p singles if at least d_p exist.  Returns (min, witness B).
"""
import sys, itertools
from math import prod

def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def demand(A):
    e = {}
    for a in A:
        for p, k in factor(a).items(): e[p] = e.get(p, 0) + k
    return e

def vval(b, p, cap):
    k = 0
    while k < cap and b % p == 0: b //= p; k += 1
    return k

def solve(A, x, return_witness=True):
    A = sorted(set(A)); m = A[-1]
    e = demand(A); P = sorted(e)
    vecs = {}
    for b in range(x + 1, x + m + 1):
        v = tuple(vval(b, p, e[p]) for p in P)
        if sum(v): vecs[b] = v
    special = [(b, v) for b, v in vecs.items() if sum(v) >= 2]
    singles = {p: [] for p in P}
    for b, v in vecs.items():
        if sum(v) == 1: singles[P[[i for i, t in enumerate(v) if t][0]]].append(b)
    E = [e[p] for p in P]
    # DP over capped states: state -> (count, chosen specials tuple)
    best = {tuple([0] * len(P)): (0, ())}
    for b, v in special:
        new = dict(best)
        for s, (c, ch) in best.items():
            t = tuple(min(E[i], s[i] + v[i]) for i in range(len(P)))
            if t not in new or new[t][0] > c + 1: new[t] = (c + 1, ch + (b,))
        best = new
    ans, wit = None, None
    for s, (c, ch) in best.items():
        deficit = [E[i] - s[i] for i in range(len(P))]
        if any(deficit[i] > len(singles[P[i]]) for i in range(len(P))): continue
        tot = c + sum(deficit)
        if ans is None or tot < ans:
            ans = tot
            wit = list(ch) + [b for i in range(len(P)) for b in singles[P[i]][:deficit[i]]]
    if ans is None: raise RuntimeError('no cover (impossible: whole window always covers)')
    # certificate check: product divisibility, size, range
    assert len(set(wit)) == len(wit) == ans
    assert all(x < b <= x + m for b in wit)
    assert prod(wit) % prod(A) == 0
    return ans, sorted(wit)

def brute_min(A, x, limit):
    """Independent check by plain subset enumeration (small windows only): least k <= limit with a cover."""
    A = sorted(set(A)); m = A[-1]; PA = prod(A)
    I = list(range(x + 1, x + m + 1))
    for k in range(1, limit + 1):
        for S in itertools.combinations(I, k):
            if prod(S) % PA == 0: return k, S
    return None, None

if __name__ == '__main__':
    tests = [([10, 12, 15, 20], 50), ([5, 10, 12, 15, 20], 50),
             ([59 * 71, 59 * 73, 61 * 71, 61 * 73], 18652287),
             ([67 * 97, 67 * 101, 73 * 97, 73 * 101, 79 * 97, 79 * 101], 3785449127)]
    for A, x in tests:
        g, w = solve(A, x)
        print(len(A), A, x, '->', g, w)
    # cross-check exact.solve against plain brute force on small random instances
    import random
    random.seed(708)
    bad = 0
    for trial in range(400):
        n = random.choice([2, 3, 4])
        A = sorted(random.sample(range(2, 23), n)); x = random.randrange(0, 5000)
        g, _ = solve(A, x)
        gb, _ = brute_min(A, x, g)
        if gb != g: bad += 1; print('MISMATCH', A, x, g, gb)
    print('brute cross-check mismatches:', bad, 'of 400')
