# Check 3: the circle-measure Fourier decay used in Lemma 6.2 and the o(sqrt|h|) estimate (6.3).
#  (a) sigma^(r) = (1/2pi) int exp(i r cos t) dt = J0(r); sup_r |J0(r)|(1+r)^{1/2} bounded.  CONTROL: exponent 1 (unbounded).
#  (b) multiplier m_h(xi) = min(h^2 xi^2,4)/((1+xi) h) is uniformly bounded.  CONTROL: no circle decay -> min(h^2xi^2,4)/h.
#  (c) (6.3) for g = indicator of the disk of radius rho0: ||S(g-g(.+h))||_L2/sqrt(h) -> 0;
#      CONTROL without the circle average S: ||g-g(.+h)||_L2/sqrt(h) -> sqrt(4 rho0) (does NOT go to 0).
#      Positive control on the Fourier formula: the no-S value is checked against the exact lens-area formula,
#      and the S-value at h=0.1 is checked against a direct real-space grid computation.
import numpy as np
from scipy.special import j0, j1
# (a)
for r in (0.0, 5.0, 50.0, 500.0):
    tt = np.linspace(0, 2*np.pi, 200001)[:-1]
    q = np.mean(np.exp(1j*r*np.cos(tt))).real
    print(f"quadrature sigma^({r}) = {q:+.10f}   J0 = {j0(r):+.10f}")
r = np.linspace(0, 2e5, 4_000_001)
A = np.abs(j0(r))
print("sup |J0(r)|(1+r)^0.5 on [0,2e5] = %.4f" % np.max(A*np.sqrt(1+r)), "(asymptotic sqrt(2/pi)=%.4f)" % np.sqrt(2/np.pi))
for R in (1e2, 1e3, 1e4, 2e5):
    m = r <= R
    print(f"  CONTROL sup_(r<={R:g}) |J0(r)|(1+r)^1 = {np.max(A[m]*(1+r[m])):.1f}")
del r, A
# (b)
xi = np.logspace(-6, 10, 200001)
for h in (1e-1, 1e-3, 1e-6):
    m = np.minimum(h*h*xi*xi, 4)/((1+xi)*h)
    mc = np.minimum(h*h*xi*xi, 4)/h
    print(f"h={h:g}: sup multiplier = {m.max():.3f};  CONTROL (no decay) sup = {mc.max():.3g}")
# (c)
rho0 = 1.5
def fourier_norm2(h, with_S, K=3e5, dk=0.02):   # neglected tail <= 1/(pi*rho0*K) ~ 7e-7
    tot = 0.0; start = dk/2; block = 1_000_000          # chunked: keeps RSS ~ 50 MB
    while start < K:
        k = start + dk*np.arange(block); k = k[k < K]
        base = (j1(rho0*k))**2 * (1 - j0(h*k)) / k
        if with_S: base = base * j0(k)**2
        tot += base.sum()*dk; start = k[-1] + dk
    return 4*np.pi*rho0**2 * tot
def lens_sym_diff(h):
    lens = 2*rho0**2*np.arccos(h/(2*rho0)) - (h/2)*np.sqrt(4*rho0**2 - h*h)
    return 2*(np.pi*rho0**2 - lens)
print("\n  h       ||g-g(.+h)||^2 Fourier   exact |D Δ (D-h)|   CONTROL ratio ||g-g(.+h)||/sqrt h    ||S(g-g(.+h))||/sqrt h")
for h in (0.1, 0.03, 0.01, 0.003, 0.001):
    n0 = fourier_norm2(h, False); nS = fourier_norm2(h, True)
    print(f"{h:<7} {n0:>16.6f} {lens_sym_diff(h):>20.6f} {np.sqrt(n0/h):>28.4f} {np.sqrt(nS/h):>28.5f}")
print("sqrt(4*rho0) =", np.sqrt(4*rho0))
# real-space cross-check of the S-version at h = 0.1: S g is radial, Sg(q) = 1 - arccos(c)/pi, c = (rho0^2-|q|^2-1)/(2|q|)
def Sg(z):
    rr = np.abs(z); c = np.clip((rho0**2 - rr**2 - 1)/(2*np.maximum(rr, 1e-12)), -1, 1)
    return 1 - np.arccos(c)/np.pi
h = 0.1; dx = 0.0025; tot = 0.0
xs = np.arange(-2.7, 2.7 + dx/2, dx)
for x0 in np.array_split(xs, 20):
    X, Y = np.meshgrid(x0, xs, indexing="ij"); Z = X + 1j*Y
    tot += np.sum((Sg(Z) - Sg(Z + h))**2)*dx*dx
print(f"real-space grid ||S(g-g(.+0.1))||^2 = {tot:.6f}   vs Fourier formula {fourier_norm2(0.1, True):.6f}")
