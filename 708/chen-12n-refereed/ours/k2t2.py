#!/usr/bin/env python3
"""K_{2,t} placements for every t (our construction).  Primes w_1<..<w_t<q_u<q_v, all in [X, sqrt2 X),
with q_u^2 >= m + q_u where m = w_t q_v (the max of A).  u = k*M, M = prod of all t+2 primes, k coprime to
every prime.  Window offsets [a, a+m-1] around u with a = -floor(m/2).  For q in {q_u,q_v} pick s_q in [1,q-1]
with (q*s_q - a) mod q^2 >= m (exists because the cyclic complement has length q^2-m >= q); then
k = -s_q * (M/q)^{-1} (mod q) by CRT, lifted to be coprime to the w_i.
Claims checked by exact.py: min|B| = 3t-1 for A (n=2t) and = 3t for A + {q_u} (n=2t+1)."""
import sys
from math import prod, isqrt
from exact import solve

def is_prime(p): return p > 1 and all(p % d for d in range(2, isqrt(p) + 1))

def choose_primes(t):
    X = 11
    while True:
        P = [p for p in range(X, isqrt(2 * X * X - 1) + 1) if is_prime(p)]   # p < sqrt2 X  <=>  p^2 < 2X^2
        for i in range(len(P) - 1, 0, -1):
            qu, qv = P[i - 1], P[i]
            ws = [p for p in P if p < qu][:t]
            if len(ws) == t:
                m = ws[-1] * qv
                if qu * qu >= m + qu and m <= 2 * ws[0] * ws[1] - 1:
                    return ws, qu, qv
        X += 1

def placement(ws, qu, qv):
    M = prod(ws) * qu * qv
    m = ws[-1] * qv
    a = -(m // 2)
    assert -a <= ws[0] * ws[1] - 1 and a + m - 1 <= ws[0] * ws[1] - 1   # pair-free window
    res = {}
    for q in (qu, qv):
        s = next(s for s in range(1, q) if (q * s - a) % (q * q) >= m)
        res[q] = (-s * pow(M // q, -1, q)) % q
    k = (res[qu] * qv * pow(qv, -1, qu) + res[qv] * qu * pow(qu, -1, qv)) % (qu * qv)
    while k == 0 or any(k % p == 0 for p in ws + [qu, qv]):
        k += qu * qv
    u = k * M
    x = u + a - 1                    # window x+1 .. x+m  = offsets a .. a+m-1
    return M, m, k, u, x

if __name__ == '__main__':
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    for t in range(2, T + 1):
        ws, qu, qv = choose_primes(t)
        M, m, k, u, x = placement(ws, qu, qv)
        A = sorted([w * qu for w in ws] + [w * qv for w in ws])
        assert len(A) == 2 * t and A[-1] == m
        g, wit = solve(A, x)
        A2 = sorted(A + [qu]); g2, wit2 = solve(A2, x)
        ok = (g == 3 * t - 1) and (g2 == 3 * t)
        print(f't={t} w={ws} q=({qu},{qv}) m={m} k={k} x={x}  n={2*t}: {g} (3t-1={3*t-1})  n={2*t+1}: {g2} (3t={3*t})  {"OK" if ok else "FAIL"}', flush=True)
