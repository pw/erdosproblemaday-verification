#!/usr/bin/env python3
"""Independent recomputation (ours) of Chen's barrier in the w_z form the reduction uses:
   L = sum_{k<=m} (w(k)-c)^+   vs   R = sum_{b in I} (w(b)-1)^+,  w(k) = sum over cluster primes of v_p(k) (all z_p = 1),
   I = the length-m window centred on P = product of the cluster, m = p_{r-1} p_r.  c = 19/10.  Exact (Fractions)."""
import sys
from fractions import Fraction as F
from math import prod, isqrt
def primes_in(a, b): return [p for p in range(a, b + 1) if p > 1 and all(p % d for d in range(2, isqrt(p) + 1))]
def run(lo, hi, c=F(19, 10)):
    ps = primes_in(lo, hi); r = len(ps); m = ps[-2] * ps[-1]; P = prod(ps)
    assert ps[-1] * ps[-1] < 2 * ps[0] * ps[0]        # within sqrt 2
    # left side: enumerate every k <= m with w(k) >= 2 directly (multiples of p*q, p<=q in the cluster)
    w = {}
    for i, p in enumerate(ps):
        for q in ps[i:]:
            d = p * q
            for k in range(d, m + 1, d): w[k] = None
    L = F(0)
    for k in w:
        wk = sum(_v(k, p) for p in ps)
        L += max(F(wk) - c, F(0))
    # right side: window [P-h, P+h] (m odd); only elements divisible by some p^2 or by two cluster primes can have w >= 2
    assert m % 2 == 1; h = (m - 1) // 2; lo_b, hi_b = P - h, P + h
    cand = set()
    for i, p in enumerate(ps):
        for q in ps[i:]:
            d = p * q
            first = -(-lo_b // d) * d
            for b in range(first, hi_b + 1, d): cand.add(b)
    R = F(0); detail = {}
    for b in cand:
        wb = sum(_v(b, p) for p in ps)
        if wb >= 2: R += wb - 1; detail[wb] = detail.get(wb, 0) + 1
    return dict(primes=f'{ps[0]}..{ps[-1]}', r=r, m=m, L=L, R=R, fails=L > R, w_hist=dict(sorted(detail.items())))
def _v(k, p):
    e = 0
    while k % p == 0: k //= p; e += 1
    return e
for lo, hi in ((503, 641), (1049, 1483)):
    out = run(lo, hi); print({k: (str(v) if isinstance(v, F) else v) for k, v in out.items()}, flush=True)
