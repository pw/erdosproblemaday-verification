#!/usr/bin/env python3
"""Theorem upper:finite (printed Thm A.1): compute F(r,k) from (A.1) literally and compare with
brute-force W_r(k) on tiny cases; check the boundary values W_r(1)=1, W_r(2)=r+1, W_1(k)=k.
W uses the paper's 1-based definition: least N such that every map [N]->[r] is constant on
some a, a+d, ..., a+(k-1)d with a,d >= 1, a+(k-1)d <= N.
CONTROL (must FAIL): the claim W_r(2) = r is rejected by the same brute force."""
import itertools
from functools import lru_cache

@lru_cache(None)
def F(r, k):
    if k == 1: return 1
    if k == 2: return r + 1
    m = 1
    for _ in range(r):
        m = 2 * m * F(r ** m, k - 1)
    return m

def has_mono(col, k):            # col: tuple indexed 1..N via col[n-1]
    N = len(col)
    for a in range(1, N + 1):
        for d in range(1, N + 1):
            if a + (k - 1) * d > N: break
            if all(col[a + j * d - 1] == col[a - 1] for j in range(k)): return True
    return False

def ramsey(N, r, k):
    return all(has_mono(col, k) for col in itertools.product(range(r), repeat=N))

def W(r, k, cap=12):
    for N in range(1, cap + 1):
        if ramsey(N, r, k): return N
    return None

print("F(r,k) small values:", {(r, k): F(r, k) for r in (1, 2) for k in (1, 2, 3)}, " F(1,4) =", F(1, 4))
res = []
for r in (1, 2, 3, 4):
    res.append((f"W_{r}(1)", W(r, 1), 1)); res.append((f"W_{r}(2)", W(r, 2), r + 1))
for k in (1, 2, 3, 4, 5):
    res.append((f"W_1({k})", W(1, k), k))
res.append(("W_2(3)", W(2, 3), 9))
for name, got, claim in res:
    print(f"{name}: brute force {got}, paper {claim}, {'OK' if got == claim else 'MISMATCH'}")
print("W_r(k) <= F(r,k):", all(W(r, k) <= F(r, k) for r, k in [(1, 3), (1, 4), (2, 3), (3, 2), (4, 2)]),
      "(W_2(3)=9 <= F(2,3)=%d)" % F(2, 3))
print("CONTROL claim W_r(2)=r:", ["rejected" if W(r, 2) != r else "ACCEPTED (bad)" for r in (1, 2, 3, 4)])
