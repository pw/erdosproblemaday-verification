"""Replay the numeric case analysis 'Structure when J<=2' of Theorem 7.1 by brute force over q-profiles.
Profile = multiset of q_y (y in O, |O|=38, q_y in 5..11). Constraints used by the paper:
 (I2) sum (q_y-5) = 8-J;  triple count 110 + sum C(11-q_y,3) >= 825 ;
 (*) single-term consequences: a y with q_y = q forces j_r >= 1 on the 11-q vertices r notin Q_y when lambda(q) > 5,
     so needs J >= 11-q (q=7,8,9,10); two q>=9 vertices with J=0 impossible, etc. We only apply the coarse
     necessary condition J >= 11-q for each single y with lambda(q)>5 (q>=7, q<=10)."""
from math import comb
from itertools import product
lam = {q: 10 - (comb(10 - q, 2) if 10 - q >= 2 else 0) for q in range(5, 12)}
print("lambda:", lam)
surv = []
for J in (0, 1, 2):
    budget = 8 - J
    # extra = q-5 in 0..6; profile of extras summing to budget over 38 slots
    def parts(rem, maxpart):
        if rem == 0:
            yield []
            return
        for p in range(min(rem, maxpart), 0, -1):
            for rest in parts(rem - p, p):
                yield [p] + rest
    for pr in parts(budget, 6):
        if len(pr) > 38:
            continue
        qs = [5 + e for e in pr] + [5] * (38 - len(pr))
        tri = 110 + sum(comb(11 - q, 3) if 11 - q >= 3 else 0 for q in qs)
        if tri < 825:
            continue
        ok = all(not (lam[q] > 5 and q <= 10 and J < 11 - q) for q in qs)
        if ok:
            surv.append((J, sorted([q for q in qs if q != 5], reverse=True), tri))
for s in surv:
    print("surviving profile: J=%d non-5 q's=%s triple-incidences=%d" % s)
