#!/usr/bin/env python3
"""Dependency-free definition-level audit of the #813 near graph."""

from itertools import combinations
from pathlib import Path


def load_masks(path: Path) -> list[int]:
    return [
        int(line.split("#", 1)[0].strip(), 16)
        for line in path.read_text().splitlines()
        if line.split("#", 1)[0].strip()
    ]


def is_clique(adj: list[int], vertices: tuple[int, ...]) -> bool:
    return all((adj[u] >> v) & 1 for u, v in combinations(vertices, 2))


def main() -> None:
    adj = load_masks(Path(__file__).with_name("best9.masks"))
    n = len(adj)
    assert n == 18
    assert all(adj[v] >> v & 1 == 0 for v in range(n))
    assert all(
        ((adj[u] >> v) & 1) == ((adj[v] >> u) & 1)
        for u, v in combinations(range(n), 2)
    )

    edges = sum((adj[u] >> v) & 1 for u, v in combinations(range(n), 2))
    triangles = sum(is_clique(adj, triple) for triple in combinations(range(n), 3))
    k5s = sum(is_clique(adj, five) for five in combinations(range(n), 5))
    bad_sevens = [
        seven
        for seven in combinations(range(n), 7)
        if not any(is_clique(adj, triple) for triple in combinations(seven, 3))
    ]
    omega = max(
        size
        for size in range(1, n + 1)
        if any(is_clique(adj, subset) for subset in combinations(range(n), size))
    )
    degrees = sorted(row.bit_count() for row in adj)

    assert edges == 96
    assert triangles == 180
    assert k5s == 0
    assert len(bad_sevens) == 9
    assert omega == 4
    assert degrees == [10] * 6 + [11] * 12
    print(f"n={n} edges={edges} triangles={triangles} K5={k5s} omega={omega}")
    print(f"triangle_free_7_sets={len(bad_sevens)} degree_sequence=10^6 11^12")
    print("PASS: exact near-graph audit; this graph is not an h(18)=4 witness.")


if __name__ == "__main__":
    main()
