#!/usr/bin/env python3
"""Seat P -- parameter constraints, the final constant, and finite-M sizes.

1. Symbolic/numeric check of (11)-(12) under the choice (67) on a (delta,beta) grid;
   the supremum of c/(1+sigma).
2. Exact finite-M evaluation (prime sieve) of every o(1)-carrying quantity in
   Sections 3-7 for the actual scales (13):
     log C_M / M            (Lemma 3.1, should -> c)
     log C(h+K,h) / M       (Lemma 6.1, should -> 1/20)
     2h*sum_{2<=m<=A+1}1/m / M  (Lemma 6.2, should -> 1/10)
     sqrt-K overhead / M    ((33),(58))
     log(Rankin product)/M  ((37)-(38))
   and the anchored-fibre condition (39) with |F| <= e^{tau M} + 2J e^{-lam beta M} * prod.
3. Rough size of M at which (39) can first hold for the paper's (67) choice.
"""
import math, sys
import numpy as np

def sieve(N):
    s = np.ones(N + 1, dtype=bool); s[:2] = False
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]

def part1():
    print("== 1. constraints under (67): lambda=1-d, c=(1-2d)b, sigma=(2+d)b, tau=b ==")
    bad = 0
    for d in [1e-4, 0.01, 0.05, 0.1, 0.2, 0.3, 0.45, 0.4999]:
        for b in [1e-3, 0.1, 1, 10, 1e3, 1e6]:
            lam, c, sig, tau = 1 - d, (1 - 2 * d) * b, (2 + d) * b, b
            ok = (0 < lam < 1) and b > 0 and (0 < c < lam * b) and (sig > 2 * b) and (tau < sig - c) and (b + 3 / 20 < 2 * (1 + tau))
            bad += (not ok)
    print(f"   grid violations: {bad}")
    for d in [0.1, 0.01, 0.001]:
        vals = [((1 - 2 * d) * b) / (1 + (2 + d) * b) for b in (1, 10, 100, 1e4, 1e8)]
        print(f"   d={d}: c/(1+sigma) at b=1,10,100,1e4,1e8 -> " + ", ".join(f"{v:.5f}" for v in vals)
              + f"  (limit (1-2d)/(2+d) = {(1 - 2 * d) / (2 + d):.5f})")
    # Is 1/2 the best this proof can give?  maximise c/(1+sigma) subject to c<lam*b<b, sigma>2b
    print("   sup over admissible tuples of c/(1+sigma) < b/(1+2b) < 1/2 ; tau, 3/20 constraints are slack.")

def part2(beta, delta, Ms):
    lam, c, sig, tau = 1 - delta, (1 - 2 * delta) * beta, (2 + delta) * beta, beta
    print(f"== 2. finite-M sizes: beta={beta} delta={delta} -> lambda={lam} c={c} sigma={sig} tau={tau} ==")
    Kmax = max(int(c * M * math.log(M) / math.log(math.log(M))) + 10 for M in Ms)
    P = sieve(Kmax)
    logP = np.log(P.astype(np.float64))
    for M in Ms:
        A = c * math.log(M) / math.log(math.log(M))
        K = int(math.floor(A * M))
        h = int(math.floor(M / (20 * math.log(A))))
        sel = (P > M) & (P <= K)
        pp = P[sel].astype(np.float64)
        logC = float(np.sum(np.log(np.ceil(pp / h))))
        lbin = math.lgamma(h + K + 1) - math.lgamma(h + 1) - math.lgamma(K + 1)
        H = sum(1.0 / m for m in range(2, int(math.floor(A + 1)) + 1))
        first = 2 * h * H
        # overhead psi(K)-theta(K) - (psi(M)-theta(M)) exactly
        def psimth(x):
            s = 0.0
            for p in P[P <= int(math.isqrt(x)) + 1]:
                p = int(p); q = p * p
                while q <= x: s += math.log(p); q *= p
            return s
        over = psimth(K) - psimth(M)
        # Rankin product (37): log prod <= sum 2K/(p^{a_p-1}(p^{1-lam}-1))
        Pk = P[P <= K]
        lp = 0.0
        for p in Pk:
            p = int(p)
            ap = 2
            while p ** ap <= K: ap += 1
            lp += math.log1p(2 * K / (p ** (ap - 1) * (p ** (1 - lam) - 1)))
        logJ = sig * M
        # anchored condition (39): log C + log(|F|+1) < log(J+1)
        logF = np.logaddexp(np.logaddexp(tau * M, math.log(2) + logJ - lam * beta * M + lp), 0.0)
        lhs = logC + logF
        pred = c * (1 + (math.log(20 * c) - 1) / math.log(math.log(M)))
        print(f"   M=1e{math.log10(M):.0f}: A={A:.2f} K={K:.3e} h={h} | logC/M={logC / M:.3f} (c={c}, heur. {pred:.3f}) "
              f"| binom/M={lbin / M:.4f} (->0.05) | first/M={first / M:.4f} (->0.1) | overhead/M={over / M:.2e} "
              f"| logRankin/M={lp / M:.3f} | (39): [logC+log(|F|+1)-logJ]/M = {(lhs - logJ) / M:+.3f} (need <0)")

def part3(beta, delta):
    lam, c, sig, tau = 1 - delta, (1 - 2 * delta) * beta, (2 + delta) * beta, beta
    # leading correction of log C_M/M - c  ~ c (log(20c)-1)/loglog M  (derived in REPORT)
    # need it below the margin lam*beta - c = delta*beta
    need = c * (math.log(20 * c) - 1) / (delta * beta)
    print(f"== 3. beta={beta} delta={delta}: entropy correction c(log20c-1)/loglogM < delta*beta needs loglog M > {need:.1f}"
          f"  i.e. log10 M > {math.exp(need) / math.log(10):.3g}")

if __name__ == '__main__':
    part1()
    part2(1.0, 0.1, [10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7])
    part2(10.0, 0.1, [10 ** 4, 10 ** 5, 10 ** 6])
    for (b, d) in [(1.0, 0.1), (10.0, 0.1), (10.0, 0.01), (100.0, 0.1)]:
        part3(b, d)
