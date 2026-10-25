#!/usr/bin/env python3
"""Exact decision procedure for the field criterion of Theorem 1.1 (OpenAI family 172) on configurations whose
coordinates lie in F = Q(tau), tau transcendental (or F = Q).  Ours, 21 Oct 2026, written independently of OpenAI's
proofs and Lean.

B = F (x)_Q F embeds in Q(x, y) (tau -> x on the left, tau -> y on the right).  m_F is y -> x.  The kernel K of the
B-linear evaluation map P |-> ((p_i(x))^T P p_i(y))_i is computed over Frac(B) = Q(x,y); since the multiplication
prime p = ker m_F has B_p = Q[x,y]_(x-y) a DVR, the F-span of m_F(K) equals the reduction mod (x - y) of a saturated
B_p-basis of K (B-generators and B_p-generators give the same F-span because denominators outside p become units).
Saturation: while the reductions are F-dependent, combine with polynomial-in-x coefficients (units of B_p), divide by
(x - y), replace.  Criterion holds  <=>  some element of that F-span has spatial block I_d (constant row/col free).
"""
import sys, sympy as sp
from sympy.polys.matrices import DomainMatrix
x, y, tau = sp.symbols('x y tau')
K2 = sp.QQ.frac_field(x, y)
K1 = sp.QQ.frac_field(x)

def kernel_basis(pts):
    """pts: list of tuples of sympy expressions in tau. returns (d, list of kernel vectors over Q(x,y), index list)."""
    d = len(pts[0]); idx = [(al, be) for al in range(d + 1) for be in range(d + 1)]
    rows = []
    for p in pts:
        aug = [sp.Integer(1)] + list(p)
        rows.append([sp.together(aug[al].subs(tau, x) * aug[be].subs(tau, y)) for (al, be) in idx])
    M = DomainMatrix([[K2.from_sympy(e) for e in r] for r in rows], (len(rows), len(idx)), K2)
    ns = M.nullspace()           # rows of ns span the kernel
    vecs = [[K2.to_sympy(ns.rep.to_ddm()[i][j]) for j in range(len(idx))] for i in range(ns.shape[0])]
    return d, vecs, idx

def polyvec(v):
    """clear denominators; make entries polynomials in x,y with no common factor (x - y)."""
    v = [sp.together(e) for e in v]
    den = sp.lcm([sp.fraction(e)[1] for e in v])
    v = [sp.expand(sp.cancel(e * den)) for e in v]
    g = 0
    for e in v: g = sp.gcd(g, e)
    if g != 0: v = [sp.cancel(e / g) for e in v]
    return [sp.expand(e) for e in v]

def saturate(vecs):
    vecs = [polyvec(v) for v in vecs]
    r = len(vecs); it = 0
    while True:
        it += 1
        red = sp.Matrix([[sp.expand(e.subs(y, x)) for e in v] for v in vecs])   # r x N over Q(x)
        if r == 0: return vecs, red, it
        Rt = DomainMatrix([[K1.from_sympy(sp.together(e)) for e in row] for row in red.tolist()], red.shape, K1)
        # dependency among rows: left nullspace = nullspace of transpose
        dep = Rt.transpose().nullspace()
        if dep.shape[0] == 0: return vecs, red, it
        c = [sp.together(K1.to_sympy(dep.rep.to_ddm()[0][j])) for j in range(r)]
        den = sp.lcm([sp.fraction(e)[1] for e in c]); c = [sp.expand(sp.cancel(e * den)) for e in c]
        new = [sp.expand(sum(c[j] * vecs[j][k] for j in range(r))) for k in range(len(vecs[0]))]
        q = [sp.cancel(e / (x - y)) for e in new]
        for e in q:
            assert sp.fraction(sp.together(e))[1].free_symbols <= set() or sp.fraction(sp.together(e))[1] == 1, "not divisible by x-y"
        jj = next(j for j in range(r) if c[j] != 0)
        vecs[jj] = polyvec(q)
        if it > 200: raise RuntimeError('saturation did not terminate')

def criterion(pts, name=''):
    d, vecs, idx = kernel_basis(pts)
    sat, red, it = saturate(vecs) if vecs else ([], sp.zeros(0, len(idx)), 0)
    sp_idx = [k for k, (al, be) in enumerate(idx) if al >= 1 and be >= 1]
    target = [1 if idx[k][0] == idx[k][1] else 0 for k in sp_idx]
    r = len(sat)
    if r == 0:
        ok = False
    else:
        A = sp.Matrix([[red[j, k] for j in range(r)] for k in sp_idx])   # spatial entries x r
        aug = A.row_join(sp.Matrix(target))
        ok = A.rank(simplify=True) == aug.rank(simplify=True)
    print(f"{name}: s={len(pts)} d={d} kernel_dim_over_Frac={len(vecs)} saturation_steps={it} criterion={'HOLDS' if ok else 'FAILS'}", flush=True)
    return ok

if __name__ == '__main__':
    t = tau
    u, v = (1 - t**2) / (1 + t**2), 2 * t / (1 + t**2)
    Q0 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    Rp = lambda q: (u * q[0] - v * q[1], v * q[0] + u * q[1])
    Rm = lambda q: (u * q[0] + v * q[1], -v * q[0] + u * q[1])
    S = lambda L: [tuple(sp.Integer(c) if isinstance(c, int) else c for c in p) for p in L]
    res = {}
    res['three_squares'] = criterion(S([Rp(q) for q in Q0] + [Rm(q) for q in Q0] + Q0), 'Prop 7.7 three squares (expect FAILS)')
    res['two_squares'] = criterion(S([Rp(q) for q in Q0] + Q0), 'two squares Q0 u R+Q0 (transitive, expect HOLDS)')
    res['kite'] = criterion(S([(-1, 0), (1, 0), (u, v), (u, -v)]), 'kite K_a, a=u(tau) (Cor 7.5, expect HOLDS)')
    res['five'] = criterion(S([(1, 0), (0, 1), (-1, 0), (sp.Rational(3, 5), sp.Rational(4, 5)), (u, v)]), 'five circle pts, one transcendental (Cor 7.4, expect HOLDS)')
    res['collinear'] = criterion(S([(sp.Integer(0),), (sp.Integer(1),), (t,)]), 'collinear {0,1,tau} (non-spherical, expect FAILS)')
    res['rational7'] = criterion(S([(1, 0), (0, 1), (-1, 0), (0, -1), (sp.Rational(3, 5), sp.Rational(4, 5)), (sp.Rational(-5, 13), sp.Rational(12, 13)), (sp.Rational(8, 17), sp.Rational(-15, 17))]), 'seven rational circle pts (F=Q, expect HOLDS)')
    print(res)
