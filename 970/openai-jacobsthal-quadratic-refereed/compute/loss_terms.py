# Independent recomputation of the first-omission loss terms L_m in Prop 6.3's margin (paper eq. (6.12)-(6.14) region,
# printed §6.3): L_m = 2 ∫_{2≥x1≥…≥xm≥1} (1/x_m){(A_m^3 − A'^3)/24 − 1_{m even}(A_m − A')/2} ∏ dx_j/x_j,
# A_m = Σx_j + x_m, A' = 0 (m=1), 2 (m=2), A_{m−2} (m≥3).  Route: x_j = 2^{U_j}, U iid uniform ⇒ ∏dx_j/x_j = λ^m ∏dU_j, ordered
# region = 1/m! of the cube.  (a) m=2,3 by deterministic nested Gauss–Legendre on the ORIGINAL integrand (not the paper's 1-D
# reductions) vs the paper's closed forms; (b) m=1..12 by Monte Carlo (seeded) ⇒ an estimate of I = 8/3 − Σ L_m; (c) the paper's
# tail majorant (6.14) evaluated exactly vs the MC tail.  Control: a perturbed integrand (A_m = Σx_j + 2x_m) must NOT reproduce L2/L3.
import numpy as np, math, sys
lam = math.log(2)
def A(x, m):            # x: array (..., m), sorted descending
    return x[..., :m].sum(-1) + x[..., m-1]
def g(x, m, pert=False):
    Am = A(x, m) + (x[..., m-1] if pert else 0)
    if m == 1: Ap = 0.0
    elif m == 2: Ap = 2.0
    else: Ap = A(x, m-2) + (x[..., m-3] if pert else 0)
    val = (Am**3 - Ap**3)/24.0 - ((Am - Ap)/2.0 if m % 2 == 0 else 0.0)
    return 2.0*val/x[..., m-1]
# (a) deterministic quadrature on the ordered simplex in U-coordinates
xs, ws = np.polynomial.legendre.leggauss(200)
def quad_ordered(m, pert=False):
    # integrate over 1 ≥ U1 ≥ U2 (≥ U3) ≥ 0 with nested change of variables
    tot = 0.0
    if m == 2:
        for a, wa in zip(xs, ws):
            u1 = (a+1)/2; W1 = wa/2
            u2 = u1*(xs+1)/2; W2 = ws*u1/2
            X = np.stack([np.full_like(u2, 2**u1), 2**u2], -1)
            tot += W1*np.sum(W2*g(X, 2, pert))
        return lam**2*tot
    if m == 3:
        for a, wa in zip(xs, ws):
            u1 = (a+1)/2; W1 = wa/2
            for b, wb in zip(xs, ws):
                u2 = u1*(b+1)/2; W2 = wb*u1/2
                u3 = u2*(xs+1)/2; W3 = ws*u2/2
                X = np.stack([np.full_like(u3, 2**u1), np.full_like(u3, 2**u2), 2**u3], -1)
                tot += W1*W2*np.sum(W3*g(X, 3, pert))
        return lam**3*tot
L2c = -35/36 - lam**2 + 3*lam
L3c = 623/432 - 19/12*lam + lam**2/3
q2, q3 = quad_ordered(2), quad_ordered(3)
p2, p3 = quad_ordered(2, True), quad_ordered(3, True)
print(f"L1 exact 1 (paper)")
print(f"L2 quad {q2:.12f}  paper closed form {L2c:.12f}  diff {q2-L2c:.2e}   | perturbed-control {p2:.6f} (must differ)")
print(f"L3 quad {q3:.12f}  paper closed form {L3c:.12f}  diff {q3-L3c:.2e}   | perturbed-control {p3:.6f} (must differ)")
# (b) Monte Carlo for m = 1..12
rng = np.random.default_rng(20261023); N = 2_000_000
Ls = {}
for m in range(1, 13):
    acc = []; 
    for rep in range(5):
        U = np.sort(rng.random((N, m)), axis=1)[:, ::-1]
        X = 2.0**U
        acc.append(g(X, m).mean())
    mu = np.mean(acc); se = np.std(acc, ddof=1)/math.sqrt(5)
    Ls[m] = (lam**m/math.factorial(m)*mu, lam**m/math.factorial(m)*se)
    print(f"L{m:<2d} MC {Ls[m][0]:.6f} ± {Ls[m][1]:.1e}")
tail_mc = sum(Ls[m][0] for m in range(4, 13))
maj = 0.5*sum((m+1)**2*lam**m/math.factorial(m)*(lam**-2 + (1.5/lam - lam**-2)/m) for m in range(4, 200))
print(f"tail m>=4: MC (m≤12) {tail_mc:.6f}; paper majorant (6.14) exact {maj:.6f} (paper says < 0.34)")
I_est = 8/3 - 1 - L2c - L3c - tail_mc
print(f"I ≈ 8/3 − 1 − L2 − L3 − tail_MC = {I_est:.6f}   (paper: I > 0.14 rigorous; remark: I > 0.2229793730)")
print(f"margin −a*+2I/M_g with M_g ≤ 4e^γ: ≥ {-0.01 + 2*I_est/(4*math.exp(0.5772156649015329)):.6f} (paper: > 0.02 from I > 0.14)")
