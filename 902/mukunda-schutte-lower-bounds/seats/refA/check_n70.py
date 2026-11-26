"""Load the 70-vertex tournament (plain text; line v = out-neighbours of v),
check it is a tournament with S_4, nu_1..nu_3, and test Lemma 6.1 / 6.3 hypotheses
wherever tight pairs / in-degree-24 vertices occur."""
import sys, itertools
import numpy as np
sys.path.insert(0, '/home/exedev/MathDyad/subs-1126/902/refA')
from tlib import *
lines = [l.split() for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
n = len(lines)
A = np.zeros((n, n), dtype=np.int8)
for v, l in enumerate(lines):
    for w in l:
        A[v, int(w)] = 1
check_tournament(A)
inm = inmasks(A)
indeg = A.sum(0)
print("n =", n, "in-degree range", indeg.min(), indeg.max())
print("nu1,nu2,nu3 =", min_dom(A, 1), min_dom(A, 2), min_dom(A, 3))
ok, w = has_S(A, 4)
print("S4:", ok, w)
tight = [(i, j) for i, j in itertools.combinations(range(n), 2) if popcount(inm[i] & inm[j]) == 11]
print("tight pairs:", len(tight))
viol = 0
for i, j in tight:
    R = inm[i] & inm[j]
    for r in range(n):
        if (R >> r) & 1 and indeg[r] < 25:
            viol += 1
print("Lemma 6.1 violations (tight-pair dominator with in-degree < 25):", viol)
Z = [v for v in range(n) if indeg[v] == 24]
print("in-degree-24 vertices:", len(Z))
for v in Z:
    Av = [x for x in range(n) if A[x, v]]
    ntight = sum(1 for a in Av if popcount(inm[a] & inm[v]) == 11)
    nz = sum(1 for a in Av if a in Z)
    print(f"  v={v}: tight pairs at v = {ntight} (Lemma 6.3 says >=12), in-nbrs in Z = {nz} (<=2)")
