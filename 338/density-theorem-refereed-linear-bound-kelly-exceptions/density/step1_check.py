"""Sanity check of Step 1' (CLAIMS.md Theorem A): for finite pieces of several sets A, compute r(n) exactly and test
   (I)  C(A(x),2) <= sum_{n<=N} r(n)
   (II) r(n) <= A(x) for all n <= N          (x = N/2)
   (III) sum_{n<=N} r(n) <= A(x)*|M_R ∩ [1,N]| + (R-1)*N
   (IV) |M_R ∩ [1,N]| >= (A(x)-1)/2 - (R-1)*N/A(x)
An inequality that is a theorem cannot fail; this guards the algebra and the off-by-ones."""
import random, sys
from math import comb
def r_counts(Aset, N):
    A = sorted(a for a in Aset if a <= N)
    inA = bytearray(N+1)
    for a in A: inA[a] = 1
    r = [0]*(N+1)
    for a in A:
        # pairs a<b, a+b<=N
        for b in range(a+1, N-a+1):
            if inA[b]: r[a+b] += 1
    return r
def sets(N, seed=1):
    rng = random.Random(seed)
    out = {}
    out['random delta=0.3'] = {n for n in range(1, N+1) if rng.random() < 0.3}
    out['random delta=0.05'] = {n for n in range(1, N+1) if rng.random() < 0.05}
    out['0,1 mod 7'] = {n for n in range(1, N+1) if n % 7 in (0, 1)}
    out['0,1 mod 40'] = {n for n in range(1, N+1) if n % 40 in (0, 1)}
    blocks = set(); x = 3
    while x <= N:
        blocks |= set(range(x, min(2*x, N)+1)); x *= 5
    out['blocks [x,2x], x*=5'] = blocks
    out['Bateman {1} U 6N'] = {1} | {n for n in range(6, N+1, 6)}
    out['multiples of 9 + sparse squares'] = {n for n in range(9, N+1, 9)} | {k*k for k in range(1, int(N**0.5)+1)}
    out['top-heavy: [N/2-N/10, N/2]'] = set(range(N//2 - N//10, N//2 + 1))
    return out
fails = 0
for N in (2000, 6000, 12000):
    x = N // 2          # N even, x = N/2
    for name, A in sets(N).items():
        r = r_counts(A, N)
        Ax = sum(1 for a in A if a <= x)
        tot = sum(r[1:N+1])
        mx = max(r[1:N+1])
        okI = comb(Ax, 2) <= tot
        okII = mx <= Ax
        for R in (1, 2, 5, 20):
            M = sum(1 for n in range(1, N+1) if r[n] >= R)
            okIII = tot <= Ax*M + (R-1)*N
            okIV = (Ax == 0) or (M >= (Ax-1)/2 - (R-1)*N/Ax)
            if not (okI and okII and okIII and okIV):
                fails += 1
                print('FAIL', N, name, R, okI, okII, okIII, okIV)
            if R == 5:
                print(f"N={N:6d} {name:34s} A(x)={Ax:5d} max r={mx:5d} |M_5∩[1,N]|={M:6d}  bound={(Ax-1)/2 - 4*N/max(Ax,1):9.1f}  M/N={M/N:.3f}  (A(x)/x)/4={Ax/x/4:.3f}")
print('failures:', fails)
