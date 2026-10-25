#!/usr/bin/env python3
"""Does a first-order derivation certificate (Palvolgyi Thm 1 / OpenAI Prop 7.7 mechanism) exist for a one-parameter
configuration?  Unknown weights lambda_i in F = Q(t); D = d/dt (any derivation of Q(t) is f(t) d/dt; conditions are
homogeneous in D).  Need sum l p p^T = 0 (zeroth/first/second moments) and sum l (Dp) p^T = 0 (mixed); the certificate
is then sum l |Dp|^2 != 0.  Report the solution space of the moment identities and the energy on it."""
import sympy as sp
t = sp.symbols('t'); u, v = (1 - t**2)/(1 + t**2), 2*t/(1 + t**2)
def analyse(P, name):
    n = len(P); lam = sp.symbols(f'l0:{n}')
    pv = [sp.Matrix([1, x, y]) for x, y in P]; dp = [sp.Matrix([0, sp.diff(x, t), sp.diff(y, t)]) for x, y in P]
    eqs = []
    M0 = sum((lam[i]*pv[i]*pv[i].T for i in range(n)), sp.zeros(3)); M1 = sum((lam[i]*dp[i]*pv[i].T for i in range(n)), sp.zeros(3))
    eqs = [sp.together(e) for e in list(M0) + list(M1)]
    sol = sp.linsolve([sp.numer(e) for e in eqs], lam)
    sol = list(sol)[0]
    E = sp.simplify(sum(sol[i]*(dp[i].T*dp[i])[0] for i in range(n)))
    free = sorted(set().union(*[s.free_symbols for s in sol]) - {t}, key=str)
    print(f"{name}: solution space dim {len(free)}; energy on it = {E}")
Q0 = [(1, 0), (0, 1), (-1, 0), (0, -1)]
rect = [(u, v), (-u, -v), (u, -v), (-u, v)]
analyse([(sp.Integer(a), sp.Integer(b)) for a, b in Q0] + rect, 'square + rectangle (census FAILS)')
Rp = [(u*a - v*b, v*a + u*b) for a, b in Q0]; Rm = [(u*a + v*b, -v*a + u*b) for a, b in Q0]
analyse(Rp + Rm + [(sp.Integer(a), sp.Integer(b)) for a, b in Q0], 'three squares (Prop 7.7, certificate expected)')
