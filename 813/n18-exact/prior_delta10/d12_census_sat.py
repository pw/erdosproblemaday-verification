#!/usr/bin/env python3
"""Rule out a degree-12 vertex using the complete order-12 neighbourhood census."""

from __future__ import annotations

from itertools import combinations
from time import perf_counter

import networkx as nx
from pysat.solvers import Solver

from neighbourhood_census_sat import build


def main() -> None:
    path = sys.argv[1]
    with open(path, "rb") as stream:
        census = list(nx.read_graph6(stream))
    assert len(census) == 8

    _, base, pairs = build(18, 5)
    edge = {pair: index for index, pair in enumerate(pairs, 1)}

    def e(u: int, v: int) -> int:
        return edge[tuple(sorted((u, v)))]

    total_conflicts = 0
    total_started = perf_counter()
    for case, neighbourhood in enumerate(census):
        assert len(neighbourhood) == 12
        clauses = list(base)

        # Root 0 has exactly the neighbourhood {1,...,12}.
        for v in range(1, 18):
            clauses.append([e(0, v) if v <= 12 else -e(0, v)])

        # Fix the induced graph on N(0) to this census representative.
        for u, v in combinations(range(12), 2):
            literal = e(u + 1, v + 1)
            clauses.append([literal if neighbourhood.has_edge(u, v) else -literal])

        started = perf_counter()
        with Solver(name="cadical195", bootstrap_with=clauses) as solver:
            result = solver.solve()
            stats = solver.accum_stats()
        elapsed = perf_counter() - started
        conflicts = stats.get("conflicts", -1)
        total_conflicts += max(conflicts, 0)
        print(
            f"case={case} neighbourhood_edges={neighbourhood.number_of_edges()} "
            f"result={result} conflicts={conflicts} seconds={elapsed:.3f}",
            flush=True,
        )
        assert result is False

    print(
        f"VERIFIED: all 8 order-12 neighbourhood types are UNSAT; "
        f"cases=8 conflicts={total_conflicts} "
        f"seconds={perf_counter() - total_started:.3f}"
    )


if __name__ == "__main__":
    main()
