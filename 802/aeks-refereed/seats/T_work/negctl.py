"""Negative controls for mech.py: each perturbed identity MUST show a large violation, proving the instrument can fail."""
import numpy as np
rng = np.random.default_rng(7)

def Hw(a, w):
    m = a > 0
    return float(np.sum(a[m] * np.log(w[m] / a[m])))
def KL(a, b):
    m = a > 0
    return float(np.sum(a[m] * np.log(a[m] / b[m])))

fails = {}
for trial in range(60):
    n = 9
    A = (rng.random((n, n)) < 0.8).astype(float); A = np.triu(A, 1); A = A + A.T
    w = np.exp(rng.normal(0, 1.5, n))
    C = (A * w) @ A
    A = A * (C > 0)  # keep only edges in triangles (one pass is enough for control purposes)
    C = (A * w) @ A
    A = A * (C > 0); C = (A * w) @ A
    h = np.array([np.sum(A[u] * w * C[u]) for u in range(n)])
    verts = [u for u in range(n) if A[u].sum() > 0]
    if not verts: continue
    Z = sum(w[u] * h[u] for u in verts)
    for u in verts:
        N = np.where(A[u] > 0)[0]
        if len(N) < 3: continue
        P = A[np.ix_(N, N)] * w[N][None, :] / C[u, N][:, None]
        Q = 0.5 * (np.eye(len(N)) + P)
        pi = w[N] * C[u, N] / h[u]
        unif = np.ones(len(N)) / len(N)
        j = 2
        Kj = P @ np.linalg.matrix_power(Q, j); Kj1 = Kj @ Q
        # NC1: increment identity averaged over a NON-stationary start (uniform) must fail
        for name, start in [('NC1 increment identity, uniform start', unif), ('PC1 increment identity, pi start', pi)]:
            lhs = sum(start[a] * Hw(Kj1[a], w[N]) for a in range(len(N))) - sum(start[a] * Hw(Kj[a], w[N]) for a in range(len(N)))
            rhs = sum(start[a] * Q[a, b] * KL(Kj[b], Kj1[a]) for a in range(len(N)) for b in range(len(N)) if Q[a, b] > 0)
            fails[name] = max(fails.get(name, 0), abs(lhs - rhs))
        # NC2: un-reversed ell must not equal entropy
        Hj_u = sum(unif[a] * Hw(Kj[a], w[N]) for a in range(len(N)))
        Eell_wrong = sum(unif[a] * Kj[a, b] * np.log(w[N][a] / Kj[b, a]) for a in range(len(N)) for b in range(len(N)) if Kj[a, b] > 0) - Hj_u + sum(pi[a] * Hw(Kj[a], w[N]) for a in range(len(N)))
        Eell_right = sum(pi[a] * Kj[a, b] * np.log(w[N][a] / Kj[b, a]) for a in range(len(N)) for b in range(len(N)) if Kj[a, b] > 0)
        Hj = sum(pi[a] * Hw(Kj[a], w[N]) for a in range(len(N)))
        fails['NC2 E_unif[ell] vs E_unif[H] (non-reversible start, should differ)'] = max(fails.get('NC2 E_unif[ell] vs E_unif[H] (non-reversible start, should differ)', 0), abs(Eell_wrong - Hj))
        fails['PC2 E[log w_v/K(y,v)] vs H_j (should agree)'] = max(fails.get('PC2 E[log w_v/K(y,v)] vs H_j (should agree)', 0), abs(Eell_right - Hj))
        # NC3: reversibility w.r.t. uniform must fail
        D = unif[:, None] * Kj
        fails['NC3 reversibility wrt uniform'] = max(fails.get('NC3 reversibility wrt uniform', 0), np.max(np.abs(D - D.T)))
        # NC4: mu-P/mu-Q identity with Q' = (I+2P)/3 must fail
        Qb = (np.eye(len(N)) + 2 * P) / 3
        tv = lambda a, b: 0.5 * np.abs(a - b).sum()
        lhs = 2 * sum(pi[a] * Qb[a, b] * tv(Kj[b], Kj1[a]) for a in range(len(N)) for b in range(len(N)))
        rhs = sum(pi[a] * tv(Kj[a], Kj1[a]) for a in range(len(N))) + sum(pi[a] * P[a, b] * tv(Kj[b], Kj1[a]) for a in range(len(N)) for b in range(len(N)))
        fails['NC4 muQ identity with wrong lazy weight'] = max(fails.get('NC4 muQ identity with wrong lazy weight', 0), abs(lhs - rhs))
for k, v in fails.items():
    print(f'{v: .3e}  {k}')
