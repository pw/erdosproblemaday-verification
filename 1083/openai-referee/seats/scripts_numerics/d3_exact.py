# (d'') exact rational versions (sympy) of the rank/codimension/nonemptiness claims around (2.6)-(2.8), d = 3, 4.
# Equal-norm rational pairs are produced exactly by a rational orthogonal Q (Cayley transform of a rational skew K).
import random
from sympy import Matrix, Rational as R, eye, zeros
random.seed(20261012)
def rr(): return R(random.randint(-9, 9), random.randint(1, 5))
def skew_basis(d):
    B = []
    for i in range(d):
        for j in range(i+1, d):
            E = zeros(d, d); E[i, j] = 1; E[j, i] = -1; B.append(E)
    return B
def cayley(d):
    K = zeros(d, d)
    for i in range(d):
        for j in range(i+1, d):
            x = rr(); K[i, j] = x; K[j, i] = -x
    return (eye(d) - K).inv()*(eye(d) + K)
for d in (3, 4):
    Bs = skew_basis(d); s0 = len(Bs)
    tallies = {"eq_norm_nonempty_codim_d-1": 0, "neq_norm_empty": 0, "u+w=0_empty": 0, "trials": 0}
    for _ in range(40):
        u = Matrix([rr() for _ in range(d)])
        if u.norm() == 0: continue
        Q = cayley(d); assert Q.T*Q == eye(d)
        w = Q*u                                   # |w| = |u| exactly
        if (u + w).norm() == 0: continue
        x, y = u + w, u - w
        Ax = Matrix.hstack(*[E*x for E in Bs])     # d x s0 : Z -> Z x in the skew basis
        rk, rka = Ax.rank(), Matrix.hstack(Ax, y).rank()
        tallies["trials"] += 1
        if rk == d-1 and rka == d-1: tallies["eq_norm_nonempty_codim_d-1"] += 1
        w2 = R(3, 2)*w; x2, y2 = u + w2, u - w2      # |w2| != |u|
        A2 = Matrix.hstack(*[E*x2 for E in Bs])
        if A2.rank() == d-1 and Matrix.hstack(A2, y2).rank() == d: tallies["neq_norm_empty"] += 1
        A3 = Matrix.hstack(*[E*zeros(d, 1) for E in Bs]); y3 = 2*u      # w = -u: Z*0 = 2u impossible
        if Matrix.hstack(A3, y3).rank() > A3.rank(): tallies["u+w=0_empty"] += 1
    print(f"d={d} (s0={s0}): {tallies}")
    # distinct pairs give distinct flats: v -> (Z -> Z v) is injective (stacked d*s0 x d matrix has rank d)
    M = Matrix.vstack(*[E for E in Bs])            # rows: E v for each basis E, as a (d*s0) x d linear map in v
    print(f"   rank of v |-> (E v)_E over all skew basis E: {M.rank()} (= d -> Z v0 = Z v0' for all skew Z forces v0 = v0')")
    # flat F_{p,q} dimension: unknowns (z, c) in C^(s0+d), equations Z v0 + c = y0 (d independent equations, c-block = I)
    v0 = Matrix([rr() for _ in range(d)])
    Mflat = Matrix.hstack(Matrix.hstack(*[E*v0 for E in Bs]), eye(d))
    print(f"   F_pq: rank of (Z,c)-system = {Mflat.rank()}, dim = s0 + d - rank = {s0 + d - Mflat.rank()} (claimed s0 = {s0})")
    # neighbour flat inside F_pq: Z(u+w) = u-w has codim d-1, so a hypersurface of F has excess h = (s0-1)-(s0-(d-1)) = d-2
    print(f"   excess dimension of a hypersurface component over a neighbour flat: {(s0-1)-(s0-(d-1))} (claimed d-2 = {d-2} = r-1, r = d-1)")
