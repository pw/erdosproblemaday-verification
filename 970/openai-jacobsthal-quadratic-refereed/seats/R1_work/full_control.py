# Control (a) redone correctly: with admission OFF the cutoff-2 polynomial is the full product over exponents in (1,2],
# which must equal 1/2 at every gap -- provided negative gaps are allowed (the full product has no gap constraint).
# Grid offset: gaps from -G0.  Then I_full from the same quadrature must be 8/3.
import numpy as np, math
from sieve_fns import build
def boundary_full(M, R=26.0, G0=30.0):
    h = 1.0/M; off = int(G0*M); nr = int(R*M)+off+1
    xs = 1.0 + np.arange(M+1)*h
    E = np.zeros((nr, M+1)); O = np.zeros((nr, M+1))
    E[:M] = 1.0; O[:M] = 1.0   # lowest rows: treat as leaves (their children are below the window); negligible weight
    for lo in range(M, nr, M):
        hi = min(lo+M, nr); k = np.arange(lo, hi)[:, None]
        cidx = k - (M + np.arange(M+1))[None, :]
        tO = O[cidx, np.arange(M+1)[None, :]]/xs; tE = E[cidx, np.arange(M+1)[None, :]]/xs
        def trap(t):
            cs = np.cumsum(t, axis=1); out = h*(cs - 0.5*t[:, :1] - 0.5*t); out[:, 0] = 0; return out
        E[lo:hi] = 1 - trap(tO); O[lo:hi] = 1 - trap(tE)
    rg = (np.arange(nr)-off)*h
    return rg, E[:, M], O[:, M]
s, hs, f, F, rho = build(40, 20000)
for M in [200, 400]:
    rg, Qe, Qo = boundary_full(M)
    sel = rg >= 0
    print(f"h=1/{M}: max|2Qe-1| on r>=0: {np.max(np.abs(2*Qe[sel]-1)):.2e}, max|2Qo-1|: {np.max(np.abs(2*Qo[sel]-1)):.2e}")
    y = rg[sel]/2-1; l = 2*Qe[sel]; u = 2*Qo[sel]
    fy = np.interp(y+1, s, f); Fy = np.interp(np.maximum(y+1, .95), s, F)
    me = y >= 1-1e-12; mo = y >= -1e-12
    tr = lambda v, x: float(np.sum((v[1:]+v[:-1])*np.diff(x)/2))
    print(f"   I_full = {tr(((y**2-1)*(l-fy))[me], y[me]) - tr((y**2*(u-Fy))[mo], y[mo]):.8f}  (8/3 = {8/3:.8f})")
