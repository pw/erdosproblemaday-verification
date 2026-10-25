#!/usr/bin/env python3
"""Randomized end-to-end simulation of the combinatorial core of lem:pair-folding + lem:batch-resolution
(OpenAI paper, folding.tex): heavy-neighbour trimming, random pair folding, loop/parallel cleanup,
an arbitrary cycle-and-edge partition of each quotient, switch demands, routes chosen in the routers
honouring exactly the constraints the routing lemma supplies (edge-disjoint over everything in one router;
interiors avoid Z_C; interiors pairwise disjoint within a team), then lifting.
Asserts: every lifted quotient cycle is ONE simple cycle (no repeated vertex, length>=3); all parts
pairwise edge-disjoint; union of parts = E(F) + used router edges; |E_err| <= 2 sum m_i; order formula;
per-vertex demand load <= d_F(x) <= a.  Route EXISTENCE (expansion) is not tested here — only that the
lemma's guaranteed properties suffice for the lifting."""
import random, sys
def E(u, v): return (u, v) if u < v else (v, u)
FORBID = set()
import sys as _s
A_PARAM = int(_s.argv[3]) if len(_s.argv) > 3 else 2
DENS = int(_s.argv[4]) if len(_s.argv) > 4 else 2
MUT = _s.argv[5] if len(_s.argv) > 5 else ''   # negative controls: 'noZ' drop Z_C; 'noteam' drop team-disjointness; 'noedge' drop router edge-disjointness

def greedy_cycle_edge_partition(adj_edges, rng):
    """arbitrary cycle-and-edge partition of a simple graph: repeatedly extract a cycle via DFS."""
    edges = set(adj_edges); parts = []
    while True:
        nbr = {}
        for (a, b) in edges:
            nbr.setdefault(a, set()).add(b); nbr.setdefault(b, set()).add(a)
        cyc = None
        verts = list(nbr); rng.shuffle(verts)
        for s in verts:
            # find a cycle through DFS from s
            parent = {s: None}; stack = [(s, iter(sorted(nbr[s], key=lambda _: rng.random())))]
            while stack and cyc is None:
                x, it = stack[-1]
                for y in it:
                    if y == parent[x]: continue
                    if y in parent:
                        # back edge x-y: cycle y ... x
                        path = [x]; cur = x
                        while cur != y:
                            cur = parent[cur]
                            if cur is None: path = None; break
                            path.append(cur)
                        if path and len(path) >= 3: cyc = path
                        if cyc: break
                        continue
                    parent[y] = x; stack.append((y, iter(sorted(nbr[y], key=lambda _: rng.random())))); break
                else:
                    stack.pop()
            if cyc: break
        if not cyc: break
        cedges = [E(cyc[i], cyc[(i+1) % len(cyc)]) for i in range(len(cyc))]
        assert len(set(cedges)) == len(cedges) and all(e in edges for e in cedges)
        for e in cedges: edges.discard(e)
        parts.append(('cycle', cyc))
    for e in edges: parts.append(('edge', e))
    return parts

def route(rng, Rverts, u, v, forbid_int, team_used, router_used, maxlen=4, tries=400):
    """random simple u-v path in the complete graph on Rverts, interior avoiding forbid_int and team_used,
    edges avoiding router_used (global edge-disjointness inside this router)."""
    pool = [x for x in Rverts if x not in forbid_int and x not in team_used and x != u and x != v]
    for _ in range(tries):
        k = rng.randint(0, min(maxlen-1, len(pool)))
        inter = rng.sample(pool, k)
        path = [u] + inter + [v]
        es = [E(path[i], path[i+1]) for i in range(len(path)-1)]
        if all(e not in router_used and e not in FORBID for e in es) and len(set(es)) == len(es):
            return path
    return None

