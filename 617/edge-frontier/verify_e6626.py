#!/usr/bin/env python3
"""Exhaustively verify the explicit 59-edge (6,6;26) Ramsey graph."""

from hashlib import sha256
from itertools import combinations
from math import comb


J_N = 11
J_EDGES = (
    (0, 1),
    (1, 2), (1, 3), (1, 4),
    (0, 5), (0, 6),
    (2, 7), (3, 7), (4, 7), (5, 7), (6, 7),
    (2, 8), (3, 8), (4, 8), (5, 8), (6, 8),
    (2, 9), (3, 9), (4, 9), (5, 9), (6, 9),
    (2, 10), (3, 10), (4, 10), (5, 10), (6, 10),
)


def normalized_edges(edges):
    return {tuple(sorted(edge)) for edge in edges}


def is_clique(vertices, edges):
    return all(pair in edges for pair in combinations(vertices, 2))


def is_independent(vertices, edges):
    return all(pair not in edges for pair in combinations(vertices, 2))


def edge_digest(n, edges):
    payload = f"n={n};" + ";".join(f"{u}-{v}" for u, v in sorted(edges))
    return sha256(payload.encode("ascii")).hexdigest()


def turan_edges(n, r):
    q, extra = divmod(n, r)
    part_sizes = [q + 1] * extra + [q] * (r - extra)
    return comb(n, 2) - sum(comb(size, 2) for size in part_sizes), part_sizes


def main():
    if not __debug__:
        raise RuntimeError("run this verifier without Python -O")
    j_edges = normalized_edges(J_EDGES)
    assert len(j_edges) == 26
    assert all(0 <= u < v < J_N for u, v in j_edges)

    triangles = [
        subset
        for subset in combinations(range(J_N), 3)
        if is_clique(subset, j_edges)
    ]
    independent_sixes = [
        subset
        for subset in combinations(range(J_N), 6)
        if is_independent(subset, j_edges)
    ]
    assert not triangles
    assert not independent_sixes

    # G is K5 + K5 + K5 + complement(J).
    g_n = 26
    g_edges = set()
    for start in (0, 5, 10):
        g_edges.update(combinations(range(start, start + 5), 2))
    for u, v in combinations(range(J_N), 2):
        if (u, v) not in j_edges:
            g_edges.add((15 + u, 15 + v))

    assert len(g_edges) == 3 * comb(5, 2) + comb(11, 2) - 26 == 59

    six_sets = 0
    six_cliques = 0
    six_independent = 0
    for subset in combinations(range(g_n), 6):
        six_sets += 1
        six_cliques += is_clique(subset, g_edges)
        six_independent += is_independent(subset, g_edges)
    assert six_sets == comb(26, 6) == 230230
    assert six_cliques == 0
    assert six_independent == 0

    five_cliques = sum(
        is_clique(subset, g_edges)
        for subset in combinations(range(g_n), 5)
    )
    five_independent = sum(
        is_independent(subset, g_edges)
        for subset in combinations(range(g_n), 5)
    )
    assert five_cliques > 0
    assert five_independent > 0

    t5, parts = turan_edges(26, 5)
    assert parts == [6, 5, 5, 5, 5]
    assert t5 == 270
    p5 = t5 - (26 // 5) + 1
    assert p5 == 266
    complement_lower_bound = comb(26, 2) - p5
    assert complement_lower_bound == 59
    assert (26 + 5 - 1) // 5 == 6

    print("explicit-edge-list verifier: PASS")
    print(f"J: vertices={J_N} edges={len(j_edges)}")
    print(f"J exhaustive subsets: C(11,3)={comb(11,3)}, C(11,6)={comb(11,6)}")
    print(f"J forbidden subsets: triangles={len(triangles)}, independent_6={len(independent_sixes)}")
    print(f"G: vertices={g_n} edges={len(g_edges)}")
    print(f"G exhaustive 6-subsets={six_sets}, K6={six_cliques}, independent_6={six_independent}")
    print(f"G 5-subsets: K5={five_cliques}, independent_5={five_independent}")
    print(f"Turan arithmetic: parts={parts}, t_5(26)={t5}, p_5(26)={p5}, lower={complement_lower_bound}")
    print(f"G edge digest={edge_digest(g_n, g_edges)}")


if __name__ == "__main__":
    main()
