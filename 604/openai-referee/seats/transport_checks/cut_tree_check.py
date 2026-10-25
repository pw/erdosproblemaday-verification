# Checks for paper section 6.2-6.3 on random hierarchies (random ultrametric "sharing depths" d):
#  (6.8)  D^nu(a0,a1) := int sum_{B in Pi(r)} |1_B(a0)-1_B(a1)| w(nu(B)) dr  ==  int w(nu{z: d(a1,z)-d(a0,z) >= u}) du
#  (6.9)  D^nu(oo,y)  := int sum_B 1_B(y) w(nu(B)) dr                       ==  int w(nu{z: d(y,z) >= u}) du
#  tree:  cells as vertices, parent = least strict supercell, edge length l(B) = |levels where B is a cell| * w(alpha(B));
#         graph path distance == D^alpha, root distance == D^alpha(oo,.), total edge length == ell
#  (6.12) optimal transport cost (LP) == sum_B l(B)|rho(B)-alpha(B)|
#  (6.14) chain: E_{alpha^3}|D(x,y)-D(x',y)| <= 2E_q|D(x,y)-g(y)| + 2E_{qY} T(rho_y,alpha) + 2T(qY,alpha)
import random, math
from scipy.optimize import linprog
import numpy as np
INF = float('inf')

def make_w(delta, symmetric=True):
    def w(t):
        if symmetric: t = min(t, 1-t)
        if t <= delta/2: return 0.0
        if t >= delta: return 1.0 if (not symmetric or t <= 1-delta) else 1.0
        return (t - delta/2)/(delta/2)
    if symmetric: return w
    # control: NOT symmetric under t -> 1-t, but still 0 on [0,delta/2] u [1-delta/2,1] (all integrals finite)
    def w2(t):
        if t <= delta/2 or t >= 1-delta/2: return 0.0
        if t <= delta: return (t - delta/2)/(delta/2)
        if t <= 0.4: return 1.0
        return (1-delta/2 - t)/(1-delta/2-0.4)
    return w2

def random_ultrametric(rng, n):
    # agglomerative: clusters merge at decreasing depths; ties produce multiway splits
    clusters = [[i] for i in range(n)]
    d = [[INF if i == j else None for j in range(n)] for i in range(n)]
    depth = 10.0
    while len(clusters) > 1:
        depth -= rng.choice([0.0, rng.random(), 2*rng.random()]) if depth < 10.0 else rng.random()
        r = rng.choice([2, 2, 2, 3]) if len(clusters) >= 3 else 2
        pick = rng.sample(range(len(clusters)), r)
        merged = []
        for p in pick:
            for a in clusters[p]:
                for b in merged: d[a][b] = d[b][a] = depth
            merged += clusters[p]
        clusters = [c for k, c in enumerate(clusters) if k not in pick] + [merged]
    return d

def levels(d, n):
    vals = sorted({d[i][j] for i in range(n) for j in range(n) if i != j})
    return vals

def partition(d, n, r):
    # classes of {d >= r}
    seen = [False]*n; parts = []
    for i in range(n):
        if seen[i]: continue
        c = [j for j in range(n) if j == i or d[i][j] >= r]
        for j in c: seen[j] = True
        parts.append(frozenset(c))
    return parts

def hierarchy(d, n):
    # list of (interval_length, partition) for finite intervals (D_k, D_{k+1}], plus partitions on rays
    vals = levels(d, n)
    segs = []
    for k in range(len(vals)-1):
        segs.append((vals[k+1]-vals[k], partition(d, n, vals[k+1])))
    return vals, segs   # ray r<=vals[0]: {P}; ray r>vals[-1]: singletons

def mass(nu, B): return sum(nu[x] for x in B)

def D_cells(d, n, nu, w, a0, a1):
    vals, segs = hierarchy(d, n)
    # rays: initial ray has only P (a0,a1 both in P => 0 unless a0 = oo); final ray: singletons
    tot = 0.0
    def ind(B, a): return 0 if a is None else (1 if a in B else 0)
    P = frozenset(range(n))
    if a0 is None:   # formal endpoint oo: initial ray contributes w(nu(P)) * infinity -> must be 0
        assert w(mass(nu, P)) == 0
    for x in range(n):
        if (a0 is not None and x == a0) or x == a1:
            assert w(nu[x]) == 0, 'singleton weight must vanish on final ray'
    for length, part in segs:
        tot += length*sum(abs(ind(B, a0)-ind(B, a1))*w(mass(nu, B)) for B in part)
    return tot

def integrate_tail(vals_at, nu, w, n):
    # int_R w(nu{z: f(z) >= u}) du, f(z) in R u {+-inf}; piecewise constant between finite values
    fin = sorted({v for v in vals_at if math.isfinite(v)})
    def g(u): return w(sum(nu[z] for z in range(n) if vals_at[z] >= u))
    lo, hi = fin[0]-1.0, fin[-1]+1.0
    assert g(lo) == 0 and g(hi) == 0, 'tails must vanish'
    pts = [lo] + fin + [hi]
    tot = 0.0
    for k in range(len(pts)-1):
        mid = 0.5*(pts[k]+pts[k+1])
        tot += (pts[k+1]-pts[k])*g(mid)
    return tot

