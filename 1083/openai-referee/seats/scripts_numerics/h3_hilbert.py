# (h) Hilbert-function toys for Lemma 3.6 (pp. 18-19):  H_V(L) >= c_n a L^k  at the DEFINING degree L, for V a union
# of k-dimensional irreducible components (total degree a) of a locus cut out by equations of degree <= L.
# Constant under test (algebra seat): c_{n,k} = 1/((n-k+1)^n k!).  Also (3.5) H_V(D) <= a C(D+k,k) and the shift
# (3.6) H_V(D) >= a C(D-q+k,k) for D >= q with q <= (n-k)(L-1).
# H is computed as an exact rank (mod two large primes) of evaluation of all degree-D forms on explicit points,
# and cross-checked with closed forms / sympy Groebner standard-monomial counts.
import itertools, math, random
from math import comb
from sympy import symbols, groebner, Poly
random.seed(166)
PR = (1000000007, 998244353)
def rank_mod(rows, p):
    rows = [[x % p for x in r] for r in rows]; rk = 0
    for c in range(len(rows[0]) if rows else 0):
        piv = next((i for i in range(rk, len(rows)) if rows[i][c]), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]; inv = pow(rows[rk][c], p-2, p)
        rows[rk] = [x*inv % p for x in rows[rk]]
        for i in range(len(rows)):
            if i != rk and rows[i][c]:
                f = rows[i][c]; rows[i] = [(a - f*b) % p for a, b in zip(rows[i], rows[rk])]
        rk += 1
    return rk
def monos(nv, D): return [e for e in itertools.product(range(D+1), repeat=nv) if sum(e) == D]
def H(pts, D):   # homogeneous degree-D restriction rank on projective points given by integer reps
    ms = monos(len(pts[0]), D)
    rows = [[math.prod(pt[i]**e[i] for i in range(len(pt))) for e in ms] for pt in pts]
    return max(rank_mod(rows, p) for p in PR)
def c_nk(n, k): return 1/((n-k+1)**n * math.factorial(k))
out = []
def row(name, n, k, a, L, h, hyp):
    ratio = h/(a*L**k); c = c_nk(n, k); up = a*comb(L+k, k)
    ok = (ratio >= c) if hyp else None
    out.append((name, n, k, a, L, h, ratio, c, ok, h <= up))
    print(f"  {name:46s} n={n} k={k} a={a:4d} L={L:2d}: H={h:5d}  H/(aL^k)={ratio:6.3f}  c_nk={c:.4f}  hyp(components of degree-L locus)={hyp}  lower-ok={ok}  (3.5) H<=aC(L+k,k)={h<=up}")

