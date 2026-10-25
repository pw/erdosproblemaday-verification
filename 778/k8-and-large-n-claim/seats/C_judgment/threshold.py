#!/usr/bin/env python3
"""Explicit n_0 from the paper's OWN stated bounds (Didin-Pimenov, (1:2) clique game).

Work in x = ln n (real). Conditions at n = e^x, paper's constants:
  a   = ceil(2 log_3 n) + 2
  l   = ceil(C ln n)                      (C fixed, C*eta > 2)   -- variant FIXED_C
      or the least integer l making Phi<1  -- variant BEST_L (C may depend on scale)
  SQ  = 3^(1 - a/2)                       (paper's bound on sum Q_A)
  SP  = (6/5) * (n * theta^((l-1)/2))^l   (paper's bound on sum P_U, binom(n,l) <= n^l)
  Phi condition: SQ + SP < 1
  R   = 1 + floor( log_{5/3}((n+3/2)/(l+3/2)) )
  win condition: R > a - 1  (i.e. R >= a)
n_0 = e^{x*}, x* = sup of the x where the conjunction FAILS (scan + breakpoint checks).
Also: variant with binom(n,l) <= n^l / l!  (slack inside the paper's own bound).
"""
import math, sys
import numpy as np

LN3 = math.log(3); LN53 = math.log(5/3)
theta = (4/3)**0.6 * (5/6)
eta = -math.log(theta)

def conds(x, lvec_fn, use_factorial=False):
    a = np.ceil(2*x/LN3) + 2
    l = lvec_fn(x, a)
    SQ = 3.0**(1 - a/2)
    logSP = math.log(6/5) + l*(x - eta*(l-1)/2)
    if use_factorial:
        from scipy.special import gammaln
        logSP = logSP - gammaln(l+1)
    SP = np.exp(np.minimum(logSP, 50))
    phi_ok = (SQ + SP) < 1
    # n + 3/2 ~ n at these scales; use log1p for honesty
    R = 1 + np.floor((x + np.log1p(1.5*np.exp(-x)) - np.log(l + 1.5)) / LN53)
    win_ok = R >= a
    return phi_ok, win_ok, a, l, R

def fixed_C(C):
    return lambda x, a: np.ceil(C*x)

def best_l(use_factorial=False):
    def f(x, a):
        SQ = 3.0**(1 - a/2)
        c0 = np.log(5*(1 - SQ)/6)           # need l*(x+eta/2) - eta l^2/2 < c0
        if not use_factorial:
            B = x + eta/2
            lstar = (B + np.sqrt(B*B - 2*eta*c0)) / eta
            return np.floor(lstar) + 1
        # with l! : solve numerically by bisection on integer l (vectorised crude)
        from scipy.special import gammaln
        lo = np.ones_like(x); hi = np.full_like(x, 1e7)
        for _ in range(60):
            mid = np.floor((lo + hi)/2)
            ok = (mid*(x + eta/2) - eta*mid*mid/2 - gammaln(mid+1)) < c0
            # ok region is l large; find least l with ok and l beyond the hump
            hi = np.where(ok & (mid > x/eta*0.5), mid, hi)
            lo = np.where(ok & (mid > x/eta*0.5), lo, mid)
        return hi
    return f

def last_failure(lfn, x_lo=20.0, x_hi=400.0, step=2e-5, use_factorial=False):
    xs = np.arange(x_lo, x_hi, step)
    phi_ok, win_ok, a, l, R = conds(xs, lfn, use_factorial)
    ok = phi_ok & win_ok
    bad = np.where(~ok)[0]
    if len(bad) == 0:
        return None, None
    i = bad[-1]
    first_good = np.where(ok)[0]
    return xs[i], (xs[first_good[0]] if len(first_good) else None)

def fmt(x):
    if x is None: return "none"
    return f"ln n = {x:.3f}  =>  n ~ 10^{x/math.log(10):.2f} = 3^{x/LN3:.2f}"

if __name__ == "__main__":
    print(f"theta = {theta:.10f}   eta = -ln theta = {eta:.10f}   2/eta = {2/eta:.4f}")
    print(f"theta^5 = {theta**5:.10f}  vs 6250/6561 = {6250/6561:.10f}")
    print(f"leading consts: 1/ln(5/3) = {1/LN53:.6f}, 2/ln3 = {2/LN3:.6f}, gap = {1/LN53-2/LN3:.6f}")
    print(f"kappa = log_3(27/25) = {math.log(27/25)/LN3:.6f}")
    print(f"Lean threshold 3^158: ln n = {158*LN3:.3f}, n ~ 10^{158*LN3/math.log(10):.2f}")
    print()
    print("Variant BEST_L (least admissible l at each n, paper's n^l bound):")
    xb, xg = last_failure(best_l())
    print("  last failure  :", fmt(xb)); print("  first success :", fmt(xg))
    print()
    print("Variant FIXED_C (l = ceil(C ln n)), paper's n^l bound:")
    best = None
    for C in [206.0, 206.5, 207, 208, 210, 212, 215, 220, 227.6, 230, 240, 250, 300]:
        if C*eta <= 2:
            print(f"  C={C:7.2f}: C*eta={C*eta:.4f} <= 2, inadmissible"); continue
        xb, xg = last_failure(fixed_C(C))
        print(f"  C={C:7.2f} (C*eta={C*eta:.4f}): last failure {fmt(xb)}")
        if xb is not None and (best is None or xb < best[1]): best = (C, xb)
    print("  best C in grid:", best[0], fmt(best[1]))
    # finer C search
    Cs = np.arange(206.0, 260.0, 0.25)
    res = []
    for C in Cs:
        if C*eta <= 2: continue
        xb, _ = last_failure(fixed_C(C), step=1e-4)
        res.append((xb, C))
    res.sort()
    print("  finer search best C =", res[0][1], fmt(res[0][0]))
    print()
    try:
        import scipy  # noqa
        print("Slack check: BEST_L with binom(n,l) <= n^l / l!:")
        xb, xg = last_failure(best_l(True), use_factorial=True, step=1e-4)
        print("  last failure  :", fmt(xb))
    except ImportError:
        print("scipy missing; skip l! variant")
    # report the numbers at the threshold
    print()
    for x in [res[0][0]+1e-3]:
        phi_ok, win_ok, a, l, R = conds(np.array([x]), fixed_C(res[0][1]))
        print(f"at x={x:.3f}: a={int(a[0])}, l={int(l[0])}, R={int(R[0])}, phi_ok={phi_ok[0]}, win_ok={win_ok[0]}")
