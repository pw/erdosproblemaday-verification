# Second instrument for the #968 empirical table (09:00Z seat, 2026-10-21): numpy segmented odd-only sieve, a different
# language/algorithm from gaps.c, and a DIFFERENT form of the increase predicate: n*(p_{n+1}-p_n) > p_n  (equivalent to
# (n+1) p_n < n p_{n+1}; int64-safe to n=1e9 since n*gap <= 1e9*1000). Gap predicate: g > C*log(p_n) in float64.
# Prints EXACT counts at checkpoints. Usage: python3 recount2.py LIMIT
import numpy as np, sys, math
LIMIT = int(sys.argv[1])
CK = [10**6, 10**7, 10**8, 10**9]
CS = [1.0, 2.0, 3.0, 6.0]
r = math.isqrt(LIMIT) + 1
base = np.ones(r + 1, dtype=bool); base[:2] = False
for i in range(2, math.isqrt(r) + 1):
    if base[i]: base[i*i::i] = False
bp = np.flatnonzero(base)[1:].astype(np.int64)   # odd base primes
SEG = 1 << 26                                     # odd numbers per segment
n = 0; prev = None
inc = 0; big = [0]*len(CS); ck = 0
def flush_upto(P):
    """P: sorted array of consecutive primes (int64), with P[0] = p_{n0+1} where n0 = n before this block."""
    global n, prev, inc, big, ck
    if prev is not None: P = np.concatenate(([prev], P))
    else:
        P = np.concatenate(([2], P)); n_start = 1  # p_1 = 2
    # pairs (P[i], P[i+1]) have index idx = n_first + i, where P[0] = p_{n_first}
    n_first = n if prev is not None else 1
    if prev is None: n = 1
    m = len(P) - 1
    if m <= 0: prev = int(P[-1]); return
    idx = np.arange(n_first, n_first + m, dtype=np.int64)
    pn = P[:-1]; pn1 = P[1:]; g = pn1 - pn
    isinc = idx * g > pn
    lp = np.log(pn.astype(np.float64))
    # checkpoints inside this block
    start = 0
    while ck < len(CK) and n_first <= CK[ck] <= n_first + m - 1:
        end = CK[ck] - n_first + 1
        inc += int(np.count_nonzero(isinc[start:end]))
        for c, C in enumerate(CS): big[c] += int(np.count_nonzero(g[start:end] > C * lp[start:end]))
        print(f"N={CK[ck]} p_N={int(pn[end-1])} inc={inc} " + " ".join(f"gt{C}={big[c]}" for c, C in enumerate(CS)), flush=True)
        start = end; ck += 1
    inc += int(np.count_nonzero(isinc[start:]))
    for c, C in enumerate(CS): big[c] += int(np.count_nonzero(g[start:] > C * lp[start:]))
    n = n_first + m
    prev = int(P[-1])
# odd numbers 2j+1, j in [j0, j0+SEG)
j0 = 1  # start at 3
first = True
while 2 * j0 + 1 <= LIMIT and ck < len(CK):
    j1 = min(j0 + SEG, (LIMIT - 1) // 2 + 1)
    lo = 2 * j0 + 1; hi = 2 * (j1 - 1) + 1
    s = np.ones(j1 - j0, dtype=bool)
    for p in bp:
        if p * p > hi: break
        st = max(p * p, (lo + p - 1) // p * p)
        if st % 2 == 0: st += p
        s[(st - lo) // 2::p] = False
    P = (2 * (np.flatnonzero(s) + j0) + 1).astype(np.int64)
    if first:
        prev = None
    flush_upto(P); first = False
    j0 = j1
print("DONE", "n=", n, "last=", prev, flush=True)
