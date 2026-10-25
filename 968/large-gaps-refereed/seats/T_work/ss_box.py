# Seat T numeric 1: singular-series box means (Lemma 5.4), s = 2, 3.
# Sum over ORDERED DISTINCT tuples with x_i in box I_i of S({x}), normalised by h^s (as in Lemma 5.4).
import numpy as np, sys, math
def primes_upto(n):
    s = np.ones(n+1, bool); s[:2] = False
    for i in range(2, int(n**0.5)+1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]
PT = primes_upto(10**7)
def tail_const(s, P):
    # prod_{p>P} (1-s/p)(1-1/p)^{-s}  (generic factor), numeric to 1e7 + analytic remainder ~ exp(-C(s,2) sum 1/p^2)
    p = PT[PT > P].astype(float)
    lg = np.sum(np.log1p(-s/p) - s*np.log1p(-1/p))
    # remainder beyond 1e7: log factor ~ -(s(s-1)/2)/p^2 ; sum_{p>1e7} 1/p^2 ~ 1/(1e7 ln 1e7)
    lg += -(s*(s-1)/2)/(1e7*math.log(1e7))
    return math.exp(lg)
def S_tuples(T, P):
    # T: (n, s) int array of distinct entries; exact local factors for p<=P, times generic tail beyond P (valid if P > diameter)
    n, s = T.shape
    logS = np.zeros(n)
    zero = np.zeros(n, bool)
    for p in PT[PT <= P]:
        R = np.sort(T % p, axis=1)
        nu = 1 + np.sum(R[:, 1:] != R[:, :-1], axis=1)
        fac = 1 - nu/p
        zero |= (fac <= 0)
        logS += np.log(np.where(fac > 0, fac, 1.0)) - s*math.log(1-1/p)
    out = np.exp(logS) * tail_const(s, P)
    out[zero] = 0.0
    return out
def box_sum(boxes, h):
    s = len(boxes)
    grids = np.meshgrid(*[np.arange(b0, b0+h) for b0 in boxes], indexing='ij')
    T = np.stack([g.ravel() for g in grids], axis=1)
    ok = np.ones(len(T), bool)
    for i in range(s):
        for j in range(i+1, s):
            ok &= T[:, i] != T[:, j]
    T = T[ok]
    P = int(T.max() - T.min()) + 2
    tot = 0.0
    for chunk in np.array_split(T, max(1, len(T)//2_000_000)):
        tot += S_tuples(chunk, P).sum()
    return tot / h**s
print("s  boxes(starts)         h     normalised_sum   1-mean   (log h)/h")
for h in [25, 50, 100, 200, 400]:
    I0, J0 = h+1, 1
    for name, boxes in [("I,I", [I0, I0]), ("J,I", [J0, I0])]:
        v = box_sum(boxes, h)
        print(f"2  {name:20s} {h:5d}   {v:.6f}       {1-v:+.5f}  {math.log(h)/h:.5f}", flush=True)
for h in [25, 50, 100, 150]:
    I0, J0 = h+1, 1
    for name, boxes in [("I,I,I", [I0, I0, I0]), ("J,I,I", [J0, I0, I0]), ("J,J,I", [J0, J0, I0])]:
        v = box_sum(boxes, h)
        print(f"3  {name:20s} {h:5d}   {v:.6f}       {1-v:+.5f}  {math.log(h)/h:.5f}", flush=True)
