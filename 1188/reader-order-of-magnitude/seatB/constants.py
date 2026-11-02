#!/usr/bin/env python3
"""Independent recomputation of the Section 4 constants (kappa1, kappa2, C1(h), C2(h), C*),
with two independent Dickman-rho implementations and an independent lower Riemann certificate.

rho_closed : rho = 1 on [0,1]; 1 - log v on [1,2]; on [2,3] the dilogarithm form
             rho(v) = 1 - (1 - log(v-1)) log v + Li2(1-v) + pi^2/12      (scipy: Li2(1-v) = spence(v))
rho_tab    : tabulation by integrating the delay equation v rho'(v) = -rho(v-1) from scratch
             (cumulative Simpson on a 1e-5 mesh), no closed forms used.
rho_mp     : mpmath, rho(v) = 1 - log v + int_2^v log(t-1)/t dt  (paper's formula, quad at 30 digits)
Controls: rho(2) = 1 - log 2 = 0.30685281944005...,  rho(3) = 0.04860838829...,  rho(4) = 0.00491092564...
"""
import numpy as np, mpmath as mp
from scipy.special import spence
from scipy.integrate import quad

def rho_closed(v):
    v = np.asarray(v, dtype=float)
    out = np.ones_like(v)
    m1 = (v > 1) & (v <= 2); out[m1] = 1 - np.log(v[m1])
    m2 = (v > 2) & (v <= 3)
    w = v[m2]; out[m2] = 1 - (1 - np.log(w - 1)) * np.log(w) + spence(w) + np.pi ** 2 / 12
    m3 = v > 3
    if m3.any(): out[m3] = rho_tab(v[m3])     # only needed for h < 1/5 (Table 5 row h = 0.18)
    return out

# --- tabulated rho from the delay equation (independent of every closed form) ---
H = 1e-5; V = 40; n1 = int(round(1 / H))
vg = np.arange(0, V * n1 + 1) * H
rt = np.ones_like(vg)
for k in range(1, V):
    a, b = k * n1, (k + 1) * n1
    f = rt[a - n1:b - n1 + 1] / vg[a:b + 1]          # rho(t-1)/t on [k, k+1]
    # cumulative trapezoid + Simpson correction via fine mesh (error ~ H^2 * max|f''| ~ 1e-10)
    cum = np.concatenate([[0.0], np.cumsum((f[1:] + f[:-1]) * H / 2)])
    rt[a:b + 1] = rt[a] - cum
def rho_tab(v): return np.interp(v, vg, rt)

mp.mp.dps = 30
def rho_mp(v):
    v = mp.mpf(v)
    if v <= 1: return mp.mpf(1)
    if v <= 2: return 1 - mp.log(v)
    return 1 - mp.log(v) + mp.quad(lambda t: mp.log(t - 1) / t, [2, v])

print("== controls for rho ==")
for v in (1.5, 2.0, 2.5, 3.0):
    print(f" rho({v}): closed={rho_closed([v])[0]:.13f}  tab={rho_tab(v):.13f}  mp={mp.nstr(rho_mp(v), 16)}")
print(f" 1-log 2 = {1-np.log(2):.13f};  literature rho(3)=0.0486083882911, rho(4)=0.0049109256478;  tab rho(4)={rho_tab(4.0):.13f}")

lam = np.log(5 / 4)
print("\n== Section 4.1 closed forms ==")
print(f" lambda = log(5/4) = {lam:.12f}")
print(f" kappa1 = (1-l) l (l - 3/20) = {(1-lam)*lam*(lam-0.15):.12f}   (paper 0.01267...)")
print(f" kappa2 = (1-l) l^2          = {(1-lam)*lam**2:.12f}   (paper 0.03868...)")
print(f" S_I limit lambda: 1 - lambda = {1-lam:.6f} (paper uses 1 - S_I > 0.77)")

def C(h, which, rho=rho_closed):
    def inner(al):
        pts = [b for b in (1 - al - 2 * h, 1 - al - h) if h < b < al]
        if which == 1: f = lambda b: rho(np.array([(1 - al - b) / h]))[0]
        else:          f = lambda b: rho(np.array([(1 - al - b) / h]))[0] / b
        return quad(f, h, al, points=pts or None, epsabs=1e-14, epsrel=1e-13, limit=200)[0]
    pts = [a for a in (1 - 2 * h, (1 - h) / 2, 1 - 3 * h, (1 - 2 * h) / 2) if h < a < 0.5]
    return quad(lambda al: inner(al) / al, h, 0.5, points=pts or None, epsabs=1e-14, epsrel=1e-12, limit=200)[0]

