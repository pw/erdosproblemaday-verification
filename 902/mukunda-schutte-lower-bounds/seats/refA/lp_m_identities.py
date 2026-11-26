"""Decorrelated cross-check of Theorem 8.2: an LP over the k-distributions of a
DRT(51) using ONLY the moment identities (M0),(M2),(M3),(M4) (with D+ >= 0, i.e.
k <= 12 - sigma). With the lower bound k >= b, is the LP feasible?
Positive control: b = 1 must be feasible (real DRT(51)s with min k = 1 exist).
Also: exact Farkas check of the paper's combination at b = 5.
"""
from math import comb
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog


def lp(b, t=12):
    n = 4 * t + 3
    ntr = n * comb(2 * t + 1, 2)
    ncy = comb(n, 3) - ntr
    s_tr = n * (2 * t + 1) * comb(t, 2)
    s_cy = n * (comb(2 * t + 1, 3) - (2 * t + 1) * comb(t, 2))
    m3 = comb(n, 2) * comb(t, 3)
    var = [(1, k) for k in range(b, t - 1 + 1)] + [(0, k) for k in range(b, t + 1)]
    if not var:
        return 'no variables'
    Aeq, beq = [], []
    Aeq.append([1 if s == 1 else 0 for s, k in var]); beq.append(ntr)
    Aeq.append([1 if s == 0 else 0 for s, k in var]); beq.append(ncy)
    Aeq.append([k if s == 1 else 0 for s, k in var]); beq.append(s_tr)
    Aeq.append([k if s == 0 else 0 for s, k in var]); beq.append(s_cy)
    Aeq.append([comb(k, 2) for s, k in var]); beq.append(m3)
    Aeq.append([comb(k, 3) - comb(t - s - k, 3) for s, k in var]); beq.append(0)
    r = linprog(np.zeros(len(var)), A_eq=np.array(Aeq, float), b_eq=np.array(beq, float),
                bounds=[(0, None)] * len(var), method='highs')
    return {0: 'FEASIBLE', 2: 'INFEASIBLE'}.get(r.status, f'status {r.status}')


for t in [12]:
    for b in range(0, 8):
        print(f"t={t} (n={4*t+3}) lower bound k>={b}: LP {lp(b, t)}")
for t, b in [(14, 5), (16, 5), (16, 6), (11, 5), (11, 4)]:
    print(f"t={t} (n={4*t+3}) lower bound k>={b}: LP {lp(b, t)}")

# Exact replay of the paper's argument at t=12, b=5, in Fractions
t = 12
vals = []
for s, mean, L in [(1, F(11, 2), 11), (0, F(6), 12)]:
    a = F(L, 2) - 1
    for k in range(5, L + 1):
        u = F(k) - mean
        lhs = F(comb(k, 3) - comb(L - k, 3))
        rhs = (u ** 3 + (3 * a * a - 1) * u) / 3
        assert lhs == rhs, (s, k)
        g = u ** 3 - (u / 4 if s == 1 else u)
        vals.append((s, k, g))
print("identity C(k,3)-C(L-k,3) = (u^3+(3a^2-1)u)/3 holds for all k in range: True")
print("g(k) = u^3-u/4 (trans) / u^3-u (cyc) for k>=5:", [(('tr' if s else 'cy'), k, str(g)) for s, k, g in vals])
p = F(280500 - 274125)
print("forced p =", p, " vs 5525/2 =", F(5525, 2), " contradiction:", p > F(5525, 2))
print("check 7650*25+15*5525 =", 7650 * 25 + 15 * 5525)
