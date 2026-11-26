"""Test the counting identities of Sections 6-7 on planted random tournaments
(N=51, a pair P={a,b} whose dominator set R is a 5-regular 11-set, every
y in O beaten by >=5 vertices of R), computing every quantity from the
definition and comparing with the paper's formula (in its general form,
i.e. without assuming the q_y structure that the proof later derives):

 (6)   D(U) for U subset R
 (I1)  #{y in O: r notin Q_y} = 20 + j_r          (j_r := d^-(r)-25)
 (I2)  sum_y q_y = 198 - J
 (I3)  sum_v c(u,v) = 20, c<=4
 (*)   sum_{U ∋ r} |D(U)| = 30 + sum_{y in O, y->r} C(10-q_y, 2)
 (tri) sum_{U subset R} |D(U)| = 110 + sum_y C(11-q_y,3)
 (R1g) s(u,v) = 3c + sum_{y in O: u,v notin Q_y} (9-q_y) - 45
 (R2g) via (R1g) summed
 Gram: G_{zz'} = |D(v,z,z')|, sum_z |D(v,z)| = sum_{x in N^-(v)} (d^+(x)-1)
 rowsum of M on a tight pair = sum_{y in O}(q_y-5)
Also Lemma 6.1 inequality chain: sum_{U∋r}|D(U)| <= 30 + 10*(d^-(r)-5).
"""
import sys, itertools, random
from math import comb
import numpy as np
sys.path.insert(0, '/home/exedev/MathDyad/subs-1126/902/refA')
from tlib import *

rng = random.Random(902)


def planted(seed):
    rng = random.Random(seed)
    N = 51
    A = np.zeros((N, N), dtype=np.int8)
    for i in range(N):
        for j in range(i + 1, N):
            if rng.random() < 0.5:
                A[i, j] = 1
            else:
                A[j, i] = 1
    a, b = 0, 1
    R = list(range(2, 13))
    O = list(range(13, 51))
    perm = R[:]
    rng.shuffle(perm)
    for x in R:
        for z in R:
            A[x, z] = 0
    for i in range(11):
        for d in range(1, 6):
            x, z = perm[i], perm[(i + d) % 11]
            A[x, z] = 1
            A[z, x] = 0
    for r in R:
        A[r, a] = 1; A[a, r] = 0
        A[r, b] = 1; A[b, r] = 0
    for y in O:
        A[a, y] = 1; A[y, a] = 0  # y does not beat a, so y notin D(P)
        # make y beaten by >=5 of R
        beaters = [r for r in R if A[r, y]]
        while len(beaters) < 5:
            r = rng.choice([r for r in R if r not in beaters])
            A[r, y] = 1; A[y, r] = 0
            beaters.append(r)
    check_tournament(A)
    return A, (a, b), R, O


def run(seed):
    A, (a, b), R, O = planted(seed)
    N = A.shape[0]
    inm = inmasks(A)
    outm = outmasks(A)
    pc = popcount
    Rmask = sum(1 << r for r in R)
    assert inm[a] & inm[b] == Rmask, "D(P) != R"
    indeg = A.sum(0)
    j = {r: int(indeg[r]) - 25 for r in R}
    J = sum(j.values())
    Q = {y: inm[y] & Rmask for y in O}  # vertices of R beating y
    q = {y: pc(Q[y]) for y in O}
    bad = []
    # (6)
    for U in itertools.combinations(R, 3):
        d = inm[U[0]] & inm[U[1]] & inm[U[2]]
        Um = sum(1 << x for x in U)
        rhs = 0
        for w in R:
            if w not in U and (outm[w] & Um) == Um:
                rhs |= 1 << w
        for y in O:
            if Q[y] & Um == 0:
                rhs |= 1 << y
        if d != rhs:
            bad.append(('(6)', U))
    # (I1)
    for r in R:
        lhs = sum(1 for y in O if not (Q[y] >> r) & 1)
        if lhs != 20 + j[r]:
            bad.append(('I1', r, lhs, 20 + j[r]))
    # (I2)
    if sum(q.values()) != 198 - J:
        bad.append(('I2', sum(q.values()), 198 - J))
    # (I3)
    c = {}
    for u in R:
        for v in R:
            if u != v:
                c[(u, v)] = pc(inm[u] & inm[v] & Rmask)
        if sum(c[(u, v)] for v in R if v != u) != 20:
            bad.append(('I3sum', u))
    if max(c.values()) > 4:
        bad.append(('I3max',))
    # (*) and Lemma 6.1 chain
    for r in R:
        lhs = 0
        for x, z in itertools.combinations([s for s in R if s != r], 2):
            lhs += pc(inm[r] & inm[x] & inm[z])
        rhs = 30 + sum(comb(10 - q[y], 2) if 10 - q[y] >= 2 else 0 for y in O if not (Q[y] >> r) & 1)
        if lhs != rhs:
            bad.append(('(*)', r, lhs, rhs))
        if lhs > 30 + 10 * (int(indeg[r]) - 5):
            bad.append(('L6.1chain', r))
    # (tri)
    lhs = sum(pc(inm[x] & inm[y_] & inm[z]) for x, y_, z in itertools.combinations(R, 3))
    rhs = 110 + sum(comb(11 - q[y], 3) if 11 - q[y] >= 3 else 0 for y in O)
    if lhs != rhs:
        bad.append(('tri', lhs, rhs))
    # (R1g)
    for u, v in itertools.permutations(R, 2):
        s = sum(pc(inm[u] & inm[v] & inm[w]) - 5 for w in R if w not in (u, v))
        f = 3 * c[(u, v)] + sum(9 - q[y] for y in O if not (Q[y] >> u) & 1 and not (Q[y] >> v) & 1) - 45
        if s != f:
            bad.append(('R1g', u, v, s, f))
    # Gram identities at v=a (any v works)
    for v in [a, 20, 33]:
        others = [z for z in range(N) if z != v]
        Dz = {z: inm[v] & inm[z] for z in others}
        for z, z2 in itertools.combinations(others, 2):
            if pc(Dz[z] & Dz[z2]) != pc(inm[v] & inm[z] & inm[z2]):
                bad.append(('Gram', v, z, z2))
                break
        Ain = [x for x in range(N) if A[x, v]]
        if sum(pc(Dz[z]) for z in others) != sum(int(A[x].sum()) - 1 for x in Ain):
            bad.append(('sumDz', v))
        # rank of Gram <= d^-(v)
        Mvec = np.array([[(Dz[z] >> x) & 1 for x in Ain] for z in others], dtype=float)
        G = Mvec @ Mvec.T
        if np.linalg.matrix_rank(G) > len(Ain):
            bad.append(('rank', v))
    # M row sum for the tight pair P={a,b} viewed from v=a, z=b
    rows = sum(pc(inm[a] & inm[b] & inm[z2]) - 5 for z2 in range(N) if z2 not in (a, b))
    if rows != sum(q[y] - 5 for y in O):
        bad.append(('Mrow', rows))
    if rows != 8 - J:
        bad.append(('Mrow=8-J', rows, 8 - J))
    return bad, J, sorted(q.values())


if __name__ == '__main__':
    tot = 0
    for seed in range(int(sys.argv[1]) if len(sys.argv) > 1 else 20):
        bad, J, qs = run(seed)
        tot += len(bad)
        print(f"seed {seed}: J={J} q-multiset head={qs[:6]}... failures={bad[:3]}")
    print("TOTAL FAILURES:", tot)
