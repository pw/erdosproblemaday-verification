#!/usr/bin/env python3
"""Test whether any of the eight known cyclic order-20 witnesses extends."""

from __future__ import annotations

import json
import time

from pysat.solvers import Solver

from generate_n21_cnf import build


CONNECTION_SETS = (
    (1, 2, 4, 14, 15, 17),
    (1, 2, 6, 12, 13, 15),
    (2, 3, 5, 6, 11, 12),
    (2, 4, 5, 7, 11, 14),
    (3, 5, 6, 16, 18, 19),
    (5, 7, 8, 14, 18, 19),
    (6, 9, 13, 15, 16, 18),
    (8, 9, 14, 15, 17, 18),
)


def main() -> None:
    cnf, _, var = build(None, degree_bounds=False)
    for connection_set in CONNECTION_SETS:
        assumptions: list[int] = []
        selected = set(connection_set)
        for u in range(20):
            for v in range(u + 1, 20):
                difference = (v - u) % 20
                if difference in selected:
                    assumptions.append(var.fwd(u, v))
                elif (-difference) % 20 in selected:
                    assumptions.append(var.fwd(v, u))
                else:
                    assumptions.append(var.none(u, v))
        started = time.perf_counter()
        with Solver(name="cadical195", bootstrap_with=cnf.clauses) as solver:
            sat = solver.solve(assumptions=assumptions)
            elapsed = time.perf_counter() - started
            if sat:
                true = {x for x in solver.get_model() if x > 0}
                new_relations = []
                for u in range(20):
                    if var.fwd(u, 20) in true:
                        state = f"{u}>20"
                    elif var.fwd(20, u) in true:
                        state = f"20>{u}"
                    else:
                        state = f"{u}~20"
                    new_relations.append(state)
            else:
                new_relations = []
        print(json.dumps({
            "connection_set": connection_set,
            "status": "SAT" if sat else "UNSAT",
            "seconds": elapsed,
            "new_relations": new_relations,
        }, separators=(",", ":")))


if __name__ == "__main__":
    main()
