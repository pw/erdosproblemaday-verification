#!/usr/bin/env python3
"""Brute-force f(n) two ways for small n:
 (A) literal Lean definition: uPart n k = prod_{p<=k prime} p^{v_p(C(n,k))}, computed by
     factoring C(n,k) exactly with Python big ints; fThr n = min{1<=k<=n : n^2 < uPart}, else TOP.
 (B) problem wording: 0<=k<=n, C(n,k)=u*v, u = k-smooth part; f = smallest k with u > n^2.
Report disagreements and every n with an empty set (f = TOP)."""
import math, sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
def primes_upto(m):
    s = bytearray([1]) * (m + 1); s[0:2] = b'\x00\x00'
    for i in range(2, int(m**0.5) + 1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(m + 1) if s[i]]
P = primes_upto(N + 1)
def vp(x, p):
    e = 0
    while x % p == 0: x //= p; e += 1
    return e
def uPart(n, k):          # (A) literal: product over primes <= k of p^{v_p(C(n,k))}
    c = math.comb(n, k); u = 1
    for p in P:
        if p > k: break
        u *= p ** vp(c, p)
    return u
def u_problem(n, k):      # (B) strip every prime factor > k from C(n,k); what is left is u
    c = math.comb(n, k); v = 1
    for p in P:
        if p <= k: continue
        if p > n: break
        e = vp(c, p); v *= p ** e
    assert c % v == 0
    return c // v
dis = 0; tops = []; fvals = {}
for n in range(0, N + 1):
    fA = None
    for k in range(1, n + 1):
        if n * n < uPart(n, k): fA = k; break
    fB = None
    for k in range(0, n + 1):
        if u_problem(n, k) > n * n: fB = k; break
    if fA != fB:
        dis += 1
        if dis <= 10: print('DISAGREE n=%d leanf=%s problemf=%s' % (n, fA, fB))
    if fA is None: tops.append(n)
    fvals[n] = fA
print('N =', N, 'disagreements:', dis)
print('n with empty set (Lean fThr = TOP):', tops[:80], '... count', len(tops), 'largest', max(tops) if tops else None)
print('sample f(n):', {n: fvals[n] for n in [10, 50, 100, 200, 300, 400] if n <= N})
