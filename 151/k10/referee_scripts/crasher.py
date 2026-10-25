import itertools, time
import networkx as nx
from ortools.sat.python import cp_model
def circulant(n, S):
    G = nx.Graph(); G.add_nodes_from(range(n))
    for v in range(n):
        for s in S: G.add_edge(v, (v + s) % n)
    return G
jobs = []
for pairs in itertools.combinations(range(1, 20), 4):
    jobs.append((40, tuple(pairs) + tuple(40 - p for p in pairs) + (20,)))
    jobs.append((40, tuple(pairs) + tuple(40 - p for p in pairs)))
for pairs in itertools.combinations(range(1, 21), 4):
    jobs.append((41, tuple(pairs) + tuple(41 - p for p in pairs)))
last = [1, 4, 5, 6, 20, 34, 35, 36, 39]
i0 = next(i for i, (n, S) in enumerate(jobs) if n == 40 and sorted(S) == last)
def alpha_le9(G):
    m = cp_model.CpModel(); x = [m.NewBoolVar('') for _ in G]
    for a, b in G.edges(): m.Add(x[a] + x[b] <= 1)
    m.Add(sum(x) >= 10); s = cp_model.CpSolver(); s.parameters.num_search_workers = 1
    return s.Solve(m) == cp_model.INFEASIBLE
for i in range(i0 + 1, len(jobs)):
    n, S = jobs[i]; G = circulant(n, S)
    if alpha_le9(G):
        print("job index", i0, "-> crasher candidate index", i, "of", len(jobs), "n", n, "S", sorted(S), flush=True)
        cl = [c for c in nx.find_cliques(G) if len(c) >= 2]
        print("omega", max(len(c) for c in cl), "#maximal cliques", len(cl), flush=True)
        m = cp_model.CpModel(); x = {v: m.NewBoolVar('') for v in G}
        for c in cl: m.Add(sum(x[v] for v in c) <= len(c) - 1)
        m.Maximize(sum(x.values())); s = cp_model.CpSolver(); s.parameters.num_search_workers = 4; s.parameters.max_time_in_seconds = 900
        t = time.time(); r = s.Solve(m)
        print("beta status", s.StatusName(r), "obj", s.ObjectiveValue(), "bound", s.BestObjectiveBound(), f"{time.time()-t:.0f}s", flush=True)
        break
