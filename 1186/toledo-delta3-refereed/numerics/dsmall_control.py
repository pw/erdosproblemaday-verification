"""Positive control for the discrete search: exhaustive V(n) for n<=16 vs SA/tabu on the same W."""
import itertools, numpy as np
from common import ap_W, count_mono_brute
import qlib
for n in range(8, 17):
    W, T = ap_W(n); M = np.ascontiguousarray(W.astype(float))
    # exhaustive via the quadratic form, fixing x_0 = +1 (colour symmetry)
    X = np.array(list(itertools.product([-1.0, 1.0], repeat=n - 1)))
    X = np.hstack([np.ones((len(X), 1)), X])
    V = (T + np.einsum("ij,jk,ik->i", X, M, X) / 2) / 4
    vmin = int(round(V.min())); arg = X[np.argmin(V)]
    assert count_mono_brute([int(c) for c in arg]) == vmin
    best = min(int(round((T + qlib.sa(M, np.random.default_rng(s).choice([-1.0, 1.0], n), s, 3000 * n, 20.0, 0.05, 0.1, max(2, n // 4))[1] / 2) / 4)) for s in range(10))
    bt = min(int(round((T + qlib.tabu(M, np.random.default_rng(s).choice([-1.0, 1.0], n), s, 300 * n, 2, 2)[1] / 2) / 4)) for s in range(10))
    print(f"n={n}: exhaustive min V={vmin}  SA best(10 runs)={best}  tabu best(10 runs)={bt}")
