#!/usr/bin/env python3
"""Independent exact-prefix/tail audit for a fixed-neighbourhood CNF."""

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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("degree", type=int)
    ap.add_argument("case", type=int)
    ap.add_argument("base")
    ap.add_argument("census")
    ap.add_argument("branch")
    args = ap.parse_args()

    with open(args.census, "rb") as source:
        lines = [line for line in source if line.strip()]
    assert 0 <= args.case < len(lines)
    edges = decode_graph6(lines[args.case], args.degree)
    assert not any(
        all(tuple(sorted(pair)) in edges for pair in combinations(four, 2))
        for four in combinations(range(args.degree), 4)
    )
    assert not any(
        all(tuple(sorted(pair)) not in edges for pair in combinations(four, 2))
        for four in combinations(range(args.degree), 4)
    )

    base_vars, base = read_cnf(args.base)
    branch_vars, branch = read_cnf(args.branch)
    assert base_vars == branch_vars and branch[:len(base)] == base
    edge18 = {pair: i for i, pair in enumerate(combinations(range(18), 2), 1)}
    expected = []
    for u, v in combinations(range(args.degree), 2):
        var = edge18[(u + 1, v + 1)]
        expected.append((var if (u, v) in edges else -var,))
    assert branch[len(base):] == expected
    print(
        f"VERIFIED degree={args.degree} case={args.case}/{len(lines)} "
        f"H_edges={len(edges)} K4_free=YES alpha_at_most_3=YES "
        f"base_exact_prefix=YES units_exact={len(expected)}"
    )


if __name__ == "__main__":
    main()
