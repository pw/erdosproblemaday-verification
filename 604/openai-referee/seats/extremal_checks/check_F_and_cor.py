# Exact pair-ratio R_P(s) = #{(x,y): x!=y, k_P(x,y) >= n^s} / (n(n-1)) for explicit configurations,
# the exact value of F_4, and the Corollary 1.2 per-pin counting inequality, each with a control that must FAIL.
# Exactness: integer / Eisenstein-integer coordinates => integer squared distances; regular polygon via
# chord index (exact combinatorics) cross-checked against 60-digit numerics.
import itertools, math, random
from fractions import Fraction as Fr
import mpmath
mpmath.mp.dps = 60

def classes_sq(P, d2):
    """For each pin x: dict squared-distance -> list of targets. d2 exact (ints)."""
    out = {}
    for x in P:
        c = {}
        for y in P:
            if y != x:
                c.setdefault(d2(x, y), []).append(y)
        out[x] = c
    return out

def kfun(P, d2):
    cl = classes_sq(P, d2)
    return {(x, y): len(cl[x][d2(x, y)]) for x in P for y in P if x != y}, cl

def ratio_threshold(P, d2, T):
    """#{(x,y): x!=y, k >= T} / (n(n-1)) with integer threshold T (k is an integer)."""
    k, _ = kfun(P, d2); n = len(P)
    return Fr(sum(1 for v in k.values() if v >= T), n*(n-1))

sq = lambda a, b: (a[0]-b[0])**2 + (a[1]-b[1])**2
eis = lambda a, b: (a[0]-b[0])**2 - (a[0]-b[0])*(a[1]-b[1]) + (a[1]-b[1])**2   # |(a-b) in Z[w]|^2

fails = []
def expect(name, got, want):
    ok = (got == want)
    show = (lambda v: f"multiset of {len(v)} values, histogram {dict(sorted(__import__('collections').Counter(v).items()))}") if isinstance(got, list) else (lambda v: v)
    print(f"{'PASS' if ok else 'FAIL'} {name}: got {show(got)} want {show(want)}")
    if not ok: fails.append(name)
    return ok

# ---- 1. 3x3 grid, hand-computed values (see report) ----
G = [(i, j) for i in range(3) for j in range(3)]
for T, want in [(1, Fr(1)), (2, Fr(60, 72)), (3, Fr(20, 72)), (4, Fr(8, 72)), (5, Fr(0))]:
    expect(f"3x3 grid ratio k>={T}", ratio_threshold(G, sq, T), want)
_, cl = kfun(G, sq)
expect("3x3 grid distinct distances corner/edge/centre",
       (len(cl[(0, 0)]), len(cl[(1, 0)]), len(cl[(1, 1)])), (5, 4, 2))

# ---- 2. regular N-gon + centre: exact chord-index model vs 60-digit numerics ----
def polygon_centre_exact(N):
    """Points 0..N-1 vertices, 'c' centre; squared distance labels exact: chord min(k,N-k), radius 'R'.
       chord j has squared length 2-2cos(2*pi*j/N) = 1 iff j/N = 1/6."""
    pts = list(range(N)) + ['c']
    def lab(a, b):
        if a == 'c' or b == 'c':
            return 'R'
        j = (a-b) % N; j = min(j, N-j)
        return 'R' if 6*j == N else ('ch', j)
    return pts, lab

def polygon_centre_numeric(N):
    pts = [(mpmath.cos(2*mpmath.pi*i/N), mpmath.sin(2*mpmath.pi*i/N)) for i in range(N)] + [(mpmath.mpf(0), mpmath.mpf(0))]
    idx = list(range(N+1))
    def lab(a, b):
        v = (pts[a][0]-pts[b][0])**2 + (pts[a][1]-pts[b][1])**2
        return mpmath.nstr(v, 40)          # equal algebraic numbers agree to 40 digits; unequal ones differ far above 1e-40 here
    return idx, lab

for N in [5, 6, 7, 8, 12, 13, 18]:
    Pe, le = polygon_centre_exact(N); Pn, ln = polygon_centre_numeric(N)
    ke, _ = kfun(Pe, le); kn, _ = kfun(Pn, ln)
    se = sorted(ke[(x, y)] for (x, y) in ke); sn = sorted(kn.values())
    expect(f"N={N} polygon+centre k-multiset exact==numeric", se, sn)
    n = N + 1
    # hand prediction of the pair count with k>=2: centre->vertices N pairs (k=N>=2);
    # vertex pins: all N-1 other vertices are in classes of size>=2 except the diameter (N even, size 1);
    # the centre is in a class of size 1 unless 6|N (then it joins chord N/6, size 3).
    rich_vertex = (N-1) - (1 if N % 2 == 0 else 0) + (1 if N % 6 == 0 else 0)
    want = Fr(N + N*rich_vertex, n*(n-1))
    expect(f"N={N} polygon+centre ratio k>=2 (hand formula)", ratio_threshold(Pe, le, 2), want)
    _, cle = kfun(Pe, le)
    expect(f"N={N} centre has exactly one distance", len(cle['c']), 1)

# ---- 3. exact F_4 : 5/6 at threshold 2, 1/2 at threshold 3 (proof in report); lattice searches ----
def best4(patch, d2, T):
    best = 0; arg = None
    for Q in itertools.combinations(patch, 4):
        k, _ = kfun(list(Q), d2)
        c = sum(1 for v in k.values() if v >= T)
        if c > best: best, arg = c, Q
    return best, arg