def D_u(d, n, nu, w, a0, a1):
    if a0 is None: f = [d[a1][z] for z in range(n)]
    else:          f = [d[a1][z]-d[a0][z] for z in range(n)]   # +inf at a1, -inf at a0
    return integrate_tail(f, nu, w, n)

def tree(d, n, w, alpha):
    vals, segs = hierarchy(d, n)
    P = frozenset(range(n))
    span = {}   # cell -> total level length where it is a cell (finite segments only)
    for length, part in segs:
        for B in part: span[B] = span.get(B, 0.0) + length
    cells = set(span) | {P} | {frozenset([x]) for x in range(n)}
    l = {}
    for B in cells:
        if B == P: continue
        wt = w(mass(alpha, B))
        if len(B) == 1:
            assert wt == 0; l[B] = 0.0   # infinite final ray times zero weight
        else:
            # cell persists on finite segments; it can also be P-ray? no (B != P)
            l[B] = span.get(B, 0.0)*wt
    parent = {}
    for B in cells:
        if B == P: continue
        sup = [C for C in cells if B < C]
        parent[B] = min(sup, key=len)
    return cells, parent, l, P

def path_dist(parent, l, P, u, v):
    # graph distance between tree vertices u, v
    def anc(x):
        out = [x]
        while x != P: x = parent[x]; out.append(x)
        return out
    au, av = anc(u), anc(v)
    common = set(au) & set(av)
    du = 0.0
    for x in au:
        if x in common: lca = x; break
        du += l[x]
    dv = 0.0
    for x in av:
        if x == lca: break
        dv += l[x]
    return du + dv

def transport_lp(C, rho, alpha):
    n = len(rho)
    c = np.array(C).reshape(-1)
    A = []; b = []
    for i in range(n):
        row = np.zeros(n*n); row[i*n:(i+1)*n] = 1; A.append(row); b.append(rho[i])
    for j in range(n):
        row = np.zeros(n*n); row[j::n] = 1; A.append(row); b.append(alpha[j])
    res = linprog(c, A_eq=np.array(A), b_eq=np.array(b), bounds=(0, None), method='highs')
    assert res.status == 0
    return res.fun

def rand_prob(rng, n, support=None):
    w = [0.0]*n
    for i in (support if support is not None else range(n)): w[i] = rng.random()+0.05
    s = sum(w); return [x/s for x in w]

rng = random.Random(6082)
w = make_w(0.3)
fails = {'6.8': 0, '6.9': 0, 'tree_path': 0, 'tree_root': 0, 'tree_total': 0, '6.12': 0, '6.12_levelform': 0, 'chain': 0}
counts = dict.fromkeys(fails, 0)
for trial in range(60):
    n = rng.randrange(8, 13)
    d = random_ultrametric(rng, n)
    alpha = [1.0/n]*n
    # a fiber-like law: uniform on a subset of size k >= 7 (so 1/k <= delta/2 = 0.15)
    k = rng.randrange(7, n+1); F = rng.sample(range(n), k); mu = [1.0/k if x in F else 0.0 for x in range(n)]
    for nu in (alpha, mu):
        for _ in range(6):
            a0, a1 = rng.sample(range(n), 2)
            counts['6.8'] += 1
            if abs(D_cells(d, n, nu, w, a0, a1) - D_u(d, n, nu, w, a0, a1)) > 1e-9: fails['6.8'] += 1
            y = rng.randrange(n); counts['6.9'] += 1
            if abs(D_cells(d, n, nu, w, None, y) - D_u(d, n, nu, w, None, y)) > 1e-9: fails['6.9'] += 1
    # tree representation with alpha weights
    cells, parent, l, P = tree(d, n, w, alpha)
    vals, segs = hierarchy(d, n)
    ell = sum(length*sum(w(mass(alpha, B)) for B in part) for length, part in segs)
    counts['tree_total'] += 1
    if abs(sum(l.values()) - ell) > 1e-9: fails['tree_total'] += 1
    Dm = [[D_cells(d, n, alpha, w, a, b) if a != b else 0.0 for b in range(n)] for a in range(n)]
    for a in range(n):
        counts['tree_root'] += 1
        if abs(path_dist(parent, l, P, frozenset([a]), P) - D_cells(d, n, alpha, w, None, a)) > 1e-9: fails['tree_root'] += 1
        for b in range(n):
            counts['tree_path'] += 1
            if abs(path_dist(parent, l, P, frozenset([a]), frozenset([b])) - Dm[a][b]) > 1e-9: fails['tree_path'] += 1
    # transport formula (6.12)
    for _ in range(3):
        rho = rand_prob(rng, n, rng.sample(range(n), rng.randrange(1, n+1)))
        lp = transport_lp(Dm, rho, alpha)
        cutform = sum(l[B]*abs(mass(rho, B)-mass(alpha, B)) for B in l)
        levelform = sum(length*sum(w(mass(alpha, B))*abs(mass(rho, B)-mass(alpha, B)) for B in part) for length, part in segs)
        counts['6.12'] += 1; counts['6.12_levelform'] += 1
        if abs(lp - cutform) > 1e-7: fails['6.12'] += 1
        if abs(levelform - cutform) > 1e-9: fails['6.12_levelform'] += 1
    # coupling chain to (6.14): arbitrary joint law q on distinct pairs, arbitrary g(y)
    for _ in range(2):
        q = {}
        for x in range(n):
            for y in range(n):
                if x != y and rng.random() < 0.3: q[(x, y)] = rng.random()
        s = sum(q.values()); q = {k: v/s for k, v in q.items()}
        qY = [sum(v for (x, y), v in q.items() if y == yy) for yy in range(n)]
        g = [rng.choice([D_cells(d, n, alpha, w, None, yy), rng.random()*3]) for yy in range(n)]
        lhs = sum(alpha[x]*alpha[xp]*alpha[yy]*abs(Dm[x][yy]-Dm[xp][yy]) for x in range(n) for xp in range(n) for yy in range(n))
        t1 = sum(v*abs(Dm[x][y]-g[y]) for (x, y), v in q.items())
        t2 = 0.0
        for yy in range(n):
            if qY[yy] > 0:
                rho_y = [q.get((x, yy), 0.0)/qY[yy] for x in range(n)]
                t2 += qY[yy]*sum(l[B]*abs(mass(rho_y, B)-mass(alpha, B)) for B in l)
        t3 = sum(l[B]*abs(mass(qY, B)-mass(alpha, B)) for B in l)
        counts['chain'] += 1
        if lhs > 2*t1 + 2*t2 + 2*t3 + 1e-9: fails['chain'] += 1
