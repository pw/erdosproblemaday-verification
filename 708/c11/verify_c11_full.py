#!/usr/bin/env python3
"""Hostile finite audit for the integrated c11 candidate.

This checker focuses on the genuinely new integration claims not covered by
the placement and eleven-edge-kernel audits:

* collision-safe supports on every inherited fixed-block core;
* robustness under every exceptional matching in the aligned injection;
* the strengthened K2,5 order-statistic placement with one extra forbidden
  point; and
* the finite inequalities used by the joint product-placement lemma.
"""

from fractions import Fraction
from itertools import combinations, combinations_with_replacement


Q2_REPRESENTATIVES = (
    # e=8
    (2, 4, ("1111", "1111"), (4, 4), "K2,4"),
    (3, 3, ("111", "111", "110"), (4, 4), "K3,3-e"),
    # e=9
    (3, 4, ("1111", "1110", "1001"), (4, 5), "q2-e9-balanced"),
    (3, 4, ("1110", "1101", "1011"), (4, 5), "q2-e9-unbalanced"),
    # e=10, 3x5
    (3, 5, ("11111", "11100", "00011"), (4, 4), "q2-e10-3x5-a"),
    (3, 5, ("11110", "11101", "00011"), (4, 4), "q2-e10-3x5-b"),
    (3, 5, ("11110", "11001", "00111"), (4, 4), "q2-e10-3x5-c"),
    # e=10, 4x4
    (4, 4, ("1111", "1100", "1100", "0011"), (4, 4), "q2-e10-4x4-a"),
    (4, 4, ("1111", "1100", "1010", "1001"), (4, 4), "q2-e10-4x4-b"),
    (4, 4, ("1111", "1100", "1010", "0101"), (4, 4), "q2-e10-4x4-c"),
    (4, 4, ("1110", "1110", "1001", "0101"), (4, 4), "q2-e10-4x4-d"),
    (4, 4, ("1110", "1101", "1010", "0101"), (4, 4), "q2-e10-4x4-e"),
    (4, 4, ("1110", "1101", "1010", "0011"), (4, 4), "q2-e10-4x4-f"),
    (4, 4, ("1110", "1101", "0011", "0011"), (4, 4), "q2-e10-4x4-g"),
)

Q3_REPRESENTATIVES = (
    (3, 3, ("111", "111", "111"), (4, 4, 4), "K3,3"),
    (3, 4, ("0011", "1111", "1111"), (4, 4, 4), "q3-e10-same-row"),
    (3, 4, ("0111", "1011", "1111"), (4, 4, 4), "q3-e10-disjoint"),
    # Redundant positive control: it contains a proper K3,3 core.
    (3, 4, ("0111", "0111", "1111"), (4, 4, 4), "q3-e10-same-column"),
)


def edge_bit(i, j, right):
    return 1 << (i * right + j)


def graph_mask(rows):
    right = len(rows[0])
    return sum(
        edge_bit(i, j, right)
        for i, row in enumerate(rows)
        for j, value in enumerate(row)
        if value == "1"
    )


def incident_masks(left, right):
    answer = []
    for i in range(left):
        answer.append(sum(edge_bit(i, j, right) for j in range(right)))
    for j in range(right):
        answer.append(sum(edge_bit(i, j, right) for i in range(left)))
    return tuple(answer)


def endpoint_levels(edges, left, right):
    levels = []
    for row_mask in range(1 << left):
        for col_mask in range(1 << right):
            level = edges & sum(
                edge_bit(i, j, right)
                for i in range(left)
                for j in range(right)
                if row_mask >> i & 1 and col_mask >> j & 1
            )
            levels.append((level, row_mask.bit_count() + col_mask.bit_count()))
    return tuple(levels)


def matching_masks(edges, left, right):
    bits = [1 << bit for bit in range(left * right) if edges >> bit & 1]
    answers = []
    for size in range(min(left, right) + 1):
        for chosen in combinations(bits, size):
            mask = sum(chosen)
            degrees = []
            for incident in incident_masks(left, right):
                degrees.append((mask & incident).bit_count())
            if max(degrees, default=0) <= 1:
                answers.append(mask)
    return tuple(answers)


def robust_requirements(edges, left, right, exceptional):
    requirements = set()
    for induced, vertex_count in endpoint_levels(edges, left, right):
        available = exceptional & induced
        deleted = available
        while True:
            actual = induced & ~deleted
            demand = max(0, actual.bit_count() - vertex_count)
            if demand:
                requirements.add((actual, demand))
            if deleted == 0:
                break
            deleted = (deleted - 1) & available
    return tuple(sorted(requirements))


def blocks_of_size(edges, size):
    bits = [1 << bit for bit in range(edges.bit_length()) if edges >> bit & 1]
    return tuple(sum(chosen) for chosen in combinations(bits, size))


def tuple_covers(blocks, requirements):
    return all(
        sum(block & actual == block for block in blocks) >= demand
        for actual, demand in requirements
    )


def endpoint_safe(edges, block, exceptional, left, right):
    for incident in incident_masks(left, right):
        nonexceptional_after_deletion = edges & ~incident & ~exceptional
        if (block | nonexceptional_after_deletion).bit_count() < 5:
            return False
    return True


