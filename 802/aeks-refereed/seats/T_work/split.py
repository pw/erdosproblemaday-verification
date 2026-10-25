"""Seat T numerics: Lemma 5.1 (shared rejection) by simulation, and the Lemma 5.3 construction H' checked
exhaustively on random weighted graphs (simplicity, projection injectivity, neighbourhood bound, triangle-survival
characterisation both directions, union bound in expectation)."""
import numpy as np, itertools, sys
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 11)

def shared_rejection(rows):
    """rows: (I x m) array of distributions on {0..m-1}. Returns label vector, exactly the paper's construction."""
    I, m = rows.shape
    out = -np.ones(I, dtype=int)
    while (out < 0).any():
        z = rng.integers(m); u = rng.random()
        acc = (out < 0) & (u <= rows[:, z])
        out[acc] = z
    return out

def tv(a, b): return 0.5 * np.abs(a - b).sum()

def exact_agree(p, q):
    d = tv(p, q)
    return ((1 - d) + np.sum(np.maximum(p - q, 0) * q) + np.sum(np.maximum(q - p, 0) * p)) / (1 + d)

worst = {}
def rec(k, v): worst[k] = max(worst.get(k, -np.inf), v)

# ---------- Lemma 5.1 ----------
for t in range(25):
    I = int(rng.integers(2, 6)); m = int(rng.integers(2, 7))
    rows = rng.dirichlet(np.ones(m) * rng.uniform(0.2, 3), size=I)
    if t % 5 == 0:  # include disjoint supports and identical rows
        rows[1] = rows[0]
    if t % 7 == 0 and m >= 2:
        rows[0] = 0; rows[0, 0] = 1; rows[-1] = 0; rows[-1, 1] = 1
    Nsim = 20000
    labs = np.array([shared_rejection(rows) for _ in range(Nsim)])
    for i in range(I):
        emp = np.bincount(labs[:, i], minlength=m) / Nsim
        se = np.sqrt(rows[i] * (1 - rows[i]) / Nsim) + 1e-12
        rec('5.1 marginal z-score max', np.max(np.abs(emp - rows[i]) / se))
    for i, k in itertools.combinations(range(I), 2):
        d = tv(rows[i], rows[k])
        dis = np.mean(labs[:, i] != labs[:, k])
        ex = 1 - exact_agree(rows[i], rows[k])
        se = np.sqrt(max(ex * (1 - ex), 1e-9) / Nsim)
        rec('5.1 exact disagreement - 2d/(1+d)', ex - 2 * d / (1 + d))
        rec('5.1 |sim - exact| z-score', abs(dis - ex) / se)
        rec('5.1 sim disagreement - 2d/(1+d) (z)', (dis - 2 * d / (1 + d)) / se)

# ---------- Lemma 5.3 construction ----------
def peel(A, w, tau):
    A = A.copy()
    while True:
        C = (A * w) @ A
        bad = np.argwhere((A > 0) & (C < tau))
        if len(bad) == 0: return A
        u, v = bad[0]; A[u, v] = A[v, u] = 0

def tri_list(A):
    n = len(A)
    return [t for t in itertools.combinations(range(n), 3) if A[t[0], t[1]] and A[t[0], t[2]] and A[t[1], t[2]]]

