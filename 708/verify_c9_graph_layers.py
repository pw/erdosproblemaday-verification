#!/usr/bin/env python3
"""Finite graph audit for the proposed proof that c_9 = 2.

The generic van Doorn--Li--Tang injection labels an edge by the difference of
its endpoints.  Thus a p^k-level graph is vertex-induced: an edge is present
exactly when both endpoints are divisible by p^k.

This checker verifies:
  * every 9-edge/7-active-vertex bipartite graph either contains an
    8-edge/6-vertex hard c_8 core, or is one of two explicit 3-by-4 types;
  * the advertised 4+5 edge partition repairs every positive-excess induced
    level in both types; and
  * the three 2-by-2 support blocks repair every endpoint-valuation pattern
    on K_3,3.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product


Edge = tuple[int, int]


def active_vertices(edges: set[Edge]) -> set[tuple[str, int]]:
    return ({("L", i) for i, _ in edges} | {("R", j) for _, j in edges})


def excess(edges: set[Edge]) -> int:
    return max(0, len(edges) - len(active_vertices(edges)))


def induced(edges: set[Edge], left: set[int], right: set[int]) -> set[Edge]:
    return {edge for edge in edges if edge[0] in left and edge[1] in right}


def contains_c8_core(edges: set[Edge]) -> bool:
    return any(
        len(active_vertices(set(core))) == 6 for core in combinations(edges, 8)
    )


def degrees(edges: set[Edge], side: str, count: int) -> list[int]:
    if side == "L":
        return [sum(i == vertex for i, _ in edges) for vertex in range(count)]
    return [sum(j == vertex for _, j in edges) for vertex in range(count)]


def partition_no_core_3x4(edges: set[Edge]) -> tuple[set[Edge], set[Edge], str]:
    """Construct the 4+5 partition used in the proof."""
    left_degrees = degrees(edges, "L", 3)
    right_degrees = degrees(edges, "R", 4)
    assert min(left_degrees + right_degrees) >= 2
    assert sorted(right_degrees) == [2, 2, 2, 3]

    full_column = right_degrees.index(3)
    other_columns = [j for j in range(4) if j != full_column]
    missing_rows = [
        next(i for i in range(3) if (i, column) not in edges)
        for column in other_columns
    ]
    missing_counts = Counter(missing_rows)

    if sorted(missing_counts.values()) == [1, 1, 1]:
        graph_type = "balanced"
        chosen_column = other_columns[0]
    else:
        assert sorted(missing_counts.values()) == [1, 2]
        graph_type = "unbalanced"
        once_missing_row = next(row for row, count in missing_counts.items() if count == 1)
        chosen_column = next(
            column
            for column, missing in zip(other_columns, missing_rows)
            if missing == once_missing_row
        )

    chosen_rows = [i for i in range(3) if (i, chosen_column) in edges]
    assert len(chosen_rows) == 2
    part4 = {
        (i, column)
        for i in chosen_rows
        for column in (full_column, chosen_column)
    }
    assert len(part4) == 4 and part4 <= edges
    part5 = edges - part4
    assert len(part5) == 5
    return part4, part5, graph_type


def audit_seven_vertex_graphs() -> None:
    totals = Counter()
    positive_pattern_counts = Counter()

    for left_count, right_count in ((2, 5), (3, 4)):
        complete = [
            (i, j) for i in range(left_count) for j in range(right_count)
        ]
        for chosen in combinations(complete, 9):
            edges = set(chosen)
            if len(active_vertices(edges)) != 7:
                continue

            if contains_c8_core(edges):
                totals[(left_count, right_count, "c8_core")] += 1
                continue

            assert (left_count, right_count) == (3, 4)
            part4, part5, graph_type = partition_no_core_3x4(edges)
            totals[(left_count, right_count, graph_type)] += 1

            positive = 0
            for left_mask in range(1 << left_count):
                left = {
                    i for i in range(left_count) if left_mask & (1 << i)
                }
                for right_mask in range(1 << right_count):
                    right = {
                        j for j in range(right_count) if right_mask & (1 << j)
                    }
                    level = induced(edges, left, right)
                    delta = excess(level)
                    if delta == 0:
                        continue
                    positive += 1
                    contained_parts = int(part4 <= level) + int(part5 <= level)
                    assert contained_parts >= delta
                    if delta == 2:
                        assert level == edges
                    else:
                        assert delta == 1
            positive_pattern_counts[graph_type, positive] += 1

    assert totals == Counter(
        {
            (2, 5, "c8_core"): 10,
            (3, 4, "c8_core"): 120,
            (3, 4, "unbalanced"): 72,
            (3, 4, "balanced"): 24,
        }
    )
    assert positive_pattern_counts == Counter(
        {("unbalanced", 6): 72, ("balanced", 4): 24}
    )
    print("9-edge / 7-vertex graphs:", dict(totals))
    print("positive induced-level patterns:", dict(positive_pattern_counts))


def audit_k33() -> None:
    edges = {(i, j) for i in range(3) for j in range(3)}
    blocks = [
        {(i, j) for i in range(3) for j in range(3) if i != missing and j != missing}
        for missing in range(3)
    ]
    assert all(len(block) == 4 for block in blocks)
    assert len(set.union(*blocks)) == 9
    assert all(len(blocks[i] | blocks[j]) == 7 for i in range(3) for j in range(i))

    positive_levels = Counter()
    for left_mask in range(8):
        left = {i for i in range(3) if left_mask & (1 << i)}
        for right_mask in range(8):
            right = {j for j in range(3) if right_mask & (1 << j)}
            level = induced(edges, left, right)
            delta = excess(level)
            if delta:
                positive_levels[(len(left), len(right), delta)] += 1
    assert positive_levels == Counter({(2, 3, 1): 3, (3, 2, 1): 3, (3, 3, 3): 1})

    # Endpoint valuations determine edge valuations by min(left,right).
    checked = 0
    for left_values in product(range(4), repeat=3):
        for right_values in product(range(4), repeat=3):
            edge_values = {
                (i, j): min(left_values[i], right_values[j])
                for i, j in edges
            }
            target = sum(edge_values.values())
            endpoint_supply = sum(left_values) + sum(right_values)
            repairs = [0, 0, 0]

            for level_number in range(1, 4):
                left = {i for i, value in enumerate(left_values) if value >= level_number}
                right = {j for j, value in enumerate(right_values) if value >= level_number}
                level = induced(edges, left, right)
                delta = excess(level)
                if delta == 3:
                    assert len(left) == len(right) == 3
                    for slot in range(3):
                        repairs[slot] += 1
                elif delta == 1:
                    if len(left) == 2:
                        missing = ({0, 1, 2} - left).pop()
                    else:
                        assert len(right) == 2
                        missing = ({0, 1, 2} - right).pop()
                    repairs[missing] += 1
                else:
                    assert delta == 0

            assert target <= endpoint_supply + sum(repairs)
            for slot, block in enumerate(blocks):
                assert repairs[slot] <= min(edge_values[edge] for edge in block)
            checked += 1

    assert checked == 4**6
    print("K_3,3 positive induced levels:", dict(positive_levels))
    print("K_3,3 endpoint-valuation vectors checked:", checked)


def main() -> None:
    audit_seven_vertex_graphs()
    audit_k33()
    print("ALL C9 GRAPH CHECKS PASSED")


if __name__ == "__main__":
    main()
