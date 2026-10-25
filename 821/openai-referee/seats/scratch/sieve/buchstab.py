# Direct numerical check of (7.18): int_{b1}^{1/2} D_a(1-a) da/a  vs  D_{b1}(1) - 1,
# with D_g(w) evaluated straight from its definition (7.15) by nested quadrature
# (NOT via the Buchstab recursion), plus comparison with Buchstab's omega via its DDE
# and with e^{-gamma}/b1 from (7.19).
import math, sys
from functools import lru_cache
from scipy.integrate import quad

EPS = float(__import__("os").environ.get("EPS","1e-9"))

def J(k, R, g):
    # integral over t_1..t_k >= g with sum <= R of 1/(R + g - sum t) * prod dt_i/t_i
    if k == 0:
        return 1.0/(R + g)
    if R < k*g - 1e-15:
        return 0.0
    hi = R - (k-1)*g
    val, err = quad(lambda t: J(k-1, R - t, g)/t, g, hi, epsabs=EPS, epsrel=EPS, limit=200)
    return val

def D(g, w):
    # (7.15): 1/w + sum_{l>=2} 1/l! * J(l-1, w-g, g)
    tot = 1.0/w
    l = 2
    while (l)*g <= w + 1e-15:      # term l nonzero only if l*g <= w
        tot += J(l-1, w - g, g)/math.factorial(l)
        l += 1
    return tot

def omega_table(umax, h=1e-4):
    # Buchstab omega: u*omega(u)=1 on [1,2]; (u omega(u))' = omega(u-1) for u>2
    import numpy as np
    n = int(round((umax-1)/h))+1
    u = 1 + h*np.arange(n)
    om = np.zeros(n)
    m1 = int(round(1/h))
    for i in range(n):
        if u[i] <= 2 + 1e-12:
            om[i] = 1.0/u[i]
    # integrate F(u)=u*omega(u): F(u) = F(2) + int_2^u omega(t-1) dt  (trapezoid)
    i2 = m1
    F = u[i2]*om[i2]
    for i in range(i2+1, n):
        F += 0.5*h*(om[i-1-m1] + om[i-m1])
        om[i] = F/u[i]
    return u, om

gammaE = 0.5772156649015329
u_tab, om_tab = omega_table(8.0)
def omega(uu):
    import numpy as np
    return float(np.interp(uu, u_tab, om_tab))

for b1 in [float(a) for a in sys.argv[1:]]:
    Db1 = D(b1, 1.0)
    pts = [p for p in (0.25, 1/3) if b1 < p < 0.5]
    rhs, err = quad(lambda a: D(a, 1-a)/a, b1, 0.5, points=pts or None, epsabs=1e-8, epsrel=1e-8, limit=200)
    print(f"b1={b1:.6f}: D_b1(1)={Db1:.10f}  D_b1(1)-1={Db1-1:.10f}  int_b1^1/2 D_a(1-a)da/a={rhs:.10f}  diff={rhs-(Db1-1):.2e} (quad err {err:.1e})")
    print(f"           omega(1/b1)/b1={omega(1/b1)/b1:.10f}   e^-gamma/b1={math.exp(-gammaE)/b1:.10f}   D_b1(1)-e^-g/b1={Db1-math.exp(-gammaE)/b1:.3e}")
