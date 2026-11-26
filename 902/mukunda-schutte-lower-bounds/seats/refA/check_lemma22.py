"""Lemma 2.2 / 2.3 on real S_4 tournaments (QR_67, QR_71, the 70-vertex one):
for every A with |A|<=3: D(A) is not dominated by any vertex; |D(A)|>=5;
for |A|<=2: T[D(A)] has min in-degree >= nu_{|A|+1} and every y outside A u D(A) is beaten by >= nu_{|A|+1} of D(A)."""
import sys, itertools
import numpy as np
sys.path.insert(0, '/home/exedev/MathDyad/subs-1126/902/refA')
from tlib import *
def load70(p):
    lines = [l.split() for l in open(p) if l.strip() and not l.startswith('#')]
    n = len(lines); A = np.zeros((n, n), dtype=np.int8)
    for v, l in enumerate(lines):
        for w in l: A[v, int(w)] = 1
    return A
for name, A in [('QR_67', paley(67)), ('QR_71', paley(71)), ('N70', load70('/home/exedev/MathDyad/subs-1126/902/repo/proof/thin_S4_N70.txt'))]:
    n = A.shape[0]; inm = inmasks(A); outm = outmasks(A)
    nu = {s: min_dom(A, s) for s in range(1, 4)}
    bad22 = bad23 = 0
    for s in range(1, 4):
        for X in itertools.combinations(range(n), s):
            R = -1
            for x in X: R &= inm[x]
            if any((outm[z] & R) == R for z in range(n)): bad22 += 1
            if popcount(R) < 5: bad22 += 1
            if s <= 2:
                Xm = sum(1 << x for x in X)
                for y in range(n):
                    if (Xm >> y) & 1: continue
                    if popcount(R & inm[y]) < nu[s + 1]: bad23 += 1
    print(f"{name}: nu={nu}  Lemma2.2 violations={bad22}  Lemma2.3 violations={bad23}", flush=True)
