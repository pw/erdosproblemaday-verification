"""Verify PARI's certificates in integer arithmetic: sum_i X_i 1_{C_i} == 3 e_S (mod 9) and sum_i Y_i 1_{C_i} == 11 e_S (mod 121),
with C_1..C_1600 the first 1600 sampled copies (copies_rows.npy) and S the first 5-set. Also re-check every row is a copy."""
import re, numpy as np
from itertools import combinations
from wstruct import V
M = np.load('copies_rows_1600.npy').astype(object)          # rows = copies
assert all(int(r.sum()) == 33 for r in M)
def ind(row): return [V[i] for i in range(1287) if row[i]]
for r in (0, 777, 1599):
    F = ind(M[r]); assert len(F) == 33 and all(len(a & b) != 3 for a, b in combinations(F, 2))
def load(fn): return [int(t) for t in re.findall(r'-?\d+', open(fn).read())]
X = load('cert_X9.txt'); Y = load('cert_Y121.txt'); assert len(X) == len(Y) == 1600
tx = [0] * 1287; ty = [0] * 1287
for i in range(1600):
    if X[i] or Y[i]:
        row = M[i]
        for c in range(1287):
            if row[c]: tx[c] += X[i]; ty[c] += Y[i]
okx = all((tx[c] - (3 if c == 0 else 0)) % 9 == 0 for c in range(1287))
oky = all((ty[c] - (11 if c == 0 else 0)) % 121 == 0 for c in range(1287))
print('X certificate (3 e_S mod 9):', okx, '| Y certificate (11 e_S mod 121):', oky, '| nonzero coefficients:', sum(1 for v in X if v), sum(1 for v in Y if v))
# negative control: perturb one coefficient
X2 = list(X); X2[next(i for i, v in enumerate(X) if v)] += 1
t2 = [0] * 1287
for i in range(1600):
    if X2[i]:
        for c in range(1287):
            if M[i][c]: t2[c] += X2[i]
print('perturbed X rejected:', not all((t2[c] - (3 if c == 0 else 0)) % 9 == 0 for c in range(1287)))
