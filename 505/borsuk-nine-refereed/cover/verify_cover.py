#!/usr/bin/env python3
"""EXACT rational certificate that n lines c_1..c_n in R^4 have covering radius < 45 degrees in RP^3.
Input: JSON with float centres. Step 1: replace each centre by a nearby EXACT rational unit vector (inverse stereographic
projection of a rational point, denominators ~DEN). Step 2: the polytope P = {x : <x,c_i>^2 <= 1/2 for all i} is bounded
(the c_i span R^4) and equals the hull of its vertices; every vertex solves <x,c_j> = s_j/sqrt2 for 4 independent c_j, i.e.
x = C_J^{-1} s / sqrt2 with s in {+-1}^4, so |x|^2 = |C_J^{-1}s|^2/2 and feasibility <x,c_l>^2 <= 1/2 <=> (c_l . C_J^{-1}s)^2 <= 1
-- all rational. M := max |x|^2 over feasible vertices. If M < 1, every unit x has max_i <x,c_i>^2 >= 1/(2M) > 1/2 (else
x*sqrt(1/(2t)) would be a point of P of norm^2 1/(2t) > M). Exit 0 iff M < 1. Pure Fractions, no floats in the decision."""
import json, sys, itertools as it
from fractions import Fraction as Fr
DEN = 10**6
def rational_unit(v):
    # inverse stereographic projection from whichever pole is far from v (keeps denominators tame)
    import math
    n = math.sqrt(sum(a*a for a in v)); v = [a / n for a in v]
    sgn = -1 if v[3] > 0 else 1                     # project from pole (0,0,0,sgn)
    t = [Fr(round(v[k] / (1 - sgn * v[3]) * DEN), DEN) for k in range(3)]
    q = sum(a*a for a in t)
    x = [2*a/(q+1) for a in t] + [sgn*(q-1)/(q+1)]
    assert sum(a*a for a in x) == 1
    return x
def solve4(A, b):
    """Gaussian elimination over Fractions; returns None if singular."""
    M = [row[:] + [bb] for row, bb in zip(A, b)]
    for c in range(4):
        p = next((r for r in range(c, 4) if M[r][c] != 0), None)
        if p is None: return None
        M[c], M[p] = M[p], M[c]
        for r in range(4):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [a - f*b2 for a, b2 in zip(M[r], M[c])]
    return [M[r][4] / M[r][r] for r in range(4)]
def certify(C):
    n = len(C); best = Fr(0); arg = None; nfeas = 0
    for J in it.combinations(range(n), 4):
        A = [C[j] for j in J]
        for s in it.product((1, -1), repeat=4):
            if s[0] == -1: continue                    # P is centrally symmetric: vertex for -s is -x
            y = solve4(A, [Fr(si) for si in s])         # y = C_J^{-1} s ; vertex x = y/sqrt2
            if y is None: break
            if all(sum(a*b for a, b in zip(c, y))**2 <= 1 for c in C):
                nfeas += 1
                m = sum(a*a for a in y) / 2
                if m > best: best, arg = m, (J, s)
    return best, arg, nfeas
if __name__ == '__main__':
    d = json.load(open(sys.argv[1]))
    C = [rational_unit(v) for v in d['centres']]
    import math
    assert all(abs(float(a) - b / math.sqrt(sum(z*z for z in v))) < 1e-5 for v, c in zip(d['centres'], C) for a, b in zip(c, v)), 'rounding moved a centre'
    M, arg, nfeas = certify(C)
    print(f'n={len(C)} feasible vertices (up to sign)={nfeas}  M = max|v|^2 = {float(M):.12f}')
    if M < 1:
        mu = 1 / (2*M); cos2rho = 2*mu - 1   # cos(2 rho) = 2cos^2 rho - 1 >= 1/M - 1
        print(f'CERTIFIED: every line is within angle rho of some centre, cos^2(rho) >= 1/(2M) = {float(mu):.12f}, rho <= {math.degrees(math.acos(math.sqrt(float(mu)))):.6f} deg')
        print(f'each cap {{x : <x,c_i>^2 >= 1/(2M)}} has Frobenius diameter^2 <= 2 - 2(1/M - 1)^2 = {float(2 - 2*(1/M - 1)**2):.12f} < 2')
        json.dump({'centres_rational': [[str(a) for a in c] for c in C], 'M': str(M), 'argmax': [list(arg[0]), list(arg[1])]}, open(sys.argv[1].replace('.json', '.cert.json'), 'w'))
        sys.exit(0)
    print('NOT CERTIFIED: covering radius >= 45 deg for this configuration (M >= 1)'); sys.exit(1)
