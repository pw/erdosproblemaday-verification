#!/usr/bin/env python3
"""Referee A: random falsification attempt of Theorem 1.3 (local lemma) on random minimal covering
systems with repeated moduli allowed (the theorem's stated generality)."""
import math, random
import numpy as np
from functools import reduce

def factor(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def vp(n, p):
    k = 0
    while n % p == 0: n //= p; k += 1
    return k

def local_property(system):
    """returns list of (p, ok, sum p^-v, count) for every prime dividing a modulus"""
    res = []
    primes = sorted({p for _, n in system for p in factor(n)})
    for p in primes:
        e = max(vp(n, p) for _, n in system)
        pe = p ** e
        hit = np.zeros(pe, dtype=bool)
        cls = [(a, n) for a, n in system if n % p == 0]
        for a, n in cls:
            v = vp(n, p)
            hit[(a % p**v)::p**v] = True
        s = sum(p ** (-vp(n, p)) for _, n in cls)
        res.append((p, bool(hit.all()), s, len(cls)))
    return res

def is_cover(system, L):
    c = np.zeros(L, dtype=np.int32)
    for a, n in system: c[a % n::n] += 1
    return c

def random_minimal(L, rng, maxmod=None):
    divs = [d for d in range(2, L + 1) if L % d == 0 and (maxmod is None or d <= maxmod)]
    c = np.zeros(L, dtype=np.int32); system = []
    while (c == 0).any():
        z = int(rng.choice(np.nonzero(c == 0)[0]))
        n = rng.choice(divs)
        system.append((z % n, n)); c[z % n::n] += 1
    system = list(dict.fromkeys(system))
    rng.shuffle(system)
    keep = []
    for a, n in system:          # one pass: a class with a private residue stays needed after later removals
        if (c[a::n] == 1).any():
            keep.append((a, n))
        else:
            c[a::n] -= 1
    system = keep
    # verify minimal
    c = is_cover(system, L)
    assert c.min() >= 1 and all((c[a::n] == 1).any() for a, n in system)
    return system

rng = random.Random(1188)
nprng = np.random.default_rng(1188)
fails = 0; tested = 0; primes_tested = 0
for L in (72, 144, 360, 720, 1080, 2520, 5040, 4200):
    for _ in range(400):
        s = random_minimal(L, rng)
        for p, ok, sm, cnt in local_property(s):
            primes_tested += 1
            if not ok or sm < 1 - 1e-12 or cnt < p:
                fails += 1
                print("COUNTEREXAMPLE?", L, s, p, ok, sm, cnt)
        tested += 1
print(f"random minimal coverings tested: {tested}; (system,prime) pairs: {primes_tested}; failures of Thm 1.3: {fails}")

# negative control: a NON-minimal covering where the property must fail
nonmin = [(0, 2), (1, 2), (0, 3)]
print("NEG CONTROL non-minimal {0 mod 2, 1 mod 2, 0 mod 3}:", local_property(nonmin))
# positive control: classical system
print("POS CONTROL classical:", local_property([(0, 2), (0, 3), (1, 4), (5, 6), (7, 12)]))
