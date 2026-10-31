#!/usr/bin/env python3
"""Seat P -- small-case checks of Lemma 4.1 (high-power tail).  SMALL-CASE EVIDENCE ONLY.

Part A (exhaustive, numpy): M=8, K=30, h=2, L=lcm(1..8)=840, all 1<=t<=J.
  * nestedness of E_{p,a}, and Z(t) == sum_p ell_p(t) log p   (eq. (26))
  * for EVERY profile r with Q(r) < J and W(r) <= Wmax: exact count of
    {t<=J : ell_p(t) >= r_p for all p}  <=  R(r)(J/Q(r)+1)  (eq. (30))
    and <= 2J prod 2K/p^{a_p+r_p-1}                         (eq. (36))
  * overhead identity (33) exactly, and log Q(r) <= 2W(r) + overhead.
  * for thresholds x where max_{r in W_x} log Q(r) < log J (the paper's
    condition (35)): #{Z>=x} <= 2J e^{-lambda x} prod(1+2K/(p^{a_p-1}(p^{1-lambda}-1)))
Part B (Monte Carlo, density form): M=30, K=150, h=3; t uniform in [1, 10^60].
  empirical P(Z>=x) vs e^{-lambda x} prod(...) (density version of (37)).
"""
import math, itertools, random
import numpy as np

def primes_upto(N):
    s = bytearray([1]) * (N + 1); s[0:2] = b'\x00\x00'
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]:
            s[i*i::i] = bytearray(len(range(i*i, N + 1, i)))
    return [i for i in range(N + 1) if s[i]]

def lcm_upto(M):
    L = 1
    for i in range(1, M + 1): L = L * i // math.gcd(L, i)
    return L

def setup(M, K):
    PR = [p for p in primes_upto(K)]
    a = {}; b = {}
    for p in PR:
        aa = 2
        while p ** aa <= K: aa += 1
        a[p] = aa
        bb = 0
        while p ** (bb + 1) <= M: bb += 1
        b[p] = bb
    return PR, a, b

def psi(x, PR):
    return sum(math.log(p) * int(math.floor(math.log(x) / math.log(p) + 1e-12)) for p in PR if p <= x)

def theta(x, PR):
    return sum(math.log(p) for p in PR if p <= x)

