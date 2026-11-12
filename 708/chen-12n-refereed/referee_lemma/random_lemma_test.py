#!/usr/bin/env python3
"""Stress the LEMMA's construction as written (not k2t2.py's prime chooser): random primes satisfying (P1),(P2),
random valid s_q (any multiple of q in C_q), random CRT lift of k prime to all w_i.  Scan F1-F3 and ILP-solve."""
import random, sys
from math import prod
from sympy import primerange
from refsolve import ilp_types, val

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 300
done = fail = 0
while done < N:
    X = random.randrange(13, 260); t = random.randrange(2, 7)
    pool = list(primerange(X, int(1.5 * X) + 2))
    if len(pool) < t + 2: continue
    ps = sorted(random.sample(pool, t + 2)); ws, qu, qv = ps[:t], ps[t], ps[t + 1]
    m = ws[-1] * qv
    if not (m < 2 * ws[0] * ws[1] and qu * qu >= m + qu): continue
    Pi = prod(ps); a = -(m // 2)
    res = {}
    for q in (qu, qv):
        C = range(a + m, a + q * q)                      # C_q as integers
        mults = [c for c in C if c % q == 0]
        assert mults and all(c % (q * q) for c in mults)  # s_q != 0 mod q
        c = random.choice(mults); s = c // q
        res[q] = (-s * pow(Pi // q, -1, q)) % q
    k0 = (res[qu] * qv * pow(qv, -1, qu) + res[qv] * qu * pow(qu, -1, qv)) % (qu * qv)
    k = k0 + qu * qv * random.randrange(0, 50)
    while k == 0 or any(k % w == 0 for w in ws): k += qu * qv
    u = k * Pi; x = u + a - 1
    I = range(x + 1, x + m + 1)
    multi = [b for b in I if sum(b % p == 0 for p in ps) >= 2]
    sq = [b for b in I if b % (qu * qu) == 0 or b % (qv * qv) == 0]
    F = (multi == [u]) and not sq and all(val(u, p) == 1 for p in ps)
    A = sorted([w * qu for w in ws] + [w * qv for w in ws])
    g = ilp_types(A, x)[0]; g2 = ilp_types(A + [qu], x)[0]
    ok = F and g == 3 * t - 1 and g2 == 3 * t
    done += 1
    if not ok:
        fail += 1; print('FAIL', ws, qu, qv, k, x, F, g, g2)
print(f'{done} random instances, {fail} failures (t in 2..6, X in 13..259)')
