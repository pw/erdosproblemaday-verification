# Checks for paper section 6.2, (6.10) and the U/V comparison, with genuine random nested grids.
# (a) exact p-adic check of (6.10) over Q (Minkowski-type factorisation Z1=u+b, Z2=u-b; the identity is algebraic)
# (b) complex place where Z1, Z2 are NOT conjugate (generic embedding): Z2 on the fiber defined by
#     (Z1(z)-Z1(x))(Z2(z)-Z2(x)) = t_e ; check (6.10) with complex moduli,
#     then build the paper's random grids (random orientation, xi ~ U[0,log2), side e^xi 2^m, nested shifts)
#     and check  U(z)-V(z) = D_{j'}(y,z) - D_j(y,z) + D_j(x,z)  [Delta's], (6.8)/(6.9) via u-integrals, and
#     |D_j^mu(x,y) - D_{j'}^mu(oo,y)| <= Lip(w) * sum_z mu(z)(|Delta_{j'}(y,z)|+|Delta_j(y,z)|+|Delta_j(x,z)|).
import random, math, cmath
from fractions import Fraction
INF = float('inf')

# ---------- (a) p-adic, exact ----------
def vp(q, p):
    q = Fraction(q); assert q != 0
    a, b, v = q.numerator, q.denominator, 0
    while a % p == 0: a //= p; v += 1
    while b % p == 0: b //= p; v -= 1
    return v
rng = random.Random(1604)
bad_a = 0; tot_a = 0
for trial in range(200):
    p = rng.choice([2, 3, 5, 7])
    x1, x2 = Fraction(rng.randint(-50, 50), rng.randint(1, 30)), Fraction(rng.randint(-50, 50), rng.randint(1, 30))
    t = Fraction(rng.choice([1, -1])*rng.randint(1, 500), rng.randint(1, 50))
    fib = []
    while len(fib) < 6:
        a = Fraction(rng.choice([1, -1])*rng.randint(1, 300), rng.randint(1, 40))
        z = (x1 + a, x2 + t/a)
        if all(z[0] != w[0] for w in fib): fib.append(z)
    X = (x1, x2)
    i = lambda j, A, B: vp(A[j]-B[j], p)        # -log|.|_p = v_p * log p ; work in units of log p
    h = vp(t, p)
    for y in fib:
        for z in fib:
            if z == y: continue
            for j in (0, 1):
                jp = 1-j
                tot_a += 1
                if i(jp, y, z) != i(j, y, z) - i(j, X, z) + h - i(j, X, y): bad_a += 1
# control: move one point off the fiber -> identity must fail somewhere
ctrl_a = 0
for trial in range(50):
    p = 2; X = (Fraction(0), Fraction(0)); t = Fraction(12)
    y = (Fraction(3), Fraction(4)); z = (Fraction(4), Fraction(3) + Fraction(1, 2**rng.randint(1, 6)))  # z off fiber
    if vp(z[1]-y[1], p) != vp(z[0]-y[0], p) - vp(z[0]-X[0], p) + vp(t, p) - vp(y[0]-X[0], p): ctrl_a += 1
print('(a) p-adic exact (6.10): %d checks, %d failures | CONTROL (z off fiber): %d/50 failures (must be > 0)' % (tot_a, bad_a, ctrl_a))

# ---------- (b) complex place with random nested grids ----------
def make_grid(rng, mlo, mhi):
    th = rng.random()*2*math.pi; xi = rng.random()*math.log(2)
    l = {m: math.exp(xi)*2.0**m for m in range(mlo, mhi+1)}
    s0 = [rng.random()*l[0], rng.random()*l[0]]
    sh = {0: s0}
    for m in range(0, mhi):
        sh[m+1] = [(sh[m][a] + (l[m] if rng.random() < 0.5 else 0.0)) % l[m+1] for a in (0, 1)]
    for m in range(mlo, 0): sh[m] = [s0[a] % l[m] for a in (0, 1)]
    return th, l, sh
def cell(g, zc, m):
    th, l, sh = g
    r = zc*cmath.exp(-1j*th)
    return (math.floor((r.real - sh[m][0])/l[m]), math.floor((r.imag - sh[m][1])/l[m]))
def depth(g, za, zb, mlo, mhi):
    prev = False
    for m in range(mlo, mhi+1):
        same = cell(g, za, m) == cell(g, zb, m)
        assert not (prev and not same), 'grids not nested'
        if same and not prev: first = m
        prev = prev or same
    assert prev, 'never share'
    return -math.log(g[1][first])

def make_w(delta):
    def w(t):
        t = min(t, 1-t)
        if t <= delta/2: return 0.0
        if t >= delta: return 1.0
        return (t-delta/2)/(delta/2)
    return w
delta = 0.3; w = make_w(delta); Lip = 2/delta

def tail_integral(f, nu, n):
    fin = sorted({v for v in f if math.isfinite(v)})
    def g(u): return w(sum(nu[z] for z in range(n) if f[z] >= u))
    lo, hi = fin[0]-1, fin[-1]+1
    assert g(lo) == 0 and g(hi) == 0
    pts = [lo]+fin+[hi]
    return sum((pts[k+1]-pts[k])*g(0.5*(pts[k]+pts[k+1])) for k in range(len(pts)-1))

def D_cells(dm, n, nu, a0, a1):
    vals = sorted({dm[i][j] for i in range(n) for j in range(n) if i != j})
    tot = 0.0
    for k in range(len(vals)-1):
        r = vals[k+1]
        def cellof(a): return frozenset(z for z in range(n) if z == a or dm[a][z] >= r)
        cells = {cellof(a) for a in range(n)}
        for B in cells:
            inA0 = 0 if a0 is None else int(a0 in B)
            tot += (vals[k+1]-vals[k])*abs(inA0 - int(a1 in B))*w(sum(nu[z] for z in B))
    return tot

