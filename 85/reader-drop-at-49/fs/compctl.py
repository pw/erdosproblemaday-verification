#!/usr/bin/env python3
"""Composition control for the FULL fs pipeline (normalisation + R1 + R1b + class SB + high-perm SB) on the small
saturated analogues n = d^2 (low degree d, high degree d+1).  For each (d, h, T):
  BASE = c4cnf on the normalised fixed high-low structure, NO R1/R1b/SB.  PIPE = the full fs encoding.
  Enumerate ALL solutions of both (SAT + blocking clauses).  Map each to its isomorphism class with the highs
  coloured (pynauty certificate) -- these are exactly the orbits of the group the SB is drawn from.
  Require: orbits(PIPE) == orbits(BASE)  (SB + R1 + R1b lose no graph and admit nothing new), and every BASE
  solution satisfies R1/R1b semantically (the theorem, checked on real graphs)."""
import itertools, sys, time
from pathlib import Path
from pysat.solvers import Cadical153
from pynauty import Graph, certificate
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fsenc, c4cnf
LIMIT = 300000
def enum(clauses, var, n, fixed):
    out = []
    edges = sorted(var)
    with Cadical153(bootstrap_with=clauses) as s:
        while s.solve():
            m = set(l for l in s.get_model() if l > 0)
            on = [e for e in edges if var[e] in m]
            out.append(on)
            s.add_clause([-var[e] for e in on] + [var[e] for e in edges if var[e] not in m])
            if len(out) >= LIMIT: return out, False
    return out, True
def cert(n, h, fixed, on):
    adj = {v: [] for v in range(n)}
    for a, b in list(fixed) + on: adj[a].append(b); adj[b].append(a)
    g = Graph(n, adjacency_dict=adj, vertex_coloring=[set(range(h)), set(range(h, n))])
    return certificate(g)
def r1ok(n, h, fixed, on):
    adj = {v: set() for v in range(n)}
    for a, b in list(fixed) + on: adj[a].add(b); adj[b].add(a)
    return all(len(adj[v] & adj[x]) == 1 for x in range(h) for v in range(n) if v != x)
d = int(sys.argv[1]); n = d * d
for h in range(1, d + 3):
    if (d * n + h) % 2: continue
    Ts = [[]]
    if d >= 6:
        Ts, seen = [], set()
        trip = list(itertools.combinations(range(h), 3))
        for t in range(0, h * (h - 1) // 6 + 1):
            for sysT in itertools.combinations(trip, t):
                if any(len(set(a) & set(b)) > 1 for a, b in itertools.combinations(sysT, 2)): continue
                key = min(tuple(sorted(tuple(sorted(p[x] for x in b)) for b in sysT)) for p in itertools.permutations(range(h)))
                if key not in seen: seen.add(key); Ts.append([list(b) for b in key])
    for T in Ts:
        c = fsenc.stratum_gen(n, d, h, T)
        if c is None: continue
        H, fixed, target, blocks = c
        t0 = time.time()
        base, var, F, adjS = c4cnf.build(n, H, fixed, target)
        bs, bdone = enum(base.clauses, var, n, fixed)
        cnf, var2, F2, adjS2, st, cls = fsenc.build(n, H, fixed, target, highs=H, sb="all", r1=True, r1b=True, hdeg=d + 1)
        assert var2 == var
        perms = []
        for a, b in itertools.combinations(range(h), 2):
            sig = list(range(h)); sig[a], sig[b] = b, a
            try: perms.append(fsenc.high_perm(h, h, blocks, sig))
            except AssertionError: pass
        top = max([abs(l) for cl in cnf.clauses for l in cl] + [len(var)])
        top, nc = fsenc.add_perm_sb(cnf, var, n, perms, top)
        ps, pdone = enum(cnf.clauses, var, n, fixed)
        A = {cert(n, h, fixed, on) for on in bs}
        B = {cert(n, h, fixed, on) for on in ps}
        r1 = all(r1ok(n, h, fixed, on) for on in bs)
        print(f"d={d} h={h} T={T} base_solutions={len(bs)}{'' if bdone else '+(capped)'} pipe_solutions={len(ps)}{'' if pdone else '+(capped)'} "
              f"orbits_base={len(A)} orbits_pipe={len(B)} EQUAL={A == B} base_all_satisfy_R1R1b={r1} classes={st['sb_classes']} "
              f"highperms={len(perms)} {round(time.time()-t0,1)}s", flush=True)
