# (d) skew-form identities (2.6)-(2.8) and the polarization identities, pp. 11-13.
import numpy as np, itertools
from sympy import Matrix, Rational, symbols, zeros, eye
rng = np.random.default_rng(166)

def skew_basis(d):
    B = []
    for i in range(d):
        for j in range(i+1, d):
            E = np.zeros((d, d)); E[i, j] = 1; E[j, i] = -1; B.append(E)
    return B

def flat_system(p, q):
    """Linear system on unknowns (z_ij (i<j), c) for F_{p,q}: Z v0 + c = y0."""
    d = len(p); B = skew_basis(d); s0 = len(B)
    v0 = (p+q)/2; y0 = (p-q)/2
    Mz = np.column_stack([E @ v0 for E in B])        # d x s0
    M = np.hstack([Mz, np.eye(d)])                    # d x (s0+d)
    return M, y0

def omega(Z, c):
    d = len(c)
    O = np.zeros((d+1, d+1)); O[:d, :d] = Z; O[:d, d] = c; O[d, :d] = -c
    return O

for d in (3, 4):
    B = skew_basis(d); s0 = len(B)
    print(f"===== d={d}, s0={s0} (d(d-1)/2={d*(d-1)//2}), ambient skew forms on C^{d+1}: dim {s0+d} = d(d+1)/2 = {d*(d+1)//2}")
    worst_eval = 0.0; worst_quad = 0.0
    for trial in range(200):
        p, q = rng.normal(size=d), rng.normal(size=d)
        v0, y0 = (p+q)/2, (p-q)/2
        # random point of F_{p,q}: choose Z skew, set c = y0 - Z v0
        z = rng.normal(size=s0); Z = sum(zz*E for zz, E in zip(z, B)); c = y0 - Z @ v0
        O = omega(Z, c)
        v = np.append(v0, 1.0); y = np.append(y0, -v0 @ y0)
        worst_eval = max(worst_eval, np.abs(O @ v - y).max())
        worst_quad = max(worst_quad, abs(v0 @ Z @ v0))
    print(f"  (2.7) Omega v == y on F_pq: max residual over 200 random points {worst_eval:.2e};  v0.Z v0 = 0: max {worst_quad:.2e}")
    # converse + dimension: evaluation equation Omega v = y as a linear system in (Z,c) has rank d (last row dependent)
    p, q = rng.normal(size=d), rng.normal(size=d); v0, y0 = (p+q)/2, (p-q)/2
    v = np.append(v0, 1.0)
    rows = []
    basis_full = [omega(E, np.zeros(d)) for E in B] + [omega(np.zeros((d, d)), e) for e in np.eye(d)]
    Mfull = np.column_stack([Ob @ v for Ob in basis_full])      # (d+1) x (s0+d)
    rk_full = np.linalg.matrix_rank(Mfull); rk_first = np.linalg.matrix_rank(Mfull[:d])
    print(f"  evaluation system Omega v = y: rank of all d+1 rows = {rk_full}, rank of first d rows = {rk_first} -> flat dim = {s0+d-rk_full} (claimed s0={s0})")
    # last row is v^T Omega v - v.y == 0 identically? check: last row coefficient vector = -(first d rows)^T v0 combination
    lastrow_dep = np.linalg.matrix_rank(np.vstack([Mfull[:d], Mfull[d:]])) == rk_first
    print(f"  last (d+1)-th coordinate equation implied by first d: {lastrow_dep}  (uses v.Omega v = 0 and v.y = 0: v.y = {v @ np.append(y0, -v0@y0):.2e})")
    # distinct pairs -> distinct flats
    distinct_ok = True
    for trial in range(200):
        p, q, p2, q2 = (rng.normal(size=d) for _ in range(4))
        M1, y1 = flat_system(p, q); M2, y2 = flat_system(p2, q2)
        # same flat iff same row space AND consistent: stacked system rank == individual rank and solvable
        st = np.vstack([np.hstack([M1, y1[:, None]]), np.hstack([M2, y2[:, None]])])
        same = np.linalg.matrix_rank(st) == np.linalg.matrix_rank(M1) == np.linalg.matrix_rank(M2)
        if same: distinct_ok = False
    # also degenerate: pairs sharing p or sharing q
    p, q, q2 = rng.normal(size=d), rng.normal(size=d), rng.normal(size=d)
    M1, y1 = flat_system(p, q); M2, y2 = flat_system(p, q2)
    st = np.vstack([np.hstack([M1, y1[:, None]]), np.hstack([M2, y2[:, None]])])
    same2 = np.linalg.matrix_rank(st) == d
    print(f"  distinct random pairs give distinct flats (200 trials): {distinct_ok};  (p,q) vs (p,q') same flat? {same2}")
    # recover (p,q) from flat: Z=0 -> c=y0; then Z v0 = y0 - c for all Z determines v0
    # (2.8): F_pq cap F_p'q' = {Z : Z(u+w) = u - w}
    worst = 0.0
    for trial in range(100):
        p, q = rng.normal(size=d), rng.normal(size=d)
        u = rng.normal(size=d)
        # make |w| = |u| with w random direction
        w = rng.normal(size=d); w *= np.linalg.norm(u)/np.linalg.norm(w)
        p2, q2 = p+u, q+w
        M1, y1 = flat_system(p, q); M2, y2 = flat_system(p2, q2)
        # solve intersection, then check every solution satisfies Z(u+w)=u-w and dimension
        Mst = np.vstack([M1, M2]); yst = np.concatenate([y1, y2])
        sol, res, rk, _ = np.linalg.lstsq(Mst, yst, rcond=None)
        Zs = sum(zz*E for zz, E in zip(sol[:s0], B))
        worst = max(worst, np.abs(Zs @ (u+w) - (u-w)).max(), np.abs(Mst @ sol - yst).max())
        dim_int = s0 + d - rk
    print(f"  (2.8) intersection of neighbouring flats satisfies Z(u+w)=u-w: max residual {worst:.2e}; intersection dim = {dim_int} = s0-(d-1) = {s0-(d-1)}")
    # nonempty iff |u|=|w| (u+w != 0); codim exactly d-1 inside Z-space
    print("  {Z skew: Z x = y}, x=u+w, y=u-w:")
    for label, u, w in [("|u|=|w|", rng.normal(size=d), None), ("|u|!=|w|", rng.normal(size=d), "neq"), ("u+w=0", rng.normal(size=d), "neg")]:
        if w is None:
            w = rng.normal(size=d); w *= np.linalg.norm(u)/np.linalg.norm(w)
        elif w == "neq":
            w = rng.normal(size=d); w *= 1.3*np.linalg.norm(u)/np.linalg.norm(w)
        else:
            w = -u
        x, y = u+w, u-w
        A = np.column_stack([E @ x for E in B])   # d x s0
        rkA = np.linalg.matrix_rank(A, tol=1e-9); rkAug = np.linalg.matrix_rank(np.hstack([A, y[:, None]]), tol=1e-9)
        print(f"    {label:9s}: rank[Z->Zx] = {rkA}, rank augmented = {rkAug} -> {'NONEMPTY' if rkA==rkAug else 'EMPTY'}, codim in Z-space = {rkA if rkA==rkAug else '-'}  (x.y = |u|^2-|w|^2 = {x@y:+.3e})")
    # exact rational check of rank d-1 for a rational example
    xs = [Rational(1), Rational(2), Rational(-3), Rational(5)][:d]
    Mx = Matrix([[ (E @ np.array([float(t) for t in xs]))[i] for E in B] for i in range(d)])
    print(f"  exact rank of Z->Zx for x={xs}: {Matrix(Mx).applyfunc(lambda t: Rational(t).limit_denominator(1000)).rank()} (claimed d-1={d-1})")
    # distinct local parameters -> distinct neighbour flats  (flat {Zx=y} determines [x:y] for d>=3)
    okloc = True
    for trial in range(200):
        x1, x2 = rng.normal(size=d), rng.normal(size=d)
        A1 = np.column_stack([E @ x1 for E in B]); A2 = np.column_stack([E @ x2 for E in B])
        # direction spaces ker(A1), ker(A2) equal?
        if np.linalg.matrix_rank(np.vstack([A1, A2])) == np.linalg.matrix_rank(A1): okloc = False
    x1 = rng.normal(size=d); A1 = np.column_stack([E @ x1 for E in B]); A2 = np.column_stack([E @ (2.5*x1) for E in B])
    print(f"  non-proportional x give different direction spaces (200 trials): {okloc}; proportional x give same: {np.linalg.matrix_rank(np.vstack([A1,A2]))==np.linalg.matrix_rank(A1)}")
    # polarization identities
    wg = 0.0; wl = 0.0
    for trial in range(200):
        p, q, p2, q2 = (rng.normal(size=d) for _ in range(4))
        v0, y0, v1, y1_ = (p+q)/2, (p-q)/2, (p2+q2)/2, (p2-q2)/2
        X1 = np.concatenate([v0, [1.0], y0, [-v0 @ y0]]); X2 = np.concatenate([v1, [1.0], y1_, [-v1 @ y1_]])
        Bform = lambda X, Y: X[:d+1] @ Y[d+1:] + Y[:d+1] @ X[d+1:]
        lhs = Bform(X1, X2); rhs = -(v0-v1) @ (y0-y1_); phys = -(np.sum((p-p2)**2) - np.sum((q-q2)**2))/4
        wg = max(wg, abs(lhs-rhs), abs(rhs-phys))
        ui, wi, uj, wj = (rng.normal(size=d) for _ in range(4))
        L = (ui-wi) @ (uj+wj) + (uj-wj) @ (ui+wi); Rr = 2*(ui @ uj - wi @ wj)
        Bloc = (ui+wi) @ (uj-wj) + (uj+wj) @ (ui-wi)
        wl = max(wl, abs(L-Rr), abs(Bloc-L))
    print(f"  global polarization: B(X,X') = -(v0-v0').(y0-y0') = -(|p-p'|^2-|q-q'|^2)/4 : max err {wg:.2e}")
    print(f"  local polarization: (ui-wi).(uj+wj)+(uj-wj).(ui+wi) = 2(ui.uj - wi.wj) = B([ui+wi:ui-wi],[uj+wj:uj-wj]): max err {wl:.2e}")
    # Prop 2.2 radius-class identity: |z_i-p|=|z_j-p| => (|q-z_i|=|q-z_j| <=> (q-p).(z_i-z_j)=0)
    werr = 0.0
    for trial in range(200):
        pp, qq, zi = rng.normal(size=d), rng.normal(size=d), rng.normal(size=d)
        r = np.linalg.norm(zi-pp); zj = rng.normal(size=d); zj = pp + r*(zj/np.linalg.norm(zj))
        lhs = np.sum((qq-zi)**2) - np.sum((qq-zj)**2); rhs = -2*(qq-pp) @ (zi-zj)
        werr = max(werr, abs(lhs-rhs))
    print(f"  Prop 2.2 identity |q-z_i|^2-|q-z_j|^2 = -2(q-p).(z_i-z_j) on a radius class: max err {werr:.2e}")