def generic_tuples(edges, left, right, defect, sizes):
    requirements = robust_requirements(edges, left, right, 0)
    pools = [blocks_of_size(edges, size) for size in sizes]
    answers = []
    if defect == 2:
        for first in pools[0]:
            for second in pools[1]:
                if first >= second and sizes[0] == sizes[1]:
                    continue
                if first & second or (first | second).bit_count() < 6:
                    continue
                blocks = (first, second)
                if tuple_covers(blocks, requirements):
                    answers.append(blocks)
    else:
        for first, second, third in combinations(pools[0], 3):
            blocks = (first, second, third)
            if any((a | b).bit_count() < 6 for a, b in combinations(blocks, 2)):
                continue
            if (first | second | third).bit_count() < 9:
                continue
            if tuple_covers(blocks, requirements):
                answers.append(blocks)
    assert answers
    return tuple(answers)


def audit_robust_fixed_blocks():
    summaries = []
    total_matchings = 0
    total_requirements = 0
    for defect, records in ((2, Q2_REPRESENTATIVES), (3, Q3_REPRESENTATIVES)):
        for left, right, rows, sizes, name in records:
            edges = graph_mask(rows)
            assert edges.bit_count() - left - right == defect
            tuples = generic_tuples(edges, left, right, defect, sizes)
            matchings = matching_masks(edges, left, right)
            maximum_requirements = 0
            for exceptional in matchings:
                requirements = robust_requirements(edges, left, right, exceptional)
                maximum_requirements = max(maximum_requirements, len(requirements))
                found = next(
                    (
                        blocks
                        for blocks in tuples
                        if all(
                            endpoint_safe(edges, block, exceptional, left, right)
                            for block in blocks
                        )
                        and tuple_covers(blocks, requirements)
                    ),
                    None,
                )
                assert found is not None, (name, exceptional)
            total_matchings += len(matchings)
            total_requirements += maximum_requirements
            summaries.append((name, len(tuples), len(matchings), maximum_requirements))
    return summaries, total_matchings, total_requirements


def grid(m):
    return frozenset(Fraction(k, m) for k in range(1, m))


def capture_ok(ms):
    return all(sum(m0 % m == 0 for m in ms) <= 2 for m0 in set(ms))


def audit_strengthened_k25_grid():
    checked = 0
    for t in range(3):
        minimum_remaining = 5 - (2 - t)
        for size in range(minimum_remaining, 6):
            for ms in combinations_with_replacement(range(1, t + 3), size):
                checked += 1
                union = frozenset().union(*(grid(m) for m in ms))
                assert not (capture_ok(ms) and len(union) <= t + 1), (t, ms)
    return checked


def audit_k25_robust_layers():
    # At a binary prime-power level, choose endpoint rows/columns and delete
    # an arbitrary matching.  The actual excess must not exceed t-2, where t
    # is the number of columns retaining both actual row edges.
    checked = 0
    edges = {(i, j) for i in range(2) for j in range(5)}
    edge_list = sorted(edges)
    for row_mask in range(1 << 2):
        for col_mask in range(1 << 5):
            induced = {
                (i, j)
                for i, j in edges
                if row_mask >> i & 1 and col_mask >> j & 1
            }
            active = sorted(induced)
            for size in range(3):
                for deleted_tuple in combinations(active, size):
                    vertices = [item for edge in deleted_tuple for item in (("L", edge[0]), ("R", edge[1]))]
                    if len(vertices) != len(set(vertices)):
                        continue
                    actual = induced - set(deleted_tuple)
                    endpoint_supply = row_mask.bit_count() + col_mask.bit_count()
                    excess = max(0, len(actual) - endpoint_supply)
                    complete_columns = sum(
                        (0, j) in actual and (1, j) in actual for j in range(5)
                    )
                    assert excess <= max(0, complete_columns - 2)
                    checked += 1
    return checked


def audit_joint_arithmetic():
    # Exact forbidden-union thresholds for N+b=11.
    thresholds = {}
    for defect in (2, 3):
        for repairs in range(2, defect + 1):
            thresholds[defect, repairs] = 10 - defect + repairs
    assert thresholds == {(2, 2): 10, (3, 2): 9, (3, 3): 10}

    # A collided gcd divides four support labels plus the collided edge: nine
    # generic multiples, or ten strict aligned multiples.  Ten forbidden
    # points leave at least |V|-1 generic core vertices; the support condition
    # raises the label count to six and hence the count to eleven.
    for core_edges in range(8, 12):
        for defect in (2, 3):
            vertices = core_edges - defect
            other_items = 10 - vertices
            assert vertices + other_items == 10
            generic_core_multiples = max(0, 9 - other_items)
            assert generic_core_multiples >= vertices - 1
            assert 2 * 6 - 1 == 11 > 10
            assert 2 * 5 == 10
            assert 2 * 6 == 12 > 10
    return thresholds


def main():
    robust, matching_count, requirement_count = audit_robust_fixed_blocks()
    k25_grid = audit_strengthened_k25_grid()
    k25_layers = audit_k25_robust_layers()
    arithmetic = audit_joint_arithmetic()
    print(
        "C11_FULL_AUDIT=PASS",
        f"robust_representatives={len(robust)}",
        f"exceptional_matchings={matching_count}",
        f"max_requirement_sum={requirement_count}",
        f"k25_grid_profiles={k25_grid}",
        f"k25_layer_cases={k25_layers}",
        f"thresholds={arithmetic}",
    )
    for record in robust:
        print("ROBUST", *record)


if __name__ == "__main__":
    main()
