# End-to-end continuous-model check of the B^{-2} boundary contribution (paper (6.10)-(6.11), Prop 6.3), by a route that
# uses NO regeneration/renewal theory: propagate the cutoff-2 anomaly delta_i through exponents x>2 by solving
#   Phi_e(r,b) = delta_e(r) - int_2^b Phi_o(r-x,x) dx/x ,   Phi_o(r,b) = delta_o(r) - int_2^b 1{r-x>=2x} Phi_e(r-x,x) dx/x
# on a 2-D grid, and compare  T(s,B) = (s^2 B^2/phi_e(s)) Phi_e(sB,B)  with the paper's limit 2I/M_g (Prop 4.5 + 5.5(iv)).
# Second, independent check of the decomposition itself: solve the FULL continuous reference recursion Q_e(r,b)
# (exponents in (1,b], admission r-x >= max(2x,x+2)) directly and compare Q_e(sB,B) - f_i(s)/B with Phi_e(sB,B).
import numpy as np, math, sys
from sieve_fns import build, A, EG
from boundary_I import boundary
s_, hs, f, F, rho = build(60, 20000)
fe = lambda x: np.where(x >= 2, np.interp(x, s_, f), A*np.log(np.maximum(x-1, 1e-300))/x)   # f with starting extension
Fi = lambda x: np.where(x >= 1, np.interp(np.maximum(x, 1), s_, F), A/np.maximum(x, 1e-300))
a = 1-f; c = F-1
def phi_e(x):
    x = np.asarray(x, float)
    ordinary = x*(np.interp(x, s_, a) + np.interp(np.maximum(x-1, 0), s_, c))
    ext = A*(x/(x-1) - np.log(x-1))
    return np.where(x >= 2, ordinary, ext)

# anomalies on a fine r grid (Richardson-extrapolated in the boundary mesh)
rg8, Qe8, Qo8 = boundary(800, R=40.0)
rg4, Qe4, Qo4 = boundary(400, R=40.0)
Qe = 2*Qe8[::2] - Qe4; Qo = 2*Qo8[::2] - Qo4; rgb = rg4
de = np.where(rgb >= 4, Qe - 0.5*np.interp(rgb/2, s_, f), 0.0)
do = np.where(rgb >= 2, Qo - 0.5*np.interp(np.maximum(rgb/2, 1), s_, F), 0.0)
print("anomaly samples: delta_e(4,6,10) =", [f"{np.interp(r, rgb, de):.3e}" for r in (4, 6, 10)],
      " delta_o(2,4,10) =", [f"{np.interp(r, rgb, do):.3e}" for r in (2, 4, 10)])
sys.stdout.flush()
I_ref = 0.3593435; Mg = 4.56458616
target = 2*I_ref/Mg
print(f"target 2I/M_g = {target:.6f}")

def propagate(hinv, Bmax, smax=2.32):
    h = 1.0/hinv; nb = int(round((Bmax-2)*hinv))+1; nr = int(round(smax*Bmax*hinv))+1
    xs = 2.0 + np.arange(nb)*h; rr = np.arange(nr)*h
    dE = np.interp(rr, rgb, de, right=0.0); dO = np.interp(rr, rgb, do, right=0.0)
    PE = np.zeros((nr, nb)); PO = np.zeros((nr, nb))
    w = 2*hinv
    for lo in range(0, nr, w):
        hi = min(lo+w, nr); k = np.arange(lo, hi)[:, None]
        cidx = k - (w + np.arange(nb))[None, :]
        valid = cidx >= 0; cc = np.where(valid, cidx, 0)
        tO = np.where(valid, PO[cc, np.arange(nb)[None, :]], 0.0)/xs
        tE = np.where(valid, PE[cc, np.arange(nb)[None, :]], 0.0)/xs
        r = rr[lo:hi][:, None]
        tE = tE*(r - xs >= 2*xs - 1e-12)
        def trap(t):
            cs = np.cumsum(t, axis=1); out = h*(cs - 0.5*t[:, :1] - 0.5*t); out[:, 0] = 0; return out
        PE[lo:hi] = dE[lo:hi, None] - trap(tO)
        PO[lo:hi] = dO[lo:hi, None] - trap(tE)
    return rr, xs, PE

def direct_Q(hinv, Bmax, smax=2.32):
    # full continuous reference polynomial, exponents in (1,b]
    h = 1.0/hinv; nb = int(round((Bmax-1)*hinv))+1; nr = int(round(smax*Bmax*hinv))+1
    xs = 1.0 + np.arange(nb)*h; rr = np.arange(nr)*h
    E = np.zeros((nr, nb)); O = np.zeros((nr, nb)); w = hinv
    for lo in range(0, nr, w):
        hi = min(lo+w, nr); k = np.arange(lo, hi)[:, None]
        cidx = k - (w + np.arange(nb))[None, :]
        valid = cidx >= 0; cc = np.where(valid, cidx, 0)
        tO = np.where(valid, O[cc, np.arange(nb)[None, :]], 0.0)/xs
        tE = np.where(valid, E[cc, np.arange(nb)[None, :]], 0.0)/xs
        r = rr[lo:hi][:, None]
        tE = tE*(r - xs >= np.maximum(2*xs, xs+2) - 1e-12)
        def trap(t):
            cs = np.cumsum(t, axis=1); out = h*(cs - 0.5*t[:, :1] - 0.5*t); out[:, 0] = 0; return out
        E[lo:hi] = 1 - trap(tO); O[lo:hi] = 1 - trap(tE)
    return rr, xs, E

def read(rr, xs, P, s, B):
    j = int(round((B - xs[0])/(xs[1]-xs[0]))); assert abs(xs[j]-B) < 1e-9
    return float(np.interp(s*B, rr, P[:, j]))

if __name__ == "__main__":
    svals = [1.995, 2.0, 2.05, 2.1, 2.2, 2.3]
    out = {}
    for hinv in [25, 50, 100]:
        rr, xs, PE = propagate(hinv, 80)
        out[hinv] = (rr, xs, PE)
        print(f"--- propagate h=1/{hinv}")
        for B in [10, 20, 40, 80]:
            row = [(s*s*B*B/phi_e(s))*read(rr, xs, PE, s, B) for s in svals]
            print(f"  B={B:3d}: T(s,B) for s={svals}: " + " ".join(f"{t:.5f}" for t in row))
        sys.stdout.flush()
    rr1, xs1, P1 = out[50]; rr2, xs2, P2 = out[100]
    print("--- Richardson (1/50,1/100):")
    for B in [10, 20, 40, 80]:
        row = [(s*s*B*B/phi_e(s))*(2*read(rr2, xs2, P2, s, B) - read(rr1, xs1, P1, s, B)) for s in svals]
        print(f"  B={B:3d}: " + " ".join(f"{t:.5f}" for t in row) + f"   (target {target:.5f})")
    sys.stdout.flush()
    print("--- direct full recursion Q_e vs f_i/B + Phi_e (decomposition check), B=8,12")
    for hinv in [100, 200]:
        rq, xq, E = direct_Q(hinv, 12)
        for B in [8, 12]:
            for s in [1.995, 2.0, 2.1, 2.2]:
                q = read(rq, xq, E, s, B); bench = float(fe(np.array(s)))/B
                ph = 2*read(rr2, xs2, P2, s, B) - read(rr1, xs1, P1, s, B)
                print(f"  h=1/{hinv} B={B} s={s}: Q_e={q:.7f}  f/B={bench:.7f}  Q_e-f/B={q-bench:.3e}  Phi_e={ph:.3e}")
        sys.stdout.flush()
