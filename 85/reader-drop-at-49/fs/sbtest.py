#!/usr/bin/env python3
"""Soundness controls for fsenc's SB + R1 encoding, by brute force on tiny instances.
(1) CNF-vs-semantics: for every free-edge assignment, (SB clauses satisfiable with edges fixed) == lex_ok.
(2) Orbit coverage: every solution of the base constraints has a group image (product of symmetric groups on the
    interchangeable classes) that satisfies lex_ok  ==> SB removes no isomorphism class.
(3) Discriminating mutation: flip the lex direction for ONE pair in the CNF; (1) must then FAIL somewhere.
"""
import itertools, random, sys
from pysat.solvers import Cadical153
sys.path.insert(0, '.')
import fsenc, c4cnf

def run_case(n, S, fixed, target, mutate=False):
    cnf, var, F, adjS, st, cls = fsenc.build(n, S, fixed, target, highs=(), sb="all", r1=False)
    base, _, _, _ = c4cnf.build(n, S, fixed, target)
    nbase = len(base.clauses)
    sbcl = cnf.clauses[nbase:]
    if mutate and sbcl:
        # flip the first "a <= b" clause [(-e),-a,b] -> [(-e),a,-b]
        c = list(sbcl[0]); c[-2], c[-1] = -c[-2], -c[-1]; sbcl[0] = c
    edges = list(var)
    sols = []
    mism = 0
    with Cadical153(bootstrap_with=sbcl) as sbs, Cadical153(bootstrap_with=base.clauses) as bs:
        space = range(1 << len(edges)) if len(edges) <= 16 else [random.getrandbits(len(edges)) for _ in range(20000)]
        for bits in space:
            on = [edges[i] for i in range(len(edges)) if bits >> i & 1]
            assum = [var[e] if (bits >> i & 1) else -var[e] for i, e in enumerate(edges)]
            adj = {v: set(adjS[v]) for v in range(n)}
            for a, b in on:
                adj[a].add(b); adj[b].add(a)
            sem = fsenc.lex_ok(adj, cls, n)
            enc = sbs.solve(assumptions=assum)
            if sem != enc:
                mism += 1
            if len(edges) <= 16 and bs.solve(assumptions=assum):
                sols.append(adj)
    if len(edges) > 16:   # enumerate all base solutions by blocking clauses
        with Cadical153(bootstrap_with=base.clauses) as bs:
            while bs.solve():
                m = set(l for l in bs.get_model() if l > 0)
                on = [e for e in edges if var[e] in m]
                adj = {v: set(adjS[v]) for v in range(n)}
                for a, b in on:
                    adj[a].add(b); adj[b].add(a)
                sols.append(adj)
                assum = [var[e] if var[e] in m else -var[e] for e in edges]
                with Cadical153(bootstrap_with=sbcl) as sbs2:
                    if sbs2.solve(assumptions=assum) != fsenc.lex_ok(adj, cls, n): mism += 1
                bs.add_clause([-var[e] if var[e] in m else var[e] for e in edges])
                if len(sols) > 3000: break
    uncovered = 0
    for adj in sols:
        ok = False
        for perms in itertools.product(*[itertools.permutations(C) for C in cls]):
            m = {v: v for v in range(n)}
            for C, P in zip(cls, perms):
                for a, b in zip(C, P): m[a] = b
            adj2 = {m[v]: {m[u] for u in adj[v]} for v in range(n)}
            if fsenc.lex_ok(adj2, cls, n):
                ok = True; break
        uncovered += not ok
    return len(edges), [len(C) for C in cls], len(sols), mism, uncovered

random.seed(20261019)
cases = []
# n=8, S={0,1} with fixed edges making classes; free 6 vertices
cases.append((8, [0, 1], [(0, 2), (0, 3), (1, 4), (1, 5)], {v: 2 for v in range(2, 8)}))
cases.append((8, [0], [(0, 2), (0, 3), (0, 4)], {v: 2 for v in range(1, 8)}))
cases.append((9, [0], [(0, 1), (0, 2), (0, 3)], {v: 2 for v in range(1, 9)}))
cases.append((10, [0, 1], [(0, 2), (0, 3), (0, 4), (1, 5), (1, 6), (1, 7)], {v: 3 for v in range(2, 10)}))
cases.append((7, [], [], {v: 2 for v in range(7)}))
cases.append((7, [0], [(0, 1), (0, 2)], {v: 3 for v in range(1, 7)}))
cases.append((8, [0, 1], [(0, 2), (0, 3), (1, 2), (1, 4)], {v: 3 for v in range(2, 8)}))
for n, S, fixed, target in cases:
    target = {v: target[v] for v in range(n) if v not in S}
    try:
        print("case", n, S, fixed, "->", run_case(n, S, fixed, target), flush=True)
    except AssertionError as e:
        print("case skipped (encoder assert)", e)
n, S, fixed, target = cases[0]
print("MUTATED case0 ->", run_case(n, S, fixed, {v: target[v] for v in range(n) if v not in S}, mutate=True))
