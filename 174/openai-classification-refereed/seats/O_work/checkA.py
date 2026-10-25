# Task (A): explicit instance of Prop 2.4's colouring for non-spherical sets,
# plus a check that the explicit (multiplicative) route is impossible for spherical sets.
import random, itertools
from fractions import Fraction as Fr
import sympy as sp

random.seed(172)

def solve_c(A):
    """Find c_i with sum c_i = 0, sum c_i a_i = 0, sum c_i |a_i|^2 = -1 (exact), or None."""
    s = len(A); d = len(A[0])
    c = sp.symbols('c0:%d' % s)
    eqs = [sum(c)]
    for a in range(d):
        eqs.append(sum(c[i]*A[i][a] for i in range(s)))
    eqs.append(sum(c[i]*sum(x*x for x in A[i]) for i in range(s)) + 1)
    sol = sp.solve(eqs, c, dict=True)
    if not sol: return None
    sol = sol[0]
    # set free params to 0
    vals = [sp.nsimplify(sol.get(ci, ci)).subs({cj: 0 for cj in c}) for ci in c]
    return [sp.Rational(v) for v in vals]

def verify_identity(A, cvals):
    """Check sum_i c_i (v + a_i.u)^2 + L(uu^T) == 0 identically, L(M) = -sum c_i a_i^T M a_i, and L(I)=1."""
    d = len(A[0])
    v = sp.Symbol('v'); u = sp.symbols('u0:%d' % d)
    expr = sum(cvals[i]*(v + sum(A[i][a]*u[a] for a in range(d)))**2 for i in range(len(A)))
    Lmat = -sum((cvals[i]*sp.Matrix(A[i])*sp.Matrix(A[i]).T for i in range(len(A))), sp.zeros(d, d))
    uu = sp.Matrix(u)
    expr += (uu.T*Lmat*uu)[0]
    return sp.expand(expr) == 0, sp.simplify(Lmat.trace())

def rat_unit(D):
    # inverse stereographic projection of a random rational point -> rational point on S^{D-1}
    s = [Fr(random.randint(-9, 9), random.randint(1, 9)) for _ in range(D-1)]
    n2 = sum(x*x for x in s)
    return [2*x/(1+n2) for x in s] + [(1-n2)/(1+n2)]

def rat_orth(D, d):
    # Cayley transform of a random rational skew matrix -> rational orthogonal; take first d columns
    S = sp.zeros(D, D)
    for i in range(D):
        for j in range(i+1, D):
            x = sp.Rational(random.randint(-5, 5), random.randint(1, 5)); S[i, j] = x; S[j, i] = -x
    O = (sp.eye(D) - S)*(sp.eye(D) + S).inv()
    assert sp.simplify(O.T*O - sp.eye(D)) == sp.zeros(D, D)
    return O[:, :d]

def colour(z2, cvals, K):
    # z2 = |z|^2 ; h_i(x) = c_i x^2 so H_i(z) = c_i |z|^2
    out = []
    for ci in cvals:
        val = Fr(int(sp.numer(ci*z2)), int(sp.denom(ci*z2))) if not isinstance(ci*z2, Fr) else ci*z2
        r = val % 2                      # representative in [0,2)
        out.append(int(r * K // 2))      # label of half-open interval of length 2/K
    return tuple(out)

def run(A, name, dims, trials):
    s = len(A); d = len(A[0]); K = 2*s + 1
    cvals = solve_c(A)
    print('==', name, ' s=%d d=%d K=%d colours<=%d' % (s, d, K, K**s))
    print('   c =', cvals)
    ok, LI = verify_identity(A, cvals)
    print('   identity (5) holds symbolically:', ok, '  L(I_d) =', LI)
    bad = 0; checked = 0
    for D in dims:
        for _ in range(trials):
            Q = rat_orth(D, d)
            t = sp.Matrix([sp.Rational(random.randint(-50, 50), random.randint(1, 7)) for _ in range(D)])
            B = [t + Q*sp.Matrix(a) for a in A]
            n2 = [sp.Rational((b.T*b)[0]) for b in B]
            tot = sum(cvals[i]*n2[i] for i in range(s))
            assert tot == -1, tot          # identity (7)
            cols = [colour(Fr(int(sp.numer(x)), int(sp.denom(x))), cvals, K) for x in n2]
            checked += 1
            if len(set(cols)) == 1: bad += 1
    print('   random exact copies checked: %d, identity (7) = -1 in all, monochromatic: %d' % (checked, bad))
    return cvals, K

# Example 1: three collinear points (non-spherical), F = Q.
A1 = [[0], [1], [2]]
c1, K1 = run(A1, 'collinear {0,1,2}', dims=[1, 2, 3, 5], trials=40)

# Adversarial grid for Example 1: copies b_i = t + i*u, |u|=1, depend only on x=|t|^2, y=t.u (x>=y^2, D>=2).
# |b_0|^2 = x, |b_1|^2 = x+2y+1, |b_2|^2 = x+4y+4. Search a fine rational grid for a monochromatic triple.
cfr = [Fr(int(sp.numer(c)), int(sp.denom(c))) for c in c1]
def col(z2): return tuple(int(((ci*z2) % 2) * K1 // 2) for ci in cfr)
N = 0; mono = 0; best = 0
for xn in range(0, 4000):
    x = Fr(xn, 97)
    for yn in range(-300, 301, 3):
        y = Fr(yn, 131)
        if y*y > x: continue
        N += 1
        cs = [col(x), col(x+2*y+1), col(x+4*y+4)]
        agree = sum(1 for k in range(3) if cs[0][k] == cs[1][k] == cs[2][k])
        best = max(best, agree)
        if cs[0] == cs[1] == cs[2]: mono += 1
print('   adversarial grid: %d (x,y) pairs, monochromatic: %d, max #components agreeing on all three points: %d/3' % (N, mono, best))

# Example 2: four points in the plane, non-spherical.
A2 = [[0, 0], [1, 0], [0, 1], [2, 2]]
run(A2, 'planar {(0,0),(1,0),(0,1),(2,2)}', dims=[2, 3, 4], trials=25)

# Example 3: spherical sets -> the multiplicative ansatz l_i = c_i * m_R has NO solution.
for A in ([[0, 0], [1, 0], [0, 1]], [[1, 0], [0, 1], [-1, 0], [0, -1]], [[0], [1]]):
    print('== spherical', A, ' multiplicative obstruction exists?', solve_c(A) is not None)
