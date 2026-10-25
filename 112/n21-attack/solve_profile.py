#!/usr/bin/env python3
"""Solve one canonical N=21 profile and print a compact witness if SAT."""

from __future__ import annotations

import argparse
import json
import time

from pysat.solvers import Solver

from generate_n21_cnf import ORDER, PROFILES, build


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", choices=["-".join(map(str, p)) for p in PROFILES])
    parser.add_argument("--solver", default="kissat404")
    parser.add_argument("--no-degree-bounds", action="store_true")
    args = parser.parse_args()
    profile = tuple(map(int, args.profile.split("-")))
    cnf, pool, var = build(profile, degree_bounds=not args.no_degree_bounds)
    started = time.perf_counter()
    with Solver(name=args.solver, bootstrap_with=cnf.clauses) as solver:
        sat = solver.solve()
        elapsed = time.perf_counter() - started
        stats = solver.accum_stats()
        if not sat:
            print(json.dumps({"profile": profile, "status": "UNSAT", "seconds": elapsed, "stats": stats}))
            return
        true = {literal for literal in solver.get_model() if literal > 0}
    arcs = []
    nonedges = []
    for u in range(ORDER):
        for v in range(u + 1, ORDER):
            if var.fwd(u, v) in true:
                arcs.append((u, v))
            elif var.fwd(v, u) in true:
                arcs.append((v, u))
            else:
                assert var.none(u, v) in true
                nonedges.append((u, v))
    print(json.dumps({
        "profile": profile,
        "status": "SAT",
        "seconds": elapsed,
        "stats": stats,
        "arcs": arcs,
        "nonedges": nonedges,
    }, separators=(",", ":")))


if __name__ == "__main__":
    main()
