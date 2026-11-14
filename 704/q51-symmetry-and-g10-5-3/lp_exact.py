"""Exact rational verification of the LP solutions: re-solve on the float support in Fractions; check z >= 0, cover rows = 1, cuts."""
import json, sys, numpy as np
from fractions import Fraction
mode = sys.argv[1]
with open('lp_cols.bin', 'rb') as f:
    n = int(np.frombuffer(f.read(8), dtype=np.int64)[0]); D = int(np.frombuffer(f.read(4), dtype=np.int32)[0])
    C = np.frombuffer(f.read(n * D), dtype=np.uint8).reshape(n, D)
O = json.load(open('orbits.json')); n5, n4, n6, npt = O['n5'], O['n4'], O['n6'], O['npt']
Wf = [int(x) for x in open('W_features.txt').read().split()]
sup = json.load(open(f'lp_{mode}_feasible.json'))['support']; cols = [c for c, _ in sup]; m = len(cols)
A = [[Fraction(int(C[c, r])) for c in cols] + [Fraction(O['size5'][r])] for r in range(n5)]
# Gaussian elimination over Q (n5 x m system, expect a unique solution on this support)
piv = []; r = 0
for c in range(m):
    p = next((i for i in range(r, n5) if A[i][c] != 0), None)
    if p is None: continue
    A[r], A[p] = A[p], A[r]; inv = 1 / A[r][c]; A[r] = [x * inv for x in A[r]]
    for i in range(n5):
        if i != r and A[i][c] != 0:
            fct = A[i][c]; A[i] = [x - fct * y for x, y in zip(A[i], A[r])]
    piv.append(c); r += 1
assert all(all(x == 0 for x in row[:m]) and row[m] == 0 for row in A[r:]), 'inconsistent'
z = [Fraction(0)] * m
for i, c in enumerate(piv): z[c] = A[i][m]
print('rank', r, 'of', m, 'support columns; min z =', min(z), '; sum z =', sum(z))
ok_cover = all(sum(z[k] * int(C[cols[k], rr]) for k in range(m)) == O['size5'][rr] for rr in range(n5))
cut4 = all(sum(z[k] * int(C[cols[k], n5 + o]) for k in range(m)) <= 4 * O['size4'][o] - Wf[n5 + o] for o in range(n4))
cut6 = all(sum(z[k] * int(C[cols[k], n5 + n4 + o]) for k in range(m)) <= 3 * O['size6'][o] - Wf[n5 + n4 + o] for o in range(n6))
cpt = all(sum(z[k] * int(C[cols[k], n5 + n4 + n6 + o]) for k in range(m)) >= O['sizept'][o] - Wf[n5 + n4 + n6 + o] for o in range(npt))
print('exact: z >= 0:', min(z) >= 0, '| cover rows exact:', ok_cover, '| 4-set cuts:', cut4, '| 6-set cuts:', cut6, '| point rows:', cpt)
json.dump(dict(cols=cols, z=[str(x) for x in z]), open(f'lp_{mode}_exact.json', 'w'))
