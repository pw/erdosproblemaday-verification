#!/usr/bin/env python3
"""Seat P -- end-to-end SMALL-CASE illustration (evidence only, not a test of the asymptotics).

Build n = tL - h - 1 with ||tL||_p < h for all M < p <= K (CRT, random signed targets,
random high part), compute f(n) exactly by Legendre, and print f(n), K, log n, and the
largest log u(n,k) over k <= K vs 2 log n.  For comparison: APSSV's n = M_K - 1 and
random n of the same size.
"""
import math, random

def primes_upto(N):
    s = bytearray([1]) * (N + 1); s[0:2] = b'\x00\x00'
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]: s[i*i::i] = bytearray(len(range(i*i, N + 1, i)))
    return [i for i in range(N + 1) if s[i]]

PR = primes_upto(20000)

def logu(n, k):
    s = 0.0
    for p in PR:
        if p > k: break
        q = p
        while q <= n:
            if n % q < k % q: s += math.log(p)
            q *= p
    return s

def f(n, kmax=20000):
    two = 2 * math.log(n)
    for k in range(1, kmax + 1):
        if logu(n, k) > two: return k
    return None

def lcm_upto(M):
    L = 1
    for i in range(1, M + 1): L = L * i // math.gcd(L, i)
    return L

def build(M, h, K, rng):
    L = lcm_upto(M)
    P2 = [p for p in PR if M < p <= K]
    P = 1
    for p in P2: P *= p
    t0 = 0
    for p in P2:
        z = rng.randint(-h + 1, h - 1)
        Np = P // p
        t0 = (t0 + (z * pow(L, -1, p) % p) * Np * pow(Np, -1, p)) % P
    t = t0 + P * rng.randint(1, 10 ** 6)
    return t * L - h - 1

if __name__ == '__main__':
    rng = random.Random(684)
    for (M, h, K) in [(30, 3, 150), (40, 4, 240), (60, 5, 360)]:
        for _ in range(2):
            n = build(M, h, K, rng)
            fn = f(n)
            mx = max(logu(n, k) for k in range(1, K + 1))
            nr = rng.randint(n // 2, n)
            print(f"M={M} h={h} K={K}: log n={math.log(n):.1f}  f(n)={fn}  f(n)/log n={fn / math.log(n):.2f}  "
                  f"max_(k<=K) log u={mx:.1f} vs 2log n={2 * math.log(n):.1f}  | random n same size: f={f(nr)}")
    for Kq in (60, 100, 150):
        MK = 1
        for p in PR:
            if p > Kq: break
            MK *= p ** (int(math.floor(math.log(Kq) / math.log(p) + 1e-12)) + 1)
        n = MK - 1
        fn = f(n)
        print(f"APSSV n=M_K-1, K={Kq}: log n={math.log(n):.1f} f(n)={fn} f/log n={fn / math.log(n):.2f}")
