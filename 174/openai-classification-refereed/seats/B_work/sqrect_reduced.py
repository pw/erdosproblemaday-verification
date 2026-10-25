import sys; sys.path.insert(0, '/tmp/oaimath/172/compute')
import sympy as sp
from criterion import kernel_basis, saturate, tau, x
t = tau; u, v = (1 - t**2)/(1 + t**2), 2*t/(1 + t**2)
P = [(sp.Integer(1), sp.Integer(0)), (sp.Integer(0), sp.Integer(1)), (sp.Integer(-1), sp.Integer(0)), (sp.Integer(0), sp.Integer(-1)),
     (u, v), (-u, -v), (u, -v), (-u, v)]
d, vecs, idx = kernel_basis(P)
sat, red, it = saturate(vecs)
print('kernel dim', len(vecs), 'steps', it)
for j in range(len(sat)):
    row = [sp.factor(red[j, k]) for k in range(9)]
    print('reduced vector', j, 'spatial block', [[row[4], row[5]], [row[7], row[8]]])
    print('   const row/col', row[0], row[1], row[2], row[3], row[6])
