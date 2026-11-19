from fractions import Fraction as F
import numpy as np
from common import *

t, s = phistar_breaks()
QA = Q_step(t, s)
print("route A (exact section-length integration, Fractions): Q(phi*) =", QA, " == -5/137 ?", QA == F(-5, 137))
# area sanity: area(R) must be 1/2; area of unit square pieces sums
print("  area(R) =", rect_area(F(0), F(1), F(0), F(1)))
for N in (548, 1096, 2192):
    K = grid_K(N)
    x = phistar_grid(N)
    QB = F(int(x @ K @ x), 4 * N * N)
    print(f"route B (grid formula via law of 2t-s, N={N}): Q(phi*) = {QB}; sum K/(4N^2) = {F(int(K.sum()),4*N*N)}")
# cross-check the two area routes on random rectangles
rng = np.random.default_rng(1)
N = 37
K = grid_K(N)
bad = 0
for _ in range(300):
    i, j = rng.integers(0, N, 2)
    a = rect_area(F(i, N), F(i + 1, N), F(j, N), F(j + 1, N))
    if a != F(int(K[i, j]), 4 * N * N):
        bad += 1
print("route A vs route B on 300 random cells (N=37): mismatches =", bad)

# KKT switching function G(a) = int_{(a,b) in R} phi*(b) db + int_{(b,a) in R} phi*(b) db
def Phi(x):  # cumulative integral of phi*
    x = F(x)
    tot = F(0)
    for i in range(12):
        lo, hi = t[i], t[i + 1]
        if x <= lo: break
        tot += s[i] * (min(x, hi) - lo)
    return tot
def Gsw(a):
    a = F(a)
    return Phi((1 + a) / 2) - Phi(a / 2) + Phi(min(F(1), 2 * a)) - Phi(max(F(0), 2 * a - 1))
# G is piecewise linear with kinks at points where a/2,(1+a)/2,2a,2a-1 hit breaks, or a=1/2
kinks = set(t)
for b in t:
    for p in (2 * b, 2 * b - 1, b / 2, (1 + b) / 2):
        if 0 <= p <= 1: kinks.add(p)
kinks.add(F(1, 2))
kinks = sorted(kinks)
worst = None
viol = []
for u, v in zip(kinks, kinks[1:]):
    mid = (u + v) / 2
    # sign of phi* on (u,v)
    k = max(i for i in range(12) if t[i] <= mid)
    sg = s[k]
    for p in (u, v):
        val = sg * Gsw(p)      # optimality needs phi*(a) G(a) <= 0
        if worst is None or val > worst[0]:
            worst = (val, p)
        if val > 0: viol.append((p, val))
print("KKT: max over a of phi*(a)*G(a) =", worst[0], "at a =", worst[1], " (<=0 required); #violating kink endpoints:", len(viol))
print("G at the 11 interior breakpoints:", [str(Gsw(b)) for b in t[1:-1]])
# margin: min |G| on interiors away from breaks, reported at kinks
print("Distinct G-values at kinks (first 12):", [str(Gsw(p)) for p in kinks[:12]])

# discrete counts
def twelve_block_col(n):
    assert n % 548 == 0
    r = n // 548
    col = []
    for idx, L in enumerate(BLOCKS):
        col += [1 if idx % 2 == 0 else -1] * (L * r)
    return col
for n, claim in ((548, 15756), (1096, 63568), (2192, 255368)):
    col = twelve_block_col(n)
    v = count_mono_brute(col)
    form = F(117 * n * n, 2192) - F(n, 2)
    W, T = ap_W(n) if n <= 1096 else (None, None)
    vq = (T + int(np.array(col) @ W @ np.array(col)) // 2) // 4 if W is not None else None
    print(f"n={n}: brute-force mono 3-APs = {v}, claimed {claim}, quadratic-form route = {vq}, 117n^2/2192 - n/2 = {form}")
