# Decorrelated numerical probe of Prop 3.1 in the HOM normalisation the paper uses:
#   g(W) = t(C4,W) - rho^3 + (3/64) rho  >= 0   for triangle-free step graphons W.
# Minimise g over vertex weights for every triangle-free graph on <= 9 vertices (nauty geng -t),
# connected ones on 10, and named larger graphs.  (d) computer search, NOT a proof.  seat MATH.
import numpy as np, sys
from scipy.optimize import minimize
sys.path.insert(0, '/tmp/erdos1800/seats/math')
from graphs import *
rng = np.random.default_rng(31)
G3 = 3/64
def g_and_grad(w, A):
    W = np.diag(w); M = A@W
    M2 = M@M; t = np.trace(M2@M2)
    rho = w@A@w
    gt = 4*np.diag(M2@M@A)
    gr = 2*A@w
    return t - rho**3 + G3*rho, gt - 3*rho**2*gr + G3*gr, rho, t
def minimise(A, starts=4):
    n = len(A); best = (np.inf, None)
    cons = ({'type':'eq', 'fun': lambda w: w.sum()-1, 'jac': lambda w: np.ones_like(w)},)
    for k in range(starts):
        w0 = np.full(n, 1/n) if k == 0 else rng.dirichlet(np.ones(n))
        r = minimize(lambda w: g_and_grad(w,A)[0], w0, jac=lambda w: g_and_grad(w,A)[1], method='SLSQP',
                     bounds=[(0,1)]*n, constraints=cons, options=dict(ftol=1e-14, maxiter=500))
        w = np.clip(r.x, 0, None); w /= w.sum()
        val, _, rho, t = g_and_grad(w, A)
        if val < best[0]: best = (val, (rho, t, w))
    return best
overall = (np.inf, None)
for n in range(2, 10):
    gs = geng(n); loc = (np.inf, None)
    for A in gs:
        v, info = minimise(A, 3)
        if v < loc[0]: loc = (v, info)
    print(f"n={n}: {len(gs)} graphs, min g = {loc[0]:+.6e} at rho={loc[1][0]:.4f}")
    if loc[0] < overall[0]: overall = (loc[0], (n, loc[1][0]))
gs = geng(10, ('-c',)); loc = (np.inf, None)
for A in gs:
    v, info = minimise(A, 2)
    if v < loc[0]: loc = (v, info)
print(f"n=10 connected: {len(gs)} graphs, min g = {loc[0]:+.6e} at rho={loc[1][0]:.4f}")
named = [('C5',cycle(5)),('Petersen',petersen()),('Clebsch',clebsch()),('MobiusKantor',mobius_kantor())] + \
        [(f'Andrasfai{k}', andrasfai(k)) for k in range(2,9)] + [(f'C{k}', cycle(k)) for k in (7,9,11)]
Cl = clebsch()
for v in range(1): named.append(('Clebsch-minus-vertex', np.delete(np.delete(Cl, 0, 0), 0, 1)))
named.append(('Clebsch-minus-edge', Cl - np.outer(np.eye(16)[0], Cl[0]) * 0 ))
E = np.argwhere(np.triu(Cl)); Cm = Cl.copy(); i,j = E[0]; Cm[i,j]=Cm[j,i]=0; named[-1] = ('Clebsch-minus-edge', Cm)
for name, A in named:
    assert is_tf(A)
    v, (rho, t, w) = minimise(A, 6)
    n = len(A); vu, _, ru, tu = g_and_grad(np.full(n,1/n), A)
    print(f"{name:22s} n={n:2d}: uniform g={vu:+.3e} (rho={ru:.4f});  min over weights g={v:+.3e} at rho={rho:.4f}")
# local second-order check around uniform Clebsch: g along eigen-directions of A
lam, U = np.linalg.eigh(Cl); u = np.full(16, 1/16)
for th in (1.0, -3.0):
    vec = U[:, np.isclose(lam, th)][:,0]; vec -= vec.mean()
    for eps in (1e-3, -1e-3, 1e-2):
        w = u + eps*vec/16
        val, _, rho, t = g_and_grad(w, Cl)
        print(f"Clebsch weight perturbation along theta={th:+.0f}, eps={eps:+.0e}: rho-5/16={rho-5/16:+.3e}, g={val:+.3e}")
