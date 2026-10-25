# Direct computation of the continuous boundary polynomials Q_e(r,2), Q_o(r,2) (paper §6.2, exponents in (1,2],
# admission r-x >= x+2 at upper nodes) by solving their recursion on a 2-D grid, then the signed correction integral I
# of (6.11) directly from l,u,f,F.  This route never uses the first-omission series (6.13).
# Controls: (a) admission switched off  => Q must equal the full product 1/2 and I_full must equal 8/3;
#           (b) admission threshold perturbed (x+2 -> x+2+eps) => I must move away from 8/3 - sum L_m.
import numpy as np, math, sys
from sieve_fns import build, A, EG

def boundary(h_inv, R=26.0, adm_shift=0.0, admission=True):
    M = h_inv; h = 1.0/M
    nr = int(R*M)+1
    xs = 1.0 + np.arange(M+1)*h                    # cutoff / exponent grid on [1,2]
    E = np.zeros((nr, M+1)); O = np.zeros((nr, M+1))
    rgrid = np.arange(nr)*h
    for lo in range(0, nr, M):                     # block of rows [lo, lo+M): children have gap index < lo
        hi = min(lo+M, nr)
        k = np.arange(lo, hi)[:, None]
        cidx = k - (M + np.arange(M+1))[None, :]   # child gap index (r - x)
        valid = cidx >= 0
        cc = np.where(valid, cidx, 0)
        tO = np.where(valid, O[cc, np.arange(M+1)[None, :]], 0.0)/xs[None, :]
        tE = np.where(valid, E[cc, np.arange(M+1)[None, :]], 0.0)/xs[None, :]
        r = rgrid[lo:hi][:, None]
        if admission:
            adm = (r - xs[None, :] >= xs[None, :] + 2.0 + adm_shift - 1e-12)
            tE = tE*adm
        def trap(t):
            cs = np.cumsum(t, axis=1)
            out = h*(cs - 0.5*t[:, :1] - 0.5*t)
            out[:, 0] = 0.0
            return out
        E[lo:hi] = 1.0 - trap(tO)
        O[lo:hi] = 1.0 - trap(tE)
    return rgrid, E[:, M], O[:, M]

def I_direct(h_inv, **kw):
    s, hs, f, F, rho = build(40, 20000)
    Ns = int(round(1/hs))
    rg, Qe, Qo = boundary(h_inv, **kw)
    M = h_inv
    y = rg/2 - 1                                   # r = 2y+2
    fy = np.interp(y+1, s, f); Fy = np.interp(np.maximum(y+1, 0.95), s, F)
    l = 2*Qe; u = 2*Qo
    me = y >= 1 - 1e-12; mo = y >= -1e-12
    def trapz(v, x):
        return float(np.sum((v[1:]+v[:-1])*(x[1:]-x[:-1])/2))
    Ie = trapz(((y**2-1)*(l-fy))[me], y[me])
    Io = trapz((y**2*(u-Fy))[mo], y[mo])
    return Ie - Io, Ie, Io, (y, l, u, fy, Fy)

if __name__ == "__main__":
    lam = math.log(2)
    L2 = -35/36 - lam**2 + 3*lam; L3 = 623/432 - 19/12*lam + lam**2/3
    print("full-product control (admission off):")
    for hinv in [200, 400]:
        I, Ie, Io, (y, l, u, fy, Fy) = I_direct(hinv, admission=False)
        print(f"  h=1/{hinv}: max|l-1|={np.max(np.abs(l[y>=1]-1)):.2e} max|u-1|={np.max(np.abs(u[y>=0]-1)):.2e}  I_full={I:.6f} (8/3={8/3:.6f})")
    res = {}
    for hinv in [200, 400, 800, 1600]:
        I, Ie, Io, data = I_direct(hinv)
        res[hinv] = I
        print(f"true rule h=1/{hinv}: I = {I:.8f}  (even part {Ie:.6f}, odd part {Io:.6f})")
        sys.stdout.flush()
    hs_ = sorted(res)
    for a, b in zip(hs_, hs_[1:]):
        print(f"  Richardson O(h) from 1/{a},1/{b}: {2*res[b]-res[a]:.8f}")
    for eps in [0.05, -0.05]:
        I, *_ = I_direct(800, adm_shift=eps)
        print(f"perturbed admission x+2{eps:+}: I = {I:.6f}")
    print(f"paper pieces: L1=1, L2={L2:.10f}, L3={L3:.10f}; 8/3-1-L2-L3 = {8/3-1-L2-L3:.8f}")
