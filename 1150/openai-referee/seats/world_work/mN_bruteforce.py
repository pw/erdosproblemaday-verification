"""Brute-force m_N = min over eps in {±1}^N of max_{|z|=1} |sum eps_k z^k| / sqrt(N), N <= NMAX.
Rigour: f = |P(e^{i th})|^2 is a real trig poly of degree n = N-1 with max S^2 at th*, f'(th*) = 0, ||f''|| <= n^2 S^2 (Bernstein
twice). Every point is within pi/M of a grid point, so grid max g satisfies g^2 >= S^2 (1 - n^2 pi^2 / (2 M^2)).
Stage 1 (all 2^(N-1) vectors with eps_0=+1, M=1024 grid on the half circle via rfft): U = min_P g(P)/sqrt(1-r) >= min sup;
  candidates = {P : g(P) <= U}  (every non-candidate has sup >= g > U >= min sup, so cannot be a minimiser).
Stage 2 (candidates): fine grid M2 = 2^16 + golden-section refinement of the top grid maxima -> exact sup to ~1e-12,
  bracket [refined local max, g_fine/sqrt(1-r2)].
"""
import sys, itertools, math, time
import numpy as np

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20
M = 1024
M2 = 1 << 16

def signs_block(N, start, count):
    idx = np.arange(start, start + count, dtype=np.int64)
    bits = ((idx[:, None] >> np.arange(N - 1)) & 1).astype(np.float64)
    E = np.empty((count, N)); E[:, 0] = 1.0; E[:, 1:] = 1.0 - 2.0 * bits
    return E

def absP2(eps, th):
    k = np.arange(len(eps))
    z = np.exp(1j * np.outer(th, k))
    return np.abs(z @ eps) ** 2

def exact_sup(eps):
    n = len(eps) - 1
    vals = np.abs(np.fft.rfft(eps, M2)) ** 2          # theta in [0, pi], step 2pi/M2
    gfine = math.sqrt(vals.max())
    r2 = (n * math.pi / M2) ** 2 / 2
    upper = gfine / math.sqrt(1 - r2)
    # refine around the top local maxima
    best = 0.0
    loc = np.argsort(vals)[-8:]
    h = 2 * math.pi / M2
    for j in loc:
        a, b = (j - 1) * h, (j + 1) * h
        gr = (math.sqrt(5) - 1) / 2
        for _ in range(60):
            c = b - gr * (b - a); d = a + gr * (b - a)
            fc, fd = absP2(eps, np.array([c, d]))
            if fc > fd: b = d
            else: a = c
        best = max(best, math.sqrt(absP2(eps, np.array([(a + b) / 2]))[0]))
    return max(best, gfine), upper

out = []
for N in range(1, NMAX + 1):
    t0 = time.time()
    n = N - 1
    r = (n * math.pi / M) ** 2 / 2
    total = 1 << (N - 1)
    B = 1 << 14
    gmins = []
    allg = np.empty(total)
    for s in range(0, total, B):
        c = min(B, total - s)
        E = signs_block(N, s, c)
        F = np.abs(np.fft.rfft(E, M, axis=1)) ** 2
        allg[s:s + c] = np.sqrt(F.max(axis=1))
    U = allg.min() / math.sqrt(1 - r)
    cand = np.nonzero(allg <= U)[0]
    res = []
    for ci in cand:
        eps = signs_block(N, int(ci), 1)[0]
        lo, hi = exact_sup(eps)
        res.append((lo, hi, eps))
    res.sort(key=lambda x: x[0])
    lo, hi, eps = res[0]
    # number of minimisers among eps_0=+1 vectors (ties within 1e-9)
    nmin = sum(1 for x in res if x[0] <= lo + 1e-9)
    s = ''.join('+' if e > 0 else '-' for e in eps)
    line = (f"N={N:2d} deg={n:2d}  min sup|P| in [{lo:.9f}, {min(hi, lo + 1e-6) if hi < lo else hi:.9f}]  "
            f"m_N={lo/math.sqrt(N):.7f}  m_N^2*N={lo*lo:.6f}  #cand={len(cand)} #minimisers(eps0=+1)={nmin}  "
            f"example={s}  ({time.time()-t0:.1f}s)")
    print(line, flush=True)
    out.append((N, lo, hi, s))
