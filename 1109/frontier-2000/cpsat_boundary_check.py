#!/usr/bin/env python3
"""Independent CP-SAT formulations of two #1109 boundary decisions."""

from math import isqrt
from time import monotonic

from ortools.sat.python import cp_model


CASES = ((1501, 44, False), (1509, 44, True))


def squarefree(value: int) -> bool:
    return value > 0 and all(
        value % (divisor * divisor) for divisor in range(2, isqrt(value) + 1)
    )


def main():
    for new_value, target, expected in CASES:
        neighbors = [
            old for old in range(1, new_value)
            if squarefree(2 * old) and squarefree(old + new_value)
        ]
        model = cp_model.CpModel()
        selected = [model.new_bool_var(f"x_{index}") for index in range(len(neighbors))]
        nonedges = 0
        for left_index, left in enumerate(neighbors):
            for right_index in range(left_index + 1, len(neighbors)):
                if not squarefree(left + neighbors[right_index]):
                    model.add(selected[left_index] + selected[right_index] <= 1)
                    nonedges += 1
        model.add(sum(selected) >= target)

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 300
        solver.parameters.num_search_workers = 8
        solver.parameters.random_seed = 1109
        started = monotonic()
        status = solver.solve(model)
        seconds = monotonic() - started
        exists = status in (cp_model.FEASIBLE, cp_model.OPTIMAL)
        assert status != cp_model.UNKNOWN
        assert exists == expected, (new_value, solver.status_name(status))

        witness = []
        if exists:
            chosen = [
                value for value, variable in zip(neighbors, selected)
                if solver.value(variable)
            ]
            assert len(chosen) >= target
            witness = sorted(chosen[:target] + [new_value])
            assert all(
                squarefree(left + right)
                for left_index, left in enumerate(witness)
                for right in witness[left_index:]
            )

        print(
            f"n={new_value} target={target} neighbors={len(neighbors)} "
            f"nonedges={nonedges} status={solver.status_name(status)} "
            f"seconds={seconds:.3f} conflicts={solver.num_conflicts} "
            f"branches={solver.num_branches} witness={{{','.join(map(str, witness))}}}",
            flush=True,
        )
    print("CONCLUSION independent OR-Tools CP-SAT boundary decisions agree")


if __name__ == "__main__":
    main()
