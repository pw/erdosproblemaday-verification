#!/usr/bin/env python3
"""Regression-check the all-r extremal construction and closed formulas."""

from itertools import combinations
from math import comb


def make_j(r):
    """Build J from K_(r,r+1), using both deletion types."""
    assert r >= 2
    x_part = tuple(range(r))
    y_part = tuple(range(r, 2 * r + 1))
    y1, y2 = y_part[:2]
    edges = {
        (x, y)
        for x in x_part
        for y in y_part
    }
    edges.add((y1, y2))
    # x=0 misses y1; every other x misses y2.  Both kinds occur for r>=2.
    edges.remove((0, y1))
    for x in x_part[1:]:
        edges.remove((x, y2))
    return x_part, y_part, y1, y2, edges


def is_clique(vertices, edges):
    return all(tuple(sorted(pair)) in edges for pair in combinations(vertices, 2))


def is_independent(vertices, edges):
    return all(tuple(sorted(pair)) not in edges for pair in combinations(vertices, 2))


def make_g(r, j_edges):
    """Build (r-2) K_r disjoint union complement(J)."""
    edges = set()
    offset = 0
    for _ in range(r - 2):
        block = range(offset, offset + r)
        edges.update(combinations(block, 2))
        offset += r

    j_n = 2 * r + 1
    for u, v in combinations(range(j_n), 2):
        if (u, v) not in j_edges:
            edges.add((offset + u, offset + v))
    return offset + j_n, edges


def check_structural_j(r):
    x_part, y_part, y1, y2, edges = make_j(r)
    assert len(edges) == r * r + 1
    assert all((u, v) not in edges for u, v in combinations(x_part, 2))
    assert {
        pair for pair in combinations(y_part, 2) if pair in edges
    } == {(y1, y2)}

    other_y = set(y_part) - {y1, y2}
    deletion_types = set()
    for x in x_part:
        assert all((x, y) in edges for y in other_y)
        adjacent_special = {y for y in (y1, y2) if (x, y) in edges}
        assert len(adjacent_special) == 1
        deletion_types.add(({y1, y2} - adjacent_special).pop())
    assert deletion_types == {y1, y2}

    # Bit-intersection triangle check is cubic only in the tiny 2r+1 graph.
    adjacency = [0] * (2 * r + 1)
    for u, v in edges:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    assert all(not (adjacency[u] & adjacency[v]) for u, v in edges)


def check_exact_small_cases():
    exact_j_cases = 0
    for r in range(2, 11):
        _, _, _, _, j_edges = make_j(r)
        vertices = range(2 * r + 1)
        assert any(is_independent(s, j_edges) for s in combinations(vertices, r))
        assert not any(
            is_independent(s, j_edges)
            for s in combinations(vertices, r + 1)
        )
        assert any(is_clique(s, j_edges) for s in combinations(vertices, 2))
        assert not any(is_clique(s, j_edges) for s in combinations(vertices, 3))
        exact_j_cases += 1

    exact_g_cases = 0
    for r in range(2, 6):
        _, _, _, _, j_edges = make_j(r)
        n, g_edges = make_g(r, j_edges)
        vertices = range(n)
        assert any(is_clique(s, g_edges) for s in combinations(vertices, r))
        assert any(is_independent(s, g_edges) for s in combinations(vertices, r))
        assert not any(is_clique(s, g_edges) for s in combinations(vertices, r + 1))
        assert not any(
            is_independent(s, g_edges)
            for s in combinations(vertices, r + 1)
        )
        exact_g_cases += 1
    return exact_j_cases, exact_g_cases


def check_formulas(r):
    n = r * r + 1
    complete = comb(n, 2)
    within_turan_parts = comb(r + 1, 2) + (r - 1) * comb(r, 2)
    turan = complete - within_turan_parts
    p_r = turan - n // r + 1
    lower = complete - p_r
    closed = (r**3 - r**2 + 4 * r - 2) // 2
    construction = (r - 2) * comb(r, 2) + comb(2 * r + 1, 2) - (r * r + 1)
    slack = complete - r * closed

    assert n >= r + 3
    assert 2 * r <= n - 1
    assert n // r == r
    assert lower == within_turan_parts + r - 1 == closed == construction
    assert slack == r * (r - 1) * (r - 2) // 2


def main():
    if not __debug__:
        raise RuntimeError("run this verifier without Python -O")
    for r in range(2, 51):
        check_structural_j(r)
    exact_j_cases, exact_g_cases = check_exact_small_cases()
    for r in range(2, 10001):
        check_formulas(r)

    _, _, _, _, j5 = make_j(5)
    n5, g5 = make_g(5, j5)
    assert (n5, len(j5), len(g5)) == (26, 26, 59)

    print("general construction/formula verifier: PASS")
    print("structural J cases: r=2..50 (49 cases)")
    print(f"exact subset cases: J={exact_j_cases} (r=2..10), G={exact_g_cases} (r=2..5)")
    print("integer formula cases: r=2..10000 (9999 cases)")
    print("r=5 specialization: n=26, e(J)=26, e(G)=59, partition slack=30")


if __name__ == "__main__":
    main()
