import itertools, math, sys
import numpy as np
c = (36 - 5*math.sqrt(3))/66
def build(n, b, m):
    s = n - b; sizes = [b//m + (1 if i < b % m else 0) for i in range(m)]
    A = np.zeros((n, n), dtype=np.uint8); idx = s
    A[:s, s:] = 1; A[s:, :s] = 1
    for sz in sizes:
        A[idx:idx+sz, idx:idx+sz] = 1; idx += sz
    np.fill_diagonal(A, 0); return A, sizes
def brute_maxY(A):
    n = len(A); N = [int(''.join(map(str, A[i][::-1])), 2) for i in range(n)]; best = -1
    for a in range(n):
        for b in range(a+1, n):
            if not A[a][b]: continue
            for cc in range(b+1, n):
                if A[a][cc] and A[b][cc]:
                    y = (N[a] & N[b]) | (N[a] & N[cc]) | (N[b] & N[cc]); best = max(best, bin(y).count('1'))
    return best
def formula_maxY(n, b, m):
    s = n - b; sizes = [b//m + (1 if i < b % m else 0) for i in range(m)]
    return s + max(sizes)
def edges(n, b, m):
    s = n - b; sizes = [b//m + (1 if i < b % m else 0) for i in range(m)]
    return s*b + sum(x*(x-1)//2 for x in sizes)
for n in [40, 66, 90, 120]:
    best = None
    for m in range(2, 10):
        for b in range(n+1):
            if 4*edges(n, b, m) > n*n:
                f = formula_maxY(n, b, m)
                if best is None or f < best[0]: best = (f, m, b)
    f, m, b = best; A, sizes = build(n, b, m); bm = brute_maxY(A)
    print(f"n={n}: best m={m} b={b} sizes={sizes} e={edges(n,b,m)} > n^2/4={n*n/4}; max|Y+| formula={f} brute={bm} ratio={f/n:.5f}  c*={c:.5f}")
for n in [10**3, 10**4, 10**5, 10**6]:
    res = {}
    for m in [5, 6, 7]:
        # smallest admissible max|Y+| for this m: scan b near alpha_m n
        am = m/(2*m-1)*(1+1/math.sqrt(2*m)); lo = int(am*n) - 3*m - 5
        cands = [(formula_maxY(n, b, m), b) for b in range(max(lo, 0), min(n, lo + 6*m + 20)) if 4*edges(n, b, m) > n*n]
        res[m] = min(cands)[0]/n
    print(f"n={n}: min max|Y+|/n  m=5 {res[5]:.6f}  m=6 {res[6]:.6f}  m=7 {res[7]:.6f}   c*={c:.6f}  (|Y|=|Y+|-3)")
