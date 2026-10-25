#!/usr/bin/env python3
"""Stress-test the verifier's coloring recursion against literal enumeration."""

from __future__ import annotations

from itertools import combinations
from random import Random


def coloring_decision(adjacency: list[int], pool: int, target: int) -> bool:
    chosen = 0

    def search(candidates: int) -> bool:
        nonlocal chosen
        if chosen == target:
            return True
        if chosen + candidates.bit_count() < target:
            return False

        remaining = candidates
        order = []
        bounds = []
        color = 0
        while remaining:
            color += 1
            available = remaining
            color_class = []
            while available:
                bit = available & -available
                vertex = bit.bit_length() - 1
                color_class.append(vertex)
                order.append(vertex)
                bounds.append(color)
                remaining ^= bit
                available ^= bit
                available &= ~adjacency[vertex]
            assert all(
                not (adjacency[u] >> v) & 1
                for i, u in enumerate(color_class)
                for v in color_class[i + 1 :]
            )

        for position in range(len(order) - 1, -1, -1):
            if chosen + bounds[position] < target:
                return False
            vertex = order[position]
            bit = 1 << vertex
            if candidates & bit:
                chosen += 1
                if search(candidates & adjacency[vertex]):
                    return True
                chosen -= 1
                candidates ^= bit
        return False

    return search(pool)


def brute_decision(adjacency: list[int], pool: int, target: int) -> bool:
    vertices = [v for v in range(len(adjacency)) if (pool >> v) & 1]
    for subset in combinations(vertices, target):
        if all((adjacency[u] >> v) & 1 for i, u in enumerate(subset) for v in subset[i + 1 :]):
            return True
    return target == 0


def graph_from_mask(n: int, mask: int) -> list[int]:
    adjacency = [0] * n
    bit = 0
    for u in range(n):
        for v in range(u + 1, n):
            if (mask >> bit) & 1:
                adjacency[u] |= 1 << v
                adjacency[v] |= 1 << u
            bit += 1
    return adjacency


def check(adjacency: list[int], pool: int) -> int:
    cases = 0
    for target in range(len(adjacency) + 1):
        got = coloring_decision(adjacency, pool, target)
        want = brute_decision(adjacency, pool, target)
        assert got == want, (adjacency, pool, target, got, want)
        cases += 1
    return cases


def main() -> None:
    cases = 0
    graphs = 0
    for n in range(1, 6):
        for mask in range(1 << (n * (n - 1) // 2)):
            adjacency = graph_from_mask(n, mask)
            graphs += 1
            for pool in range(1 << n):
                cases += check(adjacency, pool)

    rng = Random(1109_20260811)
    random_graphs = 3000
    for _ in range(random_graphs):
        n = rng.randrange(6, 13)
        mask = rng.getrandbits(n * (n - 1) // 2)
        adjacency = graph_from_mask(n, mask)
        pool = rng.getrandbits(n)
        cases += check(adjacency, pool)

    print(f"exhaustive_graphs_n_le_5={graphs}")
    print(f"random_graph_pool_pairs_n_6_to_12={random_graphs}")
    print(f"target_decisions_checked={cases}")
    print("PASS coloring-bound recursion agrees with literal clique enumeration")


if __name__ == "__main__":
    main()