tri = [(a, b) for a in range(-2, 3) for b in range(-2, 3)]          # Eisenstein patch, 25 points
sqp = [(a, b) for a in range(0, 5) for b in range(0, 5)]            # square patch, 25 points
bt2, at2 = best4(tri, eis, 2); bt3, _ = best4(tri, eis, 3)
expect("F_4 threshold 2: Eisenstein-patch max pair count (= 10 = 5/6*12, rhombus)", bt2, 10)
expect("F_4 threshold 3: Eisenstein-patch max pair count (= 6 = 1/2*12)", bt3, 6)
print("   maximiser at threshold 2:", at2)
bs2, as2 = best4(sqp, sq, 2)
print(f"   square-lattice patch max at threshold 2: {bs2} (no equilateral triangles, so must be < 10)")
if not bs2 < 10: fails.append("square patch should not reach 10")

# ---- 4. Corollary 1.2 counting, per pin and in total, paper form and Lean form ----
def cor_check(P, d2, eps, variant="paper"):
    n = len(P); k, cl = kfun(P, d2)
    s = eps/2
    bad = [x for x in P if len(cl[x]) < n**(1-eps)]
    rich = {x: sum(1 for y in P if y != x and k[(x, y)] >= n**s) for x in P}
    ok = True
    for x in bad:
        light = (n-1) - rich[x]
        bound = n**(1-eps+s) if variant == "paper" else n**(1-eps)   # control drops the class-size factor n^s
        if not light < bound and not (light == 0):
            ok = False
    pairs = sum(rich.values())
    b = len(bad)
    if variant == "paper":
        # b*(n-1-n^{1-eps/2}) <= pairs  (paper),   b/n <= pairs/(n(n-1)) + n^{1-eps/2}/(n-1)  (Lean, before the factor 2)
        if b*(n-1-n**(1-eps/2)) > pairs + 1e-9: ok = False
        if b/n > pairs/(n*(n-1)) + n**(1-eps/2)/(n-1) + 1e-12: ok = False
    return ok, b
random.seed(604)
configs = [("3x3 grid", G, sq), ("6x6 grid", [(i, j) for i in range(6) for j in range(6)], sq),
           ("Eisenstein hexagon r=3", [(a, b) for a in range(-3, 4) for b in range(-3, 4) if abs(a-b) <= 3], eis)]
for N in [12, 30, 60]:
    Pe, le = polygon_centre_exact(N); configs.append((f"{N}-gon+centre", Pe, le))
# concentric squares-of-circles style: integer points on circles x^2+y^2=r^2 (r=5,25,65) plus origin
circ = {(0, 0)}
for r2 in [25, 625, 4225]:
    r = int(math.isqrt(r2))
    for x in range(-r, r+1):
        y2 = r2 - x*x; y = math.isqrt(y2)
        if y*y == y2: circ |= {(x, y), (x, -y)}
configs.append(("origin + lattice points on 3 circles", sorted(circ), sq))
# generic concentric circles about a centre: 10 circles x 2 points + 5 circles x 16 points, n = 101.
# Radii and angles are random (60-digit), so all non-centre distances are distinct; the centre is a bad pin
# for eps=0.4 (15 classes < 101^0.6 = 15.9) with 20 neighbours in light classes (size 2 < 101^0.2 = 2.52).
rnd = random.Random(1957)
cc = [(mpmath.mpf(0), mpmath.mpf(0))]
for size in [2]*10 + [16]*5:
    r = mpmath.mpf(1) + rnd.random()*10
    for _ in range(size):
        a = 2*mpmath.pi*rnd.random(); cc.append((r*mpmath.cos(a), r*mpmath.sin(a)))
ccidx = list(range(len(cc)))
ccd = lambda a, b: mpmath.nstr((cc[a][0]-cc[b][0])**2 + (cc[a][1]-cc[b][1])**2, 40)
configs.append(("centre + 10x2 + 5x16 generic concentric circles", ccidx, ccd))
for t in range(6):
    configs.append((f"random 30 pts of 7x7 grid #{t}", random.sample([(i, j) for i in range(7) for j in range(7)], 30), sq))
n_viol_paper = 0; n_viol_control = 0
for name, P, d2 in configs:
    for eps in [0.2, 0.4, 0.6, 0.8, 0.95]:
        okp, b = cor_check(P, d2, eps, "paper"); okc, _ = cor_check(P, d2, eps, "control")
        n_viol_paper += (not okp); n_viol_control += (not okc)
print(f"Corollary counting: {len(configs)*5} (config,eps) cases; paper-form violations = {n_viol_paper}; "
      f"CONTROL (light < n^(1-eps), class-size factor dropped) violations = {n_viol_control}")
if n_viol_paper: fails.append("corollary paper form violated")
if n_viol_control == 0: fails.append("control failed to fail")

# ---- 5. controls on the exact ratio checker itself ----
print("CONTROLS (must FAIL):")
c1 = ratio_threshold(G, sq, 2) == Fr(61, 72)                       # wrong claimed value
G2 = [p if p != (2, 2) else (3, 3) for p in G]                     # perturbed grid: moving a corner must change the count
c2 = ratio_threshold(G2, sq, 3) == Fr(20, 72)
def kfun_wrong(P, d2):   # forgets that k counts y itself (counts z != x,y)
    k, cl = kfun(P, d2); return {key: v-1 for key, v in k.items()}
c3 = sum(1 for v in kfun_wrong(G, sq).values() if v >= 2) == 60
for nm, c in [("claimed 61/72 for 3x3 grid at k>=2", c1), ("perturbed grid keeps 20/72 at k>=3", c2), ("k without y itself reproduces 60", c3)]:
    print(f"  control '{nm}': {'ACCEPTED (BAD)' if c else 'rejected (good)'}")
    if c: fails.append("control " + nm)
print("OVERALL:", "ALL CHECKS PASS, ALL CONTROLS FAIL" if not fails else f"PROBLEMS: {fails}")
