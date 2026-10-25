#!/usr/bin/env python3
"""Exact SAT computation of the Problem 80 finite frontier M_k(9).

M_k(n) is the maximum number of edges in a simple n-vertex graph in which
every edge belongs to a triangle and no edge belongs to more than k triangles.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


def build(n: int, k: int, at_least: int):
    pool = IDPool()
    edges = list(itertools.combinations(range(n), 2))
    edge_var = {e: pool.id(("e",) + e) for e in edges}
    triangles = list(itertools.combinations(range(n), 3))
    tri_var = {t: pool.id(("t",) + t) for t in triangles}
    cnf = CNF()

    incident_triangles = {e: [] for e in edges}
    for tri in triangles:
        tv = tri_var[tri]
        tri_edges = list(itertools.combinations(tri, 2))
        for e in tri_edges:
            ev = edge_var[e]
            cnf.append([-tv, ev])
            incident_triangles[e].append(tv)

    # Every selected edge has a selected (hence actual) containing triangle.
    for e, ev in edge_var.items():
        cnf.append([-ev] + incident_triangles[e])

    # Conditional codegree cap.  If uv and all two-edge paths u-w-v for a
    # (k+1)-set of w are selected, uv lies in too many triangles.
    for u, v in edges:
        others = [w for w in range(n) if w not in (u, v)]
        for ws in itertools.combinations(others, k + 1):
            clause = [-edge_var[(u, v)]]
            for w in ws:
                clause.append(-edge_var[tuple(sorted((u, w)))])
                clause.append(-edge_var[tuple(sorted((v, w)))])
            cnf.append(clause)

    card = CardEnc.atleast(
        lits=[edge_var[e] for e in edges],
        bound=at_least,
        vpool=pool,
        encoding=EncType.seqcounter,
    )
    cnf.extend(card.clauses)
    return cnf, edges, edge_var


def graph_stats(n: int, selected):
    chosen = {tuple(e) for e in selected}
    codegrees = {}
    for u, v in chosen:
        q = sum(
            tuple(sorted((u, w))) in chosen
            and tuple(sorted((v, w))) in chosen
            for w in range(n)
            if w not in (u, v)
        )
        codegrees[(u, v)] = q
    assert all(q >= 1 for q in codegrees.values())
    return max(codegrees.values(), default=0), sorted(codegrees.values())


def solve(n: int, k: int, target: int, solver_name: str):
    cnf, edges, edge_var = build(n, k, target)
    start = time.monotonic()
    with Solver(name=solver_name, bootstrap_with=cnf.clauses) as solver:
        sat = solver.solve()
        model = set(solver.get_model() or [])
        try:
            accum = solver.accum_stats()
        except NotImplementedError:
            accum = {"note": "solver does not expose counters through PySAT"}
    elapsed = time.monotonic() - start
    selected = [e for e in edges if edge_var[e] in model] if sat else []
    if sat:
        book, codegrees = graph_stats(n, selected)
        assert len(selected) >= target and book <= k
    else:
        book, codegrees = None, []
    return {
        "n": n,
        "k": k,
        "target": target,
        "sat": sat,
        "variables": cnf.nv,
        "clauses": len(cnf.clauses),
        "solver": solver_name,
        "elapsed_seconds": round(elapsed, 6),
        "solver_stats": accum,
        "edges": [list(e) for e in selected],
        "edge_count": len(selected),
        "booksize": book,
        "codegrees": codegrees,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--k", type=int)
    parser.add_argument("--target", type=int)
    args = parser.parse_args()
    # SAT witnesses at the claimed optima and UNSAT immediately above them.
    # Monotonicity makes larger targets unnecessary.
    jobs = [(args.k, args.target)] if args.k is not None else [
        (1, 18), (1, 19), (2, 21), (2, 22),
    ]
    rows = []
    for k, target in jobs:
        row = solve(9, k, target, args.solver)
        rows.append(row)
        print(json.dumps(row, sort_keys=True), flush=True)
    claims = [
        {key: row[key] for key in (
            "n", "k", "target", "sat", "edges", "edge_count", "booksize", "codegrees"
        )}
        for row in rows
    ]
    canonical = json.dumps(claims, sort_keys=True, separators=(",", ":")).encode()
    print("claims_sha256=" + hashlib.sha256(canonical).hexdigest())


if __name__ == "__main__":
    main()
