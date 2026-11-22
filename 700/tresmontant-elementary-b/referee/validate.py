#!/usr/bin/env python3
"""Stage A: cross-validate the three f-computations against each other."""
import sys, time
from ref700 import *

t0 = time.time()
# A1: f_comb == f_leg for every n in [4, 1200] (primes, prime powers, everything)
bad = 0; above = []
for n in range(4, 1201):
    a = f_comb(n); b = f_leg(n)
    if a != b: bad += 1; print("A1 MISMATCH", n, a, b)
    if a * a > n and len(factor(n)) + sum(factor(n).values()) > 2:  # composite
        above.append((n, a))
comp_above = [(n, a) for n, a in above if sum(factor(n).values()) >= 2]
print(f"A1 f_comb vs f_leg, n=4..1200: mismatches={bad}")
print(f"A1 composite n<=1200 with f(n)>sqrt(n): {comp_above}")

# A1b: f_enum2 (Lucas-subset method) vs f_comb on every squarefree composite n in [6,1200]
bad=0; c1=0
for n in range(6, 1201):
    fa = factor(n)
    if len(fa) >= 2 and all(v == 1 for v in fa.values()):
        c1 += 1
        if f_enum2(tuple(sorted(fa))) != f_comb(n): bad += 1; print("A1b MISMATCH", n)
print(f"A1b f_enum2 vs f_comb on {c1} squarefree composites <=1200: mismatches={bad}")
# A2: f_leg == f_enum on every triple of primes p<q<r with n<=4e6 (no hypothesis filter)
P = sieve(2000); cnt = 0; bad = 0; nabove = 0; nbelow = 0
for i in range(len(P)):
    for j in range(i + 1, len(P)):
        if P[i] * P[j] * P[j + 1 if j + 1 < len(P) else j] > 4_000_000: break
        for k in range(j + 1, len(P)):
            p, q, r = P[i], P[j], P[k]
            n = p * q * r
            if n > 4_000_000: break
            if n > 600_000 and (p*7919 + q*104729 + r) % 50: continue   # deterministic ~2% sample of the expensive end
            if n > 150_000 and n <= 600_000 and (p*7919 + q*104729 + r) % 8: continue
            a = f_leg(n); b = f_enum(p, q, r); c = f_enum2((p, q, r))
            cnt += 1
            if not (a == b == c): bad += 1; print("A2 MISMATCH", p, q, r, a, b, c)
            if a * a > n: nabove += 1
            else: nbelow += 1
print(f"A2 f_leg vs f_enum vs f_enum2 on {cnt} prime triples n<=4e6 (all n<=150k, 1/8 of 150k..600k, 1/50 above): mismatches={bad}, f>sqrt n: {nabove}, f<sqrt n: {nbelow}")

# A3: f_leg == f_enum on all hypothesis triples with p<=400 (largest n here ~ 6.8e7)
cnt = 0; bad = 0
for i, p in enumerate(P):
    if p > 400: break
    for j in range(i + 1, len(P)):
        q = P[j]
        if 2 * (q - p) ** 2 >= p: break
        for k in range(j + 1, len(P)):
            r = P[k]
            if 2 * (r - p) ** 2 >= p: break
            if not hyp(p, q, r): continue
            a = f_leg(p * q * r); b = f_enum(p, q, r); c = f_enum2((p, q, r)); cnt += 1
            print(f"A3 {p},{q},{r} d={q-p} h={r-q} e={r-p} f_leg={a} f_enum={b} f_enum2={c} pq={p*q} f==pq:{a==p*q} f^2>n={a*a>p*q*r}")
            if not (a == b == c): bad += 1
print(f"A3 hypothesis triples p<=400: {cnt}, mismatches={bad}")
print(f"elapsed {time.time()-t0:.0f}s")
