# Seat F: minimal third validator for certificates.jsonl, written from the paper's lemmas (not from either checker).
# - initial constraints re-derived by EXPLICIT construction of the candidate new path systems (Lemma 9.4 via Lemma 6.2)
# - required-path constraints by plain DFS over simple paths (Lemma 9.5)
# - every round's additions re-justified by re-running its stated trial witness (Lemma 9.9) on my own trial data
# - every packing witness re-checked against my own ball bounds (Lemma 9.7) and compatibility (9.12)
import json, sys
from itertools import combinations

def build(pattern):
    lab = 0; Q = []; paths = []
    for comp in pattern:
        Q.append(lab)
        for q in comp:
            p = list(range(lab, lab + q + 2)); paths.append(p); lab = p[-1]; Q.append(lab)
        lab += 1
    n = lab
    adj = [set() for _ in range(n)]
    for a, b in combinations(Q, 2):
        adj[a].add(b); adj[b].add(a)
    for p in paths:
        for a, b in zip(p, p[1:]):
            adj[a].add(b); adj[b].add(a)
    return n, Q, paths, adj

def is_linear_forest(edges):
    # edges: list of (u,v) clique pairs; multigraph allowed in input -> reject parallels/loops
    seen = set(); deg = {}; parent = {}
    def f(x):
        while parent[x] != x: x = parent[x]
        return x
    for u, v in edges:
        if u == v: return False
        key = (min(u, v), max(u, v))
        if key in seen: return False
        seen.add(key)
        for w in (u, v):
            deg[w] = deg.get(w, 0) + 1; parent.setdefault(w, w)
            if deg[w] > 2: return False
        ru, rv = f(u), f(v)
        if ru == rv: return False
        parent[ru] = rv
    return True

def initial(k, t, n, Q, paths):
    L = n - t; e = len(paths); h = k + 1 - t
    Qs = set(Q)
    M = {}
    for x, y in combinations(range(n), 2):
        forb = set()
        def segs(v):
            if v in Qs: return [[v]]
            p = [p for p in paths if v in p[1:-1]]
            assert len(p) == 1; p = p[0]; i = p.index(v)
            return [p[:i + 1][::-1], p[i:]]   # lists starting at v, ending at a clique endpoint
        others = [p for p in paths if x not in p[1:-1] and y not in p[1:-1]]
        for sx in segs(x):
            for sy in segs(y):
                if set(sx) & set(sy): continue          # new path must be simple
                z, w = sx[-1], sy[-1]
                if z == w: continue
                newint = (set(sx) | set(sy)) - {z, w}  # interior vertices of the new path taken from S
                for r in range(len(others) + 1):
                    for E in combinations(others, r):
                        ints = [set(p[1:-1]) for p in E]
                        # interiors pairwise disjoint and disjoint from the new path's S-part
                        allint = set(); ok = True
                        for s in ints + [newint]:
                            if allint & s: ok = False; break
                            allint |= s
                        if not ok: continue
                        # the new path's endpoints must not be interior of kept paths (they are clique vertices: automatic)
                        rep = [(p[0], p[-1]) for p in E] + [(z, w)]
                        if not is_linear_forest(rep): continue
                        ep = len(E) + 1
                        vp = len({u for ed in rep for u in ed})
                        base = sum(len(p) - 2 for p in E) + len(newint)
                        for d in range(1, k + 2):
                            A = base + d
                            if L + (1 if ep >= e else 0) <= A <= k + 1 - vp:   # Lemma 6.2 interval
                                forb.add(d)
        M[(x, y)] = forb
    return M

def get(M, i, j):
    if i == j: return set()
    return M.get((min(i, j), max(i, j)), set())

def req_paths(k, nX, adj, M):
    M2 = {key: set(v) for key, v in M.items()}
    for s in range(nX):
        stack = [(s, 1 << s, 0)]
        while stack:
            v, used, ell = stack.pop()
            if ell >= 1 and v > s:
                M2.setdefault((s, v), set()).add(k - ell)
            if ell == k: continue
            for w in adj[v]:
                if not used >> w & 1:
                    stack.append((w, used | (1 << w), ell + 1))
    return M2

def ball_weights(k, t, nX, M, i):
    W = {-1: 1}
    N0 = sum(1 for j in range(nX) if j != i and 0 in get(M, i, j))
    b = k + 1 - nX + N0
    if b <= 0: return W
    u = 2 if b >= t else 1
    W[0] = u
    for r in (1, 2):
        T = sum(1 for j in range(nX) if j != i and set(range(1, r + 1)) <= get(M, i, j))
        bn = max(b, k * u + 1 - nX + T)
        uh = max(u, 1 + (bn > t) + (bn > max(k, 2 * t)))
        if uh == 1 and b == bn == t and k + 1 - nX + T >= t:
            uh = 2
        W[r] = uh
        b, u = bn, uh
    return W

def check_witness(k, t, nX, adj, M, wit):
    if wit['kind'] == 'required_forbidden_edge':
        a, b = wit['edge']
        return b in adj[a] and 0 in get(M, a, b)
    opts = wit['options']
    bases = [o[0] for o in opts]
    if len(set(bases)) != len(bases): return False
    tot = 0
    for b0, r, w in opts:
        W = ball_weights(k, t, nX, M, b0)
        if r not in W or w > W[r] or w < 1: return False
        tot += w
    for (i, r, _), (j, s, _) in combinations(opts, 2):
        need = {0} if r == s == -1 else set(range(1, r + s + 3))
        if not need <= get(M, i, j): return False
    return tot > k

bad = 0; cnt = 0; init_mismatch = 0
for line in open(sys.argv[1]):
    R = json.loads(line); cnt += 1
    k, t = R['k'], R['t']
    pat = [tuple(c) for c in R['pattern']]
    n, Q, paths, adj = build(pat)
    assert len(Q) == t
    M = initial(k, t, n, Q, paths)
    tr = {(a, b): {d for d in range(64) if f >> d & 1} for a, b, f in R['initial']}
    mine = {key: v for key, v in M.items() if v}
    if mine != tr:
        init_mismatch += 1
        print('INITIAL MISMATCH', k, t, pat, {kk: (mine.get(kk), tr.get(kk)) for kk in set(mine) | set(tr) if mine.get(kk) != tr.get(kk)})
    if R['classification'] == 1:
        if R['rounds'] or not check_witness(k, t, n, adj, M, R['final']):
            bad += 1; print('BAD class1', k, t, pat)
        continue
    # class 1 must genuinely fail? (not needed for soundness) -- skip
    M = req_paths(k, n, adj, M)
    for rnd in R['rounds']:
        adds = []
        for a in rnd:
            i, j = a['pair']; d = a['d']
            assert i != j and d in (0, 1)
            if d == 0:
                adj2 = [set(s) for s in adj]; adj2[i].add(j); adj2[j].add(i); nX = n
            else:
                adj2 = [set(s) for s in adj] + [set()]; adj2[i].add(n); adj2[j].add(n); adj2[n] |= {i, j}; nX = n + 1
            M2 = req_paths(k, nX, adj2, M)     # old entries kept for old pairs; new vertex starts empty
            if not check_witness(k, t, nX, adj2, M2, a['witness']):
                bad += 1; print('BAD round witness', k, t, pat, a['pair'], d)
            adds.append((min(i, j), max(i, j), d))
        for i, j, d in adds:
            M.setdefault((i, j), set()).add(d)
    if not check_witness(k, t, n, adj, M, R['final']):
        bad += 1; print('BAD final', k, t, pat)
print('records', cnt, 'bad', bad, 'initial mismatches', init_mismatch)
