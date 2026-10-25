"""Seat T numerics: mechanical identities of Lemmas 3.3, 4.1, 5.2 on random weighted graphs.
Every check prints max violation; a positive violation beyond 1e-9 (relative) is a counterexample.
Negative controls at the bottom deliberately break an identity and must FAIL.
"""
import numpy as np, itertools, sys

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 1)

def rand_graph(n, p, sig):
    A = (rng.random((n, n)) < p).astype(float)
    A = np.triu(A, 1); A = A + A.T
    w = np.exp(rng.normal(0, sig, n))
    return A, w

def peel(A, w, tau):
    """Lemma 3.3 peeling: delete an edge with c_uv < tau, repeat. Returns A', total weight lost."""
    A = A.copy(); lost = 0.0; delsum = 0.0
    while True:
        C = (A * w) @ A  # C[u,v] = sum_z A[u,z] w_z A[z,v]
        cand = np.argwhere((A > 0) & (C < tau))
        if len(cand) == 0:
            return A, lost, delsum
        u, v = cand[rng.integers(len(cand))]
        lost += w[u] * w[v] * C[u, v]; delsum += w[u] * w[v]
        A[u, v] = A[v, u] = 0

def T_mass(A, w):
    n = len(w); t = 0.0
    for a, b, c in itertools.combinations(range(n), 3):
        if A[a, b] and A[a, c] and A[b, c]:
            t += w[a] * w[b] * w[c]
    return t

def M_mass(A, w):
    return 0.5 * w @ A @ w

worst = {}
def rec(name, val):
    worst[name] = max(worst.get(name, -np.inf), val)

def Hw(a, w):
    m = a > 0
    return float(np.sum(a[m] * np.log(w[m] / a[m])))

def KL(a, b):
    m = a > 0
    if np.any(b[m] <= 0):
        return np.inf
    return float(np.sum(a[m] * np.log(a[m] / b[m])))

def tv(a, b):
    return 0.5 * np.abs(a - b).sum()

