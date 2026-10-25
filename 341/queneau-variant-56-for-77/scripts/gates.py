#!/usr/bin/env python3
"""Rail dynamics of a Li-type shield for Erdős #341 under the EQUAL (i ≤ j, Dickson) and STRICT (i < j, Queneau) rules.

Rails p·2^i (i < m) modulo M = (2^m − 1)p.  Y_i[q] = [Mq + 2^i p ∈ S].  For t > N the shield leaves only the diagonal
P+P sources, so
    Y_{i+1}[q] = NOT ∃ u, v ∈ Y_i (u ≠ v if strict): u + v = q          (i < m−1)
    Y_0[q]     = NOT ∃ u, v ∈ Y_{m−1} (u ≠ v if strict): u + v = q − 1  (the wrap 2^{m−1}p + 2^{m−1}p = M + p)
processed in the order of the integers (residue p first inside block q, then 2p, 4p, …).  The initial condition fixes
the rails for q ≤ q0 (the seed is S ∩ [1, M q0 + M − 1]); everything after is forced.

Controls: Li's IC under the equal rule must reproduce his closed-form Y0/Y1/Y2 (positive control, run with --control);
the same IC under the strict rule must come out periodic (we certified the greedy on his seed under the distinct rule:
membership period 5,733 = 49·117 ⇒ rail period | 117).
"""
import numpy as np, sys, itertools, argparse

def li_closed_form(Q):
    """Li's Y0, Y1, Y2 on [0, Q)."""
    Y0 = np.zeros(Q, bool); Y1 = np.zeros(Q, bool); Y2 = np.zeros(Q, bool)
    Y0[0] = True; Y1[1:4] = True; Y2[0:2] = True; Y2[7:16] = True
    a = 1
    while a < Q:
        Y0[4*a:min(8*a, Q)] = True
        Y1[16*a-1:min(32*a, Q)] = True
        Y2[64*a-1:min(128*a, Q)] = True
        a *= 8
    return [Y0, Y1, Y2]

def run(m, strict, ic, Q):
    """ic: list of m boolean lists (rail content for q = 0..q0).  Returns m arrays on [0,Q)."""
    q0 = len(ic[0]) - 1
    Y = [np.zeros(Q, bool) for _ in range(m)]
    # sums[i][s] = True iff s = u + v with u, v ∈ Y_i (u ≠ v if strict), u, v ≤ current q
    sums = [np.zeros(Q, bool) for _ in range(m)]
    def add(i, q):
        Y[i][q] = True
        # new sums q + u for u ∈ Y_i, u ≤ q (strict: u ≠ q)
        us = np.flatnonzero(Y[i][:q+1])
        if strict: us = us[us != q]
        s = us + q
        sums[i][s[s < Q]] = True
    for i in range(m):
        for q in range(q0 + 1):
            if ic[i][q]: add(i, q)
    for q in range(q0 + 1, Q):
        # residue p first: depends on Y_{m-1} sums at q-1
        if not sums[m-1][q-1]: add(0, q)
        for i in range(1, m):
            if not sums[i-1][q]: add(i, q)
    return Y

def classify(Y, Q, Kmax=None, Pmax=None):
    """Smallest (K, P) with Y[q+P] == Y[q] for all K ≤ q < Q−P, P ≤ Pmax, K ≤ Kmax, requiring ≥ 3 periods past K."""
    W = np.packbits(np.stack(Y), axis=0, bitorder='little')[0]  # m ≤ 8 rails → one byte per q
    Kmax = Q // 2 if Kmax is None else Kmax; Pmax = Q // 4 if Pmax is None else Pmax
    for P in range(1, Pmax + 1):
        d = np.flatnonzero(W[P:] != W[:-P])
        K = 0 if d.size == 0 else int(d[-1]) + 1
        if K <= Kmax and Q - P - K >= 3 * P:
            return K, P
    return None

def li_ic():
    # Li's seed on the rails for q ≤ 1: 7 (Y0[0]), 28 (Y2[0]), 63 = 49+14 (Y1[1]), 77 = 49+28 (Y2[1]); not 14, 56, 
    return [[True, False], [False, True], [True, True]]

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--Q', type=int, default=8**5); ap.add_argument('--control', action='store_true')
    ap.add_argument('--m', type=int, default=3); ap.add_argument('--strict', type=int, default=1)
    ap.add_argument('--ic', help='m comma-separated bitstrings, e.g. 10,01,11 (Li)')
    a = ap.parse_args(); Q = a.Q
    if a.control:
        Y = run(3, False, li_ic(), Q); C = li_closed_form(Q)
        mism = [int(np.sum(Y[i] != C[i])) for i in range(3)]
        print(f"[control] Li IC, EQUAL rule, Q={Q}: mismatches vs closed form Y0/Y1/Y2 = {mism} -> {'PASS' if mism==[0,0,0] else 'FAIL'}")
        print(f"[control] equal-rule classify: {classify(Y, Q)} (expected None = aperiodic to Q)")
        Ys = run(3, True, li_ic(), Q); cl = classify(Ys, Q)
        print(f"[control] Li IC, STRICT rule: classify = {cl} (expected periodic with P | 117)")
        # mutation: equal rule with one IC bit flipped must NOT match the closed form
        bad = run(3, False, [[True, True], [False, True], [True, True]], Q)
        print(f"[control] mutated IC (Y0[1]=1), equal rule: mismatches = {[int(np.sum(bad[i]!=C[i])) for i in range(3)]} (expected nonzero)")
        sys.exit(0)
    ic = [[c == '1' for c in s] for s in a.ic.split(',')]
    Y = run(a.m, bool(a.strict), ic, Q)
    print("classify:", classify(Y, Q))
    for i in range(a.m):
        print(f"Y{i}:", ''.join('1' if b else '0' for b in Y[i][:160]))
