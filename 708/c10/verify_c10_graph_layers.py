#!/usr/bin/env python3
"""Finite hostile audit for the candidate proof that c_10 = 2.

This file checks only finite claims.  The written proof supplies the uniform
prime-power layer argument, interval placement, and the aligned-endpoint
reduction.

The generic two-halves injection has ten distinct edges and has the exact
valuation property

    v_p(edge label) = min(v_p(left endpoint), v_p(right endpoint)).

After nested Hall reduction, the genuinely new kernels are:

* two-critical ten-edge/eight-vertex bipartite graphs; and
* three-critical ten-edge/seven-vertex bipartite graphs.

The first family has two disjoint four-edge repair supports.  The second is
K_2,5 or one of the 54 minimal K_3,4 graphs with two deleted edges. The 12
same-column deletions contain a proper K_3,3; their valid certificates are
checked as redundant positive controls. K_2,5 has a separate order-statistic
gcd certificate, also checked below for capped endpoint valuations.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product


Edge = tuple[int, int]
Block = frozenset[Edge]


def vertices(edges: set[Edge] | frozenset[Edge]) -> set[tuple[str, int]]:
    return {("L", i) for i, _ in edges} | {("R", j) for _, j in edges}


def excess(edges: set[Edge] | frozenset[Edge]) -> int:
    return max(0, len(edges) - len(vertices(edges)))


def induced_levels(edges: set[Edge], left_count: int, right_count: int):
    levels = []
    for left_mask in range(1 << left_count):
        for right_mask in range(1 << right_count):
            level = {
                (i, j)
                for i, j in edges
                if left_mask >> i & 1 and right_mask >> j & 1
            }
            levels.append((level, excess(level)))
    return levels


def is_q_critical(
    edges: set[Edge], left_count: int, right_count: int, q: int
) -> bool:
    if len(edges) - len(vertices(edges)) != q:
        return False
    return all(
        level == edges or delta < q
        for level, delta in induced_levels(edges, left_count, right_count)
    )


def supports_levels(levels, blocks: tuple[Block, ...]) -> bool:
    return all(sum(block <= level for block in blocks) >= delta for level, delta in levels)


def find_two_blocks(edges: set[Edge], left_count: int, right_count: int):
    """Find disjoint four-edge blocks supporting every induced excess."""
    positive = [
        (level, delta)
        for level, delta in induced_levels(edges, left_count, right_count)
        if delta
    ]
    one_levels = [level for level, delta in positive if delta == 1]
    target = (1 << len(one_levels)) - 1
    candidates = []
    for chosen in combinations(sorted(edges), 4):
        block = frozenset(chosen)
        coverage = sum((block <= level) << index for index, level in enumerate(one_levels))
        candidates.append((block, coverage))

    for index, (first, first_coverage) in enumerate(candidates):
        for second, second_coverage in candidates[index + 1 :]:
            if first & second:
                continue
            if first_coverage | second_coverage != target:
                continue
            blocks = (first, second)
            if supports_levels(positive, blocks):
                return blocks
    return None


def find_three_blocks(edges: set[Edge], left_count: int, right_count: int):
    """Find three four-edge blocks with the placement unions used in the proof."""
    positive = [
        (level, delta)
        for level, delta in induced_levels(edges, left_count, right_count)
        if delta
    ]
    candidates = [frozenset(chosen) for chosen in combinations(sorted(edges), 4)]
    for first_index, first in enumerate(candidates):
        for second_index in range(first_index + 1, len(candidates)):
            second = candidates[second_index]
            if len(first | second) < 6:
                continue
            for third in candidates[second_index + 1 :]:
                if len(first | third) < 6 or len(second | third) < 6:
                    continue
                if len(first | second | third) < 9:
                    continue
                blocks = (first, second, third)
                if supports_levels(positive, blocks):
                    return blocks
    return None


def relabelled_edge_sets(edges: set[Edge], left_count: int, right_count: int):
    """All labelled copies, allowing transpose for square graphs."""
    answers = set()
    orientations = [(edges, left_count, right_count)]
    if left_count == right_count:
        orientations.append(({(j, i) for i, j in edges}, left_count, right_count))
    for oriented, left_size, right_size in orientations:
        for left_perm in permutations(range(left_size)):
            for right_perm in permutations(range(right_size)):
                answers.add(
                    frozenset((left_perm[i], right_perm[j]) for i, j in oriented)
                )
    return answers


# These are the ten isomorphism representatives printed by the exhaustive
# search.  A row string records adjacency to the right-side vertices.
TWO_CRITICAL_TABLE = {
    (3, 5): {
        ("11111", "11100", "00011"): (
            ((0, 0), (0, 1), (0, 2), (1, 0)),
            ((0, 3), (0, 4), (2, 3), (2, 4)),
        ),
        ("11110", "11101", "00011"): (
            ((0, 0), (0, 1), (0, 2), (1, 0)),
            ((0, 3), (1, 4), (2, 3), (2, 4)),
        ),
        ("11110", "11001", "00111"): (
            ((0, 0), (0, 1), (0, 2), (1, 0)),
            ((0, 3), (1, 4), (2, 3), (2, 4)),
        ),
    },
    (4, 4): {
        ("1111", "1100", "1100", "0011"): (
            ((0, 0), (0, 1), (0, 2), (0, 3)),
            ((1, 0), (1, 1), (2, 0), (2, 1)),
        ),
        ("1111", "1100", "1010", "1001"): (
            ((0, 0), (0, 1), (1, 0), (1, 1)),
            ((0, 2), (0, 3), (2, 0), (2, 2)),
        ),
        ("1111", "1100", "1010", "0101"): (
            ((0, 0), (0, 1), (0, 2), (2, 0)),
            ((0, 3), (1, 0), (1, 1), (3, 1)),
        ),
        ("1110", "1110", "1001", "0101"): (
            ((0, 0), (0, 1), (0, 2), (1, 0)),
            ((1, 1), (2, 0), (2, 3), (3, 1)),
        ),
        ("1110", "1101", "1010", "0101"): (
            ((0, 0), (0, 1), (0, 2), (1, 0)),
            ((1, 1), (1, 3), (3, 1), (3, 3)),
        ),
        ("1110", "1101", "1010", "0011"): (
            ((0, 0), (0, 1), (0, 2), (1, 0)),
            ((1, 3), (2, 0), (2, 2), (3, 2)),
        ),
        ("1110", "1101", "0011", "0011"): (
            ((0, 0), (0, 1), (0, 2), (1, 0)),
            ((1, 3), (2, 2), (2, 3), (3, 2)),
        ),
    },
}


def edges_from_rows(rows: tuple[str, ...]) -> set[Edge]:
    return {
        (i, j)
        for i, row in enumerate(rows)
        for j, character in enumerate(row)
        if character == "1"
    }


def audit_two_critical_graphs():
    counts = Counter()
    class_counts = {}
    representative_certificates = []

    for dimensions in ((3, 5), (4, 4)):
        left_count, right_count = dimensions
        table_orbits = set()
        separate_orbits = []
        for rows in TWO_CRITICAL_TABLE[dimensions]:
            orbit = relabelled_edge_sets(
                edges_from_rows(rows), left_count, right_count
            )
            assert all(not (orbit & old_orbit) for old_orbit in separate_orbits)
            separate_orbits.append(orbit)
            table_orbits.update(orbit)
        complete = [
            (i, j) for i in range(left_count) for j in range(right_count)
        ]
        for chosen in combinations(complete, 10):
            edges = set(chosen)
            if len(vertices(edges)) != 8:
                continue
            if not is_q_critical(edges, left_count, right_count, 2):
                continue
            counts[dimensions] += 1
            assert frozenset(edges) in table_orbits
        class_counts[dimensions] = len(TWO_CRITICAL_TABLE[dimensions])

        for rows, raw_blocks in TWO_CRITICAL_TABLE[dimensions].items():
            edges = edges_from_rows(rows)
            blocks = tuple(frozenset(block) for block in raw_blocks)
            assert is_q_critical(edges, left_count, right_count, 2)
            assert not (blocks[0] & blocks[1])
            assert supports_levels(
                induced_levels(edges, left_count, right_count), blocks
            )
            representative_certificates.append(
                (dimensions, rows, tuple(sorted(edges)), blocks)
            )

    assert counts == Counter({(3, 5): 210, (4, 4): 2040})
    assert class_counts == {
        (3, 5): 3,
        (4, 4): 7,
    }
    return counts, class_counts, representative_certificates


THREE_CRITICAL_REPRESENTATIVES = {
    # The two missing edges share a row.
    "same_row": (
        {(0, 0), (0, 1)},
        (
            ((0, 2), (0, 3), (1, 2), (1, 3)),
            ((1, 0), (1, 1), (2, 0), (2, 1)),
            ((1, 2), (1, 3), (2, 2), (2, 3)),
        ),
    ),
    # The two missing edges are disjoint.
    "disjoint": (
        {(0, 0), (1, 1)},
        (
            ((0, 1), (0, 2), (1, 2), (2, 1)),
            ((0, 2), (0, 3), (2, 2), (2, 3)),
            ((1, 0), (1, 3), (2, 0), (2, 3)),
        ),
    ),
    # This type contains a K_3,3 core, but the direct certificate also works.
    "same_column": (
        {(0, 0), (1, 0)},
        (
            ((0, 1), (0, 2), (1, 1), (1, 2)),
            ((0, 1), (0, 3), (2, 1), (2, 3)),
            ((1, 2), (1, 3), (2, 2), (2, 3)),
        ),
    ),
}


def audit_three_deletion_patterns():
    complete = {(i, j) for i in range(3) for j in range(4)}
    counts = Counter()
    critical_counts = Counter()
    for missing in combinations(sorted(complete), 2):
        if missing[0][0] == missing[1][0]:
            kind = "same_row"
        elif missing[0][1] == missing[1][1]:
            kind = "same_column"
        else:
            kind = "disjoint"
        counts[kind] += 1
        edges = complete - set(missing)
        if is_q_critical(edges, 3, 4, 3):
            critical_counts[kind] += 1

    assert counts == Counter({"disjoint": 36, "same_row": 18, "same_column": 12})
    assert critical_counts == Counter({"disjoint": 36, "same_row": 18})
    for name, (missing, raw_blocks) in THREE_CRITICAL_REPRESENTATIVES.items():
        edges = complete - missing
        blocks = tuple(frozenset(block) for block in raw_blocks)
        assert supports_levels(induced_levels(edges, 3, 4), blocks), name
        assert all(len(blocks[i] | blocks[j]) >= 6 for i in range(3) for j in range(i))
        assert len(set.union(*(set(block) for block in blocks))) >= 9
    return counts, critical_counts


def assign_repairs(edges: tuple[Edge, ...], blocks: tuple[Block, ...], values):
    """Run the uniform layer assignment for one endpoint-valuation vector."""
    left_values, right_values = values
    edge_values = {
        (i, j): min(left_values[i], right_values[j]) for i, j in edges
    }
    repairs = [0] * len(blocks)
    for level_number in range(1, max(left_values + right_values, default=0) + 1):
        level = {
            edge for edge, value in edge_values.items() if value >= level_number
        }
        delta = excess(level)
        available = [index for index, block in enumerate(blocks) if block <= level]
        assert len(available) >= delta
        for index in available[:delta]:
            repairs[index] += 1

    target = sum(edge_values.values())
    endpoint_supply = sum(left_values) + sum(right_values)
    assert target <= endpoint_supply + sum(repairs)
    for index, block in enumerate(blocks):
        assert repairs[index] <= min(edge_values[edge] for edge in block)


def audit_capped_valuations(representative_certificates, cap=3):
    checked = Counter()
    for dimensions, rows, ordered_edges, blocks in representative_certificates:
        left_count, right_count = dimensions
        for vector in product(range(cap + 1), repeat=left_count + right_count):
            assign_repairs(
                ordered_edges,
                blocks,
                (vector[:left_count], vector[left_count:]),
            )
            checked[dimensions] += 1

    complete34 = {(i, j) for i in range(3) for j in range(4)}
    for name, (missing, raw_blocks) in THREE_CRITICAL_REPRESENTATIVES.items():
        edges = tuple(sorted(complete34 - missing))
        blocks = tuple(frozenset(block) for block in raw_blocks)
        for vector in product(range(cap + 1), repeat=7):
            assign_repairs(edges, blocks, (vector[:3], vector[3:]))
            checked[name] += 1

    # The inherited K_3,3 three-block certificate.
    edges33 = tuple((i, j) for i in range(3) for j in range(3))
    blocks33 = tuple(
        frozenset(
            (i, j)
            for i in range(3)
            for j in range(3)
            if i != missing and j != missing
        )
        for missing in range(3)
    )
    for vector in product(range(cap + 1), repeat=6):
        assign_repairs(edges33, blocks33, (vector[:3], vector[3:]))
        checked["K33"] += 1

    expected = {
        (3, 5): 3 * (cap + 1) ** 8,
        (4, 4): 7 * (cap + 1) ** 8,
        "same_row": (cap + 1) ** 7,
        "same_column": (cap + 1) ** 7,
        "disjoint": (cap + 1) ** 7,
        "K33": (cap + 1) ** 6,
    }
    assert checked == Counter(expected)
    return checked


def audit_k25_order_statistic(cap=5):
    """Check the q_j triple-product residual formula on K_2,5."""
    checked = 0
    for vector in product(range(cap + 1), repeat=7):
        left = vector[:2]
        right = vector[2:]
        edge_values = [min(left[i], right[j]) for i in range(2) for j in range(5)]
        q_values = [min(left[0], left[1], right[j]) for j in range(5)]
        triple_gcd_value = sum(sorted(q_values)[:3])
        layer_repair = sum(
            max(0, sum(value >= level for value in q_values) - 2)
            for level in range(1, max(q_values, default=0) + 1)
        )
        assert layer_repair == triple_gcd_value
        assert sum(edge_values) <= sum(vector) + triple_gcd_value
        checked += 1
    assert checked == (cap + 1) ** 7
    return checked


def interval_multiples(d: int, doubled_left: int, maximum: int) -> set[int]:
    return {
        value
        for value in range(1, (doubled_left + 4 * maximum) // 2 + 2)
        if doubled_left < 2 * value < doubled_left + 4 * maximum and value % d == 0
    }


def audit_nine_point_progression_lemma(maximum_limit=80):
    """Finite phase stress test of the strengthened AP-overlap lemma."""
    checked_pairs = 0
    for maximum in range(4, maximum_limit + 1):
        for doubled_left in range(4 * maximum):
            sets = {
                d: interval_multiples(d, doubled_left, maximum)
                for d in range(1, maximum // 4 + 1)
            }
            candidates = [d for d, points in sets.items() if len(points) >= 7]
            for first_index, first in enumerate(candidates):
                for second in candidates[first_index + 1 :]:
                    checked_pairs += 1
                    assert len(sets[first] | sets[second]) >= 10
    return checked_pairs


def main():
    two_counts, class_counts, representatives = audit_two_critical_graphs()
    three_counts, three_critical = audit_three_deletion_patterns()
    valuations = audit_capped_valuations(representatives)
    k25 = audit_k25_order_statistic()
    progression_pairs = audit_nine_point_progression_lemma()
    print("two-critical labelled graphs:", dict(two_counts))
    print("two-critical isomorphism classes:", class_counts)
    print("K_3,4 minus two edges:", dict(three_counts))
    print("minimal three-critical patterns:", dict(three_critical))
    print("capped endpoint valuations:", dict(valuations))
    print("K_2,5 order-statistic valuations:", k25)
    print("distinct progression pairs stress-tested:", progression_pairs)
    print("ALL C10 GRAPH/VALUATION CHECKS PASSED")


if __name__ == "__main__":
    main()
