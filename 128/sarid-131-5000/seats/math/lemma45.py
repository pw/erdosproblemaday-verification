# Independent route for Lemma 4.5: brute 2-D grid over the true domain, exact-rational re-evaluation,
# scipy local refinement, and the balancing-rho remark.  (seat MATH)
import numpy as np
from fractions import Fraction as Fr
from scipy.optimize import minimize, brentq, minimize_scalar

I0 = 2/47
def Lf(a):
    ah = np.minimum(a, 1-a)
    return np.minimum(4*ah**2, ah*(1-ah))
def F(a, mu, r0=7/22, I0=I0):
    c = 1-a
    P = a*r0/2 + c*I0
    return np.minimum(P - (1+a)/(4*c)*mu, mu/4) - Lf(a)/c**2*mu**3

N = 2000
a = np.linspace(0, 0.5, N+1)[:,None]
t = np.linspace(0, 1, N+1)[None,:]
mu = t*4*I0*(1-a)**2          # mu ranges over [0, 4 I0 c^2] for each a
V = F(a, mu)
i, j = np.unravel_index(np.argmax(V), V.shape)
amax, mumax = a[i,0], mu[i,j]
print(f"grid {N+1}x{N+1}: max F = {V[i,j]:.10f} at a={amax:.6f} mu={mumax:.6f} (mu/cap={t[0,j]:.4f})")
print(f"  88/417 = {88/417:.6f}; mu* = {18424/173889:.6f}")
# exact rational evaluation at the grid argmax
def Fexact(a, mu, r0=Fr(7,22), I0=Fr(2,47)):
    c = 1-a; P = a*r0/2 + c*I0
    ah = min(a,1-a); L = min(4*ah*ah, ah*(1-ah))
    return min(P - (1+a)/(4*c)*mu, mu/4) - L/c**2*mu**3
ae = Fr(int(i), 2*N); mue = Fr(int(j), N)*4*Fr(2,47)*(1-ae)**2
print("  exact F at grid argmax:", float(Fexact(ae, mue)), " < 131/5000:", Fexact(ae,mue) < Fr(131,5000))
# exact rational on a coarser exact grid (200x200) -- every point
worst = Fr(-1); arg=None
for ii in range(0, 201):
    ax = Fr(ii, 400)
    cap = 4*Fr(2,47)*(1-ax)**2
    for jj in range(0, 201):
        v = Fexact(ax, cap*Fr(jj,200))
        if v > worst: worst, arg = v, (ax, jj)
print("exact-rational 201x201 grid: max F =", float(worst), "at a =", arg[0], "mu/cap =", arg[1]/200, " <131/5000:", worst < Fr(131,5000))
# scipy refinement from the grid max (Nelder-Mead on the nonsmooth min)
def neg(x):
    aa, tt = x
    if not (0 <= aa <= 0.5 and 0 <= tt <= 1): return 1.0
    return -F(np.array(aa), np.array(tt)*4*I0*(1-aa)**2)
best = None
for x0 in [(amax, t[0,j]), (0.2, 0.9), (0.3, 1.0), (0.1, 0.5), (0.45, 1.0), (0.21, 0.999)]:
    r = minimize(neg, x0, method='Nelder-Mead', options=dict(xatol=1e-12, fatol=1e-15, maxiter=20000))
    if best is None or r.fun < best.fun: best = r
print(f"scipy NM: max F = {-best.fun:.12f} at a={best.x[0]:.8f} mu/cap={best.x[1]:.8f}")
# envelope check: for each a the inner max over mu by dense 1-D search equals min(nu, cap)
errs = []
for aa in np.linspace(0, 0.5, 501):
    cap = 4*I0*(1-aa)**2
    m = np.linspace(0, cap, 200001)
    v = F(np.array(aa), m)
    nu = 2*(1-aa)*(aa*(7/22)/2 + (1-aa)*I0)
    errs.append(abs(m[np.argmax(v)] - min(nu, cap)))
print("max |argmax_mu - min(nu,cap)| over 501 a-values:", max(errs))
# the min-ordering sentence: 'the first exceeding the second for mu > nu(a)'
aa = 0.15; c=1-aa; P = aa*(7/22)/2 + c*I0; nu = 2*c*P
for muv in [0.5*nu, 1.5*nu]:
    first = P - (1+aa)/(4*c)*muv; second = muv/4
    print(f"a={aa}: mu={'<' if muv<nu else '>'}nu : first={first:.5f} second={second:.5f}  first>second? {first>second}")

# ---- balancing remark: high bound H(r)=r/8-r^2/4+gamma/4 vs low-density max M(r)
gamma = 3/64 + 1/5e10
def M(r0):
    def negF(x):
        aa, tt = x
        if not (0 <= aa <= 0.5 and 0 <= tt <= 1): return 1.0
        return -F(np.array(aa), np.array(tt)*4*I0*(1-aa)**2, r0=r0)
    aa = np.linspace(0, 0.5, 1001)[:,None]; tt = np.linspace(0,1,1001)[None,:]
    VV = F(aa, tt*4*I0*(1-aa)**2, r0=r0)
    k, l = np.unravel_index(np.argmax(VV), VV.shape)
    r = minimize(negF, (aa[k,0], tt[0,l]), method='Nelder-Mead', options=dict(xatol=1e-12, fatol=1e-16, maxiter=20000))
    return max(-r.fun, VV[k,l])
H = lambda r: r/8 - r*r/4 + gamma/4
for r in [0.30, 0.31, 7/22, 0.3184, 0.32, 0.33]:
    print(f"rho0={r:.5f}: high H={H(r):.8f}  low M={M(r):.8f}")
rb = brentq(lambda r: H(r) - M(r), 0.30, 0.33, xtol=1e-12)
print(f"balancing rho = {rb:.6f}, value = {H(rb):.8f}; cost of splitting at 7/22: max(H,M)(7/22) - value = {max(H(7/22),M(7/22))-H(rb):.3e};"
      f" cost of stating 131/5000: {131/5000 - H(rb):.3e}")
