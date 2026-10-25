#!/usr/bin/env python3
"""Seek an N=21 witness near one of the cyclic N=20 witnesses."""

from __future__ import annotations

import argparse
import json
import time

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

from generate_n21_cnf import ORDER, build
from test_d20_extensions import CONNECTION_SETS


def state_literal(var, selected: set[int], u: int, v: int) -> int:
    difference = (v - u) % 20
    if difference in selected:
        return var.fwd(u, v)
    if (-difference) % 20 in selected:
        return var.fwd(v, u)
    return var.none(u, v)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-changes", type=int, default=1)
    parser.add_argument("--max-changes", type=int, default=20)
    parser.add_argument("--solver", default="cadical195")
    args = parser.parse_args()

    base, pool, var = build(None, degree_bounds=True)
    for change_bound in range(args.min_changes, args.max_changes + 1):
        for connection_set in CONNECTION_SETS[:4]:  # the other four are reversals
            selected = set(connection_set)
            unchanged = [
                state_literal(var, selected, u, v)
                for u in range(20)
                for v in range(u + 1, 20)
            ]
            extra = CardEnc.atmost(
                lits=[-literal for literal in unchanged],
                bound=change_bound,
                vpool=pool,
                encoding=EncType.seqcounter,
            ).clauses
            started = time.perf_counter()
            with Solver(name=args.solver, bootstrap_with=base.clauses + extra) as solver:
                sat = solver.solve()
                elapsed = time.perf_counter() - started
                print(
                    f"k={change_bound} C={connection_set} "
                    f"status={'SAT' if sat else 'UNSAT'} seconds={elapsed:.3f}",
                    flush=True,
                )
                if not sat:
                    continue
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
                "status": "SAT",
                "change_bound": change_bound,
                "connection_set": connection_set,
                "arcs": arcs,
                "nonedges": nonedges,
            }, separators=(",", ":")))
            return

    print("NO WITNESS WITHIN REQUESTED CHANGE BOUND")


if __name__ == "__main__":
    main()
