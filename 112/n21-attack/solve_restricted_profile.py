#!/usr/bin/env python3
"""Witness-first SAT search with canonical extremal root-class templates."""

from __future__ import annotations

import argparse
import json
import time

from pysat.solvers import Solver

from generate_n21_cnf import ORDER, PROFILES, build


def fix_d8(cnf, var, vertices: list[int]) -> None:
    assert len(vertices) == 8
    for i in range(8):
        for j in range(i + 1, 8):
            d = (j - i) % 8
            if d in {1, 6}:
                cnf.append([var.fwd(vertices[i], vertices[j])])
            elif (-d) % 8 in {1, 6}:
                cnf.append([var.fwd(vertices[j], vertices[i])])
            else:
                cnf.append([var.none(vertices[i], vertices[j])])


def fix_paley_t7(cnf, var, vertices: list[int]) -> None:
    assert 1 <= len(vertices) <= 7
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            d = (j - i) % 7
            if d in {1, 2, 4}:
                cnf.append([var.fwd(vertices[i], vertices[j])])
            else:
                cnf.append([var.fwd(vertices[j], vertices[i])])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", choices=["-".join(map(str, p)) for p in PROFILES])
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--fix-eight", action="store_true")
    parser.add_argument("--fix-non", action="store_true")
    args = parser.parse_args()

    profile = tuple(map(int, args.profile.split("-")))
    out_size, in_size, _ = profile
    cnf, _, var = build(profile, degree_bounds=True)
    out = list(range(1, 1 + out_size))
    inn = list(range(1 + out_size, 1 + out_size + in_size))
    non = list(range(1 + out_size + in_size, ORDER))
    if args.fix_eight:
        if len(out) == 8:
            fix_d8(cnf, var, out)
        if len(inn) == 8:
            fix_d8(cnf, var, inn)
    if args.fix_non:
        fix_paley_t7(cnf, var, non)

    started = time.perf_counter()
    with Solver(name=args.solver, bootstrap_with=cnf.clauses) as solver:
        sat = solver.solve()
        elapsed = time.perf_counter() - started
        if not sat:
            print(json.dumps({"profile": profile, "status": "UNSAT", "seconds": elapsed}))
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
                nonedges.append((u, v))
    print(json.dumps({
        "profile": profile,
        "status": "SAT",
        "seconds": elapsed,
        "arcs": arcs,
        "nonedges": nonedges,
    }, separators=(",", ":")))


if __name__ == "__main__":
    main()
