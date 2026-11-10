#!/usr/bin/env python3
# thm2_check.py — referee numerics for Theorem 2 (density of moves). Own sieve; uses the
# (proved, checked) jump rule: for m = kQ, Q prime > k (<=> Q^2 > m), k >= 2, with n = m-1,
#   A = no prime p != Q has e_n(p) = k,  B = no prime p != Q has e_n(p) = k-1;  up iff A&~B, down iff B&~A.
# Large primes (p > isqrt(n)) via windows; primes p <= isqrt(n) handled EXACTLY (Legendre) whenever
# k >= isqrt(n) - 1 (the only case where they can hold k or k-1).
import numpy as np, math, time, sys
X = 10**9
t0 = time.time()
size = X // 2 + 1
s = np.ones(size, dtype=bool); s[0] = False
for i in range(1, (math.isqrt(X) - 1) // 2 + 1):
    if s[i]:
        p = 2 * i + 1
        s[p * p // 2::p] = False
P = np.concatenate((np.array([2], dtype=np.int64), 2 * np.nonzero(s)[0].astype(np.int64) + 1))
P = P[P <= X]
del s
assert len(P) == 50847534, len(P)      # pi(10^9)
print("sieve ok", round(time.time() - t0), "s", flush=True)
pi = lambda x: np.searchsorted(P, x, side='right')

def leg(n, p):
    e = 0; t = p
    while t <= n: e += n // t; t *= p
    return e

def block(lo, hi, perk=False, Lk=0):
    up = down = 0; exc = 0
    per = {}
    K = math.isqrt(hi)
    for k in range(2, K + 1):
        a = max(k, lo // k); b = hi // k
        if b <= a: continue
        i0, i1 = int(pi(a)), int(pi(b))
        if i1 <= i0: continue
        Q = P[i0:i1]; idx = np.arange(i0, i1, dtype=np.int64)
        n = k * Q - 1
        r = np.floor(np.sqrt(n.astype(np.float64))).astype(np.int64)
        r -= (r * r > n); r += ((r + 1) * (r + 1) <= n)
        leftA = np.maximum(n // (k + 1), r)
        cntA = idx - pi(leftA)                       # primes in (leftA, Q-1]  (pi(Q-1) = idx)
        cntA = np.maximum(cntA, 0)
        cntB = pi(n // (k - 1)) - (idx + 1)          # primes in (Q, n//(k-1)]
        A = cntA == 0; B = cntB == 0
        ex = np.nonzero(k >= r - 1)[0]
        for j in ex:                                 # exact small-prime fix-up
            exc += 1
            nn = int(n[j]); rr = int(r[j])
            lo_p = nn // (k + 1)                     # small p with floor(n/p) <= k must exceed n/(k+1)
            for p in P[int(pi(lo_p)):int(pi(rr))]:
                v = leg(nn, int(p))
                if v == k: A[j] = False
                if v == k - 1: B[j] = False
        u = int(np.count_nonzero(A & ~B)); d = int(np.count_nonzero(B & ~A))
        up += u; down += d
        if perk and k <= Lk:
            per[k] = (u + d, int(np.count_nonzero(A | B)), len(Q))
        elif perk:
            per.setdefault('big', [0, 0]); per['big'][0] += u + d
    return up, down, exc, per

# 1) decade (1e8, 1e9] vs bf_1e9.log
u, d, exc, _ = block(10**8, 10**9)
print("decade (1e8,1e9]: up=%d down=%d moves=%d share=%.4f%%  exceptional-k rows=%d  (%ds)"
      % (u, d, u + d, 100 * (u + d) / 9e8, exc, round(time.time() - t0)), flush=True)
print("bf_1e9.log      : up=%d down=%d" % (22410411 - 2420609, 22392178 - 2414440), flush=True)

# 2) dyadic block (N, 2N], N = 5e8: per-k counts for k <= L, vs 4k+4
N = 5 * 10**8
L = int(math.sqrt(N / math.log(N)))
u, d, exc, per = block(N, 2 * N, perk=True, Lk=L)
small = sum(v[0] for k, v in per.items() if k != 'big')
big = per['big'][0]
print("block (5e8,1e9]: L=%d  moves=%d  k<=L: %d (%.3f%% of steps)  k>L: %d (%.3f%%)"
      % (L, u + d, small, 100 * small / N, big, 100 * big / N))
viol = [(k, v) for k, v in per.items() if k != 'big' and v[1] > 4 * k + 4]
print("k<=L with #(A or B) > 4k+4:", viol[:10], "count", len(viol))
first = min([k for k, v in per.items() if k != 'big' and v[0] > 0] or [None])
print("smallest k with a move:", first)
worst = max(((v[1] / (4 * k + 4), k, v) for k, v in per.items() if k != 'big'))
print("max over k<=L of #(A or B)/(4k+4) = %.4f at k=%d %s" % worst)
for k in (2, 100, 500, 1000, 1500, 2000, 3000, 4000, L):
    if k in per: print("  k=%d moves=%d #(AvB)=%d #Q=%d 4k+4=%d" % (k, per[k][0], per[k][1], per[k][2], 4 * k + 4))
print("time", round(time.time() - t0), "s")