NG = 0
for trial in range(400):
    n = int(rng.integers(6, 16)); p = rng.uniform(0.35, 0.95); sig = rng.uniform(0.2, 2.5)
    A0, w = rand_graph(n, p, sig)
    # Lemma 3.3 identities on the raw graph
    T0 = T_mass(A0, w); M0 = M_mass(A0, w)
    C0 = (A0 * w) @ A0
    s = A0 @ w
    h = np.array([np.sum(A0[u] * w * C0[u]) for u in range(n)])
    rec('3.2a |sum_edges w w c - 3T|', abs(0.5 * np.sum(A0 * np.outer(w, w) * C0) - 3 * T0) / max(T0, 1e-300))
    rec('3.2b |sum w h - 6T|', abs(w @ h - 6 * T0) / max(T0, 1e-300))
    L = s.max()
    rec('3.3 T - L/3 M', (T0 - L / 3 * M0) / max(M0, 1e-300))
    tau = rng.uniform(0.0, 1.0) * np.median(C0[A0 > 0]) if np.any(A0 > 0) else 0.1
    tau = max(tau, 1e-6)
    A, lost, delsum = peel(A0, w, tau)
    T1 = T_mass(A, w)
    rec('3.4 telescoping exact |T0-T1-lost|', abs(T0 - T1 - lost) / max(T0, 1e-300))
    rec('3.4 (T0 - tau M0) - T1', (T0 - tau * M0 - T1) / max(M0, 1e-300))
    Cc = (A * w) @ A
    s1 = A @ w
    h1 = np.array([np.sum(A[u] * w * Cc[u]) for u in range(n)])
    nonis = A.sum(1) > 0
    if nonis.any():
        rec('3.3 tau - s_u (nonisolated)', np.max(tau - s1[nonis]))
        rec('3.3 tau s_u - h_u', np.max(tau * s1[nonis] - h1[nonis]))
        rec('3.3 tau - c_uv remaining', np.max(tau - Cc[A > 0]))
    if not nonis.any():
        continue
    NG += 1
    # ---- Lemma 4.1 objects ----
    x = 1.0 / Cc[A > 0].min()  # so that c_uv >= 1/x
    x = max(x, 1.0)
    Z = w @ h1
    rec('Z = 6T', abs(Z - 6 * T1) / Z)
    verts = np.where(nonis)[0]
    K = {}  # K[u][j] matrices on N(u)
    Pm = {}; Qm = {}; pi = {}; Nu = {}
    J = 12
    for u in verts:
        N = np.where(A[u] > 0)[0]; Nu[u] = N
        sub = A[np.ix_(N, N)]
        c = Cc[u, N]
        P = sub * w[N][None, :] / c[:, None]
        Q = 0.5 * (np.eye(len(N)) + P)
        pi_u = w[N] * c / h1[u]
        Pm[u] = P; Qm[u] = Q; pi[u] = pi_u
        rec('P row sums -1', np.max(np.abs(P.sum(1) - 1)))
        rec('pi sums -1', abs(pi_u.sum() - 1))
        Ks = [P]
        for j in range(1, J + 1):
            Ks.append(Ks[-1] @ Q)
        K[u] = Ks
        for j, Kj in enumerate(Ks):
            D = pi_u[:, None] * Kj
            rec('reversibility |pi K - (pi K)^T|', np.max(np.abs(D - D.T)) / np.max(D))
            rec('stationarity |pi K - pi|', np.max(np.abs(pi_u @ Kj - pi_u)))
            rec('(4.5) K(v,y) - x w_y', np.max(Kj - x * w[N][None, :]) / x)
            rec('commute P Q^j = Q^j P', np.max(np.abs(Kj - np.linalg.matrix_power(Q, j) @ P)))
    # mu and ordered triangle law (4.4)
    mu = {}
    for u in verts:
        for k, v in enumerate(Nu[u]):
            mu[(u, v)] = w[u] * w[v] * Cc[u, v] / Z
    rec('mu total -1', abs(sum(mu.values()) - 1))
    for u in verts:
        N = Nu[u]
        for a, v in enumerate(N):
            for b, z in enumerate(N):
                if A[v, z]:
                    lhs = mu[(u, v)] * Pm[u][a, b]
                    rec('(4.4) ordered triangle law', abs(lhs - w[u] * w[v] * w[z] / Z) / lhs)
        # conditional of v given u is pi_u
        marg = sum(mu[(u, v)] for v in N)
        rec('cond v|u = pi_u', np.max(np.abs(np.array([mu[(u, v)] for v in N]) / marg - pi[u])))
        rec('marginal u = w_u h_u/Z', abs(marg - w[u] * h1[u] / Z))
    # H_j and increments
    H = []
    for j in range(J + 1):
        H.append(sum(mu[(u, v)] * Hw(K[u][j][a], w[Nu[u]]) for u in verts for a, v in enumerate(Nu[u])))
    for j in range(J + 1):
        rec('(4.6) -log x - H_j', -np.log(x) - H[j])
        rec('H_j <= log max s_u', H[j] - np.log(s1.max()))
    for j in range(J):
        rec('(4.6) monotone H_j - H_{j+1}', H[j] - H[j + 1])
        # (4.11) exact increment identity
        inc = 0.0; tvQ = 0.0; tvP_az_bv = 0.0; tvmu_av_bv = 0.0; tvP_av_az = 0.0; maxpairTVvsD = -np.inf
        for u in verts:
            N = Nu[u]; Kj = K[u][j]; Kj1 = K[u][j + 1]; Q = Qm[u]; P = Pm[u]
            for a, v in enumerate(N):
                m = mu[(u, v)]
                tvmu_av_bv += m * tv(Kj[a], Kj1[a])
                for b in range(len(N)):
                    if Q[a, b] > 0:
                        d = KL(Kj[b], Kj1[a])
                        inc += m * Q[a, b] * d
                        t_ = tv(Kj[b], Kj1[a])
                        tvQ += m * Q[a, b] * t_
                        maxpairTVvsD = max(maxpairTVvsD, t_ - np.sqrt(max(d, 0.0)))
                    if P[a, b] > 0:
                        tvP_az_bv += m * P[a, b] * tv(Kj[b], Kj1[a])
                        tvP_av_az += m * P[a, b] * tv(Kj[a], Kj[b])
        rec('(4.11) |H_{j+1}-H_j - E_muQ D| abs', abs(H[j + 1] - H[j] - inc))
        if inc > 1e-6:
            rec('(4.11) rel err when inc>1e-6', abs(H[j + 1] - H[j] - inc) / inc)
        rec('TV - sqrt(D) per pair', maxpairTVvsD)
        rec('E_muQ TV - sqrt(H_{j+1}-H_j)', tvQ - np.sqrt(max(H[j + 1] - H[j], 0)))
        rec('mu-P/mu-Q identity |2E_muQ - (E_mu + E_muP)|', abs(2 * tvQ - (tvmu_av_bv + tvP_az_bv)))
        rec('final E_muP||a_v-a_z|| - 2sqrt(dH)', tvP_av_az - 2 * np.sqrt(max(H[j + 1] - H[j], 0)))
        # Lemma 5.2: E ell = H_j, law identity, ell >= -log x, Markov
        Eell = 0.0; law = 0.0; ells = []; probs = []
        for u in verts:
            N = Nu[u]; Kj = K[u][j]
            for a, v in enumerate(N):
                for b, y in enumerate(N):
                    if Kj[a, b] > 0:
                        pr = mu[(u, v)] * Kj[a, b]
                        law = max(law, abs(pr - mu[(u, y)] * Kj[b, a]) / pr)
                        ell = np.log(w[v] / Kj[b, a])
                        Eell += pr * ell; ells.append(ell); probs.append(pr)
        ells = np.array(ells); probs = np.array(probs)
        rec('5.2 law (u,v,y)=(u,y,v)', law)
        rec('5.2 |E ell - H_j|', abs(Eell - H[j]))
        rec('5.2 -log x - ell', np.max(-np.log(x) - ells))
        for sv in [0.0, 0.5, 1.0, 2.0, 4.0]:
            if sv + np.log(x) > 0:
                lhs = probs[ells > sv].sum()
                rec('5.2 Markov P(ell>s) - (H_j+log x)/(s+log x)', lhs - (H[j] + np.log(x)) / (sv + np.log(x)))
print('graphs with edges after peeling:', NG)
for k, v in worst.items():
    flag = 'VIOLATION' if v > 1e-8 else 'ok'
    print(f'{flag:9s} {v: .3e}  {k}')
