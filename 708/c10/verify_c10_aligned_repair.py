#!/usr/bin/env python3
"""Independent finite audit for the repaired aligned case of c_10 = 2.

This script does not import the frozen c_10 checker.  It checks:

* the exact gcd/2-adic description of the corrected aligned injection;
* every nine-edge/seven-vertex no-core graph, every possible exceptional
  matching, every endpoint-induced level, and every subset deleted at its
  surplus two-adic level;
* every exceptional matching and robust block choice on K_3,3;
* the nonexceptional-edge facts used in the forbidden-midpoint placement; and
* the strict open-interval multiple count for small scales and all aligned
  phases tested.

The graph checks are exhaustive.  The arithmetic loops are stress tests; the
written proof establishes their formulas uniformly.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations
from math import gcd


Edge = tuple[int, int]
Block = frozenset[Edge]


def active_vertices(edges: set[Edge] | frozenset[Edge]):
    return {("L", i) for i, _ in edges} | {("R", j) for _, j in edges}


def active_excess(edges: set[Edge] | frozenset[Edge]) -> int:
    return max(0, len(edges) - len(active_vertices(edges)))


def induced(edges: set[Edge], left_mask: int, right_mask: int) -> set[Edge]:
    return {
        (i, j)
        for i, j in edges
        if left_mask >> i & 1 and right_mask >> j & 1
    }


def is_matching(edges: set[Edge] | tuple[Edge, ...]) -> bool:
    return (
        len({i for i, _ in edges}) == len(edges)
        and len({j for _, j in edges}) == len(edges)
    )


def all_matchings(edges: set[Edge], maximum_size: int):
    ordered = sorted(edges)
    for size in range(maximum_size + 1):
        for chosen in combinations(ordered, size):
            if is_matching(chosen):
                yield frozenset(chosen)


def contains_eight_edge_six_vertex_core(edges: set[Edge]) -> bool:
    return any(
        len(active_vertices(set(core))) == 6
        for core in combinations(sorted(edges), 8)
    )


def find_standard_four_five_certificate(
    edges: set[Edge], left_count: int, right_count: int
) -> tuple[Block, Block] | None:
    """Discover a c_9 certificate without using either supplied table."""
    levels = []
    for left_mask in range(1 << left_count):
        for right_mask in range(1 << right_count):
            level = induced(edges, left_mask, right_mask)
            levels.append((level, active_excess(level)))

    for chosen in combinations(sorted(edges), 4):
        first = frozenset(chosen)
        second = frozenset(edges - first)
        if all(
            int(first <= level) + int(second <= level) >= delta
            for level, delta in levels
        ):
            return first, second
    return None


def robust_for_exceptional_matching(
    edges: set[Edge],
    left_count: int,
    right_count: int,
    blocks: tuple[Block, ...],
    exceptional: Block,
) -> bool:
    """Check all endpoint levels and all same-level exceptional deletions."""
    exceptional_order = sorted(exceptional)
    for left_mask in range(1 << left_count):
        for right_mask in range(1 << right_count):
            endpoint_level = induced(edges, left_mask, right_mask)
            endpoint_supply = left_mask.bit_count() + right_mask.bit_count()
            for deleted_mask in range(1 << len(exceptional_order)):
                deleted = {
                    edge
                    for index, edge in enumerate(exceptional_order)
                    if deleted_mask >> index & 1
                }
                if not deleted <= endpoint_level:
                    continue
                label_level = endpoint_level - deleted
                missing = max(0, len(label_level) - endpoint_supply)
                available = sum(block <= label_level for block in blocks)
                if available < missing:
                    return False
    return True


def audit_no_core_graphs():
    graph_count = 0
    graph_matching_pairs = 0
    matching_sizes = Counter()

    for left_count, right_count in ((2, 5), (3, 4)):
        complete = [
            (i, j)
            for i in range(left_count)
            for j in range(right_count)
        ]
        for chosen in combinations(complete, 9):
            edges = set(chosen)
            if len(active_vertices(edges)) != 7:
                continue
            if contains_eight_edge_six_vertex_core(edges):
                continue

            certificate = find_standard_four_five_certificate(
                edges, left_count, right_count
            )
            assert certificate is not None
            first, second = certificate
            assert len(first) == 4 and len(second) == 5
            assert not first & second and first | second == edges
            graph_count += 1

            for exceptional in all_matchings(edges, 3):
                assert robust_for_exceptional_matching(
                    edges,
                    left_count,
                    right_count,
                    certificate,
                    exceptional,
                )
                # If every graph vertex is divisible by the four-block factor,
                # its five-edge complement has an exact edge outside X.
                assert second - exceptional
                graph_matching_pairs += 1
                matching_sizes[len(exceptional)] += 1

    assert graph_count == 96
    assert graph_matching_pairs == 3888
    return graph_count, graph_matching_pairs, matching_sizes


def disjoint_pairing(exceptional: Block):
    for pairing in permutations(range(3)):
        paired_edges = {(i, pairing[i]) for i in range(3)}
        if not paired_edges & exceptional:
            return pairing
    return None


def audit_k33():
    edges = {(i, j) for i in range(3) for j in range(3)}
    checked = 0
    sizes = Counter()

    for exceptional in all_matchings(edges, 3):
        pairing = disjoint_pairing(exceptional)
        assert pairing is not None
        blocks = tuple(
            frozenset(
                (row, column)
                for row, column in edges
                if row != index and column != pairing[index]
            )
            for index in range(3)
        )
        assert all(len(block) == 4 for block in blocks)
        assert all(
            len(blocks[i] | blocks[j]) == 7
            for i, j in combinations(range(3), 2)
        )
        assert len(set().union(*blocks)) == 9

        # Every exceptional edge is off the pairing and lies in exactly one
        # block, which is the full-level robustness mechanism.
        assert all(sum(edge in block for block in blocks) == 1 for edge in exceptional)
        assert robust_for_exceptional_matching(
            edges, 3, 3, blocks, exceptional
        )
        checked += 1
        sizes[len(exceptional)] += 1

    assert checked == 34
    assert sizes == Counter({2: 18, 1: 9, 3: 6, 0: 1})
    return checked, sizes


def audit_hard_core_placement():
    cases = 0
    graphs = (
        (
            {(i, j) for i in range(2) for j in range(4)},
            (
                frozenset((i, j) for i in range(2) for j in (0, 1)),
                frozenset((i, j) for i in range(2) for j in (2, 3)),
            ),
        ),
        (
            {(i, j) for i in range(3) for j in range(3)} - {(2, 2)},
            (
                frozenset({(2, 0), (2, 1), (0, 0), (1, 1)}),
                frozenset({(0, 2), (1, 2), (0, 1), (1, 0)}),
            ),
        ),
    )

    for edges, blocks in graphs:
        assert not blocks[0] & blocks[1]
        assert blocks[0] | blocks[1] == edges
        for exceptional in all_matchings(edges, 3):
            for supported in blocks:
                complement = edges - supported
                assert complement - exceptional
                cases += 1
    return cases


def corrected_pair(maximum: int, multiplier: int, label: int):
    x = multiplier * maximum
    midpoint = x + maximum
    if midpoint % label:
        left = (midpoint // label) * label
        right = left + label
        edge_type = 1
    elif 2 * label < maximum and midpoint % (2 * label):
        left = midpoint - 2 * label
        right = midpoint + 2 * label
        edge_type = 2
    else:
        left = midpoint - label
        right = midpoint + label
        edge_type = 3
    exceptional = (
        edge_type == 3
        and midpoint % label == 0
        and (midpoint // label) % 2 == 1
    )
    return left, right, edge_type, exceptional


def audit_corrected_injection(maximum_limit: int = 100, multiplier_limit: int = 50):
    graph_cases = 0
    label_cases = 0
    exceptional_cases = 0

    for maximum in range(2, maximum_limit + 1):
        for multiplier in range(multiplier_limit + 1):
            x = multiplier * maximum
            midpoint = x + maximum
            pairs = {}
            exceptional_edges = []
            for label in range(1, maximum):
                left, right, edge_type, exceptional = corrected_pair(
                    maximum, multiplier, label
                )
                assert x < left < midpoint < right < x + 2 * maximum
                assert left != midpoint != right
                assert left % label == right % label == 0
                assert (left, right) not in pairs
                pairs[left, right] = label

                common_ratio = gcd(left, right) // label
                assert common_ratio == (2 if exceptional else 1)
                if exceptional:
                    assert edge_type == 3
                    assert 2 * label > maximum
                    exceptional_edges.append((left, right))
                    exceptional_cases += 1
                label_cases += 1

            assert len(pairs) == maximum - 1
            assert len({left for left, _ in exceptional_edges}) == len(exceptional_edges)
            assert len({right for _, right in exceptional_edges}) == len(exceptional_edges)
            graph_cases += 1

    assert graph_cases == (maximum_limit - 1) * (multiplier_limit + 1)
    return graph_cases, label_cases, exceptional_cases


def open_interval_multiple_count(maximum: int, multiplier: int, divisor: int) -> int:
    left = multiplier * maximum
    right = left + 2 * maximum
    return (right - 1) // divisor - left // divisor


def audit_strict_multiple_count(maximum_limit: int = 200, multiplier_limit: int = 50):
    checked = 0
    for maximum in range(10, maximum_limit + 1):
        for label_count in range(1, 10):
            for divisor in range(1, (maximum - 1) // label_count + 1):
                for multiplier in range(multiplier_limit + 1):
                    assert (
                        open_interval_multiple_count(maximum, multiplier, divisor)
                        >= 2 * label_count
                    )
                    checked += 1
    return checked


def main():
    graph_count, robust_pairs, no_core_sizes = audit_no_core_graphs()
    k33_count, k33_sizes = audit_k33()
    hard_cases = audit_hard_core_placement()
    injection = audit_corrected_injection()
    strict_counts = audit_strict_multiple_count()

    print("no-core nine-edge graphs:", graph_count)
    print("no-core graph/exceptional-matching pairs:", robust_pairs)
    print("no-core exceptional matching sizes:", dict(no_core_sizes))
    print("K_3,3 exceptional matchings:", k33_count, dict(k33_sizes))
    print("hard-core nonexceptional-complement checks:", hard_cases)
    print("corrected injection graph/label/exceptional cases:", injection)
    print("strict aligned multiple counts checked:", strict_counts)
    print("ALL ALIGNED-REPAIR CHECKS PASSED")


if __name__ == "__main__":
    main()
