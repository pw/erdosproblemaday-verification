#!/usr/bin/env python3
"""Referee's own implementation of the chained lower bound (written independently of bound.py):
L_M(t) = exact h_M(t) where computed, else max(sup_{s<=t} L_M(s), L_Mc(t) + L_Mc(t/p)); W = int L t^-2."""
import json
from fractions import Fraction as Fr
def divs(M): return [d for d in range(1, M + 1) if M % d == 0]
def prof(M, src):
    return {r['t']: r['h'] for r in json.load(open('/tmp/ref301/prof_%d%s.json' % (M, src)))}
def make(M, exact, child=None):
    D = divs(M); L = {}; best = 0
    for d in D:
        if d in exact: v = exact[d]
        else:
            v = best
            if child: v = max(v, child(d) + child(Fr(d, M // childM[0])))
        assert v >= best   # exact data must itself be nondecreasing
        best = v; L[d] = v
    def f(t):
        r = 0
        for d in D:
            if d > t: break
            r = L[d]
        return r
    W = sum(L[d] * (Fr(1, d) - (Fr(1, D[i + 1]) if i + 1 < len(D) else 0)) for i, d in enumerate(D))
    return f, W
childM = [None]
f5, W5 = make(5040, prof(5040, '_dfs'))
childM[0] = 5040; f55, W55 = make(55440, prof(55440, '_dfs'), f5)
childM[0] = 55440; f72, W72 = make(720720, prof(720720, '_ihs'), f55)
d72 = Fr(55, 248)
print('W5040 =', W5, ' W55440 >=', W55, float(W55), ' W720720 >=', W72, float(W72))
print('C <=', 1 - d72 * W72, float(1 - d72 * W72))
