"""Referee test of Lemma 1'' (CLAIMS.md section A''): finite inequality
   K (A(N) - K) <= K |M_R cap [1, N']| + (R-1) N',   N' = N + a_K,
plus the pointwise facts c(n) <= min(K, r(n)) computed directly, and measured |M_R cap [1,N]|/N vs delta.
r(n) computed by FFT and cross-checked by exact integer convolution (see test_thmA.py for the r routines).
"""
import numpy as np, random
from math import comb
import importlib.util, sys
spec = importlib.util.spec_from_file_location("tA", __file__.replace("test_lemma1pp.py", "rfuncs.py"))
tA = importlib.util.module_from_spec(spec); spec.loader.exec_module(tA)

def run_set(name, ind, delta, Ns, Ks, Rs, bad):
    r = tA.r_fft(ind)
    r_ex = tA.r_exact(ind[:30_001])
    assert np.array_equal(r[:30_001], r_ex[:30_001]), name
    A = np.nonzero(ind)[0]
    A = A[A >= 1]
    cum = np.cumsum(ind.astype(np.int64)); cum -= int(ind[0])  # A(N) = |A cap [1,N]|
    for N in Ns:
        for K in Ks:
            if K >= len(A) or A[K - 1] >= N: continue
            aK = int(A[K - 1]); Np = N + aK
            if Np >= len(ind): continue
            AN = int(cum[N])
            # direct c(n): pairs (a_i, b), b in A cap (a_K, N]
            B = A[(A > aK) & (A <= N)]
            c = np.zeros(Np + 1, np.int64)
            for ai in A[:K]:
                c[ai + B] += 1
            assert c.sum() == K * (AN - K)
            if (c > K).any(): bad.append((name, N, K, 'c>K'))
            if (c > r[:Np + 1]).any(): bad.append((name, N, K, 'c>r'))
            for R in Rs:
                M = int((r[1:Np + 1] >= R).sum())
                lhs = K * (AN - K); rhs = K * M + (R - 1) * Np
                if lhs > rhs: bad.append((name, N, K, R, 'fin', lhs, rhs))
                lb = AN - K - (R - 1) * Np / K
                if M < lb - 1e-9: bad.append((name, N, K, R, 'lb', M, lb))
    # measured density of M_R on [1,N] vs delta (no K involved)
    out = []
    for R in (1, 10, 100, 1000):
        dens = [(int((r[1:N + 1] >= R).sum()) / N) for N in (50_000, 100_000, 150_000, 190_000)]
        out.append((R, dens))
    print(f"{name:30s} delta={delta}")
    for R, dens in out:
        print(f"    R={R:5d}  |M_R cap [1,N]|/N at N=50k,100k,150k,190k: " + ", ".join(f"{d:.4f}" for d in dens)
              + ("   <-- BELOW delta" if delta is not None and min(dens[-2:]) < delta - 0.002 else ""))

def main():
    NMAX = 200_000
    n = np.arange(NMAX + 1)
    rng = np.random.default_rng(1338)
    sets = [
        ('random d=0.3', (rng.random(NMAX + 1) < 0.3) & (n >= 1), 0.3),
        ('random d=0.02', (rng.random(NMAX + 1) < 0.02) & (n >= 1), 0.02),
        ('0,1 mod 7', ((n % 7 == 0) | (n % 7 == 1)) & (n >= 1), 2 / 7),
        ('20N', (n % 20 == 0) & (n >= 1), 1 / 20),
        ('7N', (n % 7 == 0) & (n >= 1), 1 / 7),
        ('Bateman {1} u 5N', ((n % 5 == 0) | (n == 1)) & (n >= 1), 1 / 5),
        ('3N u {1,2} (sparse start)', (((n % 3 == 0) & (n >= 1000)) | (n == 1) | (n == 2)), 1 / 3),
        ('odd numbers', (n % 2 == 1), 1 / 2),
    ]
    blk = np.zeros(NMAX + 1, bool); k = 1
    while 4 ** k <= NMAX:
        blk[4 ** k: min(2 * 4 ** k, NMAX + 1)] = True; k += 1
    sets.append(('blocks [4^k,2*4^k) (no density)', blk, None))
    Ns = [2000, 20_000, 100_000, 150_000]
    Ks = [1, 2, 5, 50, 500]
    Rs = [1, 2, 5, 50, 1000]
    bad = []
    for name, ind, delta in sets:
        run_set(name, ind, delta, Ns, Ks, Rs, bad)
    # adversarial hill-climb on the finite inequality, small N, 0 allowed or not
    for allow0 in (False, True):
        rnd = random.Random(7 + allow0); best = None
        for trial in range(300):
            N = rnd.choice([10, 15, 20, 30]); K = rnd.choice([1, 2, 3, 4]); R = rnd.choice([1, 2, 3])
            lo = 0 if allow0 else 1
            def score(S):
                S = sorted(S)
                if len(S) <= K or S[K - 1] >= N: return None
                aK = S[K - 1]; Np = N + aK
                ind = np.zeros(Np + 1, bool)
                for a in S: ind[a] = True
                r = tA.r_exact(ind)
                AN = sum(1 for a in S if 1 <= a <= N)
                M = int((r[1:Np + 1] >= R).sum())
                return K * (AN - K) - (K * M + (R - 1) * Np)
            S = set(x for x in range(lo, N + 1) if rnd.random() < 0.5)
            s = score(S)
            if s is None: continue
            for it in range(300):
                y = rnd.randint(lo, N); T = set(S) ^ {y}
                t = score(T)
                if t is not None and t >= s: S, s = T, t
            if best is None or s > best[0]: best = (s, N, K, R, sorted(S))
        print(f"hill-climb allow0={allow0}: max(lhs - rhs) = {best[0]} at N={best[1]} K={best[2]} R={best[3]} A={best[4]}")
    print("VIOLATIONS:", bad if bad else "none")

main()
