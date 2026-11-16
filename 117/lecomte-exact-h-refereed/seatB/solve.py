#!/usr/bin/env python3
"""Read export.g output; for each group compute a(G) (min abelian cover) exactly and omega(G)
(max pairwise-noncommuting set) via CP-SAT, using maximal abelian subgroups (= maximal cliques of
the commuting graph on G/Z(G)\{1}) as covering sets / clique constraints.
omega is reported exact when CP-SAT proves optimality, otherwise as a lower bound '>=k'.
Verdict: OK if a <= T(omega_lb) (valid since T nondecreasing and omega >= omega_lb)."""
import sys, networkx as nx
from ortools.sat.python import cp_model

def T(n):
    if n <= 2: return 1
    if n <= 6: return n
    if n <= 8: return 10
    return 1 + 2 ** ((n - 1) // 2)

def parse(path):
    cur = None
    for line in open(path):
        p = line.split()
        if not p: continue
        if p[0] == 'G':
            if cur is not None and 'id' in cur: yield cur
            cur = {'label': p[1], 'n': int(p[2]), 'order': int(p[3]), 'comm': {}, 'extra': ' '.join(p[4:])}
        elif p[0] == 'ID':
            cur['id'] = int(p[1])
        else:
            i = int(p[0]); cur['comm'][i] = set(int(x) for x in p[1:])
    if cur is not None and 'id' in cur: yield cur

def analyse(g, tl_cover=300, tl_omega=60):
    n, idv, comm = g['n'], g['id'], g['comm']
    V = [v for v in range(1, n + 1) if v != idv]
    if not V:
        return dict(omega=1, exact=True, a=1, nmax=1)
    for v in V:
        for w in comm[v]:
            assert v in comm[w], "asymmetric commuting relation"
    H = nx.Graph(); H.add_nodes_from(V)
    for v in V:
        for w in comm[v]:
            if w != idv and w > v: H.add_edge(v, w)
    maxab = [frozenset(c) for c in nx.find_cliques(H)]
    # a: min number of maximal abelian subgroups covering V
    m2 = cp_model.CpModel(); y = [m2.NewBoolVar(f"y{i}") for i in range(len(maxab))]
    cover = {v: [] for v in V}
    for i, c in enumerate(maxab):
        for v in c: cover[v].append(y[i])
    for v in V: m2.AddBoolOr(cover[v])
    m2.Minimize(sum(y))
    s2 = cp_model.CpSolver(); s2.parameters.max_time_in_seconds = tl_cover; s2.parameters.num_workers = 4
    r2 = s2.Solve(m2)
    assert r2 == cp_model.OPTIMAL, ("cover not optimal", g['label'], s2.StatusName(r2))
    a = int(round(s2.ObjectiveValue()))
    chosen = [maxab[i] for i in range(len(maxab)) if s2.Value(y[i])]
    assert set().union(*chosen) >= set(V)
    for c in chosen:
        for a1 in c: assert c <= comm[a1] | {a1}
    # omega
    m = cp_model.CpModel(); x = {v: m.NewBoolVar(f"x{v}") for v in V}
    for c in maxab: m.Add(sum(x[v] for v in c) <= 1)
    m.Maximize(sum(x.values()))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl_omega; s.parameters.num_workers = 4
    r = s.Solve(m)
    assert r in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    clique = [v for v in V if s.Value(x[v])]
    for i, a1 in enumerate(clique):
        for b in clique[i+1:]: assert b not in comm[a1]
    om = len(clique)
    return dict(omega=om, exact=(r == cp_model.OPTIMAL), a=a, nmax=len(maxab), ub=int(s.BestObjectiveBound()))

def verdict(res):
    om, a = res['omega'], res['a']
    if a < om: return 'BUG a<omega'
    if a > T(om):
        return 'OPEN (a > T(omega_lb); need exact omega)' if not res['exact'] else '*** VIOLATION a > T(omega)'
    if res['exact'] and om >= 9 and a == T(om): return 'EQUALITY(omega>=9)'
    return 'ok'

if __name__ == '__main__':
    for g in parse(sys.argv[1]):
        res = analyse(g)
        om = f"{res['omega']}" if res['exact'] else f">={res['omega']}(ub{res['ub']})"
        print(f"{g['label']}\t|G|={g['order']}\t|G/Z|={g['n']}\tomega={om}\ta={res['a']}\tT={T(res['omega'])}\t#maxab={res['nmax']}\t{g['extra']}\t{verdict(res)}", flush=True)
