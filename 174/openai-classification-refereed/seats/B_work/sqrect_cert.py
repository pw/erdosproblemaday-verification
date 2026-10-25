#!/usr/bin/env python3
"""Blind seat B: does the square+rectangle admit a FIRST-ORDER derivation certificate in the sense of Palvolgyi's
Lemma A.1 (mixed moment M = sum l D(p) p^T only required SYMMETRIC, not zero)?  D = d/dtau on Q(tau).
(1) solve the Lemma A.1 conditions; (2) report energy; (3) verify the invariance identity on an explicit congruent copy
in R^3 whose entries are rational functions of tau (and of a second parameter s with D(s)=0), so D acts on them."""
import sympy as sp
t, s = sp.symbols('tau s')
u, v = (1 - t**2)/(1 + t**2), 2*t/(1 + t**2)
P = [(sp.Integer(1), sp.Integer(0)), (sp.Integer(-1), sp.Integer(0)), (sp.Integer(0), sp.Integer(1)), (sp.Integer(0), sp.Integer(-1)),
     (u, v), (u, -v), (-u, v), (-u, -v)]
n = len(P); lam = sp.symbols('l0:%d' % n)
D = lambda e: sp.diff(e, t)
p = [sp.Matrix([x, y]) for x, y in P]; dp = [p_.applyfunc(D) for p_ in p]
eqs = [sum(lam), *(sum(lam[i]*p[i][k] for i in range(n)) for k in range(2))]
Q = sum((lam[i]*p[i]*p[i].T for i in range(n)), sp.zeros(2)); eqs += list(Q)
eqs += [sum(lam[i]*dp[i][k] for i in range(n)) for k in range(2)]
M = sum((lam[i]*dp[i]*p[i].T for i in range(n)), sp.zeros(2))
eqs_sym = eqs + [M[0, 1] - M[1, 0]]            # Lemma A.1: M symmetric
eqs_zero = eqs + list(M)                        # derivation_cert.py: M = 0 (stronger)
for name, E_ in (('M symmetric (Lemma A.1)', eqs_sym), ('M = 0 (derivation_cert.py)', eqs_zero)):
    sol = list(sp.linsolve([sp.numer(sp.together(e)) for e in E_], lam))[0]
    free = sorted(set().union(*[x.free_symbols for x in sol]) - {t}, key=str)
    En = sp.simplify(sum(sol[i]*(dp[i].T*dp[i])[0] for i in range(n)))
    Msol = sp.simplify(M.subs(dict(zip(lam, sol))))
    print(f"{name}: solution dim {len(free)}; weights {[sp.simplify(x) for x in sol]}; energy {En}; M = {Msol.tolist()}")
# explicit certificate and invariance check on a copy in R^3
lam0 = [-2*u**2, -2*u**2, -2*v**2, -2*v**2, 1, 1, 1, 1]
w = s  # second parameter; D(s) = 0 under d/dtau, but we also mix tau into the embedding
c1, s1 = (1 - (t*s)**2)/(1 + (t*s)**2), 2*t*s/(1 + (t*s)**2)       # cos/sin rational in tau, s
c2, s2 = (1 - (t + s)**2)/(1 + (t + s)**2), 2*(t + s)/(1 + (t + s)**2)
R1 = sp.Matrix([[c1, -s1, 0], [s1, c1, 0], [0, 0, 1]]); R2 = sp.Matrix([[1, 0, 0], [0, c2, -s2], [0, s2, c2]])
A = (R2*R1)[:, :2]                                # 3x2, A^T A = I
assert sp.simplify(A.T*A - sp.eye(2)) == sp.zeros(2)
tr = sp.Matrix([t**2, 1/(1 + t), s*t])
total = 0
for i in range(n):
    q = tr + A*p[i]
    dq = q.applyfunc(D)
    total += lam0[i]*(dq.T*dq)[0]
total = sp.simplify(total)
base = sp.simplify(sum(lam0[i]*(dp[i].T*dp[i])[0] for i in range(n)))
print('energy of the original set:', base)
print('energy of a tau-dependent congruent copy in R^3 minus original:', sp.simplify(total - base))
