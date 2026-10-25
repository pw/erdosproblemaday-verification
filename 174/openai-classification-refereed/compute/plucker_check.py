#!/usr/bin/env python3
"""Second instrument for ANY kernel dimension r = 9 - rank (one-parameter configs, three-squares labels).  Exact Fractions,
no sympy, no saturation loop.  m_F(K) = the limit, as h -> 0, of the subspace ker M(x0, x0+h) in the Grassmannian
(the reduction of the saturated lattice over the DVR is the specialisation of the generic kernel).  Plücker
coordinates of ker M are the complementary maximal minors of M (Hodge duality, sign = parity of (t, complement));
each is a polynomial in h of degree <= 2*rank: recovered exactly by interpolation; divide by the least power h^m
common to all, set h = 0, rebuild a basis by Cramer (u^(j)_k = q(S0[j<-k]) / q(S0)), test whether some combination has
spatial block I.  The sign convention is VALIDATED at a non-sample h: the rebuilt basis must satisfy M u = 0 exactly."""
from fractions import Fraction as Fr
import itertools, sys, re
from minor_check import rows, det, interp_coeffs
def perm_sign(seq):
    seq = list(seq); s = 1
    for i in range(len(seq)):
        for j in range(i+1, len(seq)):
            if seq[i] > seq[j]: s = -s
    return s
def pluck(M, r):
    n = 9; out = {}
    for t in itertools.combinations(range(n), r):
        comp = [k for k in range(n) if k not in t]
        out[t] = perm_sign(list(t) + comp) * det([[row[k] for k in comp] for row in M])
    return out
def q_of(q, tup):
    if len(set(tup)) < len(tup): return Fr(0)
    srt = tuple(sorted(tup)); return perm_sign(tup) * q[srt]   # alternating
def basis_from(q, r):
    S0 = max(q, key=lambda t: abs(q[t]))
    assert q[S0] != 0
    B = []
    for j in range(r):
        B.append([q_of(q, S0[:j] + (k,) + S0[j+1:]) / q[S0] for k in range(9)])
    return B
def has_identity(B):
    # unknown coefficients c (len r): sum c_j B_j[spatial] = I ; spatial indices (1,1)=4,(1,2)=5,(2,1)=7,(2,2)=8
    idx = [4, 5, 7, 8]; tgt = [Fr(1), Fr(0), Fr(0), Fr(1)]; r = len(B)
    A = [[B[j][i] for j in range(r)] + [t] for i, t in zip(idx, tgt)]
    # rank test by elimination
    def rank(Mx):
        Mx = [x[:] for x in Mx]; rk = 0
        for c in range(len(Mx[0])):
            p = next((i for i in range(rk, len(Mx)) if Mx[i][c] != 0), None)
            if p is None: continue
            Mx[rk], Mx[p] = Mx[p], Mx[rk]
            for i in range(len(Mx)):
                if i != rk and Mx[i][c] != 0:
                    f = Mx[i][c]/Mx[rk][c]; Mx[i] = [a - f*b for a, b in zip(Mx[i], Mx[rk])]
            rk += 1
        return rk
    return rank([a[:-1] for a in A]) == rank(A)
def verdict(labels, x0):
    s = len(labels); r = 9 - s
    # validate rank s at a generic h and the sign convention
    hv = Fr(5, 11); Mv = rows(labels, x0, x0 + hv)
    qv = pluck(Mv, r)
    Bv = basis_from(qv, r)
    for u in Bv:
        assert all(sum(a*b for a, b in zip(row, u)) == 0 for row in Mv), 'sign convention failed'
    hs = [Fr(k, 97) for k in range(1, 2*s + 3)]
    samples = [pluck(rows(labels, x0, x0 + h), r) for h in hs]
    polys = {t: interp_coeffs(hs, [smp[t] for smp in samples]) for t in samples[0]}
    for m in range(len(hs)):
        q0 = {t: polys[t][m] for t in polys}
        if any(q0.values()): break
    return has_identity(basis_from(q0, r)), m
if __name__ == '__main__':
    k = int(sys.argv[1]); agree = dis = 0
    for line in open(f'census_k{k}.log'):
        mm = re.match(rf"k={k} \(([\d, ]+)\): .*criterion=(\w+)", line)
        if not mm: continue
        S = tuple(int(x) for x in mm.group(1).split(',')); v1 = mm.group(2)
        vs = []
        for x0 in (Fr(2, 7), Fr(-5, 3)):
            ok, m = verdict(S, x0); vs.append('HOLDS' if ok else 'FAILS')
        good = all(v == v1 for v in vs); agree += good; dis += (not good)
        print(S, 'census', v1, 'plucker', vs, f'm={m}', 'AGREE' if good else 'DISAGREE', flush=True)
    print(f"SUMMARY k={k} agree {agree} disagree {dis}")
