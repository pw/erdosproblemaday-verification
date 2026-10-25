"""Seat T numerics: exact best cross-mass constant C*(G,w) for small graphs, and Lemma 3.2 preservation under
random maps that are injective on directed edges (splits + deletions), with a negative control (a blow-up that is
NOT injective on directed edges must be able to increase C*)."""
import numpy as np, sys, itertools
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 3)

def g(x, s):
    out = np.zeros_like(s)
    pos = s > 0
    out[pos] = s[pos] * (x[pos] + np.maximum(0.0, np.log(1.0 / s[pos])))
    return out

def cstar(A, w):
    n = len(w)
    S = np.arange(1 << n)
    ind = ((S[:, None] >> np.arange(n)[None, :]) & 1).astype(float)  # subsets x vertices
    wS = ind @ w
    best = 0.0
    for lo in range(1, 1 << n, 1024):
        hi = min(1 << n, lo + 1024)
        IA = ind[lo:hi]
        F = (IA @ (A * w[:, None])) * w[None, :]  # F[a_set, b] = w_b * w(N(b) cap Aset)
        E = F @ ind.T  # e(Aset, Bset)
        wa = wS[lo:hi][:, None]; wb = wS[None, :]
        x = np.maximum(1.0, np.maximum(np.log(wa), np.log(np.maximum(wb, 1e-300))))
        x = np.broadcast_to(x, E.shape)
        G = g(x, np.broadcast_to(wa, E.shape).copy())
        r = np.where(G > 0, E / np.where(G > 0, G, 1), 0)
        best = max(best, r.max())
    return best

def T_mass(A, w):
    return sum(w[a]*w[b]*w[c] for a, b, c in itertools.combinations(range(len(w)), 3) if A[a,b] and A[a,c] and A[b,c])

def random_split(A, w, keep=0.85):
    """Split every vertex into copies indexed by random groups of its incident edges; keep each edge w.p. keep."""
    n = len(w)
    copy_of = {}  # (u, v) incidence -> copy id of u
    verts = []
    for u in range(n):
        nb = list(np.where(A[u] > 0)[0])
        k = int(rng.integers(1, max(2, len(nb)) + 1))
        ids = []
        for c in range(k):
            ids.append(len(verts)); verts.append(u)
        for v in nb:
            copy_of[(u, v)] = ids[int(rng.integers(k))]
        if not nb:
            pass
    m = len(verts)
    B = np.zeros((m, m))
    for u in range(n):
        for v in range(u + 1, n):
            if A[u, v] and rng.random() < keep:
                a, b = copy_of[(u, v)], copy_of[(v, u)]
                B[a, b] = B[b, a] = 1
    used = sorted(set(np.where(B.sum(1) > 0)[0]) | set(rng.choice(m, size=min(m, 2), replace=False)))
    B = B[np.ix_(used, used)]
    proj = np.array([verts[i] for i in used])
    return B, w[proj], proj

worst = {}
def rec(k, v): worst[k] = max(worst.get(k, -np.inf), v)
cnt = 0
for t in range(200):
    n = int(rng.integers(4, 8))
    A = (rng.random((n, n)) < rng.uniform(0.4, 1.0)).astype(float); A = np.triu(A, 1); A = A + A.T
    if A.sum() == 0: continue
    w = np.exp(rng.normal(rng.uniform(-3, 3), rng.uniform(0.3, 3), n))
    c0 = cstar(A, w)
    B, wb, proj = random_split(A, w)
    if len(wb) > 13: continue
    c1 = cstar(B, wb)
    cnt += 1
    rec('3.2 C*(H)/C*(G) - 1', c1 / c0 - 1)
    rec('3.2 M_H - M_G', 0.5 * wb @ B @ wb - 0.5 * w @ A @ w)
    rec('3.2 T_H - T_G', T_mass(B, wb) - T_mass(A, w))
    rec('3.2 nbhd_H - nbhd_G(image)', np.max(B @ wb - (A @ w)[proj]))
print('pairs tested:', cnt)
for k, v in worst.items():
    print(f'{v: .3e}  {k}')
# negative control: blow up one edge uv into K_{m,m} (not injective on directed edges) -> C* must be able to go up
inc = 0.0
for t in range(30):
    wu, wv = np.exp(rng.normal(0, 2, 2))
    A = np.array([[0, 1], [1, 0]], float); w = np.array([wu, wv])
    c0 = cstar(A, w)
    m = 5
    B = np.zeros((2 * m, 2 * m)); B[:m, m:] = 1; B[m:, :m] = 1
    c1 = cstar(B, np.array([wu] * m + [wv] * m))
    inc = max(inc, c1 / c0 - 1)
print(f'NEG CONTROL (non-injective blow-up) max C* increase ratio-1: {inc:.3e}  (must be > 0)')
