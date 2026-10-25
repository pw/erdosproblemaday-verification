#!/usr/bin/env python3
"""Dependency-free check of the explicit upper-bound witness h(18) <= 5."""

from itertools import combinations

MASKS = [
    int(value, 16)
    for value in """
    179de 21ffd 273bb 34457 3ed8f 3c6c6 1afab 1ea77 33e57
    2c5e6 3ab7a 1b5d3 18907 20dd5 382bd 35ef0 2ddf9 1e73e
    """.split()
]

n = len(MASKS)
assert n == 18
assert all(not (MASKS[v] >> v & 1) for v in range(n))
assert all(
    (MASKS[u] >> v & 1) == (MASKS[v] >> u & 1)
    for u in range(n)
    for v in range(n)
)


def clique(vertices):
    return all(MASKS[u] >> v & 1 for u, v in combinations(vertices, 2))


triangles = [triple for triple in combinations(range(n), 3) if clique(triple)]
omega = max(
    size
    for size in range(1, n + 1)
    if any(clique(vertices) for vertices in combinations(range(n), size))
)
bad_sevens = [
    seven
    for seven in combinations(range(n), 7)
    if not any(set(triangle) <= set(seven) for triangle in triangles)
]

assert sum(mask.bit_count() for mask in MASKS) // 2 == 100
assert len(triangles) == 223
assert omega == 5
assert not bad_sevens
print(
    "W18 upper witness: vertices=18 edges=100 triangles=223 "
    "omega=5 triangle_free_7sets=0 h18_at_most_5=PASS"
)
