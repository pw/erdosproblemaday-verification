#!/usr/bin/env python3
"""Classify the referee's 27-seed census (own greedy, to 1e6, both rules).
For each greedy output: (i) shield sanity beyond 97: every B-rail integer present, every non-Q residue absent;
(ii) forcedness: the P-rails obey the rail recurrence Y1 = cpl(Y0 (+) Y0), Y2 = cpl(Y1 (+) Y1), Y0 = 1 + cpl(Y2 (+) Y2)
for 2 <= q < QMAX (strict sums under rule Q, equal-allowed under rule D) -- i.e. the greedy really is the rail model;
(iii) smallest rail period P <= 2550 holding on q in [QMAX/2, QMAX) (>= 4 repeats), else 'none'."""
import numpy as np, glob, os, sys
L = 10**6; QMAX = L // 49          # rails known for q < QMAX (49q+28 <= L)
P_ = [7, 14, 28]; B = [3, 22, 32, 40, 48]; Qres = set(P_) | set(B)
def sumset(Y, strict):
    n = len(Y); f = np.fft.rfft(Y.astype(float), 2 * n); c = np.rint(np.fft.irfft(f * f, 2 * n)[:n]).astype(np.int64)
    if strict:
        ev = np.arange(0, n, 2); c[ev] -= Y[ev // 2]
    return c > 0
rows = []
for path in sorted(glob.glob('/tmp/ref341/census/[QD]_*.txt')):
    name = os.path.basename(path)[:-4]; rule, tag = name.split('_', 1)
    el = np.loadtxt(path, dtype=np.int64)
    ind = np.zeros(L + 1, bool); ind[el] = True
    t = np.arange(98, L + 1); r = t % 49
    shield_ok = bool(ind[t[np.isin(r, B)]].all() and not ind[t[~np.isin(r, list(Qres))]].any())
    Y = [ind[49 * np.arange(QMAX) + p] for p in P_]
    st = (rule == 'Q'); S = [sumset(y, st) for y in Y]
    q = np.arange(2, QMAX)
    rec = [int((Y[1][q] == S[0][q]).sum()), int((Y[2][q] == S[1][q]).sum()), int((Y[0][q] == S[2][q - 1]).sum())]
    W = (Y[0].astype(np.uint8) | (Y[1].astype(np.uint8) << 1) | (Y[2].astype(np.uint8) << 2))
    lo = QMAX // 2; per = None
    for Pp in range(1, 2551):
        if np.array_equal(W[lo:QMAX - Pp], W[lo + Pp:QMAX]): per = Pp; break
    rows.append((tag, rule, shield_ok, rec, per))
by = {}
for tag, rule, sh, rec, per in rows: by.setdefault(tag, {})[rule] = (sh, rec, per)
print(f"{'R (rail elements at q<=1)':28s} | shieldOK recurrence-violations(G1,G2,G3) rail-period[Q] | same for rule D")
nQ = nD = 0
for tag in sorted(by):
    q = by[tag].get('Q'); d = by[tag].get('D')
    print(f"{tag:28s} | Q: {q[0]} {q[1]} {q[2] or 'none'}  | D: {d[0]} {d[1]} {d[2] or 'none'}")
    nQ += q[2] is None; nD += d[2] is None
print(f"seeds: {len(by)}; rule Q no rail period <= 2550 on q in [{QMAX//2},{QMAX}): {nQ}; rule D: {nD}")
print("all shield sanity OK:", all(v[0] for x in by.values() for v in x.values()),
      "; all rail recurrences hold:", all(v[1] == [0, 0, 0] for x in by.values() for v in x.values()))
