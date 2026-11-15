"""Referee misc checks.
1. Key Lemma (CLAIMS sec K): a+b+2c=k, a,b,c in X, a!=b solvable iff k != 3^j-1 -- brute force over X, k <= 40000.
2. Theorem B(2) construction for j = 3..60 in exact integers: n = 2*3^j = 12 + 16 + (2a+1) + (2b+1).
   Also the base-3 digits of 3^j - 15.
3. Third route for Theorem B: plain itertools enumeration of subsets of size <= 4, N = 1500.
4. Lower-bound example A = {n = 0,1 mod m}: restricted order exactly m-1 (exceptions for <= m-2 and <= m-1),
   by exact layered DP over distinct elements (set-of-sums per count), n <= Nm.
"""
from itertools import combinations

def inX(v):
    while v:
        if v % 3 == 2: return False
        v //= 3
    return True

def base3(v):
    s = ''
    while v: s = str(v % 3) + s; v //= 3
    return s or '0'

# 1
KMAX = 40000
X = [x for x in range(KMAX + 1) if inX(x)]
Xs = set(X)
import numpy as np
Xa = np.array(X)
D = np.zeros(KMAX + 1, bool)          # D[s]: s = a + b with a != b in X
for a in X:
    t = a + Xa[(Xa != a) & (a + Xa <= KMAX)]
    D[t] = True
solv = np.zeros(KMAX + 1, bool)
for c in X:
    if 2 * c > KMAX: break
    solv[2 * c:] |= D[:KMAX + 1 - 2 * c]
unsolv = [k for k in range(KMAX + 1) if not solv[k]]
pred = [3 ** j - 1 for j in range(0, 12) if 3 ** j - 1 <= KMAX]
print("1. Key Lemma: unsolvable k <=", KMAX, ":", unsolv, "| predicted 3^j-1:", pred, "MATCH" if unsolv == pred else "MISMATCH")

# 2
ok = True
for j in range(3, 61):
    n = 2 * 3 ** j
    t = 3 ** j - 15
    d = base3(t)
    expect = '2' * (j - 3) + '110'
    if d != expect: ok = False; print("digit mismatch", j, d)
    a = b = 0; p = 1; v = t
    while v:
        dg = v % 3
        if dg == 2: a += p; b += p
        elif dg == 1: a += p
        v //= 3; p *= 3
    parts = [12, 16, 2 * a + 1, 2 * b + 1]
    if not (inX(a) and inX(b) and a != b and sum(parts) == n and len(set(parts)) == 4 and inX(3) and inX(4)):
        ok = False; print("construction fails", j)
print("2. B(2) construction j=3..60 and 3^j-15 = 2..2110_3:", "OK" if ok else "FAIL")

# 3
N = 1500
A = sorted(set([2 * x + 1 for x in X if 2 * x + 1 <= N] + [4 * x for x in X if x >= 1 and 4 * x <= N]))
cover = {t: set() for t in range(1, 5)}
for t in range(1, 5):
    for S in combinations(A, t):
        s = sum(S)
        if s <= N: cover[t].add(s)
le3 = cover[1] | cover[2] | cover[3]
le4 = le3 | cover[4]
print("3. itertools N=1500: exc<=3 =", [n for n in range(1, N + 1) if n not in le3],
      " exc<=4 =", [n for n in range(1, N + 1) if n not in le4])

# 4
for m in range(2, 9):
    Nm = 60 * m * m
    Am = [x for x in range(1, Nm + 1) if x % m in (0, 1)]
    layers = [set([0])] + [set() for _ in range(m)]
    for e in Am:  # 0/1 knapsack on sets, distinct elements
        for t in range(m, 0, -1):
            layers[t] |= {s + e for s in layers[t - 1] if s + e <= Nm}
    upto = lambda T: set().union(*layers[1:T + 1])
    em1 = [n for n in range(1, Nm + 1) if n not in upto(m - 1)]
    em2 = [n for n in range(1, Nm + 1) if n not in upto(m - 2)] if m >= 3 else ['(m-2=0: every n)']
    tail = [n for n in em2 if isinstance(n, int) and n > Nm // 2]
    print(f"4. m={m}: exceptions for <= m-1 = {em1[:12]}{'...' if len(em1) > 12 else ''} (max {max(em1) if em1 else None});"
          f" exceptions for <= m-2 in upper half [{Nm//2},{Nm}]: {len(tail)} (all = -1 mod m: {all(n % m == m - 1 for n in tail)})")