print("== T1: D' concurrent lines through [0:0:1] in P^2 (n=2,k=1), tested at degree D ==")
for D in range(1, 7):
    for Dp in sorted(set((1, max(1, D//2), D, D+1, 2*D+2, 4*D+4))):
        pts = [(1, i, z) for i in range(1, Dp+1) for z in range(D+1)]       # D+1 points on each line {y = i x}
        h = H(pts, D) if Dp*(D+1) <= 300 else None
        closed = comb(D+2, 2) - (comb(D-Dp+2, 2) if Dp <= D else 0)
        if h is not None: assert h == closed, (D, Dp, h, closed)
        # lines are components of Env_D(Y) iff Dp <= D (for Dp > D every degree-D form vanishing on them is 0)
        row(f"{Dp} concurrent lines @deg D={D}", 2, 1, Dp, D, closed, Dp <= D)
print("  same lines at their defining degree L = D' (one equation: product of D' linear forms):")
for Dp in (2, 4, 8, 12, 20):
    row(f"{Dp} concurrent lines @deg L=D'={Dp}", 2, 1, Dp, Dp, comb(Dp+2, 2) - 1, True)
print("  failure threshold when the hypothesis is dropped: H(D) = C(D+2,2) < c*D'*D  iff  D' > C(D+2,2)/(c D); c=1/4, D=3: D' >", comb(5,2)/(0.25*3))

print("== T2: complete intersection of two degree-D surfaces in P^3 (curve, degree D^2), at L = D ==")
X, Y, Z, W = symbols('x y z w')
for D in range(1, 6):
    # (a) product CI: {prod_i (x - i w) = 0, prod_j (y - j w) = 0} = D^2 lines {x=i, y=j}; D+1 points per line
    pts = [(i, j, z, 1) for i in range(D) for j in range(D) for z in range(D+1)]
    h = H(pts, D) if D <= 4 else comb(D+3, 3) - 2
    assert D > 4 or h == comb(D+3, 3) - 2
    row(f"product CI (D^2 lines), D={D}", 3, 1, D*D, D, h, True)
for D in range(1, 5):
    rp = lambda: sum(random.randint(-5, 5)*X**e[0]*Y**e[1]*Z**e[2]*W**e[3] for e in monos(4, D))
    G = groebner([rp(), rp()], X, Y, Z, W, order='grevlex')
    lead = [Poly(g, X, Y, Z, W).monoms(order='grevlex')[0] for g in G.exprs]
    std = lambda m: sum(1 for e in monos(4, m) if not any(all(e[i] >= l[i] for i in range(4)) for l in lead))
    h = std(D)
    row(f"random CI (smooth, reduced: I(Y)=(f,g)), D={D}", 3, 1, D*D, D, h, True)
    # shift (3.6): smallest q with H(m) >= a (m - q + 1) for all m in [q, 4D+4]
    Hm = {m: std(m) for m in range(0, 4*D+5)}
    q = next(q for q in range(0, 4*D+5) if all(Hm[m] >= D*D*(m-q+1) for m in range(q, 4*D+5)))
    print(f"      (3.6) shift: minimal q = {q}  vs (n-k)(L-1) = {2*(D-1)}: {q <= 2*(D-1)}")

print("== T3: a points in P^2 (n=2,k=0): general position vs collinear, at degree D ==")
for D in (2, 3, 4):
    for a in sorted(set((2, D, D+1, D+2, comb(D+2, 2)-2, comb(D+2, 2), 2*comb(D+2, 2)))):
        gen = [(random.randint(-10**6, 10**6), random.randint(-10**6, 10**6), 1) for _ in range(a)]
        col = [(i, 2*i+3, 1) for i in range(1, a+1)]
        hg, hc = H(gen, D), H(col, D)
        # components of Env_D: general points iff the degree-D system through them has only them as base locus;
        # sufficient: a <= C(D+2,2)-2 (at least a pencil, 0-dim base locus); collinear points iff a <= D (a degree-D form
        # vanishing at D+1 points of a line vanishes on the line, so for a >= D+1 the line lies in Env_D)
        row(f"{a} general points @D={D}", 2, 0, a, D, hg, a <= comb(D+2, 2) - 2)
        row(f"{a} collinear points @D={D}", 2, 0, a, D, hc, a <= D)
print("  collinear points at their defining degree L = a (line + one degree-a form): H(a) = a, ratio 1")

print("== T4: 0-dimensional complete intersections (all D^n points are components), at L = D ==")
for D in range(1, 7):
    pts2 = [(i, j, 1) for i in range(D) for j in range(D)]
    h2 = H(pts2, D)
    row(f"CI of two degree-{D} curves in P^2 (grid)", 2, 0, D*D, D, h2, True)
    m = next(m for m in range(0, 4*D) if H(pts2, m) == D*D)
    print(f"      (3.6) shift: H(m) = a first at m = {m}  vs (n-k)(L-1) = {2*(D-1)}: q = {m} <= {2*(D-1)}: {m <= 2*(D-1)}")
for D in range(1, 5):
    pts3 = [(i, j, l, 1) for i in range(D) for j in range(D) for l in range(D)]
    h3 = H(pts3, D)
    row(f"CI of three degree-{D} surfaces in P^3 (grid)", 3, 0, D**3, D, h3, True)

print("== T5: isolated points of {l f = l g = 0} (extra 1-dim component l), f=prod(x-i), g=prod(y-j), deg L-1, at L ==")
for L in range(2, 8):
    k_ = L - 1; iso = [(i, j, 1) for i in range(k_) for j in range(k_)]
    row(f"isolated grid of {k_*k_} pts (+ a line), L={L}", 2, 0, k_*k_, L, H(iso, L), True)

print("== summary ==")
hyp = [r for r in out if r[8] is not None]
print(f"  toys satisfying the hypothesis: {len(hyp)}; lower bound H >= c_nk a L^k violated in: {sum(1 for r in hyp if not r[8])}")
print(f"  min over hypothesis-satisfying toys of (H/(aL^k))/c_nk = {min(r[6]/r[7] for r in hyp):.3f}")
nohyp = [r for r in out if r[8] is None]
print(f"  toys violating the hypothesis: {len(nohyp)}; of these, H < c_nk a L^k in {sum(1 for r in nohyp if r[6] < r[7])}  (hypothesis is needed)")
print(f"  upper bound (3.5) violated in: {sum(1 for r in out if not r[9])} of {len(out)}")
