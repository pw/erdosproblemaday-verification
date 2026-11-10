#!/usr/bin/env python3
# ref912.py — independent referee check of CLAIMS.md Claims 1-2 (Erdos #912).
# Written from scratch; does not reuse bf.c / hfast.c. Not incremental: e_n(p) is
# recomputed from Legendre's formula at every n, for every prime p <= n.
# mode "exh N": every n <= N.   mode "rand M T seed": T random + structured m <= M.
import sys, math, time, random
import numpy as np
from sympy import factorint, factorial, primerange, isprime

mode = sys.argv[1]
LIM = int(sys.argv[2]) + 2
sv = np.ones(LIM + 1, dtype=bool); sv[:2] = False
for i in range(2, math.isqrt(LIM) + 1):
    if sv[i]: sv[i*i::i] = False
P = np.nonzero(sv)[0].astype(np.int64)
if LIM <= 3_000_000:
    assert list(P) == list(primerange(2, LIM + 1)), "own sieve disagrees with sympy"

def legendre(n):
    """e_n(p) = sum_i floor(n/p^i) for every prime p <= n (full sum, all i)."""
    k = int(np.searchsorted(P, n, side='right'))
    Pk = P[:k]
    e = n // Pk
    pw = Pk * Pk
    L = k
    while True:
        L = int(np.count_nonzero(pw[:L] <= n))   # p^i increasing in p => prefix
        if L == 0: break
        pw = pw[:L]
        e[:L] += n // pw
        pw = pw * Pk[:L]
    return e

class State:
    def __init__(self, n):
        self.n = n
        self.e = legendre(n)
        self.vals, self.cnts = np.unique(self.e, return_counts=True)
        self.h = len(self.vals)
    def count(self, v):
        i = int(np.searchsorted(self.vals, v))
        return int(self.cnts[i]) if i < len(self.vals) and self.vals[i] == v else 0
    def exp(self, p):
        if p > self.n: return 0
        i = int(np.searchsorted(P, p)); assert P[i] == p
        return int(self.e[i])

stats = dict(lemma_checks=0, lemma_fail=0, lemma23=0, ctl_checks=0, ctl_fail=0,
             mono_fail=0, ident_fail=0, hm_fail=0, step_fail=0, rule_fail=0, alt_rule_fail=0,
             up=0, down=0, zero=0, caseA=0, caseB=0, small_hits_k=0, small_hits_km1=0,
             small_bound_fail=0, small_bound_tight=0, two_big=0, vQ_fail=0, eQ_fail=0,
             prime_m_nonzero=0, mut_rule_fail=0, mut_first_fail=0, move_without_Q=[], iso_small_fail=0, rule_checked=0)

