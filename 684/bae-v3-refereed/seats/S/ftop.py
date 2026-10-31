#!/usr/bin/env python3
"""Scan n<=N for empty defining set (f(n)=TOP) using Legendre's formula; also max f(n)/log n."""
import math, sys
N = int(sys.argv[1])
def primes_upto(m):
    s = bytearray([1]) * (m + 1); s[0:2] = b'\x00\x00'
    for i in range(2, int(m**0.5) + 1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(m + 1) if s[i]]
P = primes_upto(N + 1)
def leg(n, p):
    e = 0
    while n: n //= p; e += n
    return e
tops = []; best = (0, 0, 0)
for n in range(2, N + 1):
    lim = 2 * math.log(n); f = None
    for k in range(1, n + 1):
        lu = 0.0
        for p in P:
            if p > k: break
            e = leg(n, p) - leg(k, p) - leg(n - k, p)
            if e: lu += e * math.log(p)
        if lu > lim + 1e-9:
            # confirm exactly with integers
            u = 1
            for p in P:
                if p > k: break
                u *= p ** (leg(n, p) - leg(k, p) - leg(n - k, p))
            if u > n * n: f = k; break
    if f is None: tops.append(n)
    elif n > 30 and f / math.log(n) > best[0]: best = (f / math.log(n), n, f)
print('N', N, 'TOP n:', tops, 'max f(n)/log n for n>30:', best)