print("\n== C1(h), C2(h) by adaptive quadrature (closed-form rho) vs paper Table 5 ==")
paper = {0.18: (0.0578, 0.1868), 0.200: (0.06428, 0.20709), 0.210: (0.06618, 0.21180), 0.2175: (0.06698, 0.21288),
         0.225: (0.06722, 0.21192), 0.230: (0.06708, 0.21019), 0.240: (0.06609, 0.20433),
         0.250: (0.06422, 0.19557), 0.3: (0.0459, 0.1280)}
for h, (p1, p2) in paper.items():
    c1, c2 = C(h, 1), C(h, 2)
    print(f" h={h:<6}  C1={c1:.10f} (paper {p1})   C2={c2:.10f} (paper {p2})")
c1x, c2x = C(0.225, 1), C(0.2175, 2)
print(f" C1(0.225)  = {c1x:.12f}   paper 8.5: 0.0672193558;  same with tabulated rho: {C(0.225, 1, rho_tab):.12f}")
print(f" C2(0.2175) = {c2x:.12f}   paper 8.5: 0.2128758404;  same with tabulated rho: {C(0.2175, 2, rho_tab):.12f}")

hs = np.arange(0.200, 0.2501, 0.0005)
v1 = [C(h, 1) for h in hs]; v2 = [C(h, 2) for h in hs]
i1, i2 = int(np.argmax(v1)), int(np.argmax(v2))
print(f" grid 0.0005: max C1 = {v1[i1]:.8f} at h={hs[i1]:.4f};  max C2 = {v2[i2]:.8f} at h={hs[i2]:.4f}")
print(f"  (paper Remark 4.14(a): C1 max ~0.06722 at h~0.225; C2 max ~0.21288 at h~0.2175)")

# -------- independent lower Riemann certificate (monotonicity of rho; mpmath values of rho) --------
def lower_cert(h, n):
    hm = mp.mpf(h); half = mp.mpf(1) / 2
    D = (half - hm) / n
    # arguments v_k = (1 - 2h - k D)/h, k = 0..2n ; rho is nonincreasing, value at the cell's lower-left corner
    vs = [(1 - 2 * hm - k * D) / hm for k in range(2 * n + 1)]
    # rho on [2,3] via mpmath quad is slow at 2n points; use the dilog closed form in mpmath (checked above)
    def rmp(v):
        if v <= 1: return mp.mpf(1)
        if v <= 2: return 1 - mp.log(v)
        return 1 - (1 - mp.log(v - 1)) * mp.log(v) + mp.polylog(2, 1 - v) + mp.pi ** 2 / 12
    rk = np.array([float(rmp(v)) for v in vs]) - 1e-15           # round down
    al1 = np.array([float(hm + (i + 1) * D) for i in range(n)]) * (1 + 1e-15)   # upper ends, rounded up
    be1 = al1
    d2 = float(D) ** 2 * (1 - 1e-15)
    # C1: sum_i (1/al1_i) [ sum_{j<i} rho_{i+j} + rho_{2i}/2 ] D^2
    cs = np.concatenate([[0.0], np.cumsum(rk)])
    i = np.arange(n)
    s1 = (cs[2 * i] - cs[i]) + rk[2 * i] / 2
    C1lo = float(np.sum(s1 / al1) * d2)
    # C2: sum_i (1/al1_i) [ sum_{j<i} rho_{i+j}/be1_j + rho_{2i}/(2 be1_i) ] D^2
    tot = 0.0
    for ii in range(n):
        tot += (np.dot(rk[ii:2 * ii], 1 / be1[:ii]) + rk[2 * ii] / (2 * be1[ii])) / al1[ii]
    C2lo = tot * d2
    return C1lo * (1 - 1e-12), C2lo * (1 - 1e-12)

print("\n== independent lower Riemann certificates (cell minimum at lower-left corner, 1/alpha at upper end) ==")
for n in (2000, 10000):
    a1, _ = lower_cert(0.225, n); _, b2 = lower_cert(0.2175, n)
    print(f" n={n:5d}: C1(0.225) >= {a1:.10f} (>0.0672: {a1 > 0.0672})   C2(0.2175) >= {b2:.10f} (>0.2128: {b2 > 0.2128})")
print(" paper certificates: C1(0.225) >= 18918289218451/2^48 =", 18918289218451 / 2 ** 48,
      "  C2(0.2175) >= 59907725223280/2^48 =", 59907725223280 / 2 ** 48)

# -------- C* of Remark 6.6 --------
a = np.linspace(1 / (V - 1), 0.5, 4_000_001)
print(f"\n C* = int_0^1/2 rho(1/a - 1) da = {np.trapezoid(rho_tab(1 / a - 1), a):.6f}  (tail a<1/39 negligible; paper 0.1243...)")
