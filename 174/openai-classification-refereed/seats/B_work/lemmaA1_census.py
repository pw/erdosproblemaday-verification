#!/usr/bin/env python3
"""Blind seat B: Lemma A.1 (Palvolgyi) first-order certificates (M symmetric) for the five failing 8-point orbits and a
few passing ones (controls: a passing set must have energy 0 on the whole solution space, else Theorem 1.1 is contradicted)."""
import sympy as sp
t = sp.symbols('tau'); u, v = (1 - t**2)/(1 + t**2), 2*t/(1 + t**2)
Q0 = [(1, 0), (0, 1), (-1, 0), (0, -1)]
X = []
for eps in '+-0':
    for a, b in Q0:
        X.append((u*a - v*b, v*a + u*b) if eps == '+' else (u*a + v*b, -v*a + u*b) if eps == '-' else (sp.Integer(a), sp.Integer(b)))
D = lambda e: sp.diff(e, t)
def cert(S):
    P = [X[i] for i in S]; n = len(P); lam = sp.symbols('l0:%d' % n)
    p = [sp.Matrix(q) for q in P]; dp = [q.applyfunc(D) for q in p]
    eqs = [sum(lam)] + [sum(lam[i]*p[i][k] for i in range(n)) for k in range(2)]
    eqs += list(sum((lam[i]*p[i]*p[i].T for i in range(n)), sp.zeros(2)))
    eqs += [sum(lam[i]*dp[i][k] for i in range(n)) for k in range(2)]
    M = sum((lam[i]*dp[i]*p[i].T for i in range(n)), sp.zeros(2)); eqs += [M[0, 1] - M[1, 0]]
    sol = list(sp.linsolve([sp.numer(sp.together(e)) for e in eqs], lam))[0]
    free = sorted(set().union(*[x.free_symbols for x in sol]) - {t}, key=str)
    E = sp.factor(sp.simplify(sum(sol[i]*(dp[i].T*dp[i])[0] for i in range(n))))
    return len(free), E
for S in [(0, 1, 2, 4, 5, 6, 9, 11), (0, 1, 2, 4, 6, 7, 8, 10), (0, 1, 4, 7, 8, 9, 10, 11), (0, 1, 5, 6, 8, 9, 10, 11), (0, 2, 4, 6, 8, 9, 10, 11)]:
    print('census FAILS', S, '-> Lemma A.1 solution dim, energy:', cert(S), flush=True)
for S in [(0, 1, 2, 3, 4, 5, 6, 7), (0, 1, 2, 3, 8, 9, 10, 11), (0, 2, 5, 7, 8, 9, 10, 11), (0, 1, 2, 3, 4, 5, 6)]:
    print('census HOLDS (control)', S, '->', cert(S), flush=True)
