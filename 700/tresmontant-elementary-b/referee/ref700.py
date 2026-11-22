#!/usr/bin/env python3
"""Referee seat, Erdos #700(b), written from scratch (no code shared with the lead's check700.py).

f(n) = min_{1<k<=n/2} gcd(n, C(n,k)).

Three independent ways to compute f:
  f_comb(n)    : literal gcd(n, math.comb(n,k)) over all k (tiny n only)
  f_leg(n)     : Legendre valuations v_s(C(n,k)) = sum_i floor(n/s^i)-floor(k/s^i)-floor((n-k)/s^i),
                 over ALL k in (1, n/2], numpy-chunked, any n (general factorisation, prime powers too)
  f_enum(p,q,r): squarefree n=pqr only. A prime s fails to divide C(n,k) iff k <=_s n digitwise (Lucas).
                 Enumerate every k <=_s n for each s (these sets are small), and for each such k
                 compute gcd = product of the s with k NOT <=_s n. Any k outside all three sets has gcd = n.
                 Exact; does NOT use the submission's reduction (k = s*t*j, r<pq, etc.).
"""
import math, sys, itertools
import numpy as np

def sieve(N):
    b = bytearray([1]) * (N + 1); b[0:2] = b"\x00\x00"
    for i in range(2, int(N ** 0.5) + 1):
        if b[i]: b[i*i::i] = bytearray(len(b[i*i::i]))
    return [i for i in range(N + 1) if b[i]]

def factor(n):
    out = {}; d = 2
    while d * d <= n:
        while n % d == 0: out[d] = out.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: out[n] = out.get(n, 0) + 1
    return out

def f_comb(n):
    return min(math.gcd(n, math.comb(n, k)) for k in range(2, n // 2 + 1))

def f_leg(n, chunk=1 << 22):
    fac = factor(n); best = None
    lo = 2; hi = n // 2
    while lo <= hi:
        k = np.arange(lo, min(hi, lo + chunk - 1) + 1, dtype=np.int64)
        g = np.ones_like(k)
        for s, a in fac.items():
            v = np.zeros_like(k); m = s
            while m <= n:
                v += n // m - k // m - (n - k) // m; m *= s
            g *= np.power(s, np.minimum(v, a)).astype(np.int64)
        mn = int(g.min()); best = mn if best is None else min(best, mn)
        lo += chunk
    return best

def digits(x, b):
    d = []
    while x: d.append(x % b); x //= b
    return d

def dominated_set(n, s):
    """all k with 0<=k<=n and every base-s digit of k <= that of n (Lucas: s does not divide C(n,k))."""
    dn = digits(n, s)
    ks = np.zeros(1, dtype=np.int64)
    pw = 1
    for di in dn:
        ks = (ks[:, None] + (np.arange(di + 1, dtype=np.int64) * pw)[None, :]).ravel()
        pw *= s
    return ks

def dom_mask(ks, n, s):
    a = ks.copy(); ok = np.ones(ks.shape, bool); m = n
    while m:
        ok &= (a % s) <= (m % s); a //= s; m //= s
    ok &= a == 0
    return ok

def f_enum(p, q, r, want_k=False):
    n = p * q * r; P = (p, q, r)
    best = n; bestk = None
    for s in P:
        ks = dominated_set(n, s)
        ks = ks[(ks > 1) & (ks <= n // 2)]
        if ks.size == 0: continue
        g = np.ones_like(ks)
        for t in P:
            g *= np.where(dom_mask(ks, n, t), 1, t)
        i = int(g.argmin())
        if int(g[i]) < best: best = int(g[i]); bestk = int(ks[i])
    return (best, bestk) if want_k else best

def hyp(p, q, r):
    d, h, e = q - p, r - q, r - p
    return h > d and 2 * e * e < p

def digit_prod(n, s):
    return math.prod(d + 1 for d in digits(n, s))

def iter_dominated(n, s, chunk=1 << 22):
    """yield numpy chunks of all k <=_s n (mixed-radix decode of an index range); avoids building huge sets."""
    dn = digits(n, s); radices = [d + 1 for d in dn]; total = math.prod(radices)
    lo = 0; size = 4096
    while lo < total:
        hi = min(total, lo + size); size = min(chunk, size * 4)
        idx = np.arange(lo, hi, dtype=np.int64); lo = hi
        k = np.zeros_like(idx); pw = 1
        for rd in radices:
            k += (idx % rd) * pw; idx //= rd; pw *= s
        yield k

def f_enum2(primes, chunk=1 << 22):
    """Exact f(n) for squarefree n = product of the given distinct primes (any count), via Lucas:
    gcd(n,C(n,k)) = n / prod{s : k <=_s n}. For each subset S of size >= 2, decide whether some k in (1,n/2]
    is dominated in every base of S by enumerating the dominated set of the base in S with the fewest members.
    For |S| = 1 the set is nonempty iff some dominated k in (1, n/2] exists (checked directly). Returns min gcd."""
    n = math.prod(primes); half = n // 2; best = n
    subsets = []
    for size in range(len(primes), 0, -1):
        subsets += list(itertools.combinations(primes, size))
    for S in subsets:
        val = n // math.prod(S)
        if val >= best: continue
        base = min(S, key=lambda s: digit_prod(n, s)); others = [t for t in S if t != base]
        found = False
        for ks in iter_dominated(n, base, chunk):
            m = (ks > 1) & (ks <= half)
            for t in others:
                if not m.any(): break
                m &= dom_mask(ks, n, t)
            if m.any(): found = True; break
        if found: best = val
    return best