def lemma_and_identity(S):
    n, e = S.n, S.e
    k = len(e)
    if k == 0: return
    if np.any(np.diff(e) > 0): stats['mono_fail'] += 1
    Pk = P[:k]
    Lq = int(np.count_nonzero(Pk * Pk <= n + 1))
    idx = np.searchsorted(S.vals, e[:Lq])
    c = S.cnts[idx]
    for i in range(Lq):
        q = int(Pk[i])
        if (q, n) == (2, 3):
            stats['lemma23'] += int(c[i] != 1); continue
        stats['lemma_checks'] += 1
        down_ok = (i == 0) or (e[i-1] > e[i])
        nxt = e[i+1] if i + 1 < k else 0
        up_ok = e[i] > nxt
        if c[i] != 1 or not down_ok or not up_ok:
            stats['lemma_fail'] += 1
            if stats['lemma_fail'] < 10: print("LEMMA FAIL", n, q, flush=True)
    # negative control: the next prime after the Lemma's range (q^2 > n+1) is often NOT isolated
    if Lq < k:
        stats['ctl_checks'] += 1
        if S.cnts[np.searchsorted(S.vals, e[Lq])] != 1: stats['ctl_fail'] += 1
    # identity h(n) = pi(sqrt n) + #{floor(n/p) : sqrt n < p <= n}
    pis = int(np.count_nonzero(Pk * Pk <= n))
    J = len(np.unique(n // Pk[pis:]))
    if pis + J != S.h:
        stats['ident_fail'] += 1; print("IDENT FAIL", n, S.h, pis, J, flush=True)
    if len(np.unique(n // Pk)) != S.h: stats['hm_fail'] += 1

def step(Sn, Sm):
    n, m = Sn.n, Sm.n
    d = Sm.h - Sn.h
    if abs(d) > 1:
        stats['step_fail'] += 1; print("STEP FAIL", m, d, flush=True)
    stats['up' if d == 1 else 'down' if d == -1 else 'zero'] += 1
    f = factorint(m)
    bigs = [p for p in f if p * p > m]
    smalls = [q for q in f if q * q <= m]
    if len(bigs) > 1: stats['two_big'] += 1
    # isolation of small factors at both x=n and x=m
    for q in smalls:
        if m == 4: continue
        if Sn.count(Sn.exp(q)) != 1 or Sm.count(Sm.exp(q)) != 1: stats['iso_small_fail'] += 1
    if bigs:
        stats['caseB'] += 1
        Q = bigs[0]; k = m // Q
        if f[Q] != 1: stats['vQ_fail'] += 1
        if Sn.exp(Q) != k - 1 or Sm.exp(Q) != k: stats['eQ_fail'] += 1
        # statement as written: "no prime p != Q has e_n(p) = k" etc.
        ck = Sn.count(k) - (1 if Sn.exp(Q) == k else 0)
        ckm1 = (Sn.count(k - 1) - (1 if Sn.exp(Q) == k - 1 else 0)) if k >= 2 else None
        pred = int(ck == 0) - int(k >= 2 and ckm1 == 0)
        # variant over primes NOT dividing m (what the proof's 'moving one element' actually computes)
        sk = sum(1 for q in smalls if Sn.exp(q) == k)
        skm1 = sum(1 for q in smalls if Sn.exp(q) == k - 1) if k >= 2 else 0
        stats['small_hits_k'] += sk; stats['small_hits_km1'] += skm1
        for q in smalls:   # the missing lemma: e_n(q) >= m/q >= Q > k
            if Sn.exp(q) < m // q: stats['small_bound_fail'] += 1
            if Sn.exp(q) == m // q: stats['small_bound_tight'] += 1
        alt = int(ck - sk == 0) - int(k >= 2 and (ckm1 - skm1) == 0)
        stats['rule_checked'] += 1
        if d != pred and m != 4:
            stats['rule_fail'] += 1; print("RULE FAIL", m, d, pred, flush=True)
        if d != alt and m != 4: stats['alt_rule_fail'] += 1
        if m != 4 and d != int(ck == 0): stats['mut_rule_fail'] += 1        # mutant: drop vacate term
        if m != 4 and d != -int(k >= 2 and ckm1 == 0): stats['mut_first_fail'] += 1  # mutant: drop insert term
        if isprime(m) and m >= 3 and d != 0: stats['prime_m_nonzero'] += 1
    else:
        stats['caseA'] += 1
        stats['rule_checked'] += 1
        if d != 0:
            stats['move_without_Q'].append((m, d))
            if m != 4:
                stats['rule_fail'] += 1; print("RULE(a) FAIL", m, d, flush=True)

t0 = time.time()
if mode == "exh":
    N = int(sys.argv[2])
    # Legendre cross-check against sympy's factorisation of n! itself (n <= 400)
    for n in range(1, 401):
        fe = factorint(factorial(n))
        hs = len(set(fe.values()))
        S = State(n)
        assert hs == S.h, (n, hs, S.h)
        assert dict(zip(map(int, P[:len(S.e)]), map(int, S.e))) == {int(a): int(b) for a, b in fe.items()}
    print("legendre == factorint(n!) for n<=400", flush=True)
    H = [0] * (N + 1)
    prev = State(1); H[1] = prev.h
    lemma_and_identity(prev)
    for m in range(2, N + 1):
        cur = State(m); H[m] = cur.h
        lemma_and_identity(cur)
        step(prev, cur)
        prev = cur
        if m % 50000 == 0: print("..", m, round(time.time() - t0), flush=True)
    # OEIS A071626 b-file
    bad = 0; tot = 0
    for line in open('/home/exedev/MathDyad/erdos912/sources/A071626_b071626.txt.out'):
        a = line.split()
        if len(a) == 2 and a[0].isdigit():
            i, v = int(a[0]), int(a[1])
            if i <= N: tot += 1; bad += (H[i] != v)
    print("OEIS A071626 b-file: %d/%d match" % (tot - bad, tot))
    print("h(1..12) =", H[1:13])
    for x in (10, 100, 1000, 10000, 100000, 200000):
        if x <= N: print("h(%d) = %d" % (x, H[x]))
else:
    M, T, seed = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    rng = random.Random(seed)
    ms = set()
    qs = list(primerange(2, math.isqrt(M) + 1))
    for q in qs:                       # structured families
        qp = int(P[np.searchsorted(P, q, side='right')])
        for m in (q * qp, q * q, q * q + q, 2 * q * qp):
            if 5 <= m <= M: ms.add(m)
    ms = sorted(ms)
    ms = [ms[i] for i in sorted(rng.sample(range(len(ms)), min(T // 2, len(ms))))]
    ms += [rng.randrange(M // 2, M) for _ in range(T // 2)]
    ms += [int(p) for p in (P[np.searchsorted(P, M // 2)], )]   # a prime m
    for m in sorted(set(ms)):
        Sn, Sm = State(m - 1), State(m)
        lemma_and_identity(Sn); lemma_and_identity(Sm)
        step(Sn, Sm)
    print("random/structured m count:", len(set(ms)))
stats['time_s'] = round(time.time() - t0)
for k, v in stats.items(): print(k, v)
