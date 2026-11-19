"""First- and second-order local checks at phi* (exact Fractions)."""
from fractions import Fraction as F
import random
from common import phistar_breaks, Q_step
t, s = phistar_breaks()
def Phi(x):
    tot = F(0)
    for i in range(12):
        if x <= t[i]: break
        tot += s[i] * (min(x, t[i + 1]) - t[i])
    return tot
def G(a): return Phi((1 + a) / 2) - Phi(a / 2) + Phi(min(F(1), 2 * a)) - Phi(max(F(0), 2 * a - 1))
kinks = set(t)
for b in t:
    for p in (2 * b, 2 * b - 1, b / 2, (1 + b) / 2):
        if 0 <= p <= 1: kinks.add(p)
kinks.add(F(1, 2)); kinks = sorted(kinks)
interior_zeros = []; zero_intervals = []
for u, v in zip(kinks, kinks[1:]):
    if G(u) == 0 and G(v) == 0: zero_intervals.append((u, v))
for p in kinks:
    if G(p) == 0 and p not in t: interior_zeros.append(p)
print("kinks:", len(kinks), " intervals where G == 0 identically:", zero_intervals)
print("isolated zeros of G strictly inside blocks (548ths):", [p * 548 for p in interior_zeros])
# margin away from breakpoints: min over kinks of |G| excluding zeros
print("smallest nonzero |G| at kinks:", min(abs(G(p)) for p in kinks if G(p) != 0))
# second order in breakpoint space: Q(t* + eps v) - Q(t*) for random integer directions v, eps = 1/10^5
Q0 = Q_step(t, s); random.seed(1)
eps = F(1, 10 ** 5); worst = None; neg = 0; dirs = 0
D = [[1 if j == i else 0 for j in range(11)] for i in range(11)] + [[-1 if j == i else 0 for j in range(11)] for i in range(11)]
D += [[random.randint(-5, 5) for _ in range(11)] for _ in range(150)]
for v in D:
    tt = [t[0]] + [t[i + 1] + eps * v[i] for i in range(11)] + [t[12]]
    dq = Q_step(tt, s) - Q0; dirs += 1
    r = dq / (eps * eps * max(1, sum(x * x for x in v)))
    if worst is None or r < worst: worst = r
    if dq < 0: neg += 1
print(f"breakpoint-space 2nd order: {dirs} directions, #with Q decrease = {neg}, min (dQ/eps^2/|v|^2) = {float(worst):.5f}")
# two-cell insertions at (p,p') with opposite colours at the isolated interior zeros
print("Q* =", Q0)
