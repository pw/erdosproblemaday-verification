#!/usr/bin/env python3
"""Enumerate, up to isomorphism, every oriented graph on n vertices that is
(I_3, L_3)-free  (no independent triple, no transitive 3-tournament)   -- "N-types"
and every tournament on n vertices that is L_4-free (no transitive 4-subtournament) -- "T-types".

Method: SAT enumeration with blocking clauses on a canonical form. Canonical form =
lexicographically least pair-state string over all n! relabelings (n <= 8, fine).
Each found model is canonicalised, and ALL relabelings' state strings are blocked
(so each isomorphism class is produced once). Positive controls: the number of
L_4-free tournaments on 7 vertices must be 1 (Paley), on 8 must be 0 (every
8-tournament has a TT_4); (I_3,L_3)-free oriented graphs on 9 vertices must be 0
(k(3,3)=9).
"""
import sys, json, itertools
from pysat.solvers import Solver

def pairs(n): return list(itertools.combinations(range(n), 2))

class Enc:
    def __init__(self, n):
        self.n = n; self.idx = {}
        k = 1
        for u, v in pairs(n):
            self.idx[("f", u, v)] = k; self.idx[("f", v, u)] = k+1; self.idx[("z", u, v)] = k+2; k += 3
        self.top = k - 1
    def fwd(self, u, v): return self.idx[("f", u, v)]
    def none(self, u, v): a, b = sorted((u, v)); return self.idx[("z", a, b)]

def base_clauses(e, tournament):
    n = e.n; cl = []
    for u, v in pairs(n):
        f, r, z = e.fwd(u, v), e.fwd(v, u), e.none(u, v)
        if tournament:
            cl.append([f, r]); cl.append([-f, -r]); cl.append([-z])
        else:
            cl.append([f, r, z]); cl.append([-f, -r]); cl.append([-f, -z]); cl.append([-r, -z])
    if tournament:
        for S in itertools.combinations(range(n), 4):
            for order in itertools.permutations(S):
                cl.append([-e.fwd(order[i], order[j]) for i in range(4) for j in range(i+1, 4)])
    else:
        for a, b, c in itertools.combinations(range(n), 3):
            cl.append([-e.none(a, b), -e.none(a, c), -e.none(b, c)])
            for order in itertools.permutations((a, b, c)):
                cl.append([-e.fwd(order[0], order[1]), -e.fwd(order[0], order[2]), -e.fwd(order[1], order[2])])
    return cl

def state_of(e, model):
    true = set(l for l in model if l > 0)
    st = {}
    for u, v in pairs(e.n):
        st[(u, v)] = 1 if e.fwd(u, v) in true else (2 if e.fwd(v, u) in true else 0)  # 1: u->v, 2: v->u, 0: none
    return st

def relabel(st, n, perm):
    out = {}
    for (u, v), s in st.items():
        a, b = perm[u], perm[v]
        if a < b: out[(a, b)] = s
        else: out[(b, a)] = (0 if s == 0 else (2 if s == 1 else 1))
    return out

def key(st, n): return tuple(st[p] for p in pairs(n))

def block_clause(e, st):
    cl = []
    for (u, v), s in st.items():
        lit = e.fwd(u, v) if s == 1 else (e.fwd(v, u) if s == 2 else e.none(u, v))
        cl.append(-lit)
    return cl

def enumerate_types(n, tournament):
    e = Enc(n); cls = base_clauses(e, tournament)
    found = []
    perms = list(itertools.permutations(range(n)))
    with Solver(name="cadical195", bootstrap_with=cls) as s:
        while s.solve():
            st = state_of(e, s.get_model())
            orbit = {}
            for p in perms:
                r = relabel(st, n, p); orbit[key(r, n)] = r
            canon = orbit[min(orbit)]
            found.append({"n": n, "arcs": [[u, v] for (u, v), x in canon.items() if x == 1] + [[v, u] for (u, v), x in canon.items() if x == 2],
                          "aut": len(perms) // len(orbit)})
            for r in orbit.values():
                s.add_clause(block_clause(e, r))
    return found

if __name__ == "__main__":
    out = {"N": {}, "T": {}}
    for n in range(3, 9):
        t = enumerate_types(n, tournament=False)
        out["N"][n] = t; print(f"(I3,L3)-free oriented graphs on {n}: {len(t)} types; aut sizes {[x['aut'] for x in t][:20]}", flush=True)
    assert len(enumerate_types(9, tournament=False)) == 0, "CONTROL FAILED: k(3,3)=9 means none on 9"
    print("control: none on 9 vertices OK")
    for n in range(3, 8):
        t = enumerate_types(n, tournament=True)
        out["T"][n] = t; print(f"L4-free tournaments on {n}: {len(t)} types; aut sizes {[x['aut'] for x in t]}", flush=True)
    assert len(enumerate_types(8, tournament=True)) == 0, "CONTROL FAILED: every 8-tournament has a TT4"
    print("control: none on 8 vertices OK")
    json.dump(out, open("types.json", "w"))
    print("wrote types.json")
