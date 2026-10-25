# Global maximizer of F_G(w) = sum w(1-log w) - M_G(w) by multi-start coordinate ascent + Newton polish.
import numpy as np, networkx as nx, itertools

def F(A, w):
    w = np.asarray(w, float)
    with np.errstate(divide='ignore', invalid='ignore'):
        vt = np.where(w > 0, w * (1 - np.log(np.where(w > 0, w, 1))), 0.0)
    return vt.sum() - 0.5 * w @ A @ w

def coord_ascent(A, w0, iters=20000, tol=1e-15):
    w = np.array(w0, float)
    n = len(w)
    nbr = [np.nonzero(A[i])[0] for i in range(n)]
    for it in range(iters):
        delta = 0.0
        for v in range(n):
            new = np.exp(-w[nbr[v]].sum())
            delta = max(delta, abs(new - w[v]))
            w[v] = new
        if delta < tol:
            break
    return w

def newton(A, w, iters=50):
    # solve log(1/w) - A w = 0 in variables y = log w : -y - A e^y = 0
    y = np.log(w)
    for _ in range(iters):
        e = np.exp(y)
        g = -y - A @ e
        J = -np.eye(len(y)) - A * e[None, :]
        step = np.linalg.solve(J, -g)
        y = y + step
        if np.max(np.abs(step)) < 1e-16:
            break
    return np.exp(y)

def residual(A, w):
    return np.max(np.abs(np.log(1 / w) - A @ w))

def is_local_max(A, w):
    H = np.diag(1 / w) + A  # -Hessian
    return np.min(np.linalg.eigvalsh(H)) > 1e-12

def global_max(G, nrand=60, seed=0):
    nodes = sorted(G.nodes())
    idx = {v: i for i, v in enumerate(nodes)}
    n = len(nodes)
    A = np.zeros((n, n))
    for a, b in G.edges():
        A[idx[a], idx[b]] = A[idx[b], idx[a]] = 1
    rng = np.random.default_rng(seed)
    starts = [np.ones(n), np.full(n, 0.1), np.full(n, 1e-3)]
    # maximal independent sets (complement cliques) as starts
    Gc = nx.complement(nx.relabel_nodes(G, idx))
    mis = list(itertools.islice(nx.find_cliques(Gc), 400))
    for I in mis:
        s = np.full(n, 1e-3); s[list(I)] = 1.0; starts.append(s)
    for _ in range(nrand):
        starts.append(rng.uniform(0, 1.5, n) ** rng.choice([1, 3]))
    best = None; stats = []
    for s in starts:
        w = coord_ascent(A, s)
        try:
            w = newton(A, w)
        except np.linalg.LinAlgError:
            pass
        if np.any(~np.isfinite(w)) or np.any(w <= 0):
            continue
        val = F(A, w)
        stats.append(val)
        if best is None or val > best[0] + 1e-13:
            best = (val, w)
    val, w = best
    nlocal = len(set(np.round(stats, 9)))
    return A, w, val, residual(A, w), is_local_max(A, w), nlocal
