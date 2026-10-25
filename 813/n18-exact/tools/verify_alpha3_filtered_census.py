#!/usr/bin/env python3
"""Verify that a census is exactly the alpha<=3 sublist of a base census."""

from __future__ import annotations

import argparse
from itertools import combinations


def decode_graph6(line: bytes) -> tuple[int, set[tuple[int, int]]]:
    line = line.strip()
    assert line and line[0] != 126
    order = line[0] - 63
    assert 0 <= order <= 62
    bits: list[int] = []
    for char in line[1:]:
        value = char - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    pairs = [(u, v) for v in range(1, order) for u in range(v)]
    assert len(bits) >= len(pairs)
    edges = {pair for pair, bit in zip(pairs, bits) if bit}
    return order, edges


def has_independent_four(order: int, edges: set[tuple[int, int]]) -> bool:
    return any(
        all(tuple(sorted(pair)) not in edges for pair in combinations(four, 2))
        for four in combinations(range(order), 4)
    )


def has_k4(order: int, edges: set[tuple[int, int]]) -> bool:
    return any(
        all(tuple(sorted(pair)) in edges for pair in combinations(four, 2))
        for four in combinations(range(order), 4)
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("filtered")
    args = ap.parse_args()

    with open(args.base, "rb") as source:
        base = [line.strip() for line in source if line.strip()]
    with open(args.filtered, "rb") as source:
        filtered = [line.strip() for line in source if line.strip()]
    assert len(base) == len(set(base))
    assert len(filtered) == len(set(filtered))

    expected: list[bytes] = []
    orders: set[int] = set()
    for line in base:
        order, edges = decode_graph6(line)
        orders.add(order)
        assert not has_k4(order, edges)
        if not has_independent_four(order, edges):
            expected.append(line)
    assert len(orders) == 1
    assert filtered == expected
    print(
        f"VERIFIED order={next(iter(orders))} base={len(base)} "
        f"filtered={len(filtered)} removed={len(base)-len(filtered)} "
        "K4_free_base=YES exact_ordered_alpha_at_most_3_subset=YES"
    )


if __name__ == "__main__":
    main()
