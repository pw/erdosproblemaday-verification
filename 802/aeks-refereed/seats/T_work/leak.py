"""Seat T numerics: the leakage claim (4.8) with a general threshold theta (the paper's theta = x^-6/L),
the growth bound w(S_{i+1}) <= (1+L/theta) w(S_i), the exact conditional formula P(u in B | v) = e_w(B,N(v))/h_v,
and the conditioning bound behind H_R. Run single-threaded."""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1'); os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import numpy as np, sys
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 21)
worst = {}
def rec(k, v): worst[k] = max(worst.get(k, -np.inf), v)
def Hw(a, w):
    m = a > 0
    return float(np.sum(a[m] * np.log(w[m] / a[m])))
def peel(A, w, tau):
    A = A.copy()
    while True:
        C = (A * w) @ A
        bad = np.argwhere((A > 0) & (C < tau))
        if len(bad) == 0: return A
        u, v = bad[0]; A[u, v] = A[v, u] = 0
nontriv = 0
for t in range(300):
    n = int(rng.integers(8, 30))
    A = (rng.random((n, n)) < rng.uniform(0.15, 0.7)).astype(float); A = np.triu(A, 1); A = A + A.T
    w = np.exp(rng.normal(0, rng.uniform(0.3, 2.5), n))
    if A.sum() == 0: continue
    C0 = (A * w) @ A
    pos = C0[A > 0]
    if (pos > 0).sum() == 0: continue
    A = peel(A, w, max(np.quantile(pos[pos > 0], 0.05), 1e-9))
    if A.sum() == 0: continue
    Cc = (A * w) @ A; s = A @ w
    x = max(1.0, 1 / Cc[A > 0].min()); L = s.max()
    theta = rng.uniform(0.01, 0.5) / (x * x * L)
    R = 10
    h = np.array([np.sum(A[u] * w * Cc[u]) for u in range(n)])
    for v in np.where(A.sum(1) > 0)[0]:
        S = [A[v] > 0]
        for i in range(R):
            Si = S[-1]
            reach = A @ (w * Si)  # w(N(y) cap S_i)
            Snew = Si | (reach >= theta)
            rec('growth w(S_{i+1}) - (1+L/theta) w(S_i)', (w[Snew].sum() - (1 + L / theta) * w[Si].sum()) / w[Snew].sum())
            S.append(Snew)
        for u in np.where(A[v] > 0)[0]:
            N = np.where(A[u] > 0)[0]
            P = A[np.ix_(N, N)] * w[N][None, :] / Cc[u, N][:, None]
            Q = 0.5 * (np.eye(len(N)) + P)
            iv = list(N).index(v)
            row = P[iv].copy()
            for i in range(R + 1):
                out = ~S[i][N]
                leak = row[out].sum()
                bound = i * x * x * theta * L
                rec('(4.8) leak - i x^2 theta L', leak - bound)
                if leak > 0.2 * bound and bound > 0: nontriv += 1
                # conditioning bound behind H_R: H <= log2 + (1-d) log w(D) + d log w(Dc)
                D = ~out
                d = leak
                if 0 < d < 1 and D.any() and out.any():
                    rec('H_R conditioning bound', Hw(row, w[N]) - (np.log(2) + (1 - d) * np.log(w[N][D].sum()) + d * np.log(w[N][out].sum())))
                row = row @ Q
        # exact conditional formula for a random B subset N(v)
        Nv = np.where(A[v] > 0)[0]
        Bset = Nv[rng.random(len(Nv)) < 0.5]
        lhs = sum(w[u] * Cc[u, v] for u in Bset) / h[v]
        e = sum(w[u] * w[np.where((A[u] > 0) & (A[v] > 0))[0]].sum() for u in Bset) / h[v]
        rec('P(u in B|v) = e(B,N(v))/h_v', abs(lhs - e))
print('nontrivial leak instances (leak > 20% of bound):', nontriv)
for k, v in worst.items():
    print(f'{v: .3e}  {k}')
