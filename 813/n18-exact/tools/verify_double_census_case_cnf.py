#!/usr/bin/env python3
"""Independent exact-prefix/tail audit of one canonical (M,H) branch CNF."""

from __future__ import annotations

import argparse
from itertools import combinations


def read_cnf(path: str) -> tuple[int, list[tuple[int, ...]]]:
    variables = declared = None
    clauses: list[tuple[int, ...]] = []
    with open(path) as source:
        for line in source:
            if not line.strip() or line.startswith("c"):
                continue
            if line.startswith("p cnf"):
                _, _, a, b = line.split()
                variables, declared = int(a), int(b)
            else:
                values = tuple(map(int, line.split()))
                assert values[-1] == 0
                clauses.append(values[:-1])
    assert variables is not None and declared == len(clauses)
    return variables, clauses


def decode_graph6(line: bytes, order: int) -> set[tuple[int, int]]:
    line = line.strip()
    assert line and line[0] - 63 == order and order <= 62
    bits: list[int] = []
    for char in line[1:]:
        value = char - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    pairs = [(u, v) for v in range(1, order) for u in range(v)]
    assert len(bits) >= len(pairs)
    return {pair for pair, bit in zip(pairs, bits) if bit}


def clique_exists(order: int, edges: set[tuple[int, int]], size: int) -> bool:
    return any(
        all(tuple(sorted(pair)) in edges for pair in combinations(vertices, 2))
        for vertices in combinations(range(order), size)
    )


def independent_exists(order: int, edges: set[tuple[int, int]], size: int) -> bool:
    return any(
        all(tuple(sorted(pair)) not in edges for pair in combinations(vertices, 2))
        for vertices in combinations(range(order), size)
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("degree", type=int)
    ap.add_argument("flat", type=int)
    ap.add_argument("base")
    ap.add_argument("m_census")
    ap.add_argument("h_census")
    ap.add_argument("branch")
    args = ap.parse_args()

    degree = args.degree
    m_order = 17 - degree
    with open(args.m_census, "rb") as source:
        m_lines = [line for line in source if line.strip()]
    with open(args.h_census, "rb") as source:
        h_lines = [line for line in source if line.strip()]
    total = len(m_lines) * len(h_lines)
    assert 0 <= args.flat < total
    m_case, h_case = divmod(args.flat, len(h_lines))
    m_edges = decode_graph6(m_lines[m_case], m_order)
    h_edges = decode_graph6(h_lines[h_case], degree)
    assert not clique_exists(m_order, m_edges, 5)
    assert not independent_exists(m_order, m_edges, 3)
    assert not clique_exists(degree, h_edges, 4)
    assert not independent_exists(degree, h_edges, 4)

    base_vars, base = read_cnf(args.base)
    branch_vars, branch = read_cnf(args.branch)
    assert base_vars == branch_vars and branch[:len(base)] == base
    edge18 = {pair: i for i, pair in enumerate(combinations(range(18), 2), 1)}
    expected = []
    for u, v in combinations(range(m_order), 2):
        var = edge18[(u + degree + 1, v + degree + 1)]
        expected.append((var if (u, v) in m_edges else -var,))
    for u, v in combinations(range(degree), 2):
        var = edge18[(u + 1, v + 1)]
        expected.append((var if (u, v) in h_edges else -var,))
    assert branch[len(base):] == expected
    print(
        f"VERIFIED degree={degree} flat={args.flat}/{total} "
        f"m_case={m_case}/{len(m_lines)} h_case={h_case}/{len(h_lines)} "
        f"M_K5_free_alpha_at_most_2=YES "
        f"H_K4_free_alpha_at_most_3=YES "
        f"base_exact_prefix=YES units_exact={len(expected)}"
    )


if __name__ == "__main__":
    main()
