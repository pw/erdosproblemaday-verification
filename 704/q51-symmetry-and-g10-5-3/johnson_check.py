"""Second route for q_i = v^T E_i v: numerically project v = 1_W onto the eigenspaces of A_1 (the 'meet in 4' adjacency of J(13,5))
by Lagrange polynomials in A_1 applied to v (float64), compare with the exact Eberlein-formula values."""
import numpy as np
from itertools import combinations
from fractions import Fraction
from wstruct import WA
V = [frozenset(c) for c in combinations(range(13), 5)]; n = len(V)
A = np.zeros((n, n))
for i in range(n):
    for j in range(i + 1, n):
        if len(V[i] & V[j]) == 4: A[i, j] = A[j, i] = 1
theta = [(5 - i) * (8 - i) - i for i in range(6)]                       # 40, 27, 16, 7, 0, -5
ev = np.linalg.eigvalsh(A); mult = {t: int(np.sum(np.abs(ev - t) < 1e-6)) for t in theta}
print('eigenvalues/multiplicities of A_1:', mult)
v = np.array([1.0 if s in WA else 0.0 for s in V])
exact = [Fraction(11, 13), Fraction(32, 715), Fraction(389, 77), Fraction(472, 35), Fraction(347, 35), Fraction(128, 35)]
for i in range(6):
    w = v.copy()
    for j in range(6):
        if j != i: w = (A @ w - theta[j] * w) / (theta[i] - theta[j])
    print(f'i={i}: numeric v^T E_i v = {v @ w:.10f}   exact {exact[i]} = {float(exact[i]):.10f}')