stats = dict(fib610=0, fib610_bad=0, UV=0, UV_bad=0, eq68=0, eq68_bad=0, eq69=0, eq69_bad=0, bound=0, bound_bad=0)
maxratio = 0.0
for trial in range(40):
    k = 10; nextra = 3; n = 1 + k + nextra
    Z1x, Z2x = complex(rng.gauss(0, 1), rng.gauss(0, 1)), complex(rng.gauss(0, 1), rng.gauss(0, 1))
    t = complex(rng.gauss(0, 1), rng.gauss(0, 1))*rng.choice([0.1, 1, 10])
    Z1 = [Z1x]; Z2 = [Z2x]
    for _ in range(k):
        a = cmath.rect(math.exp(rng.gauss(0, 1.5)), rng.random()*2*math.pi)
        Z1.append(Z1x + a); Z2.append(Z2x + t/a)
    for _ in range(nextra):
        Z1.append(complex(rng.gauss(0, 2), rng.gauss(0, 2))); Z2.append(complex(rng.gauss(0, 2), rng.gauss(0, 2)))
    x = 0; F = list(range(1, k+1)); mu = [1.0/k if z in F else 0.0 for z in range(n)]
    Z = [Z1, Z2]
    i_ = lambda j, a, b: -math.log(abs(Z[j][a]-Z[j][b]))
    he = -math.log(abs(t))
    for y in F:
        for z in F:
            if z == y: continue
            for j in (0, 1):
                stats['fib610'] += 1
                if abs(i_(1-j, y, z) - (i_(j, y, z) - i_(j, x, z) + he - i_(j, x, y))) > 1e-9: stats['fib610_bad'] += 1
    # grids: one family per coordinate
    seps = [abs(Z[j][a]-Z[j][b]) for j in (0, 1) for a in range(n) for b in range(n) if a != b]
    mlo = math.floor(math.log2(min(seps)/math.sqrt(2))) - 2
    mhi = math.ceil(math.log2(max(seps))) + 30
    G = [make_grid(rng, mlo, mhi) for _ in (0, 1)]
    dm = [[[INF if a == b else depth(G[j], Z[j][a], Z[j][b], mlo, mhi) for b in range(n)] for a in range(n)] for j in (0, 1)]
    Dl = lambda j, a, b: dm[j][a][b] - i_(j, a, b)
    for j in (0, 1):
        jp = 1-j
        for y in F:
            U = [dm[jp][y][z] for z in range(n)]
            V = [dm[j][y][z] - dm[j][x][z] + he - i_(j, x, y) for z in range(n)]
            errsum = 0.0
            for z in F:
                if z == y:
                    assert U[z] == INF and V[z] == INF
                    continue
                stats['UV'] += 1
                pred = Dl(jp, y, z) - Dl(j, y, z) + Dl(j, x, z)
                if abs((U[z]-V[z]) - pred) > 1e-9: stats['UV_bad'] += 1
                errsum += mu[z]*(abs(Dl(jp, y, z)) + abs(Dl(j, y, z)) + abs(Dl(j, x, z)))
            Djxy = D_cells(dm[j], n, mu, x, y); Djp_root = D_cells(dm[jp], n, mu, None, y)
            # (6.8) with translation: int w(mu{V>=u}) du == D_j^mu(x,y); (6.9): int w(mu{U>=u}) du == D_j'^mu(oo,y)
            stats['eq68'] += 1; stats['eq69'] += 1
            if abs(tail_integral(V, mu, n) - Djxy) > 1e-8: stats['eq68_bad'] += 1
            if abs(tail_integral(U, mu, n) - Djp_root) > 1e-8: stats['eq69_bad'] += 1
            stats['bound'] += 1
            lhs = abs(Djxy - Djp_root)
            if lhs > Lip*errsum + 1e-9: stats['bound_bad'] += 1
            if errsum > 0: maxratio = max(maxratio, lhs/(Lip*errsum))
print('(b) complex place + random grids:', stats)
print('    max |D_j^mu(x,y)-D_jprime^mu(oo,y)| / (Lip(w) * Delta-error) = %.3f (must be <= 1)' % maxratio)

# CONTROL (b): perturb one fiber point's Z2 off the fiber -> the U-V identity must fail for that point
fails = 0
for trial in range(20):
    k = 6; n = 1 + k
    Z1x, Z2x = complex(rng.gauss(0, 1), rng.gauss(0, 1)), complex(rng.gauss(0, 1), rng.gauss(0, 1)); t = complex(1, 0.5)
    Z1 = [Z1x]; Z2 = [Z2x]
    for _ in range(k):
        a = cmath.rect(math.exp(rng.gauss(0, 1)), rng.random()*2*math.pi); Z1.append(Z1x + a); Z2.append(Z2x + t/a)
    Z2[3] += 0.3*cmath.exp(1j*rng.random()*6.28)     # point 3 leaves the fiber
    Z = [Z1, Z2]; i_ = lambda j, a, b: -math.log(abs(Z[j][a]-Z[j][b])); he = -math.log(abs(t))
    y, z, x, j = 1, 3, 0, 0
    if abs(i_(1, y, z) - (i_(0, y, z) - i_(0, x, z) + he - i_(0, x, y))) > 1e-6: fails += 1
print('CONTROL (b) (one point off the fiber): (6.10) failures = %d / 20 (must be > 0)' % fails)
