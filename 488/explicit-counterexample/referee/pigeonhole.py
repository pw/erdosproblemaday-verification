# (a) exact H(j) for small j (real S = odd primes < 257), check H(j) <= (8j+1)^53;
# (b) small analogue (S={3,5,7,11,13}, base 16): exact H, bound (4j+1)^5, first slow step, analogue endpoint_gap;
# (c) rigorous lattice-count brackets  Hc(j) <= H(j) <= Hf(j)  via integer knapsack DP with floored / ceiled
#     log2-weights at resolution R, to locate the (unspecified) slow step k for the real construction.
import sys, numpy as np
from math import log2, floor, ceil, prod
from bisect import bisect_right
sys.setrecursionlimit(10000)

def primes_below(n):
    s = bytearray([1])*n; s[0]=s[1]=0
    for i in range(2,int(n**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(n) if s[i]]

def count_smooth(X, S):   # exact #{d in [1,X] : all prime factors of d in S}, S sorted ascending
    def rec(X, i):        # primes S[0..i]
        if X < 1: return 0
        i = min(i, bisect_right(S, X) - 1)
        if i < 0: return 1
        if i == 0:
            c, y = 0, 1
            while y <= X: c, y = c+1, y*S[0]
            return c
        tot, pe = 0, 1
        while pe <= X:
            tot += rec(X // pe, i-1); pe *= S[i]
        return tot
    return rec(X, len(S)-1)

S = [p for p in primes_below(257) if p != 2]
print("(a) exact H(j), real S (53 odd primes < 257)")
Hex = {}
for j in range(0, 5):
    Hex[j] = count_smooth(256**j, S)
    print(f"   H({j}) = {Hex[j]}   <= (8j+1)^53: {Hex[j] <= (8*j+1)**53}" + (f"   ratio H({j})/H({j-1}) = {Hex[j]/Hex[j-1]:.3f}" if j else ""))

print("(b) small analogue S={3,5,7,11,13}, base 16")
Ss = [3,5,7,11,13]; Hs = [count_smooth(16**j, Ss) for j in range(0, 40)]
assert all(Hs[j] <= (4*j+1)**5 for j in range(40)); print("   H_s(j) <= (4j+1)^5 for j<40: True")
ks = next(k for k in range(39) if 2*Hs[k+1] <= 3*Hs[k])
N = next(N for N in range(1, 10**5) if 2**N * (4*N+1)**5 < 3**N)
print(f"   first slow step k={ks} (H_s={Hs[ks]}, H_s(k+1)={Hs[ks+1]}); analogue endpoint_gap first holds at N={N}; k < N: {ks < N}")
print("   ratios:", [round(Hs[j+1]/Hs[j], 3) for j in range(0, 16)])

print("(c) rigorous brackets for the real H(j) via integer-weight knapsack counts")
def dp_counts(weights, B, exact=False):
    c = np.zeros(B+1, dtype=object if exact else np.float64); c[0] = 1
    for w in weights:
        n = (B + 1 + w - 1)//w*w
        pad = np.zeros(n, dtype=c.dtype); pad[:B+1] = c
        pad = pad.reshape(-1, w).cumsum(axis=0).reshape(-1)
        c = pad[:B+1]
    return np.cumsum(c)          # cumulative: number of vectors with weighted sum <= x
def brackets(R, J, exact=False):
    Wf = [floor(log2(p)*R) for p in S]; Wc = [ceil(log2(p)*R) for p in S]
    B = 8*J*R
    Cf = dp_counts(Wf, B, exact); Cc = dp_counts(Wc, B, exact)
    # x-budget for j: weighted sum <= 8j*R  (8j*R is an integer, so <= floor(8jR) exactly)
    return [(Cc[8*j*R], Cf[8*j*R]) for j in range(J+1)]
R, J = 256, 140
br = brackets(R, J)
for j in range(5):   # positive control: exact values must sit inside the brackets
    lo, hi = br[j]; print(f"   j={j}: {lo:.6g} <= H={Hex[j]} <= {hi:.6g}: {lo <= Hex[j] <= hi}")
cert_slow = [k for k in range(J) if 2*br[k+1][1] <= 3*br[k][0]]
cert_fast = [k for k in range(J) if 2*br[k+1][0] > 3*br[k][1]]
print(f"   R={R}: certified fast steps (2H(k+1)>3H(k)) for k in [0..{max(cert_fast) if cert_fast else None}] count={len(cert_fast)}; first certified slow k = {cert_slow[0] if cert_slow else None}")
mid = [ (k, br[k+1][0]/br[k][1], br[k+1][1]/br[k][0]) for k in range(0, J, 10)]
for k, a, b in mid: print(f"   k={k}: H(k+1)/H(k) in [{a:.4f}, {b:.4f}]")
