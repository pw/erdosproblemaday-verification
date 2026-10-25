#!/usr/bin/env python3
"""Generic C4-free completion CNF (our own encoding, written from the definitions, not from the authors' code).

Instance: n vertices; a set S whose incident edges are all FIXED (given explicitly); the free set F = V \\ S;
unknown edges are exactly the pairs inside F; target degree deg[v] for every v in F (exact).
CNF says: the completed graph has deg(v) = target for v in F, and no two distinct vertices share two
neighbours (= no C4, triangles allowed).  Fixed-part conditions (S-degrees, codegrees inside S) are
checked in Python and must hold, otherwise build() raises.
"""
import itertools
from pysat.card import CardEnc, EncType
from pysat.formula import CNF


def build(n, S, fixed_edges, target):
    S = sorted(S); F = [v for v in range(n) if v not in set(S)]
    adjS = {v: set() for v in range(n)}
    for a, b in fixed_edges:
        assert a != b and (a in S or b in S), (a, b)
        adjS[a].add(b); adjS[b].add(a)
    # fixed part sanity: codegree among S-pairs comes only from fixed edges
    for a, b in itertools.combinations(S, 2):
        assert len(adjS[a] & adjS[b]) <= 1, ("fixed codegree", a, b)
    var = {}
    for a, b in itertools.combinations(F, 2):
        var[(a, b)] = len(var) + 1
    def x(a, b):
        return var[(a, b) if a < b else (b, a)]
    cnf = CNF(); top = len(var)
    # exact degree inside F
    for v in F:
        need = target[v] - len(adjS[v])
        assert need >= 0, (v, target[v], len(adjS[v]))
        lits = [x(v, w) for w in F if w != v]
        enc = CardEnc.equals(lits=lits, bound=need, top_id=top, encoding=EncType.seqcounter)
        top = max(top, enc.nv); cnf.extend(enc.clauses)
    # S-vertex s and free vertex v: common neighbours = fixed nbrs of s in F that are adjacent (free edge) to v,
    # plus fixed common neighbours in S (edges s-u-v with u in S: s's fixed nbrs in S that are fixed-adjacent to v)
    for s in S:
        NF = [u for u in adjS[s] if u in set(F)]
        for v in F:
            fixed_common = len([u for u in adjS[s] if u in set(S) and v in adjS[u]])
            cands = [x(v, u) for u in NF if u != v]
            if fixed_common >= 2:
                raise ValueError(("fixed C4", s, v))
            if fixed_common == 1:
                cnf.extend([[-l] for l in cands])
            else:
                cnf.extend([[-a, -b] for a, b in itertools.combinations(cands, 2)])
    # two free vertices v, w: fixed common neighbours (in S) + free common neighbours p in F
    for v, w in itertools.combinations(F, 2):
        c0 = len(adjS[v] & adjS[w] & set(S))
        others = [p for p in F if p != v and p != w]
        if c0 >= 2:
            raise ValueError(("fixed C4", v, w))
        if c0 == 1:
            cnf.extend([[-x(v, p), -x(w, p)] for p in others])
        else:
            cnf.extend([[-x(v, p), -x(w, p), -x(v, q), -x(w, q)] for p, q in itertools.combinations(others, 2)])
    return cnf, var, F, adjS


def decode(model, var):
    pos = set(l for l in model if l > 0)
    return [e for e, i in var.items() if i in pos]


def check_graph(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        assert a != b and b not in adj[a]
        adj[a].add(b); adj[b].add(a)
    mc = max(len(adj[a] & adj[b]) for a, b in itertools.combinations(range(n), 2))
    return [len(s) for s in adj], mc
