# Lemma 6.1 check (paper p.22): finite tree, nonneg edge lengths, total L, alpha prob on vertices,
# every POSITIVE edge separates alpha-mass >= delta/2 on both sides, 0<delta<1  ==>
#   E|d(X,Y)-d(X',Y)| >= delta^2 L / (32 (ceil(16/delta)+1)),  X,X',Y iid alpha.
# Exact enumeration over triples. Also checks the proof's intermediate claims and the Lean variant
# (TreeTransport.lean fluctuation_lower: eta^3 L <= E|...| with eta = delta/2).
import random, math, sys
from fractions import Fraction

def build(parent, ln):
    N = len(parent)
    ch = [[] for _ in range(N)]
    for v in range(1, N): ch[parent[v]].append(v)
    # subtree sets
    sub = [None]*N
    def dfs(v):
        s = {v}
        for c in ch[v]: s |= dfs(c)
        sub[v] = s; return s
    dfs(0)
    # distances: d(x,y) = sum_{v!=0} ln[v] * [exactly one of x,y in sub(v)]
    d = [[0]*N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            d[x][y] = sum(ln[v] for v in range(1, N) if ((x in sub[v]) != (y in sub[v])))
    return ch, sub, d

def euler_tour(ch, ln):
    # closed walk from root crossing each edge twice; returns list of (time, vertex) visits
    visits = []; t = 0
    def walk(v):
        nonlocal t
        visits.append((t, v))
        for c in ch[v]:
            t += ln[c]; walk(c); t += ln[c]; visits.append((t, v))
    walk(0)
    return visits, t

def check(parent, ln, al, delta, verbose=False):
    N = len(parent)
    ch, sub, d = build(parent, ln)
    L = sum(ln[1:])
    # hypothesis
    for v in range(1, N):
        if ln[v] > 0:
            m = sum(al[x] for x in sub[v])
            if not (m >= delta/2 and 1-m >= delta/2): return ('HYP_FAILS', None)
    M = math.ceil(16/delta) + 1
    lhs = sum(al[x]*al[xp]*al[y]*abs(d[x][y]-d[xp][y]) for x in range(N) for xp in range(N) for y in range(N))
    bound = delta**2 * L / (32*M)
    res = {'lhs': lhs, 'bound': bound, 'L': L, 'ok_main': lhs >= bound - 1e-12}
    # intermediate claims
    res['s1'] = all(sum(al[x]*d[x][y] for x in range(N)) >= delta*L/2 - 1e-12 for y in range(N))
    res['s2'] = all(sum(al[x] for x in range(N) if d[x][y] >= delta*L/4 - 1e-12) >= delta/4 - 1e-12 for y in range(N))
    visits, T = euler_tour(ch, ln)
    assert abs(T - 2*L) < 1e-9
    h = delta*L/8
    nint = max(1, math.ceil(2*L/h)) if L > 0 else 1
    assert nint <= M
    cls = {}
    for v in range(N):
        tv = next(t for (t, u) in visits if u == v)   # one chosen visit
        k = min(int(tv // h), nint-1) if h > 0 else 0
        cls.setdefault(k, []).append(v)
    diam_ok = all(d[a][b] <= h + 1e-9 for c in cls.values() for a in c for b in c)
    near = sum(al[xp]*al[y] for xp in range(N) for y in range(N) if d[xp][y] <= h + 1e-12)
    sq = sum(sum(al[v] for v in c)**2 for c in cls.values())
    res['s3'] = diam_ok and len(cls) <= M and near >= sq - 1e-12 and sq >= 1/M - 1e-12
    both = sum(al[x]*al[xp]*al[y] for x in range(N) for xp in range(N) for y in range(N)
               if d[x][y] >= delta*L/4 - 1e-12 and d[xp][y] <= h + 1e-12)
    res['s4'] = both >= delta/(4*M) - 1e-12
    res['lean'] = lhs >= (delta/2)**3 * L - 1e-12
    return ('OK', res)

def rand_tree(rng, N, leaf_only):
    parent = [0] + [rng.randrange(v) for v in range(1, N)]
    ln = [0.0] + [rng.choice([0.0, rng.random(), rng.random()*5]) for _ in range(1, N)]
    ch = [[] for _ in range(N)]
    for v in range(1, N): ch[parent[v]].append(v)
    if leaf_only:
        leaves = [v for v in range(N) if not ch[v]]
        w = {v: rng.random() for v in leaves}
        s = sum(w.values()); al = [w.get(v, 0)/s for v in range(N)]
    else:
        w = [rng.random()**2 for _ in range(N)]; s = sum(w); al = [x/s for x in w]
    return parent, ln, al

def delta_hyp(parent, ln, al):
    N = len(parent); _, sub, _ = build(parent, ln)
    etas = [min(sum(al[x] for x in sub[v]), 1-sum(al[x] for x in sub[v])) for v in range(1, N) if ln[v] > 0]
    return 2*min(etas) if etas else None

if __name__ == '__main__':
    rng = random.Random(604)
    stats = {'trees': 0, 'main': 0, 's1': 0, 's2': 0, 's3': 0, 's4': 0, 'lean': 0}
    minratio = float('inf'); minratio_lean = float('inf')
    for trial in range(3000):
        N = rng.randrange(2, 11)
        parent, ln, al = rand_tree(rng, N, leaf_only=(trial % 2 == 0))
        dh = delta_hyp(parent, ln, al)
        if dh is None or dh <= 1e-6: continue
        delta = min(dh, 0.999)   # largest admissible delta (bound increasing in delta)
        st, r = check(parent, ln, al, delta)
        assert st == 'OK', (parent, ln, al, delta)
        stats['trees'] += 1
        for k in ['main', 's1', 's2', 's3', 's4', 'lean']:
            stats[k] += int(r['ok_main'] if k == 'main' else r[k])
        minratio = min(minratio, r['lhs']/r['bound'])
        minratio_lean = min(minratio_lean, r['lhs']/((delta/2)**3*r['L']))
    # structured family: stars with k leaves (delta ~ 2/k, small), random lengths, near-uniform leaf masses
    for k in [4, 8, 20, 50]:
        for rep in range(5):
            parent = [0]*(k+1); ln = [0.0]+[rng.random()+0.01 for _ in range(k)]
            w = [0.0]+[1+0.2*rng.random() for _ in range(k)]; s = sum(w); al = [x/s for x in w]
            dh = delta_hyp(parent, ln, al); delta = min(dh, 0.999)
            st, r = check(parent, ln, al, delta); assert st == 'OK'
            stats['trees'] += 1
            for kk in ['main', 's1', 's2', 's3', 's4', 'lean']:
                stats[kk] += int(r['ok_main'] if kk == 'main' else r[kk])
            minratio = min(minratio, r['lhs']/r['bound']); minratio_lean = min(minratio_lean, r['lhs']/((delta/2)**3*r['L']))
    print('random trees (hypothesis satisfied at delta = 2*min side mass):', stats)
    print('min LHS/paper_bound = %.3f   min LHS/lean_bound(eta^3 L) = %.3f' % (minratio, minratio_lean))

    # adversarial hill-climb: minimise LHS/(delta^2 L) subject to hypothesis (delta = 2*min side mass)
    best = float('inf')
    for start in range(40):
        N = rng.randrange(3, 9)
        parent, ln, al = rand_tree(rng, N, leaf_only=False)
        def score(parent, ln, al):
            dh = delta_hyp(parent, ln, al)
            if dh is None or dh < 1e-3: return float('inf'), None
            delta = min(dh, 0.999)
            st, r = check(parent, ln, al, delta)
            return r['lhs']/r['bound'], r
        cur, _ = score(parent, ln, al)
        for it in range(150):
            ln2 = ln[:]; al2 = al[:]
            v = rng.randrange(1, N); ln2[v] = max(0.0, ln2[v] + rng.gauss(0, 0.5))
            u = rng.randrange(N); al2[u] = max(0.0, al2[u] + rng.gauss(0, 0.05)); s = sum(al2)
            if s <= 0: continue
            al2 = [a/s for a in al2]
            sc, r = score(parent, ln2, al2)
            if sc < cur: cur, ln, al = sc, ln2, al2
        best = min(best, cur)
    print('adversarial hill-climb: min LHS/paper_bound = %.3f (must be >= 1)' % best)

    # CONTROL 1: hypothesis violated (2-vertex tree, masses 1-eps, eps; claim delta=1/2) -> bound must FAIL
    eps = 1e-5
    parent, ln, al = [0, 0], [0.0, 1.0], [1-eps, eps]
    st, _ = check(parent, ln, al, 0.5)
    _, sub, d = build(parent, ln)
    lhs = sum(al[x]*al[xp]*al[y]*abs(d[x][y]-d[xp][y]) for x in range(2) for xp in range(2) for y in range(2))
    b = 0.25*1.0/(32*(math.ceil(16/0.5)+1))
    print('CONTROL 1 (hypothesis violated): checker status =', st, '| LHS = %.3e < bound %.3e ?' % (lhs, b), lhs < b)
    # CONTROL 2: a deliberately too-strong constant (delta*L/4 instead of delta^2 L/(32M)) must be violated somewhere
    viol = 0
    for k in [4, 8, 20, 50]:
        parent = [0]*(k+1); ln = [0.0]+[1.0]*k; al = [0.0]+[1.0/k]*k
        dh = delta_hyp(parent, ln, al); delta = min(dh, 0.999)
        st, r = check(parent, ln, al, delta)
        if r['lhs'] < delta*r['L']/4 - 1e-12: viol += 1
    print('CONTROL 2 (fake constant delta*L/4, uniform stars k=4,8,20,50): violations found =', viol, 'of 4 (must be > 0)')
