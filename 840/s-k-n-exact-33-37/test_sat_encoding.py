#!/usr/bin/env python3
"""Exhaustively compare the #840 SAT encoding with the definition for n<=8."""

from __future__ import annotations

from itertools import combinations
from pysat.solvers import Solver

import sat_audit


def main() -> None:
    instances = 0
    for n in range(1, 9):
        for k in range(1, n + 1):
            direct = max(
                sat_audit.direct_score(values)
                for values in combinations(range(n), k)
                if values[0] == 0
            )
            for target in range(max(0, direct - 1), min(2 * n - 1, direct + 1) + 1):
                _variables, clauses = sat_audit.make_cnf(n, k, target)
                if tuple() in clauses:
                    encoded = False
                else:
                    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
                        encoded = solver.solve()
                expected = direct >= target
                assert encoded == expected, (n, k, target, direct, encoded, expected)
                instances += 1
    print(f"minimum-zero definition/CNF instances checked: {instances}")
    print("SAT ENCODING SELF-TEST PASSED")


if __name__ == "__main__":
    main()