def one_instance(rng, stats):
    nY = rng.randint(60, 140)
    Y = list(range(nY))
    # pieces: disjoint vertex sets inside Y
    perm = Y[:]; rng.shuffle(perm)
    pieces = []; pos = 0
    while pos < nY - 10 and len(pieces) < 6:
        sz = rng.randint(15, 35); pieces.append(set(perm[pos:pos+sz])); pos += sz
    piece_of = {x: i for i, P in enumerate(pieces) for x in P}
    a = A_PARAM; L0 = max(8, a*a)          # L0 >= max(8, a^2)
    # batches: overlapping subsets W, edge-disjoint graphs J_W
    batches = []; usedF = set()
    for _ in range(rng.randint(2, 5)):
        W = set(rng.sample(Y, rng.randint(25, min(70, nY))))
        Wl = sorted(W); J = set()
        for _ in range(rng.randint(len(W)//3, DENS*len(W))):
            x, y = rng.sample(Wl, 2); e = E(x, y)
            if e not in usedF: usedF.add(e); J.add(e)
        batches.append((W, J))
    F = usedF
    global FORBID; FORBID = F          # router graph P_R := complete graph on V(R) minus E(F)
    degF = {x: 0 for x in Y}
    for (x, y) in F: degF[x] += 1; degF[y] += 1
    good = {x for x in Y if degF[x] <= a}
    parts = []                                  # ('edge', e) | ('cycle', [vertex list])
    router_used = [set() for _ in pieces]
    load = {}                                   # demand-end occurrences per vertex
    for W, J in batches:
        # active sets
        act = {}
        for i, P in enumerate(pieces):
            X = sorted(good & W & P)
            if len(X) >= L0: act[i] = set(X)
        actv = set().union(*act.values()) if act else set()
        # heavy neighbours (heavy-neighbour work; path decomposition done greedily here)
        J0 = set(J)
        for i, X in act.items():
            nbrX = {}
            for (p, q) in J:
                if p in X and q not in X: nbrX.setdefault(q, []).append(p)
                if q in X and p not in X: nbrX.setdefault(p, []).append(q)
            HX = {v for v, l in nbrX.items() if len(l) > a}
            assert not (HX & actv)
            EX = {e for e in J if (e[0] in X and e[1] in HX) or (e[1] in X and e[0] in HX)}
            J0 -= EX
            # greedy path decomposition of the bipartite graph (X, HX; EX)
            rem = set(EX)
            while rem:
                e = rem.pop(); path = [e[0], e[1]]
                ext = True
                while ext:
                    ext = False
                    for end in (0, -1):
                        t = path[end]
                        for f in list(rem):
                            if t in f:
                                o = f[0] if f[1] == t else f[1]
                                if o not in path:
                                    rem.discard(f)
                                    if end == 0: path.insert(0, o)
                                    else: path.append(o)
                                    ext = True; break
                # trim H_X terminal edges
                if path[0] in HX: parts.append(('edge', E(path[0], path[1]))); path = path[1:]
                if len(path) >= 2 and path[-1] in HX: parts.append(('edge', E(path[-2], path[-1]))); path = path[:-1]
                if len(path) < 2: continue
                assert path[0] in X and path[-1] in X and len(path) >= 3
                Rv = pieces[i]
                forbid = set(path) & Rv
                rt = route(rng, Rv, path[0], path[-1], forbid, set(), router_used[i])
                if rt is None: stats['route_fail'] += 1; return False
                for k in range(len(rt)-1): router_used[i].add(E(rt[k], rt[k+1]))
                for xend, term in ((path[0], E(path[0], path[1])), (path[-1], E(path[-2], path[-1]))):
                    load.setdefault(xend, set()).add(term)
                cyc = path + rt[-2:0:-1]
                parts.append(('cycle', cyc))
        # random pair folding on J0 with the active sets
        pi = {x: ('s', x) for x in W}; pairs = {}
        msum = 0
        for i, X in act.items():
            Xl = sorted(X); rng.shuffle(Xl); msum += len(Xl)
            for k in range(0, len(Xl) - 1, 2):
                u, v = Xl[k], Xl[k+1]; f = ('f', u, v)
                pi[u] = f; pi[v] = f; pairs[f] = (u, v, i)
        qverts = set(pi.values())
        assert len(qverts) == len(W) - sum(len(X)//2 for X in act.values())
        rep = {}; Eerr = []
        for e in sorted(J0, key=lambda _: rng.random()):
            qa, qb = pi[e[0]], pi[e[1]]
            if qa == qb: Eerr.append(e); continue
            key = E(qa, qb)
            if key in rep: Eerr.append(e); continue
            rep[key] = e
        if act: assert len(Eerr) <= 2*msum, (len(Eerr), msum)
        stats['err_ratio'] = max(stats['err_ratio'], len(Eerr)/max(1, msum))
        for e in Eerr: parts.append(('edge', e))
        # arbitrary cycle-and-edge partition of the quotient
        qparts = greedy_cycle_edge_partition(list(rep), rng)
        for kind, obj in qparts:
            if kind == 'edge': parts.append(('edge', rep[obj])); continue
            z = obj; s = len(z)
            hat = [rep[E(z[j], z[(j+1) % s])] for j in range(s)]
            def end_in(e, fib):
                return e[0] if pi[e[0]] == fib else e[1]
            ZC = set(x for e in hat for x in e)
            team_int = {}            # per router: interiors used by this cycle's team
            walk = []
            for j in range(s):
                fib = z[j]
                uj = end_in(hat[j-1], fib); vj = end_in(hat[j], fib)
                if uj == vj: walk.append(uj)
                else:
                    pu, pv, i = pairs[fib]
                    assert {uj, vj} == {pu, pv}
                    Rv = pieces[i]
                    rt = route(rng, Rv, uj, vj, set() if MUT=='noZ' else (ZC & Rv), (team_int.setdefault(i, set()) and set()) if MUT=='noteam' else team_int.setdefault(i, set()), set() if MUT=='noedge' else router_used[i])
                    if rt is None: stats['route_fail'] += 1; return False
                    for k in range(len(rt)-1): router_used[i].add(E(rt[k], rt[k+1]))
                    team_int[i] |= set(rt[1:-1])
                    load.setdefault(uj, set()).add(hat[j-1]); load.setdefault(vj, set()).add(hat[j])
                    walk.extend(rt[:-1]); walk.append(vj)
                # traverse hat[j] from vj to u_{j+1}: next loop appends u_{j+1}
            # verify consecutive steps are edges and closed walk is a simple cycle
            assert len(walk) == len(set(walk)), "repeated vertex in lifted cycle"
            assert len(walk) >= 3
            stats['lifted'] += 1
            stats['switches'] += sum(1 for j in range(s) if end_in(hat[j-1], z[j]) != end_in(hat[j], z[j]))
            parts.append(('cycle', walk))
    # global edge accounting
    seen = {}
    for kind, obj in parts:
        es = [obj] if kind == 'edge' else [E(obj[k], obj[(k+1) % len(obj)]) for k in range(len(obj))]
        if kind == 'cycle': assert len(set(es)) == len(es) and len(obj) >= 3 and len(set(obj)) == len(obj)
        for e in es:
            assert e not in seen, "edge used twice"
            seen[e] = kind
    allR = set().union(*router_used) if router_used else set()
    for i in range(len(pieces)):
        for j in range(i+1, len(pieces)): assert not (router_used[i] & router_used[j])
    assert not (allR & F), "router edge collides with F (would need E(R) disjoint from F)"
    assert set(seen) == F | allR, "edge accounting mismatch"
    for x, es in load.items():
        assert len(es) <= degF[x] <= a, ("load", x, len(es), degF[x])
    return True

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
stats = {'lifted': 0, 'switches': 0, 'route_fail': 0, 'err_ratio': 0.0}
ok = 0; N = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
for t in range(N):
    if one_instance(rng, stats): ok += 1
print(f"instances completed={ok}/{N}  lifted quotient cycles={stats['lifted']}  switch paths={stats['switches']}  "
      f"route sampling failures (skipped, not a proof failure)={stats['route_fail']}  max |E_err|/sum m_i={stats['err_ratio']:.3f}")
print("ALL ASSERTIONS PASSED")
