#!/usr/bin/env python3
"""Exact checker for (minimal, distinct) covering systems over Z/L, plus number-theory helpers.

check(classes) -> dict(covering, minimal, distinct, L, k, maxmod, bad)
  classes: list of (a, n), n >= 2.
  Covering: every z in Z/L lies in some class.
  Minimal:  every class contains a z (mod L) lying in no other class (Lemma 2.1).
  Distinct: the moduli are pairwise different.
"""
import numpy as np
from math import gcd
from functools import reduce

def lcm(a, b): return a // gcd(a, b) * b
def lcmlist(xs): return reduce(lcm, xs, 1)

def check(classes, Lmax=300_000_000):
    mods = [n for a, n in classes]
    assert all(n >= 2 for n in mods)
    L = lcmlist(mods)
    if L > Lmax:
        raise ValueError(f"period {L} too large")
    cnt = np.zeros(L, dtype=np.int16)
    for a, n in classes:
        cnt[a % n::n] += 1
    covering = bool(cnt.min() >= 1)
    bad = []
    for i, (a, n) in enumerate(classes):
        if not (cnt[a % n::n] == 1).any():
            bad.append((a, n))
    distinct = len(set(mods)) == len(mods)
    return dict(covering=covering, minimal=(not bad), distinct=distinct, L=L,
                k=len(classes), maxmod=max(mods), uncovered=int((cnt == 0).sum()), no_private=bad)

def ok(res):  # minimal distinct covering system
    return res['covering'] and res['minimal'] and res['distinct']

def primes_upto(n):
    s = bytearray([1]) * (n + 1); s[0:2] = b'\x00\x00'
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n + 1) if s[i]]

def factor(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def crt(pairs):
    """pairs of (residue, modulus) with pairwise coprime moduli -> (r, M)."""
    r, M = 0, 1
    for a, m in pairs:
        a %= m
        # solve r + M t = a mod m
        g = gcd(M, m); assert g == 1, (M, m)
        t = ((a - r) * pow(M, -1, m)) % m
        r, M = r + M * t, M * m
    return r % M, M

if __name__ == "__main__":
    # controls
    pos = [(0, 2), (0, 3), (1, 4), (5, 6), (7, 12)]
    print("POSITIVE control {0(2),0(3),1(4),5(6),7(12)}:", check(pos), "=> ok" if ok(check(pos)) else "=> NOT ok")
    neg1 = pos[:-1]
    print("NEGATIVE control, drop 7(12):", check(neg1), "=> ok" if ok(check(neg1)) else "=> NOT ok")
    neg2 = pos + [(0, 8)]
    print("NEGATIVE control, add redundant 0(8):", check(neg2), "=> ok" if ok(check(neg2)) else "=> NOT ok")
    neg3 = [(0, 2), (1, 2)]
    print("NEGATIVE control, {0(2),1(2)} (not distinct):", check(neg3), "=> ok" if ok(check(neg3)) else "=> NOT ok")
