# Finite check of the Markov steps (7.1) -> (7.2), (7.3) of the #604 preprint, on explicit
# n-point configurations, with the paper's normalization U = e^m Z + b, m = E_pi i = -E_pi log|Z(x)-Z(y)|.
import numpy as np
rng = np.random.default_rng(1604)

def pairlogs(U):
    D = np.abs(U[:, None] - U[None, :])
    iu = ~np.eye(len(U), dtype=bool)
    return np.log(D[iu])                      # all n(n-1) ordered distinct pairs (pi-uniform)

def run(name, Z, signed_control=False):
    n = len(Z)
    m = -pairlogs(Z).mean()                   # m_j = E_pi i_j
    U = np.exp(m) * Z
    L = pairlogs(U)
    C1 = np.abs(L).mean()                     # (7.1): E_pi |log|U(x)-U(y)||
    print(f"[{name}] n={n}  E_pi log|U-U'| = {L.mean():+.2e} (=0 by the choice of m)  "
          f"C1=E|log|={C1:.4f}  E(log)_+={np.maximum(L,0).mean():.4f}  E(log)_-={np.maximum(-L,0).mean():.4f}")
    if signed_control:
        C1 = max(L.mean(), 0.0)              # what the mangled paper.txt line 'E_pi log|U-U'| <= C1' would allow
        print(f"   CONTROL: using signed C1 := max(E log, 0) = {C1:.3g}")
    # (alpha x alpha){|z-z'|>R} <= C1/log R
    D = np.abs(U[:, None] - U[None, :])
    ok_pair = all((D > R).mean() <= C1/np.log(R) + 1e-12 for R in (1.5, 3, 10, 1e3, 1e6))
    R0 = np.exp(2*C1) * 1.0001 if C1 > 0 else 1.0001
    far = (D > R0).mean(axis=1)               # alpha{|z' - z| > R0} for each empirical center z
    zc = U[np.argmin(far)]
    V = U - zc                                # b chosen to move the center to 0
    ok72 = True; worst72 = 0
    for R in 2*R0*np.array([1.01, 2, 10, 1e2, 1e4, 1e8]):
        lhs = (np.abs(V) > R).mean(); rhs = 2*C1/np.log(R/2)
        worst72 = max(worst72, lhs - rhs); ok72 &= lhs <= rhs + 1e-12
    ok73 = True; worst73 = -1; arg = None
    centers = np.concatenate([V[rng.integers(0, n, 200)], (rng.standard_normal(50)+1j*rng.standard_normal(50))])
    for r in (0.49, 0.1, 1e-2, 1e-4, 1e-8, 1e-12):
        for z0 in centers:
            lhs = ((np.abs(V - z0) < r).mean())**2
            rhs = 1.0/n + (C1/np.log(1/(2*r)))
            if lhs - rhs > worst73: worst73, arg = lhs - rhs, (r, lhs, rhs)
            ok73 &= lhs <= rhs + 1e-12
    print(f"   pair tail ok={ok_pair}  (7.2) ok={ok72} (max lhs-rhs={worst72:+.3g})  "
          f"(7.3) ok={ok73} (max lhs-rhs={worst73:+.3g} at r,lhs,rhs={arg})")

n = 1200
# config 1: multi-scale mixture
Z1 = np.concatenate([rng.standard_normal(400)+1j*rng.standard_normal(400),
                     5+0.01*(rng.standard_normal(400)+1j*rng.standard_normal(400)),
                     30*np.exp(2j*np.pi*rng.random(400))])
run("multiscale", Z1)
# config 2: clustered -- half the points inside a disk of radius 1e-9 (all distinct)
Z2 = np.concatenate([1e-9*(rng.random(600)+1j*rng.random(600)), rng.random(600)*2-1+1j*(rng.random(600)*2-1)])
run("clustered", Z2)
run("clustered", Z2, signed_control=True)
# config 3: spread -- 1150 points in unit disk, 50 at radius 1e12
Z3 = np.concatenate([np.sqrt(rng.random(1150))*np.exp(2j*np.pi*rng.random(1150)), 1e12*np.exp(2j*np.pi*rng.random(50))])
run("spread", Z3)
run("spread", Z3, signed_control=True)