def partA():
    M, K, h = 8, 30, 2
    L = lcm_upto(M)
    J = 20_000_000
    PR, a, b = setup(M, K)
    t = np.arange(1, J + 1, dtype=np.int64)
    n = t * L - h - 1
    nmax = int(n[-1])
    ell = {}
    Z = np.zeros(J)
    nest_fail = 0
    for p in PR:
        lp = np.zeros(J, dtype=np.int64)
        alive = np.ones(J, dtype=bool)
        aa = a[p]
        prev = None
        while p ** aa <= nmax * p:  # go one level past n to be safe
            q = p ** aa
            ev = (n % q) < K
            if prev is not None:
                nest_fail += int(np.count_nonzero(ev & ~prev))  # E_{a+1} => E_a
            # direct Z contribution (definition (23))
            Z += math.log(p) * ev
            alive &= ev
            lp += alive
            prev = ev
            aa += 1
        ell[p] = lp
    Zdepth = sum(ell[p] * math.log(p) for p in PR)
    print(f"[A] M={M} K={K} h={h} L={L} J={J}")
    print(f"    nestedness violations: {nest_fail};  max|Z - sum ell_p log p| = {np.max(np.abs(Z - Zdepth)):.2e}")
    # overhead identity (33)
    lhs = sum((a[p] - 1 - b[p]) * math.log(p) for p in PR if p <= M)
    rhs = (psi(K, PR) - theta(K, PR)) - (psi(M, PR) - theta(M, PR))
    print(f"    overhead identity (33): lhs={lhs:.6f} rhs={rhs:.6f}")
    # per-prime classes: number of residue classes mod Q_p(r) is <= 2K/g_p
    cls_fail = 0
    for p in PR:
        g = p ** b[p]
        for r in range(1, 4):
            Q = p ** (a[p] + r - 1 - b[p])
            mod = p ** (a[p] + r - 1)
            classes = set()
            for s in range(K):
                if (h + 1 + s) % g: continue
                # t*L == h+1+s (mod p^{a+r-1}) -> t mod Q
                u = (h + 1 + s) // g
                Lp = L // g
                classes.add((u * pow(Lp, -1, Q)) % Q)
            if len(classes) > 2 * K / g: cls_fail += 1
    print(f"    per-prime class-count violations (#classes > 2K/g_p): {cls_fail}")
    # all profiles with small weight
    logJ = math.log(J)
    Wmax = 7.0
    supp_primes = PR
    # enumerate profiles by DFS over primes with W <= Wmax
    profiles = []
    def dfs(i, cur, W):
        if i == len(supp_primes):
            if W > 0: profiles.append(dict(cur))
            return
        p = supp_primes[i]
        r = 0
        while W + r * math.log(p) <= Wmax + 1e-12:
            if r: cur[p] = r
            dfs(i + 1, cur, W + r * math.log(p))
            r += 1
        cur.pop(p, None)
    dfs(0, {}, 0.0)
    over = rhs
    nprof = 0; bad30 = bad36 = badQ = 0; worst_ratio = 0.0
    for r in profiles:
        W = sum(v * math.log(p) for p, v in r.items())
        logQ = sum((a[p] + v - 1 - b[p]) * math.log(p) for p, v in r.items())
        if logQ > 2 * W + over + 1e-9: badQ += 1
        if logQ >= logJ: continue
        nprof += 1
        mask = np.ones(J, dtype=bool)
        for p, v in r.items(): mask &= ell[p] >= v
        cnt = int(np.count_nonzero(mask))
        R = 1.0
        for p, v in r.items(): R *= 2 * K / p ** b[p]
        b30 = R * (J / math.exp(logQ) + 1)
        b36 = 2 * J
        for p, v in r.items(): b36 *= 2 * K / p ** (a[p] + v - 1)
        if cnt > b30 + 1e-6: bad30 += 1
        if cnt > b36 + 1e-6: bad36 += 1
        if b36 > 0: worst_ratio = max(worst_ratio, cnt / b36)
    print(f"    profiles with W<={Wmax}: {len(profiles)}, with Q<J tested: {nprof}; "
          f"logQ>2W+overhead: {badQ}; (30) violations: {bad30}; (36) violations: {bad36}; max count/(36)-bound = {worst_ratio:.3f}")
    # aggregate Rankin bound for thresholds x where W_x has Q<J
    for lam in (0.5, 0.8):
        prod = 1.0
        for p in PR: prod *= 1 + 2 * K / (p ** (a[p] - 1) * (p ** (1 - lam) - 1))
        for x in (1.0, 2.0, 3.0, 4.0, 5.0):
            # max logQ over W_x = {x <= W < x + log K}
            mx = -1
            for r in profiles:
                W = sum(v * math.log(p) for p, v in r.items())
                if x <= W < x + math.log(K):
                    mx = max(mx, sum((a[p] + v - 1 - b[p]) * math.log(p) for p, v in r.items()))
            complete = (x + math.log(K) <= Wmax)
            cnt = int(np.count_nonzero(Z >= x - 1e-12))
            bnd = 2 * J * math.exp(-lam * x) * prod
            ok = "Q<J holds" if (complete and mx < logJ) else "Q<J FAILS/unknown -> (37) not licensed"
            print(f"    lam={lam} x={x}: #Z>=x = {cnt:9d}  bound(37) = {bnd:.3e}  maxlogQ(W_x)={mx:.2f} vs logJ={logJ:.2f}  [{ok}]")

def partB(samples=60000, seed=7):
    M, K, h = 30, 150, 3
    L = lcm_upto(M)
    PR, a, b = setup(M, K)
    rng = random.Random(seed)
    Zs = []
    for _ in range(samples):
        t = rng.randint(1, 10 ** 60)
        n = t * L - h - 1
        Z = 0.0
        for p in PR:
            q = p ** a[p]
            while q <= n and n % q < K:
                Z += math.log(p); q *= p
        Zs.append(Z)
    Zs = np.array(Zs)
    print(f"[B] M={M} K={K} h={h}; {samples} random t<=1e60; mean Z={Zs.mean():.2f}, sqrt K={math.sqrt(K):.1f}")
    for lam in (0.5, 0.8, 0.95):
        prod = 1.0
        for p in PR: prod *= 1 + 2 * K / (p ** (a[p] - 1) * (p ** (1 - lam) - 1))
        line = []
        for x in (5, 10, 15, 20, 25, 30):
            emp = float(np.mean(Zs >= x))
            bnd = math.exp(-lam * x) * prod
            line.append(f"x={x}: emp={emp:.2e} bnd={bnd:.2e}{' VIOL' if emp > bnd else ''}")
        print(f"    lam={lam} log prod={math.log(prod):.1f} | " + " | ".join(line))

if __name__ == '__main__':
    partA()
    partB()
