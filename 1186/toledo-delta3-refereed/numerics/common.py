"""Shared exact/float machinery for the erdos1186 referee numerics (own code)."""
from fractions import Fraction as F
import numpy as np

BLOCKS = [28, 6, 28, 37, 59, 116, 116, 59, 37, 28, 6, 28]   # out of 548
assert sum(BLOCKS) == 548

def phistar_breaks():
    t = [F(0)]
    for L in BLOCKS:
        t.append(t[-1] + F(L, 548))
    signs = [1 if i % 2 == 0 else -1 for i in range(12)]
    return t, signs

# ---------- route A: exact area of R ∩ [a0,a1]x[b0,b1] by integrating section length ----------
def section_len(a, b0, b1):
    lo = max(b0, a / 2)
    hi = min(b1, (1 + a) / 2)
    return max(F(0) if isinstance(a, F) else 0.0, hi - lo)

def rect_area(a0, a1, b0, b1):
    pts = {a0, a1}
    for p in (2 * b0 - 1, 2 * b1 - 1, 2 * b0, 2 * b1):
        if a0 < p < a1:
            pts.add(p)
    pts = sorted(pts)
    tot = 0
    for u, v in zip(pts, pts[1:]):
        tot += (v - u) * (section_len(u, b0, b1) + section_len(v, b0, b1)) / 2
    return tot

def Q_step(breaks, signs):
    """Q for step function with value signs[i] on [breaks[i],breaks[i+1]] (exact if Fractions)."""
    k = len(signs)
    tot = 0
    for i in range(k):
        for j in range(k):
            if signs[i] * signs[j] == 0:
                continue
            tot += signs[i] * signs[j] * rect_area(breaks[i], breaks[i + 1], breaks[j], breaks[j + 1])
    return tot

# ---------- route B: grid matrix. A_ij = h^2 (G(N-m) - G(-m)), m = 2j - i, cell coords ----------
def Gcdf4(c):
    """4 * P(2t - s <= c) for s,t ~ U[0,1], integer c."""
    c = np.asarray(c)
    return np.where(c <= -1, 0, np.where(c == 0, 1, np.where(c == 1, 3, 4)))

def grid_K(N):
    """Integer matrix K with K = 4 N^2 A, A_ij = area(R ∩ cell_i x cell_j) (i = a-cell, j = b-cell)."""
    i = np.arange(N)[:, None]
    j = np.arange(N)[None, :]
    m = 2 * j - i
    return (Gcdf4(N - m) - Gcdf4(-m)).astype(np.int64)

def grid_S2(N):
    """2K symmetrised: S2 = K + K^T, so Q = x^T S2 x / (8 N^2)."""
    K = grid_K(N)
    return K + K.T

def phistar_grid(N):
    assert N % 548 == 0
    r = N // 548
    x = []
    for idx, L in enumerate(BLOCKS):
        x += [1 if idx % 2 == 0 else -1] * (L * r)
    return np.array(x, dtype=np.int64)

def blocks_of(x, tol=0.0):
    """Run-length encode a +-1 (or rounded) vector: list of (sign, length)."""
    s = np.sign(np.where(np.abs(x) <= tol, 0, x)).astype(int)
    out = []
    for v in s:
        if out and out[-1][0] == v:
            out[-1][1] += 1
        else:
            out.append([int(v), 1])
    return [(a, b) for a, b in out]

# ---------- discrete 3-AP machinery ----------
def count_mono_brute(col):
    """col: sequence of +-1 for elements 1..n (index 0..n-1). Count {a,a+d,a+2d}, d>=1 monochromatic."""
    n = len(col)
    c = np.asarray(col)
    tot = 0
    for d in range(1, (n - 1) // 2 + 1):
        a = c[: n - 2 * d]
        b = c[d: n - d]
        e = c[2 * d:]
        tot += int(np.sum((a == b) & (b == e)))
    return tot

def ap_W(n):
    """W_uv = # 3-APs containing both u and v (u != v), 0-indexed, plus T = # 3-APs."""
    W = np.zeros((n, n), dtype=np.int64)
    T = 0
    for d in range(1, (n - 1) // 2 + 1):
        a = np.arange(0, n - 2 * d)
        b = a + d
        e = a + 2 * d
        T += len(a)
        np.add.at(W, (a, b), 1); np.add.at(W, (b, a), 1)
        np.add.at(W, (b, e), 1); np.add.at(W, (e, b), 1)
        np.add.at(W, (a, e), 1); np.add.at(W, (e, a), 1)
    return W, T
# V(x) = (T + x^T W x / 2) / 4 for x in {+-1}^n
