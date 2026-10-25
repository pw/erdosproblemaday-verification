#!/usr/bin/env python3
"""Re-check (main seat) of seat B's finding: Palvolgyi's Lemma A.1 certificates need sum l = 0, sum l p = 0, sum l p p^T = 0,
sum l D(p) = 0 and M = sum l D(p) p^T SYMMETRIC (not zero; derivation_cert.py imposed M = 0, the special case of his Thm 1 and
OpenAI's (31)). Cross term 2 tr(D(A)^T A M) vanishes because D(A)^T A is skew when A^T A = I. D = d/dt on Q(t)."""
import sympy as sp
t = sp.symbols('t'); u, v = (1 - t**2)/(1 + t**2), 2*t/(1 + t**2)
def cert(P, name):
    n = len(P); lam = sp.symbols(f'l0:{n}')
    p = [sp.Matrix([x, y]) for x, y in P]; dp = [sp.Matrix([sp.diff(x, t), sp.diff(y, t)]) for x, y in P]
    eqs = [sum(lam), *(sum(lam[i]*p[i][k] for i in range(n)) for k in range(2))]
    S = sum((lam[i]*p[i]*p[i].T for i in range(n)), sp.zeros(2)); eqs += [S[0,0], S[0,1], S[1,1]]
    eqs += [sum(lam[i]*dp[i][k] for i in range(n)) for k in range(2)]
    M = sum((lam[i]*dp[i]*p[i].T for i in range(n)), sp.zeros(2)); eqs += [M[0,1] - M[1,0]]
    sol = list(sp.linsolve([sp.numer(sp.together(e)) for e in eqs], lam))[0]
    free = sorted(set().union(*[s.free_symbols for s in sol]) - {t}, key=str)
    E = sp.factor(sp.simplify(sum(sol[i]*(dp[i].T*dp[i])[0] for i in range(n))))
    Msol = sp.simplify(M.subs(dict(zip(lam, sol))))
    print(f"{name}: dim {len(free)}; energy {E}; M = {Msol.tolist()}")
Q0 = [(sp.Integer(1), sp.Integer(0)), (sp.Integer(0), sp.Integer(1)), (sp.Integer(-1), sp.Integer(0)), (sp.Integer(0), sp.Integer(-1))]
rect = [(u, v), (-u, -v), (u, -v), (-u, v)]
if __name__ == "__main__": cert(Q0 + rect, 'square + rectangle')
if __name__ == "__main__": Rp = [(u*a - v*b, v*a + u*b) for a, b in Q0]; Rm = [(u*a + v*b, -v*a + u*b) for a, b in Q0]
if __name__ == "__main__": cert(Q0 + Rp, 'two squares (transitive control: must be dim 0 or energy 0)')
if __name__ == "__main__": cert(Q0 + [Rp[0], Rp[1], Rm[0]], 'a passing 7-subset (0,1,4,8,9,10,11) control')
