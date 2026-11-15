"""Referee test of Step 1' of Theorem A (CLAIMS.md).
For a set A (given as a boolean indicator on [0, NMAX]), compute r(n) = #{a<b in A : a+b=n} exactly, then check
  (ii)  max_{n<=N} r(n) <= A(x),  x = N/2,  A(x) = |A cap [1,x]|
  (fin) C(A(x),2) <= A(x)*|M_R cap [1,N]| + (R-1)*N
  (lb)  |M_R cap [1,N]| >= (A(x)-1)/2 - (R-1)N/A(x)
Two routes for r(n): (1) FFT convolution rounded, (2) exact integer np.convolve (O(N^2)) on N <= 40000.
"""
import numpy as np, sys, random
from math import comb

def r_fft(ind):
    n = len(ind)
    L = 1 << (2 * n).bit_length()
    f = np.fft.rfft(ind.astype(np.float64), L)
    conv = np.rint(np.fft.irfft(f * f, L)[: 2 * n - 1]).astype(np.int64)
    # ordered pairs incl. a=b ; remove diagonal, halve
    diag = np.zeros(2 * n - 1, dtype=np.int64)
    diag[0::2] = ind.astype(np.int64)
    r = (conv - diag)
    assert np.all(r % 2 == 0)
    return r // 2

def r_exact(ind):
    v = ind.astype(np.int64)
    conv = np.convolve(v, v)
    diag = np.zeros(len(conv), dtype=np.int64)
    diag[0::2] = v
    return (conv - diag) // 2

def check(name, ind, Ns, Rs, route=r_fft, verbose=True):
    r = route(ind)
    bad = []
    rows = []
    for N in Ns:
        x = N / 2
        Ax = int(ind[1: int(np.floor(x)) + 1].sum())
        rmax = int(r[1:N + 1].max())
        if rmax > Ax:
            bad.append((name, N, 'ii', rmax, Ax))
        for R in Rs:
            M = int((r[1:N + 1] >= R).sum())
            lhs = comb(Ax, 2)
            rhs = Ax * M + (R - 1) * N
            if lhs > rhs:
                bad.append((name, N, R, 'fin', lhs, rhs))
            lb = (Ax - 1) / 2 - (R - 1) * N / Ax if Ax > 0 else -1e18
            if M < lb - 1e-9:
                bad.append((name, N, R, 'lb', M, lb))
            rows.append((N, R, Ax, rmax, M, lb, lhs, rhs))
    if verbose:
        for (N, R, Ax, rmax, M, lb, lhs, rhs) in rows:
            print(f"  {name:28s} N={N:7d} R={R:4d} A(x)={Ax:6d} maxr={rmax:6d} |M_R|={M:7d} "
                  f"lb={lb:10.1f} |M_R|/N={M/N:.4f} A(x)/(N/2)={Ax/(N/2):.4f} slack={rhs-lhs}")
    return bad, r

def main():
    NMAX = 200_000
    rng = np.random.default_rng(338)
    n = np.arange(NMAX + 1)
    sets = {}
    sets['random d=0.3'] = (rng.random(NMAX + 1) < 0.3) & (n >= 1)
    sets['0,1 mod 7'] = ((n % 7 == 0) | (n % 7 == 1)) & (n >= 1)
    blk = np.zeros(NMAX + 1, bool)
    k = 1
    while 4 ** k <= NMAX:
        blk[4 ** k: min(2 * 4 ** k, NMAX + 1)] = True
        k += 1
    sets['blocks [4^k,2*4^k)'] = blk
    sets['20N (r concentrated)'] = (n % 20 == 0) & (n >= 1)
    sets['Bateman {1} u 5N'] = ((n % 5 == 0) | (n == 1)) & (n >= 1)
    # a set making r(n) as large as allowed on a short window: all of [1,L] plus a mirror window near N
    tight = np.zeros(NMAX + 1, bool)
    tight[1:5001] = True
    for c in (50_000, 100_000, 200_000):
        tight[c - 5000: c] = True
    sets['windows (r~A(x) near N)'] = tight
    # ternary-type sparse set (density 0), and odd numbers
    sets['odd numbers'] = (n % 2 == 1)
    Ns = [1000, 9999, 50_000, 100_000, 200_000]
    Rs = [1, 2, 5, 20, 100, 1000]
    allbad = []
    for name, ind in sets.items():
        print(name)
        bad, r1 = check(name, ind, Ns, Rs)
        allbad += bad
        # second route on N <= 40000 (exact integer convolution)
        sub = ind[:40_001]
        r2 = r_exact(sub)
        agree = np.array_equal(r1[:40_001], r2[:40_001])
        print(f"  second route (exact np.convolve, n<=40000) agrees with FFT: {agree}")
        if not agree:
            allbad.append((name, 'route-disagree'))
    # adversarial hill-climb on small N: maximize lhs - rhs, with and without 0 allowed
    for allow0 in (False, True):
        best = -10 ** 9; bestA = None
        rnd = random.Random(1 + allow0)
        for trial in range(300):
            N = rnd.choice([12, 16, 20, 24, 30, 40])
            R = rnd.choice([1, 2, 3, 4])
            lo = 0 if allow0 else 1
            A = set(x for x in range(lo, N + 1) if rnd.random() < 0.5)
            def score(A):
                ind = np.zeros(N + 1, bool)
                for a in A: ind[a] = True
                r = r_exact(ind)
                Ax = sum(1 for a in A if 1 <= a <= N / 2)
                M = int((r[1:N + 1] >= R).sum())
                rmax = int(r[1:N + 1].max()) if N >= 1 else 0
                return comb(Ax, 2) - (Ax * M + (R - 1) * N), rmax - Ax
            s, _ = score(A)
            for it in range(400):
                y = rnd.randint(lo, N)
                B = set(A); B ^= {y}
                t, _ = score(B)
                if t >= s: A, s = B, t
            _, ii = score(A)
            if s > best: best, bestA = s, (N, R, sorted(A), ii)
        print(f"hill-climb allow0={allow0}: max(lhs-rhs) = {best} at N,R,A,(maxr-A(x)) = {bestA}")
    # explicit witness for (ii) when 0 in A: A = {0..N} minus {N/2}
    N = 20
    ind = np.ones(N + 1, bool); ind[N // 2] = False
    r = r_exact(ind)
    Ax = int(ind[1:N // 2 + 1].sum())
    print(f"0 in A witness: A={{0..{N}}}\\{{{N//2}}}: r({N})={r[N]}, A(x)={Ax}  -> (ii) {'FAILS' if r[N] > Ax else 'holds'}")
    print("VIOLATIONS (0 in A excluded):", allbad if allbad else "none")

main()
