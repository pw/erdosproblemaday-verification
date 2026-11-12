#!/usr/bin/env python3
"""K_{2,t} family of Chen §(incidence sharpness): A = {w_i q_u, w_i q_v}, n = 2t.
Our placement: centre the window on u = k*M (M = product of the t+2 primes), k coprime to every prime and
chosen (CRT) so that the multiples of q_u^2 and q_v^2 nearest u are about q^2/2 away.  Then u is the only
window element divisible by two demanded primes and no element is divisible by q_u^2 or q_v^2.
Each instance is checked by the exact solver (exact.py), which uses no part of this reasoning."""
import sys
from math import prod, isqrt
from exact import solve

def primes_between(a, b):
    return [p for p in range(max(2, a), b) if all(p % d for d in range(2, isqrt(p) + 1))]

def choose_primes(t):
    # smallest X such that [X, sqrt2*X) holds t+2 primes w_1<..<w_t<q_u<q_v with q_u^2 > w_t q_v
    X = 11
    while True:
        P = [p for p in primes_between(X, int(1.41421356 * X) + 1) if p * p < 2 * X * X]
        if len(P) >= t + 2:
            for i in range(len(P) - 1, 0, -1):          # try (q_u,q_v) as high consecutive pairs
                qu, qv = P[i - 1], P[i]
                ws = [p for p in P if p < qu][:t]
                if len(ws) == t and qu * qu > ws[-1] * qv and qv * qv < 2 * ws[0] * ws[0]:
                    return ws, qu, qv
        X += 1

def placement(ws, qu, qv):
    M = prod(ws) * qu * qv
    m = ws[-1] * qv
    R_u, R_v = M // qu, M // qv
    # want k*R_u = -floor(qu/2) mod qu and k*R_v = -floor(qv/2) mod qv, k coprime to all primes
    ku = (-(qu // 2) * pow(R_u, -1, qu)) % qu
    kv = (-(qv // 2) * pow(R_v, -1, qv)) % qv
    k0 = (ku * qv * pow(qv, -1, qu) + kv * qu * pow(qu, -1, qv)) % (qu * qv)
    k = k0
    while any(k % p == 0 for p in ws + [qu, qv]) or k == 0:
        k += qu * qv
    u = k * M
    x = u - (m + 1) // 2          # window x+1..x+m contains u near its centre
    return M, m, k, u, x

if __name__ == '__main__':
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    for t in range(2, T + 1):
        ws, qu, qv = choose_primes(t)
        M, m, k, u, x = placement(ws, qu, qv)
        A = sorted([w * qu for w in ws] + [w * qv for w in ws])
        assert len(A) == 2 * t and A[-1] == m
        g, wit = solve(A, x)
        print(f't={t} n={2*t} w={ws} q=({qu},{qv}) m={m} k={k} x={x} -> min|B|={g} (3t-1={3*t-1})', flush=True)
