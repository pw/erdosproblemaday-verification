# (h) Hilbert-function toys for Lemma 3.6 (3.7): H_V(L) >= c_n * a * L^k for V = components (dim k, total degree a)
# of a locus cut out by equations of degree <= L, tested at the DEFINING degree L = D.
# H is computed as the rank of evaluation of all degree-D monomials on enough points of Y (exact integers, rank mod p
# for two large primes), cross-checked against closed forms / sympy Groebner bases.
import itertools, random, math
from math import comb
from sympy import symbols, groebner, Poly, binomial
random.seed(166)
PR = [1000000007, 998244353]
def rank_mod(rows, p):
    rows = [[x % p for x in r] for r in rows]; rk = 0; ncol = len(rows[0]) if rows else 0
    for c in range(ncol):
        piv = next((i for i in range(rk, len(rows)) if rows[i][c]), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        inv = pow(rows[rk][c], p-2, p)
        rows[rk] = [x*inv % p for x in rows[rk]]
        for i in range(len(rows)):
            if i != rk and rows[i][c]:
                f = rows[i][c]; rows[i] = [(a - f*b) % p for a, b in zip(rows[i], rows[rk])]
        rk += 1
    return rk
def monos(nvars, D):
    return [e for e in itertools.product(range(D+1), repeat=nvars) if sum(e) == D]
def H_points(pts, D, p=None):
    ms = monos(len(pts[0]), D)
    rows = [[math.prod(pow(pt[i], e[i], p) if p else pt[i]**e[i] for i in range(len(pt))) for e in ms] for pt in pts]
    r = [rank_mod(rows, q) for q in PR]
    return max(r)
print("== Y = D' concurrent lines in P^2 through [0:0:1]; H_Y(D) at degree D; compare c*deg*D^dim = c*D'*D ==")
for D in range(1, 7):
    for Dp in sorted(set((1, max(1, D//2), D, D+1, 2*D+2, 3*D+3))):
        # lines {b_i x - a_i y = 0}; sample D+1 points on each line (degree-D form vanishing at D+1 points of a line kills it)
        lines = [(1, i) for i in range(1, Dp+1)]
        # D+1 DISTINCT points [a:b:z], z=0..D, on the line through [0:0:1] and [a:b:0]
        pts = [(a, b, z) for (a, b) in lines for z in range(D+1)]
        H = H_points(pts, D)
        closed = comb(D+2, 2) - (comb(D-Dp+2, 2) if Dp <= D else 0)
        envP2 = (H == comb(D+2, 2))
        print(f"  D={D} D'={Dp:2d}: H_Y(D)={H:3d} (closed form {closed:3d}) ; H/(D'*D) = {H/(Dp*D):.3f}; Env_D(Y) = P^2 (lines NOT components): {envP2}")
print("== Y = complete intersection of two random degree-D surfaces in P^3 (curve, degree D^2); H_Y(D) vs c*D^2*D ==")
X, Yv, Z, W = symbols('x y z w')
for D in range(1, 5):
    # Groebner: Hilbert function of S/(f,g) in degree D  (= C(D+3,3)-2 for a complete intersection)
    def rp():
        return sum(random.randint(-5, 5)*X**e[0]*Yv**e[1]*Z**e[2]*W**e[3] for e in monos(4, D))
    f, g = rp(), rp()
    G = groebner([f, g], X, Yv, Z, W, order='grevlex')
    lead = [Poly(gg, X, Yv, Z, W).monoms(order='grevlex')[0] for gg in G.exprs]
    std = [m for m in monos(4, D) if not any(all(m[i] >= l[i] for i in range(4)) for l in lead)]
    Hs = len(std)
    # independent check: F_p points on the affine curve w=1 over a small prime, rank of degree-D evaluation
    p = 211
    import numpy as np
    def ev(poly, pts):
        P = Poly(poly, X, Yv, Z, W)
        return [sum(c*pow(a, e[0], p)*pow(b, e[1], p)*pow(cc, e[2], p) for e, c in zip(P.monoms(), P.coeffs())) % p for (a, b, cc) in pts]
    Pf = Poly(f, X, Yv, Z, W); Pg = Poly(g, X, Yv, Z, W)
    fz = [(e, int(c)) for e, c in zip(Pf.monoms(), Pf.coeffs())]; gz = [(e, int(c)) for e, c in zip(Pg.monoms(), Pg.coeffs())]
    arr = np.arange(p, dtype=np.int64)
    pts = []
    for a in range(p):
        # evaluate f,g on all (a,b,c) at once
        B, C = np.meshgrid(arr, arr, indexing='ij')
        fv = np.zeros_like(B); gv = np.zeros_like(B)
        for e, c in fz: fv = (fv + c*pow(a, e[0], p)*np.mod(B**e[1], p)*np.mod(C**e[2], p)) % p
        for e, c in gz: gv = (gv + c*pow(a, e[0], p)*np.mod(B**e[1], p)*np.mod(C**e[2], p)) % p
        idx = np.argwhere((fv == 0) & (gv == 0))
        pts += [(a, int(b), int(c)) for b, c in idx]
        if len(pts) > 4*D**3 + 60: break
    ms = monos(4, D)
    rows = [[pow(a, e[0], p)*pow(b, e[1], p)*pow(c, e[2], p) % p for e in ms] for (a, b, c) in pts]
    Hpts = rank_mod(rows, p)
    print(f"  D={D}: Groebner H_(S/(f,g))(D) = {Hs} (closed form C(D+3,3)-2 = {comb(D+3,3)-2}); F_{p} curve points used: {len(pts)} (> D^3={D**3}), evaluation rank = {Hpts};  H/(D^2*D) = {Hs/D**3:.3f}  (limit 1/6 = 0.1667)")
print("== Y = a points in P^2: general position vs collinear; H_Y(D) vs c*a ==")
for D in (2, 3, 4):
    for a in (2, D, D+1, comb(D+2, 2)-2, comb(D+2, 2), 2*comb(D+2, 2)):
        gen = [(random.randint(-10**6, 10**6), random.randint(-10**6, 10**6), 1) for _ in range(a)]
        col = [(i, 2*i+3, 1) for i in range(1, a+1)]
        Hg, Hc = H_points(gen, D), H_points(col, D)
        print(f"  D={D} a={a:3d}: general position H={Hg:3d} (min(a,C(D+2,2))={min(a, comb(D+2,2))}), H/a={Hg/a:.3f} | collinear H={Hc:3d} (min(a,D+1)={min(a, D+1)}), H/a={Hc/a:.3f}")
print("== the extremal 0-dimensional case: Y = complete intersection of two degree-D curves in P^2 (D^2 points = all isolated) ==")
for D in range(1, 7):
    # product-of-lines CI: {prod (x - i z) = 0, prod (y - j z) = 0} -> D^2 grid points, ideal = CI
    pts = [(i, j, 1) for i in range(D) for j in range(D)]
    H = H_points(pts, D)
    print(f"  D={D}: a=D^2={D*D}, H_Y(D)={H} (C(D+2,2)-2={comb(D+2,2)-2}), H/a = {H/(D*D):.3f}  (-> 1/2)")
