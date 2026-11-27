"""Clean-room evaluator for the continuous minimum-overlap objective of a step function.

Setup (White 2022 eq (1.1), shifted to [0,2)): f = a_i/D on cell i = [i w,(i+1) w), w = 2/N,
g = 1 - f on [0,2), both zero outside. H(s) = int f(t) g(t-s) dt.
Each cell pair (i,j) contributes a_i (D-a_j)/D^2 * w * tent(s/w - (i-j)), tent(t)=max(0,1-|t|),
so H is piecewise linear with breakpoints exactly at s = k w, and H(k w) = w T_k / D^2 with
T_k = sum_i a_i (D - a_{i-k}).
Route here: limb-split int64 np.convolve of a against reversed b = D - a (NOT the
autocorrelation identity, NOT Kronecker packing), recombined in Python ints.
"""
import numpy as np
from fractions import Fraction as F

def exact_T(a, D):
    """Return dict k -> T_k (exact Python ints) for -N < k < N, plus zeros at |k| = N.
    Generic limb split: 20-bit limbs, int64 np.convolve per limb pair (products < 2^40, sums < 2^54)."""
    N = len(a)
    b = [D - x for x in a]
    LB = 20
    assert N < (1 << 14), "int64 headroom assumes N < 2^14"
    nl = max(1, (max(D, 1).bit_length() + LB - 1) // LB)
    def limbs(v):
        return [np.array([(x >> (LB * t)) & ((1 << LB) - 1) for x in v], dtype=np.int64) for t in range(nl)]
    Al = limbs(a); Bl = limbs(b[::-1])
    acc = [0] * (2 * N - 1)
    for p_ in range(nl):
        for q_ in range(nl):
            c = np.convolve(Al[p_], Bl[q_])
            assert c.min() >= 0 and c.max() < (1 << 62)
            sh = LB * (p_ + q_)
            for m in range(2 * N - 1):
                acc[m] += int(c[m]) << sh
    T = {m - (N - 1): acc[m] for m in range(2 * N - 1)}   # c[N-1+k] = sum_i a_i b_{i-k}
    T[-N] = 0; T[N] = 0
    return T

def T_direct(a, D, k):
    """Pure-Python definition-level sum for one lag (cross-check)."""
    N = len(a)
    return sum(a[i] * (D - a[i - k]) for i in range(N) if 0 <= i - k < N)

def side_conditions(a, D):
    N = len(a)
    errs = []
    if not all(type(x) is int for x in a): errs.append("non-integer height")
    if not all(0 <= x <= D for x in a): errs.append("height outside [0,D]")
    if 2 * sum(a) != N * D: errs.append(f"mass != 1: integral = {F(2*sum(a), N*D)}")
    return errs

def scores(a, D):
    N = len(a)
    T = exact_T(a, D)
    scale = F(2, N * D * D)
    mx = max(T.values())
    argmax = sorted(k for k, v in T.items() if v == mx)
    return T, mx, argmax, scale

def H_direct_exact(a, D, s):
    """Direct exact integral of f(t) g(t-s) dt by merging the two step partitions (independent of tent formula)."""
    N = len(a); w = F(2, N)
    # f breakpoints: i*w ; g(t-s) breakpoints: s + j*w
    pts = set(F(i) * w for i in range(N + 1)) | set(s + F(j) * w for j in range(N + 1))
    pts = sorted(p for p in pts if F(0) <= p <= F(2))
    tot = F(0)
    for lo, hi in zip(pts, pts[1:]):
        if hi <= lo: continue
        mid = (lo + hi) / 2
        i = int(mid / w)
        if not (0 <= i < N): continue
        u = mid - s
        if not (F(0) <= u < F(2)): continue
        j = int(u / w)
        tot += F(a[i], D) * F(D - a[j], D) * (hi - lo)
    return tot

def H_fft_float(a, D):
    """float64 FFT cross-correlation at the vertices; returns array indexed k+N for k in [-N..N]."""
    N = len(a)
    f = np.array(a, dtype=np.float64) / D
    g = 1.0 - f
    L = 1
    while L < 2 * N: L *= 2
    Ff = np.fft.rfft(f, L); Gr = np.fft.rfft(g[::-1], L)
    c = np.fft.irfft(Ff * Gr, L)[:2 * N - 1]  # c[N-1+k] = sum_i f_i g_{i-k}
    out = np.zeros(2 * N + 1)
    out[1:2 * N] = c * (2.0 / N)
    return out
