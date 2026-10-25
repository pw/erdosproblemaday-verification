#!/usr/bin/env python3
"""'Build one' attempt for Erdős #151 at k = 10: search circulant graphs on Z_40 (degree 8 and 9) and Z_41 (degree 8)
for a graph with alpha <= 9, Delta <= 9 and beta <= 9 (beta = largest set containing no maximal clique of size >= 2).
A hit would be a counterexample to tau(G) <= n - H(n) at n = R(3,10) (if n = R(3,10)); none is expected.
Filter order: cheap greedy independent 10-set (reject) -> exact alpha (networkx, complement cliques) -> exact beta (CP-SAT).
"""
import itertools, sys, time, random
import networkx as nx
from ortools.sat.python import cp_model

def circulant(n, S):
    G = nx.Graph(); G.add_nodes_from(range(n))
    for v in range(n):
        for s in S:
            G.add_edge(v, (v + s) % n)
    return G

def greedy_alpha_ge(G, k, tries=40):
    """Return True if a greedy search finds an independent set of size >= k."""
    nodes = list(G.nodes())
    for t in range(tries):
        random.shuffle(nodes)
        S = []; banned = set()
        for v in nodes:
            if v not in banned:
                S.append(v); banned.add(v); banned.update(G[v])
        if len(S) >= k: return True
    return False

def exact_alpha(G):
    return max(len(c) for c in nx.find_cliques(nx.complement(G)))

def exact_beta(G):
    cl = [c for c in nx.find_cliques(G) if len(c) >= 2]
    m = cp_model.CpModel(); x = {v: m.NewBoolVar(f"x{v}") for v in G.nodes()}
    for c in cl:
        m.Add(sum(x[v] for v in c) <= len(c) - 1)
    m.Maximize(sum(x.values()))
    s = cp_model.CpSolver(); s.parameters.num_search_workers = 1; s.parameters.max_time_in_seconds = 300
    r = s.Solve(m)
    if r == cp_model.OPTIMAL:
        return int(s.ObjectiveValue())
    # not proved optimal within the time limit: return (lower bound, upper bound) — a hit needs ub <= 9
    lb = int(s.ObjectiveValue()) if r == cp_model.FEASIBLE else 0
    return (lb, int(s.BestObjectiveBound()))

def main():
    random.seed(1)
    jobs = []
    # Z_40: degree 9 = four ± pairs + {20}; degree 8 = four ± pairs (no 20)
    for pairs in itertools.combinations(range(1, 20), 4):
        jobs.append((40, tuple(pairs) + tuple(40 - p for p in pairs) + (20,)))
        jobs.append((40, tuple(pairs) + tuple(40 - p for p in pairs)))
    # Z_41: degree 8 = four ± pairs
    for pairs in itertools.combinations(range(1, 21), 4):
        jobs.append((41, tuple(pairs) + tuple(41 - p for p in pairs)))
    print(f"{len(jobs)} circulants", flush=True)
    t0 = time.time(); n_alpha = 0; n_exact = 0; hits = []
    for idx, (n, S) in enumerate(jobs):
        G = circulant(n, S)
        if greedy_alpha_ge(G, 10):
            continue
        a = exact_alpha(G); n_alpha += 1
        if a >= 10:
            continue
        b = exact_beta(G); n_exact += 1
        print(f"alpha<=9 candidate: n={n} S={sorted(S)} alpha={a} beta={b} omega={max(len(c) for c in nx.find_cliques(G))}" + ("" if isinstance(b, int) else "  [NOT PROVED OPTIMAL in 300 s: (lb, ub)]"), flush=True)
        if (b if isinstance(b, int) else b[1]) <= 9:
            hits.append((n, S, a, b)); print("*** HIT ***", n, S, a, b, flush=True)
        if idx % 1000 == 0:
            print(f"[{idx}/{len(jobs)}] {time.time()-t0:.0f}s exact-alpha runs={n_alpha} beta runs={n_exact}", flush=True)
    print(f"DONE {len(jobs)} circulants in {time.time()-t0:.0f}s; exact-alpha runs={n_alpha}; beta runs={n_exact}; hits={hits}")

if __name__ == '__main__':
    main()
