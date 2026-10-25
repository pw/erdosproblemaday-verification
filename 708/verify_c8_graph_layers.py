#!/usr/bin/env python3
"""Finite audit of the two hard graph lemmas in the proposed c_8 proof.

For an edge-labelled bipartite graph, a p-adic level consists of the edges
whose labels are divisible by p^k.  Its positive edge/vertex excess is the
valuation that is not automatically supplied by the endpoint product.  The
proof partitions the eight edges into two four-edge blocks and assigns every
excess unit to one of two repair factors.  This script exhausts all 2^8 level
subgraphs and all edge-valuation vectors in {0,1,2,3}^8.
"""

from __future__ import annotations

from itertools import product


Edge = tuple[int, int]


def vertices(edges: set[Edge]) -> set[tuple[str, int]]:
    return ({("L", i) for i, _ in edges} | {("R", j) for _, j in edges})


def excess(edges: set[Edge]) -> int:
    return max(0, len(edges) - len(vertices(edges)))


def k24_assignment(
    level: set[Edge], all_edges: set[Edge], parts: tuple[set[Edge], set[Edge]]
) -> list[int]:
    delta = excess(level)
    if delta == 0:
        return []
    if delta == 2:
        assert level == all_edges
        return [0, 1]

    assert delta == 1
    complete_columns = {
        j for j in range(4) if {(0, j), (1, j)} <= level
    }
    assert len(complete_columns) == 3
    incomplete_column = ({0, 1, 2, 3} - complete_columns).pop()
    slot = 0 if incomplete_column in {0, 1} else 1
    assert parts[1 - slot] <= level
    return [slot]


def k33e_assignment(
    level: set[Edge], all_edges: set[Edge], parts: tuple[set[Edge], set[Edge]]
) -> list[int]:
    delta = excess(level)
    if delta == 0:
        return []
    if delta == 2:
        assert level == all_edges
        return [0, 1]

    assert delta == 1
    missing = all_edges - level
    special_left = {(2, 0), (2, 1)}
    special_right = {(0, 2), (1, 2)}
    if len(level) == 7:
        assert len(missing) == 1
    elif len(level) == 6:
        assert missing in (special_left, special_right)
    else:
        raise AssertionError((level, vertices(level)))

    containing_slots = [slot for slot, part in enumerate(parts) if missing <= part]
    assert len(containing_slots) == 1
    slot = containing_slots[0]
    assert parts[1 - slot] <= level
    return [slot]


def audit_graph(
    name: str,
    ordered_edges: tuple[Edge, ...],
    parts: tuple[set[Edge], set[Edge]],
    assignment,
) -> None:
    all_edges = set(ordered_edges)
    assert parts[0] | parts[1] == all_edges
    assert not (parts[0] & parts[1])
    assert len(parts[0]) == len(parts[1]) == 4

    positive_levels = 0
    for mask in range(1 << len(ordered_edges)):
        level = {
            edge for index, edge in enumerate(ordered_edges) if mask & (1 << index)
        }
        slots = assignment(level, all_edges, parts)
        assert len(slots) == excess(level)
        for slot in slots:
            assert parts[1 - slot] <= level
        positive_levels += bool(slots)

    valuation_vectors = 0
    for weights in product(range(4), repeat=len(ordered_edges)):
        repair = [0, 0]
        automatic = 0
        target = sum(weights)
        for level_number in range(1, 4):
            level = {
                edge
                for edge, weight in zip(ordered_edges, weights)
                if weight >= level_number
            }
            automatic += len(vertices(level))
            for slot in assignment(level, all_edges, parts):
                repair[slot] += 1

        assert target <= automatic + sum(repair)
        for slot in (0, 1):
            supported_part = parts[1 - slot]
            assert repair[slot] <= min(
                weights[ordered_edges.index(edge)] for edge in supported_part
            )
        valuation_vectors += 1

    print(
        f"{name}: 256 level subgraphs, {positive_levels} with positive excess, "
        f"{valuation_vectors} valuation vectors checked"
    )


def main() -> None:
    k24 = tuple((i, j) for i in range(2) for j in range(4))
    k24_parts = (
        {(i, j) for i in range(2) for j in (0, 1)},
        {(i, j) for i in range(2) for j in (2, 3)},
    )
    audit_graph("K_2,4", k24, k24_parts, k24_assignment)

    k33e = tuple(
        (i, j) for i in range(3) for j in range(3) if (i, j) != (2, 2)
    )
    k33e_parts = (
        {(2, 0), (2, 1), (0, 0), (1, 1)},
        {(0, 2), (1, 2), (0, 1), (1, 0)},
    )
    audit_graph("K_3,3-e", k33e, k33e_parts, k33e_assignment)
    print("ALL GRAPH-LAYER CHECKS PASSED")


if __name__ == "__main__":
    main()
