"""Check Section 8 identities (M0)-(M4) and the third-moment identity on actual
doubly regular tournaments, in the general form for DRT(4t+3):
  (M0) #trans = n*C(2t+1,2)
  (M1) |D(Y)|+|D+(Y)| = t - sigma(Y)
  (M2) sum_trans k = n*(2t+1)*C(t,2) ; sum_cyc k = n*[C(2t+1,3)-(2t+1)C(t,2)]
  (M3) sum C(k,2) = C(n,2)*C(t,3)
  (M4) sum C(k,3) = sum C(t-sigma-k,3)
  third moment: with u = k - (t-sigma)/2 : sum u^3 = 0, and sum u = 0 per class.
Usage: check_drt.py paley p1 p2 ... | check_drt.py json FILE | check_drt.py npy FILE
"""
import sys, json, itertools
from fractions import Fraction as F
from math import comb
import numpy as np
sys.path.insert(0, '/home/exedev/MathDyad/subs-1126/902/refA')
from tlib import *


def analyse(A, name):
    check_tournament(A)
    n = A.shape[0]
    assert (n - 3) % 4 == 0, n
    t = (n - 3) // 4
    outd = A.sum(1)
    assert np.all(outd == 2 * t + 1), f"{name}: not regular"
    inm = inmasks(A)
    outm = outmasks(A)
    # doubly regular: every pair has exactly t common dominators (in-nbrs)
    pd = set()
    po = set()
    for i, j in itertools.combinations(range(n), 2):
        pd.add(popcount(inm[i] & inm[j]))
        po.add(popcount(outm[i] & outm[j]))
    assert pd == {t} and po == {t}, f"{name}: not doubly regular {pd} {po}"
    ntr = ncy = 0
    sk = {0: 0, 1: 0}
    sC2 = 0
    sC3k = 0
    sC3L = 0
    u3 = F(0)
    usum = {0: F(0), 1: F(0)}
    M1bad = 0
    dist = {0: {}, 1: {}}
    mink = None
    for Y in itertools.combinations(range(n), 3):
        i, j, k_ = Y
        k = popcount(inm[i] & inm[j] & inm[k_])
        kp = popcount(outm[i] & outm[j] & outm[k_])
        s = sigma(A, Y)
        if k + kp != t - s:
            M1bad += 1
        if s:
            ntr += 1
        else:
            ncy += 1
        sk[s] += k
        sC2 += comb(k, 2)
        sC3k += comb(k, 3)
        L = t - s
        sC3L += comb(L - k, 3) if L - k >= 0 else 0
        u = F(k) - F(L, 2)
        u3 += u ** 3
        usum[s] += u
        dist[s][k] = dist[s].get(k, 0) + 1
        mink = k if mink is None else min(mink, k)
    print(f"== {name}: n={n} t={t}")
    print(f"  (M0) trans={ntr} expected {n*comb(2*t+1,2)}; cyc={ncy} expected {comb(n,3)-n*comb(2*t+1,2)}")
    print(f"  (M1) violations: {M1bad}")
    e_tr = n * (2 * t + 1) * comb(t, 2)
    e_cy = n * (comb(2 * t + 1, 3) - (2 * t + 1) * comb(t, 2))
    print(f"  (M2) sum_trans k={sk[1]} expected {e_tr}; sum_cyc k={sk[0]} expected {e_cy}; "
          f"means {F(sk[1], ntr)} vs (t-1)/2={F(t-1,2)}, {F(sk[0], ncy)} vs t/2={F(t,2)}")
    print(f"  (M3) sum C(k,2)={sC2} expected {comb(n,2)*comb(t,3)}")
    print(f"  (M4) sum C(k,3)={sC3k}  sum C(t-sigma-k,3)={sC3L}")
    print(f"  per-class sum u: trans={usum[1]} cyc={usum[0]};  sum u^3 = {u3}")
    print(f"  min k over triples = {mink}")
    print(f"  k-distribution transitive: {dict(sorted(dist[1].items()))}")
    print(f"  k-distribution cyclic:     {dict(sorted(dist[0].items()))}")
    ok = (ntr == n * comb(2 * t + 1, 2) and M1bad == 0 and sk[1] == e_tr and sk[0] == e_cy
          and sC2 == comb(n, 2) * comb(t, 3) and sC3k == sC3L and u3 == 0
          and usum[0] == 0 and usum[1] == 0)
    print(f"  ALL IDENTITIES HOLD: {ok}", flush=True)
    return ok, mink


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'paley':
        for p in map(int, sys.argv[2:]):
            analyse(paley(p), f"QR_{p}")
    elif mode == 'json':
        d = json.load(open(sys.argv[2]))
        for idx, entry in enumerate(d):
            A = np.array(entry['A'], dtype=np.int8)
            analyse(A, f"{sys.argv[2]}[{idx}]")
    elif mode == 'npy':
        A = np.load(sys.argv[2], allow_pickle=False).astype(np.int8)
        analyse(A, sys.argv[2])
