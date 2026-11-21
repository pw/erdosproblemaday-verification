#!/usr/bin/env python3
"""Certified lower bound on W_M = int h_M(t)/t^2 dt and the resulting C_M = 1 - delta_M W_M for Erdos #301.
Inputs: profile logs (C DFS '*.out' or CP-SAT '*.log' lines 'd=.. grow|jump F=..'), exact for t <= the last line.
For M' = p*M with p not dividing M:  h_{M'}(t) >= h_M(t) + h_M(t/p)   (D(M') = D(M) disjoint-union p*D(M)).
h is nondecreasing, so lower bounds are closed under running max. W from the step function on the divisor grid.
"""
import re, sys
from fractions import Fraction as Fr

def divisors(M): return [d for d in range(1, M + 1) if M % d == 0]

def delta(M):
    r = Fr(1); m = M; p = 2
    while m > 1:
        if m % p == 0:
            e = 0
            while m % p == 0: m //= p; e += 1
            r *= Fr(p - 1, p) / (1 - Fr(1, p ** (e + 1)))
        p += 1
    return r

def read_profile(path):
    """returns {d: F} for consecutive divisors from 1."""
    prof = {}
    for line in open(path):
        m = re.match(r"\s*d=\s*(\d+)\s+(grow|jump)\s+F=\s*(\d+)", line)
        if m: prof[int(m.group(1))] = int(m.group(3))
    return prof

def exact_h(M, prof):
    """h at each divisor d of M that the profile covers (must be a prefix)."""
    D = divisors(M); out = {}
    for i, d in enumerate(D):
        if d not in prof: break
        out[d] = (i + 1) - prof[d]
    return out

def step_eval(h_by_div, D, t):
    """h at real t = value at the largest divisor <= t (0 below 1)."""
    best = 0
    for d in D:
        if d <= t: best = h_by_div.get(d, best)
        else: break
    return best

def lower_profile(M, exact, child=None):
    """lower bound of h_M at every divisor of M. child = (Mc, p, lb_child dict) for M = p*Mc."""
    D = divisors(M); lb = {}; run = 0
    for d in D:
        v = exact.get(d, 0)
        if child:
            Mc, p, lbc = child; Dc = divisors(Mc)
            v = max(v, step_eval(lbc, Dc, d) + step_eval(lbc, Dc, Fr(d, p)))
        run = max(run, v); lb[d] = run
    return lb

def W_of(M, lb):
    D = divisors(M); W = Fr(0)
    for i, d in enumerate(D):
        nxt = Fr(1, D[i + 1]) if i + 1 < len(D) else Fr(0)
        W += lb[d] * (Fr(1, d) - nxt)
    return W

if __name__ == "__main__":
    # usage: bound.py 5040:p5040.out 55440:p55440.out 720720:p720720.out   (chain, each p*previous)
    chain = [a.split(":") for a in sys.argv[1:]]
    prev = None
    for Ms, path in chain:
        M = int(Ms); prof = read_profile(path) if path != "-" else {}
        ex = exact_h(M, prof)
        child = None
        if prev:
            Mc, lbc = prev; assert M % Mc == 0 and (M // Mc) not in (1,) and Mc % (M // Mc) != 0
            child = (Mc, M // Mc, lbc)
        lb = lower_profile(M, ex, child)
        W = W_of(M, lb); dl = delta(M); C = 1 - dl * W
        last = max(ex) if ex else 0
        print(f"M={M} exact through t={last} ({len(ex)} divisors)  delta={dl}  W>={W} ({float(W):.9f})  C<={C} ({float(C):.10f})")
        prev = (M, lb)
