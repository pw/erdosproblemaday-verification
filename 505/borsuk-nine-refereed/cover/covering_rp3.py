#!/usr/bin/env python3
"""Covering radius of n lines in R^4 (points of RP^3), angle metric between lines.
Why it matters: if n lines have covering radius rho < 45deg, the n 'Voronoi caps' {x : angle(x, c_i) <= rho'} (rho < rho' < 45deg)
cover RP^3 and two lines in one cap meet at angle < 90deg, so the projector image X_4 is covered by n sets of diameter < sqrt2.
  n = 10 with rho < 45deg would CONTRADICT OpenAI's Theorem 1.1 (b(X_4) > 10).
  n = 11 with rho < 45deg gives b(X_4) <= 11, i.e. b(X_4) = 11 exactly given Theorem 1.1.
Exact covering radius of a configuration: convex hull of the 2n unit vectors {+-c_i}; every facet with unit outward normal u and
offset h has its vertices at angle arccos(h) from u and no centre closer (u is a deep-hole candidate); rho = arccos(min_f h_f).
Search: smooth max-min ascent over sample points, many random restarts, then exact evaluation."""
import numpy as np, sys, json
from scipy.spatial import ConvexHull
def exact_radius(C):
    C = C / np.linalg.norm(C, axis=1, keepdims=True)
    P = np.vstack([C, -C]); H = ConvexHull(P)
    h = -H.equations[:, -1]          # equations: n.x + b <= 0 inside, |n|=1 -> offset = -b
    return float(np.degrees(np.arccos(np.clip(h.min(), -1, 1)))), H
def ascend(n, rng, iters=1500, ns=40000):
    C = rng.standard_normal((n, 4)); C /= np.linalg.norm(C, axis=1, keepdims=True)
    X = rng.standard_normal((ns, 4)); X /= np.linalg.norm(X, axis=1, keepdims=True)
    lr = 0.05
    for t in range(iters):
        b1 = 20 + 380 * t / iters; b2 = 20 + 980 * t / iters
        D = X @ C.T; S = D * D
        A = b1 * S; A -= A.max(1, keepdims=True); p = np.exp(A); p /= p.sum(1, keepdims=True)
        m = (S * p).sum(1)          # approx max_i s_xi
        B = -b2 * m; B -= B.max(); w = np.exp(B); w /= w.sum()
        G = 2 * ((w[:, None] * p * D).T @ X)  # gradient wrt C rows
        G -= (G * C).sum(1, keepdims=True) * C
        C += lr * G / (np.linalg.norm(G) + 1e-12) * (1 - t / iters + 0.02)
        C /= np.linalg.norm(C, axis=1, keepdims=True)
        if t % 300 == 299:  # refresh samples near current deep holes
            r, H = exact_radius(C)
            U = H.equations[:, :4]; X = np.vstack([X[:ns // 2], U, rng.standard_normal((ns // 2 - len(U) if ns // 2 > len(U) else 0, 4))])
            X /= np.linalg.norm(X, axis=1, keepdims=True)
    return C
if __name__ == '__main__':
    n = int(sys.argv[1]); restarts = int(sys.argv[2]); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    rng = np.random.default_rng(seed); best = (99, None)
    for k in range(restarts):
        C = ascend(n, rng); r, _ = exact_radius(C)
        if r < best[0]: best = (r, C.copy())
        print(f'n={n} restart={k} radius={r:.4f} best={best[0]:.4f}', flush=True)
    json.dump({'n': n, 'radius_deg': best[0], 'centres': best[1].tolist()}, open(f'cover_n{n}_seed{seed}.json', 'w'))
    print('BEST', n, best[0])
