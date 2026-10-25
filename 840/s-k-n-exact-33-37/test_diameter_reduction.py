#!/usr/bin/env python3
"""Small exhaustive checks of the k=9 diameter/symmetry reduction."""

from __future__ import annotations

from itertools import combinations
from math import gcd


def direct_sums(values: tuple[int, ...]) -> set[int]:
    return {a + b for a in values for b in values}


def direct_differences(values: tuple[int, ...]) -> set[int]:
    return {a - b for a in values for b in values if a > b}


def reflection_clauses(diameter: int):
    """Clauses as (positive-values, negative-values), using set membership."""
    clauses = []
    for first_gap in range(1, diameter):
        for last_gap in range(1, first_gap):
            negative = {first_gap, diameter - last_gap}
            positive = set(range(1, first_gap))
            positive.update(range(diameter - last_gap + 1, diameter))
            clauses.append((positive, negative))
    return clauses


def main() -> None:
    sum_difference_sets = 0
    scaling_sets = 0
    reflection_sets = 0

    # A sum deficit <=1 implies a positive-difference deficit <=2.  This is
    # the small exhaustive regression test for the elementary cross-pair proof.
    for n in range(1, 14):
        for size in range(1, n + 1):
            for values in combinations(range(n), size):
                if not values or values[0] != 0:
                    continue
                sum_deficit = size * (size + 1) // 2 - len(direct_sums(values))
                difference_deficit = size * (size - 1) // 2 - len(direct_differences(values))
                if sum_deficit <= 1:
                    assert difference_deficit <= 2
                sum_difference_sets += 1

                common = 0
                for value in values[1:]:
                    common = gcd(common, value)
                if common > 1:
                    scaled = tuple(value // common for value in values)
                    assert len(scaled) == len(set(scaled)) == size
                    assert len(direct_sums(scaled)) == len(direct_sums(values))
                    scaling_sets += 1

    # Check the exact CNF condition used to retain one reflected orientation.
    for diameter in range(2, 14):
        clauses = reflection_clauses(diameter)
        for size in range(2, diameter + 2):
            for middle in combinations(range(1, diameter), size - 2):
                values = {0, *middle, diameter}
                ordered = sorted(values)
                first_gap = ordered[1]
                last_gap = diameter - ordered[-2]
                satisfies = all(
                    bool(positive & values) or not negative.issubset(values)
                    for positive, negative in clauses
                )
                assert satisfies == (first_gap <= last_gap)

                reflected = {diameter - value for value in values}
                reflected_ordered = sorted(reflected)
                assert (
                    first_gap <= last_gap
                    or reflected_ordered[1] <= diameter - reflected_ordered[-2]
                )
                reflection_sets += 1

    assert sum_difference_sets == 8191
    print(f"minimum-zero sum/difference sets checked: {sum_difference_sets}")
    print(f"nonprimitive scaling checks: {scaling_sets}")
    print(f"fixed-diameter reflection-clause checks: {reflection_sets}")
    print("DIAMETER REDUCTION SELF-TEST PASSED")


if __name__ == "__main__":
    main()