ngraph = 0
for trial in range(120):
    n = int(rng.integers(6, 13))
    A = (rng.random((n, n)) < rng.uniform(0.5, 0.95)).astype(float); A = np.triu(A, 1); A = A + A.T
    w = np.exp(rng.normal(0, rng.uniform(0.3, 2.0), n))
    C0 = (A * w) @ A
    if not np.any(A > 0): continue
    tau = max(np.quantile(C0[A > 0], 0.1), 1e-9)
    A = peel(A, w, tau)
    if not np.any(A > 0): continue
    ngraph += 1
    Cc = (A * w) @ A
    x = max(1.0, 1 / Cc[A > 0].min())
    h = np.array([np.sum(A[u] * w * Cc[u]) for u in range(n)])
    Z = w @ h
    tris = tri_list(A); T = sum(w[a] * w[b] * w[c] for a, b, c in tris)
    M = 0.5 * w @ A @ w
    j = int(rng.integers(0, 6))
    verts = [u for u in range(n) if A[u].sum() > 0]
    Nu = {u: np.where(A[u] > 0)[0] for u in verts}
    K = {}
    for u in verts:
        N = Nu[u]
        P = A[np.ix_(N, N)] * w[N][None, :] / Cc[u, N][:, None]
        Q = 0.5 * (np.eye(len(N)) + P)
        K[u] = P @ np.linalg.matrix_power(Q, j)
    # admissibility parameter s (plays the role of sqrt x): pick a quantile of ell so that some labels are rejected
    ells = []
    for u in verts:
        N = Nu[u]
        for a in range(len(N)):
            for b in range(len(N)):
                if K[u][a, b] > 0: ells.append(np.log(w[N][a] / K[u][b, a]))
    s = float(np.quantile(ells, rng.uniform(0.6, 0.98)))
    idx = {u: {v: k for k, v in enumerate(Nu[u])} for u in verts}
    def admissible(u, v, y):  # label y at incidence (u,v)
        return K[u][idx[u][y], idx[u][v]] >= w[v] * np.exp(-s)
    # exact expected union bound terms
    corner = 0.0; inadm = 0.0; tvterm = 0.0
    for (a, b, c) in tris:
        wt = w[a] * w[b] * w[c] / T  # unordered triangle prob
        for (u, v, z) in [(a, b, c), (b, a, c), (c, a, b)]:
            p = K[u][idx[u][v]]; q = K[u][idx[u][z]]
            corner += wt * (1 - exact_agree(p, q)); tvterm += wt * 2 * tv(p, q)
        for (u, v) in [(a, b), (b, a), (a, c), (c, a), (b, c), (c, b)]:
            row = K[u][idx[u][v]]
            inadm += wt * sum(row[k] for k, y in enumerate(Nu[u]) if not admissible(u, v, y))
    # average inadmissibility under mu, and its Markov bound with this s
    Hj = 0.0; inad_mu = 0.0
    for u in verts:
        for k, v in enumerate(Nu[u]):
            m_ = w[u] * w[v] * Cc[u, v] / Z
            row = K[u][k]; msk = row > 0
            Hj += m_ * np.sum(row[msk] * np.log(w[Nu[u]][msk] / row[msk]))
            inad_mu += m_ * sum(row[kk] for kk, y in enumerate(Nu[u]) if not admissible(u, v, y))
    rec('5.3 avg-over-triangles inadm = 6 * avg-over-mu inadm', abs(inadm - 6 * inad_mu))
    if s + np.log(x) > 0:
        rec('5.2 inad_mu - (H_j+log x)/(s+log x)', inad_mu - (Hj + np.log(x)) / (s + np.log(x)))
    rec('5.1 corner exact <= 2TV', corner - tvterm)
    def joint_diag(p, q):
        d = tv(p, q)
        return (np.minimum(p, q) + np.maximum(p - q, 0) * q + np.maximum(q - p, 0) * p) / (1 + d)
    exact_loss = 0.0
    for (a, b, c) in tris:
        wt = w[a] * w[b] * w[c] / T
        ps = 1.0
        for (u, v, z) in [(a, b, c), (b, a, c), (c, a, b)]:
            jd = joint_diag(K[u][idx[u][v]], K[u][idx[u][z]])
            ps *= sum(jd[k] for k, y in enumerate(Nu[u]) if admissible(u, v, y) and admissible(u, z, y))
        exact_loss += wt * (1 - ps)
    rec('5.3 EXACT E loss - union bound (corner+inadm)', exact_loss - (corner + inadm))
    losses = []
    for rep in range(150):
        Y = {u: shared_rejection(K[u]) for u in verts}  # Y[u][k] = index into N(u) of the label of incidence (u, N(u)[k])
        lab = {(u, v): Nu[u][Y[u][k]] for u in verts for k, v in enumerate(Nu[u])}
        adm = {(u, v): admissible(u, v, lab[(u, v)]) for (u, v) in lab}
        # build H'
        Vp = {}; edges = set(); dup = 0
        for (u, v), y in lab.items():
            if adm[(u, v)]:
                Vp.setdefault((u, y), len(Vp))
        for u in verts:
            for v in Nu[u]:
                if u < v and adm[(u, v)] and adm[(v, u)]:
                    a_ = Vp[(u, lab[(u, v)])]; b_ = Vp[(v, lab[(v, u)])]
                    assert a_ != b_
                    e = (min(a_, b_), max(a_, b_))
                    if e in edges: dup += 1
                    edges.add(e)
        rec('5.3 duplicate edge insertions (must be 0)', dup)
        inv = {k: key for key, k in Vp.items()}
        npv = len(Vp)
        Ap = np.zeros((npv, npv))
        for a_, b_ in edges: Ap[a_, b_] = Ap[b_, a_] = 1
        wp = np.array([w[inv[k][0]] for k in range(npv)])
        proj = np.array([inv[k][0] for k in range(npv)])
        # projection injective on directed edges and maps edges to edges
        img = [(proj[a_], proj[b_]) for a_, b_ in edges] + [(proj[b_], proj[a_]) for a_, b_ in edges]
        rec('5.3 projection non-injective directed edges', len(img) - len(set(img)))
        rec('5.3 image edge not in H', sum(1 for (p1, p2) in img if not A[p1, p2]))
        # neighbourhood bound
        if npv:
            nb = Ap @ wp
            rec('5.3 nbhd weight - e^s', np.max(nb - np.exp(s)))
            groupw = {}
            for (u, v), y in lab.items():
                if adm[(u, v)]: groupw[(u, y)] = groupw.get((u, y), 0) + w[v]
            rec('5.3 group weight - e^s', max(gw - np.exp(s) for gw in groupw.values()))
            rec('5.3 nbhd weight - w(A_uy)', max(nb[Vp[key]] - groupw[key] for key in Vp))
            rec('5.3 nbhd weight - original nbhd', np.max(nb - (A @ w)[proj]))
        # triangle survival characterisation (both directions)
        pred = set()
        for (a, b, c) in tris:
            ok = all(adm[(p, q)] for p, q in [(a, b), (b, a), (a, c), (c, a), (b, c), (c, b)]) and \
                 lab[(a, b)] == lab[(a, c)] and lab[(b, a)] == lab[(b, c)] and lab[(c, a)] == lab[(c, b)]
            if ok: pred.add((a, b, c))
        actual = [tuple(sorted(proj[list(t)])) for t in tri_list(Ap)] if npv >= 3 else []
        rec('5.3 H\' triangles with non-distinct/duplicate projection', len(actual) - len(set(actual)))
        rec('5.3 survival char: actual minus predicted', len(set(actual) - pred))
        rec('5.3 survival char: predicted minus actual', len(pred - set(actual)))
        Tp = sum(w[a] * w[b] * w[c] for a, b, c in pred)
        Mp = 0.5 * wp @ Ap @ wp if npv else 0.0
        rec('5.3 T\'-T', Tp - T); rec('5.3 M\'-M', Mp - M)
        losses.append((T - Tp) / T)
    L = np.mean(losses); se = np.std(losses) / np.sqrt(len(losses)) + 1e-12
    rec('5.3 MC E loss - (corner+inadm) union bound (z)', (L - (corner + inadm)) / se)
    se2 = np.sqrt(max(exact_loss, 1e-9) / len(losses))  # Var(loss) <= E loss since loss in [0,1]
    rec('5.3 |MC E loss - exact E loss| (z, conservative se)', abs(L - exact_loss) / se2)
    rec('5.3 MC E loss - union bound (z, conservative se)', (L - (corner + inadm)) / se2)
print('graphs:', ngraph)
for k, v in worst.items():
    print(f'{v: .3e}  {k}')
