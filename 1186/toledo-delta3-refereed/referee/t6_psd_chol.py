# My own exact PSD proof: scale, float Cholesky of A - tau I, round factor to dyadic, exact remainder diagonally dominant.
import json, sys, time
from fractions import Fraction as F
from math import lcm
import numpy as np
A = [[F(x) for x in row] for row in json.load(open(sys.argv[1]))]
n = len(A)
assert all(A[i][j] == A[j][i] for i in range(n) for j in range(n))
assert all(A[i][i] > 0 for i in range(n))
# exact dyadic rescale A' = D A D with D_i = 2^-k_i
k = [round(np.log2(float(A[i][i]))/2) for i in range(n)]
As = [[A[i][j] * F(2)**(-(k[i]+k[j])) for j in range(n)] for i in range(n)]
den = 1
for row in As:
    for x in row: den = lcm(den, x.denominator)
Z = [[int(x*den) for x in row] for row in As]
Fl = np.array([[float(x) for x in row] for row in As])
print('n', n, 'den bits', den.bit_length(), 'float min eig of rescaled', np.linalg.eigvalsh(Fl).min())
for e in range(1, 60):
    tau = 2.0**-e
    try: L = np.linalg.cholesky(Fl - tau*np.eye(n))
    except np.linalg.LinAlgError: continue
    T = e + 60
    Lz = [[int(round(x * 2**T)) for x in row] for row in L]
    scale = 1 << (2*T)
    # E = (A' - Lt Lt^T) * den * 2^(2T)
    worst = None; strict = True
    LzT = list(zip(*Lz))
    for i in range(n):
        Li = Lz[i]
        row = []
        for j in range(n):
            g = sum(a*b for a, b in zip(Li, Lz[j]))
            row.append(Z[i][j]*scale - g*den)
        off = sum(abs(row[j]) for j in range(n) if j != i)
        margin = row[i] - off
        worst = margin if worst is None else min(worst, margin)
    print('tau=2^-%d  min row margin (scaled) = %s  -> %s' % (e, '%.3e' % (worst / (den*scale)), 'DOMINANT' if worst >= 0 else 'not dominant'))
    if worst >= 0:
        diagL = all(Lz[i][i] != 0 for i in range(n))
        print('PSD PROVED exactly; strict margin:', worst > 0, ' dyadic factor nonsingular:', diagL, '=> PD' if (worst > 0 or diagL) else '')
        break
