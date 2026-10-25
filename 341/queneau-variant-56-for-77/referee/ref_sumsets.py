#!/usr/bin/env python3
"""Referee's brute-force check of Lemma 2/2' (sumsets) and Lemma 3/3' (gates) by Python big-int
bitsets (element-by-element shift-OR; no FFT, no interval algebra), on [0, L).
Also: the gates under the WRONG rule, and one-endpoint mutations (negative controls).
Usage: ref_sumsets.py LOGL [mutations]   (L = 8**LOGL)"""
import sys

def mask_from_blocks(extra, blocks, L):
    m = 0
    for x in extra:
        if x < L: m |= 1 << x
    for lo, hi in blocks:
        if lo >= L: continue
        hi = min(hi, L - 1)
        m |= ((1 << (hi - lo + 1)) - 1) << lo
    return m

def elems(m):
    out = []; i = 0
    while m:
        if m & 1: out.append(i)
        # skip zero runs fast
        if m & 1 == 0:
            low = (m & -m).bit_length() - 1
            m >>= low; i += low; continue
        m >>= 1; i += 1
    return out

def sumset(m, L, distinct):
    full = (1 << L) - 1
    acc = 0
    for v in elems(m):
        if v >= L: break
        below = m & ((1 << (v + (0 if distinct else 1))) - 1)   # u < v  (or u <= v)
        acc |= below << v
    return acc & full

def blocks(kind, L, mut=None):
    """kind in Q (strict controller) / D (equal controller). mut = (which Y, k, end 'lo'/'hi', delta)."""
    K = range(0, 12)
    if kind == 'Q':
        Y = {0: ({0, 1}, [[8**k + 1, 2 * 8**k] for k in K]),
             1: ({1},    [[4 * 8**k, 8 * 8**k] for k in K]),
             2: ({0},    [[2 * 8**k, 4 * 8**k] for k in K])}
    else:
        Y = {0: ({0, 1}, [[2 * 8**k, 4 * 8**k - 1] for k in K]),
             1: ({1},    [[8**k - 1, 2 * 8**k - 1] for k in K if k >= 1]),
             2: ({0},    [[4 * 8**k - 1, 8 * 8**k - 1] for k in K])}
    if mut:
        w, k, end, d = mut
        bl = Y[w][1]
        idx = k if not (kind == 'D' and w == 1) else k - 1
        bl[idx][0 if end == 'lo' else 1] += d
    return {w: mask_from_blocks(e, b, L) for w, (e, b) in Y.items()}

def gates(Y, L, distinct):
    """Return violation counts of (G1),(G2),(G3) for q in [2, L)."""
    S = {w: sumset(Y[w], L, distinct) for w in (0, 1, 2)}
    # bit strings, index i = bit i (avoid O(L) big-int shifts per lookup)
    tob = lambda m: bin(m)[2:][::-1].ljust(L, '0')
    y = {w: tob(Y[w]) for w in (0, 1, 2)}; s = {w: tob(S[w]) for w in (0, 1, 2)}
    v = [0, 0, 0]; first = [None, None, None]
    for q in range(2, L):
        c = [(y[1][q] == '1') == (s[0][q] == '1'),
             (y[2][q] == '1') == (s[1][q] == '1'),
             (y[0][q] == '1') == (s[2][q - 1] == '1')]
        for j in range(3):
            if c[j]:
                v[j] += 1
                if first[j] is None: first[j] = q
    return v, first, S

def claimed_sumsets(kind, L):
    K = range(0, 12)
    if kind == 'Q':
        return {0: mask_from_blocks({1, 2, 3}, [(8**k + 1, 4 * 8**k - 1) for k in K if k >= 1], L),
                1: mask_from_blocks(set(), [(4 * 8**k + 1, 16 * 8**k - 1) for k in K], L),
                2: mask_from_blocks(set(), [(2 * 8**k, 8 * 8**k - 1) for k in K], L)}
    return {0: mask_from_blocks(set(range(0, 7)), [(2 * 8**k, 8 * 8**k - 2) for k in K if k >= 1], L),
            1: mask_from_blocks({2}, [(8**k, 4 * 8**k - 2) for k in K if k >= 1], L),
            2: mask_from_blocks({0}, [(4 * 8**k - 1, 16 * 8**k - 2) for k in K], L)}

if __name__ == '__main__':
    logL = int(sys.argv[1]); L = 8**logL
    do_mut = len(sys.argv) > 2
    print(f"L = 8^{logL} = {L}")
    for kind, own_distinct in (('Q', True), ('D', False)):
        Y = blocks(kind, L)
        v, first, S = gates(Y, L, own_distinct)
        cl = claimed_sumsets(kind, L)
        # the claimed sumset formula is only trusted on [0, L - 1]; sums near L use only elements < L
        lem2 = [S[w] == cl[w] for w in (0, 1, 2)]
        print(f"[{kind}-controller, own rule {'distinct' if own_distinct else 'equal-allowed'}] "
              f"Lemma2{'' if kind=='Q' else chr(39)} (S0,S1,S2) exact on [0,L): {lem2}; gate violations q in [2,L): {v}")
        vw, fw, _ = gates(Y, L, not own_distinct)
        print(f"[{kind}-controller, WRONG rule] gate violations: {vw}, first offending q: {fw}")
    if do_mut:
        for kind, distinct in (('Q', True), ('D', False)):
            survivors = []; n = 0
            for w in (0, 1, 2):
                for k in range(0, 4):
                    if kind == 'D' and w == 1 and k == 0: continue
                    for end in ('lo', 'hi'):
                        for d in (-1, +1):
                            Y = blocks(kind, L, (w, k, end, d))
                            v, first, _ = gates(Y, L, distinct)
                            n += 1
                            if sum(v) == 0: survivors.append((w, k, end, d))
            print(f"[{kind}] one-endpoint mutations (Y0..Y2, k=0..3, lo/hi, +-1): {n} tried, "
                  f"{len(survivors)} survive all three gates: {survivors}")