print('checks run:', counts)
print('failures  :', fails)

# CONTROL A: non-symmetric weight (w(t) != w(1-t)): (6.8) must FAIL for some pairs
wbad = make_w(0.3, symmetric=False)
bad = 0; tot = 0; asserts = 0
for trial in range(20):
    n = rng.randrange(8, 13); d = random_ultrametric(rng, n); alpha = [1.0/n]*n
    for _ in range(5):
        a0, a1 = rng.sample(range(n), 2)
        try:
            tot += 1
            if abs(D_cells(d, n, alpha, wbad, a0, a1) - D_u(d, n, alpha, wbad, a0, a1)) > 1e-9: bad += 1
        except AssertionError:
            asserts += 1
print('CONTROL A (asymmetric w, finite integrals): (6.8) numeric mismatches = %d / %d, assertion trips = %d (mismatches must be > 0)' % (bad, tot, asserts))
# CONTROL B: wrong transport formula (signed instead of absolute imbalance) must disagree with the LP
n = 10; d = random_ultrametric(rng, n); alpha = [0.1]*n
cells, parent, l, P = tree(d, n, w, alpha)
Dm = [[D_cells(d, n, alpha, w, a, b) if a != b else 0.0 for b in range(n)] for a in range(n)]
mis = 0
for _ in range(10):
    rho = rand_prob(rng, n, rng.sample(range(n), 3))
    if abs(transport_lp(Dm, rho, alpha) - sum(l[B]*(mass(rho, B)-mass(alpha, B)) for B in l)) > 1e-7: mis += 1
print('CONTROL B (signed imbalance formula): LP mismatches = %d / 10 (must be > 0)' % mis)
# CONTROL C: dropping the two transport terms from the (6.14) chain must be violated:
# q puts each target's whole incoming mass on one source s(y), g(y) = D(s(y),y) => 2E_q|D-g| = 0 but LHS > 0
viol = 0
for trial in range(10):
    n = rng.randrange(8, 12); d = random_ultrametric(rng, n); alpha = [1.0/n]*n
    Dm = [[D_cells(d, n, alpha, w, a, b) if a != b else 0.0 for b in range(n)] for a in range(n)]
    src = [rng.choice([x for x in range(n) if x != y]) for y in range(n)]
    q = {(src[y], y): 1.0/n for y in range(n)}
    g = [Dm[src[y]][y] for y in range(n)]
    t1 = sum(v*abs(Dm[x][y]-g[y]) for (x, y), v in q.items())
    lhs = sum(alpha[x]*alpha[xp]*alpha[yy]*abs(Dm[x][yy]-Dm[xp][yy]) for x in range(n) for xp in range(n) for yy in range(n))
    if lhs > 2*t1 + 1e-9: viol += 1
print('CONTROL C (chain without transport terms): violations = %d / 10 (must be > 0)' % viol)
