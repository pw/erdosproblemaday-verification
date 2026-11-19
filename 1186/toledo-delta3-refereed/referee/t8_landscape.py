# Direct test of Theorem 2: minimise Q over [-1,1]-valued step functions on an N-cell grid by coordinate descent.
import numpy as np, time, sys
N = int(sys.argv[1]); budget = float(sys.argv[2])
idx = np.arange(N+1)
X0, Y0 = np.meshgrid(idx[:-1], idx[:-1], indexing='ij'); X1, Y1 = X0+1, Y0+1
def Gb(x, y): return np.where(x <= 2*y, x*x, 4*(x*y - y*y)).astype(np.int64)
def Ga(x, y):
    t = np.minimum(x, np.maximum(0, 2*y - N)); return (4*t*y - 2*t*N - t*t).astype(np.int64)
ra = lambda G: G(X1, Y1) - G(X0, Y1) - G(X1, Y0) + G(X0, Y0)
A4 = 4 - ra(Gb) - ra(Ga)
A = A4.astype(float)/(4*N*N)
S = A + A.T
target = -5/137
B = [28, 6, 28, 37, 59, 116, 116, 59, 37, 28, 6, 28]
def blockfun(lengths, N):
    tot = sum(lengths); edges = np.cumsum([0]+lengths)/tot*N
    phi = np.empty(N); c = (np.arange(N)+0.5)
    for i in range(len(lengths)): phi[(c >= edges[i]) & (c < edges[i+1])] = 1 if i % 2 == 0 else -1
    return phi
def Q(phi): return phi@A@phi
def descend(phi, sweeps=200):
    g = S@phi
    for sw in range(sweeps):
        change = 0.0
        for k in np.random.permutation(N):
            akk = A[k, k]; c = g[k] - 2*akk*phi[k]
            new = np.clip(-c/(2*akk), -1, 1) if akk > 0 else (-np.sign(c) if c != 0 else phi[k])
            dlt = new - phi[k]
            if dlt != 0:
                g += S[:, k]*dlt; phi[k] = new; change += abs(dlt)
        if change < 1e-12: break
    return phi
rng = np.random.default_rng(7)
np.random.seed(7)
phistar = blockfun(B, N)
print('N', N, 'Q(phi* on grid) =', Q(phistar), ' target', target)
best = (1.0, None); results = []
t0 = time.time(); runs = 0
while time.time() - t0 < budget:
    kind = runs % 4
    if kind == 0: phi = rng.choice([-1.0, 1.0], N)
    elif kind == 1: phi = rng.uniform(-1, 1, N)
    elif kind == 2:
        nb = rng.integers(2, 25); phi = blockfun(list(rng.integers(1, 100, nb)), N)
    else:
        phi = phistar.copy(); m = rng.integers(1, 60); pos = rng.integers(0, N-m); phi[pos:pos+m] *= -1
        phi = np.clip(phi + 0.3*rng.standard_normal(N)*(rng.random() < 0.5), -1, 1)
    phi = descend(phi)
    q = Q(phi); results.append(q); runs += 1
    dist = min(np.abs(phi - phistar).mean(), np.abs(phi + phistar).mean())
    if q < best[0]: best = (q, dist)
results = np.array(results)
print('runs', runs, ' best Q found = %.12f (target %.12f), excess %.3e, L1/2 dist of best to ±phi* %.4f' % (best[0], target, best[0]-target, best[1]))
print('fraction of runs within 1e-9 of target:', np.mean(results < target + 1e-9), '  any below target - 1e-12:', np.any(results < target - 1e-12))
srt = np.sort(results); print('lowest 10 excesses:', ['%.2e' % (x - target) for x in srt[:10]])
