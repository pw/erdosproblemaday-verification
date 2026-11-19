# Independent exact PD proof of the inner P (Sylvester via fraction-free Bareiss), with my own code.
import json, sys, time
from fractions import Fraction as F
from math import lcm
P = [[F(x) for x in row] for row in json.load(open(sys.argv[1]))]
n = len(P)
assert all(P[i][j] == P[j][i] for i in range(n) for j in range(n))
D = 1
for row in P:
    for x in row: D = lcm(D, x.denominator)
print('n', n, 'lcm denominator bits', D.bit_length())
Z = [[int(x*D) for x in row] for row in P]
t0 = time.time()
A = [r[:] for r in Z]; prev = 1; signs = []
for k in range(n):
    piv = A[k][k]
    signs.append(piv > 0)
    if piv <= 0:
        print('leading minor', k+1, 'is', 'zero' if piv == 0 else 'negative'); break
    for i in range(k+1, n):
        Aik = A[i][k]
        row_i = A[i]; row_k = A[k]
        for j in range(k+1, n):
            row_i[j] = (piv*row_i[j] - Aik*row_k[j]) // prev
    prev = piv
print('all %d leading principal minors > 0:' % n, all(signs) and len(signs) == n, ' %.1f s' % (time.time()-t0), ' det bits', prev.bit_length())
