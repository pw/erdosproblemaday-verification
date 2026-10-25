#!/usr/bin/env python3
"""Referee's closed forms, typed in from PROOF.md's formulas (not from project code).

S  (rule Q) = D u {49q+b : q>=0, b in B} u {49q+7 : q in Y0} u {49q+14 : q in Y1} u {49q+28 : q in Y2}
S' (rule D) = same with Y0', Y1', Y2'.
Also Li's S_Li (his paper, eq. Y0..Y2) for negative/positive controls.
Usage: ref_closed_form.py {Q|D|LI} LIMIT OUTFILE
"""
import sys

P = [7, 14, 28]
B = [3, 22, 32, 40, 48]
D = [1, 2, 5, 13, 27, 36, 47]

def blocks_to_set(extra, blocks, qmax):
    s = set(x for x in extra if x <= qmax)
    k = 0
    while True:
        lo, hi = blocks(k)
        if lo > qmax:
            break
        s.update(range(lo, min(hi, qmax) + 1))
        k += 1
    return s

def controller(kind, qmax):
    p = 8
    if kind == 'Q':     # PROOF.md "The strict controller"
        Y0 = blocks_to_set({0, 1}, lambda k: (p**k + 1, 2 * p**k), qmax)
        Y1 = blocks_to_set({1},    lambda k: (4 * p**k, 8 * p**k), qmax)
        Y2 = blocks_to_set({0},    lambda k: (2 * p**k, 4 * p**k), qmax)
    elif kind == 'D':   # PROOF.md "The equal-rule controller"
        Y0 = blocks_to_set({0, 1}, lambda k: (2 * p**k, 4 * p**k - 1), qmax)
        # J'_k for k>=1 only: shift index so that k=0 here means k=1 there
        Y1 = blocks_to_set({1},    lambda k: (p**(k + 1) - 1, 2 * p**(k + 1) - 1), qmax)
        Y2 = blocks_to_set({0},    lambda k: (4 * p**k - 1, 8 * p**k - 1), qmax)
    elif kind == 'LI':  # Li's paper, eqs (Y0)-(Y2)
        Y0 = blocks_to_set({0},          lambda k: (4 * p**k, 8 * p**k - 1), qmax)
        Y1 = blocks_to_set({1, 2, 3},    lambda k: (16 * p**k - 1, 32 * p**k - 1), qmax)
        Y2 = blocks_to_set(set(range(0, 2)) | set(range(7, 16)),
                           lambda k: (64 * p**k - 1, 128 * p**k - 1), qmax)
    else:
        raise SystemExit("kind must be Q, D or LI")
    return Y0, Y1, Y2

def closed_form(kind, L):
    qmax = L // 49 + 1
    Y0, Y1, Y2 = controller(kind, qmax)
    S = set(d for d in D if d <= L)
    for q in range(qmax + 1):
        for b in B:
            S.add(49 * q + b)
        if q in Y0: S.add(49 * q + 7)
        if q in Y1: S.add(49 * q + 14)
        if q in Y2: S.add(49 * q + 28)
    return sorted(x for x in S if 1 <= x <= L)

if __name__ == '__main__':
    kind, L, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    S = closed_form(kind, L)
    with open(out, 'w') as f:
        for x in S:
            f.write(f"{x}\n")
    print(f"kind={kind} limit={L} count={len(S)} prefix<=97={[x for x in S if x <= 97]}")
