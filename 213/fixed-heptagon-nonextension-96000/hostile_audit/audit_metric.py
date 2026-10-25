#!/usr/bin/env python3
"""Auditor-owned exact metric and domain checks for the fixed heptagon."""

from __future__ import annotations

import csv
import itertools
import json
import sys
from fractions import Fraction
from math import isqrt
from pathlib import Path


D = 22270
B = 96000
K = 2002
DEN = 4 * D * D


def heron(a: int, b: int, c: int) -> int:
    return (a + b + c) * (a + b - c) * (a - b + c) * (-a + b + c)


def square_root(n: int) -> int:
    r = isqrt(n)
    assert r * r == n
    return r


def distance(p: tuple[int, int], q: tuple[int, int]) -> int | None:
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    numerator = dx * dx + K * dy * dy
    if numerator <= 0 or numerator % DEN:
        return None
    squared = numerator // DEN
    r = isqrt(squared)
    if r * r != squared or r > B:
        return None
    return r


def reconstruct(matrix: list[list[int]]) -> list[tuple[int, int]]:
    points = [(0, 0), (2 * D * D, 0)]
    for j in range(2, 7):
        a, b = matrix[0][j], matrix[1][j]
        f = heron(D, a, b)
        assert f % K == 0
        points.append((a * a - b * b + D * D, square_root(f // K)))
    for j in range(3, 7):
        x, y = points[j]
        choices = [
            sign
            for sign in (-1, 1)
            if distance((x, sign * y), points[2]) == matrix[2][j]
        ]
        assert len(choices) == 1
        points[j] = (x, choices[0] * y)
    for i, j in itertools.combinations(range(7), 2):
        assert distance(points[i], points[j]) == matrix[i][j]
    return points


def load_candidates(path: Path) -> list[tuple[int, int, int]]:
    with path.open(newline="") as handle:
        rows = csv.DictReader(handle, delimiter="\t")
        result = [(int(row["a"]), int(row["b"]), int(row["s"])) for row in rows]
    assert result == sorted(set(result))
    return result


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: audit_metric.py MATRIX.json CANDIDATES.tsv AUTHOR.tsv")
    data = json.loads(Path(sys.argv[1]).read_text())
    matrix = data["distance_matrix"]
    assert data["diameter"] == D and data["characteristic"] == K
    points = reconstruct(matrix)
    expected_coordinates = [
        (Fraction(0), Fraction(0)),
        (Fraction(22270), Fraction(0)),
        (Fraction(26127018, 2227), Fraction(932064, 2227)),
        (Fraction(245363, 17), Fraction(3144, 17)),
        (Fraction(17615968, 2227), Fraction(238464, 2227)),
        (Fraction(56068, 17), Fraction(3144, 17)),
        (Fraction(19079044, 2227), Fraction(-54168, 2227)),
    ]
    got_coordinates = [
        (Fraction(x, 2 * D), Fraction(y, 2 * D)) for x, y in points
    ]
    assert got_coordinates == expected_coordinates
    assert all(distance(point, point) is None for point in points)
    for j, point in enumerate(points):
        assert all(distance(point, points[i]) is not None for i in range(7) if i != j)

    candidates = load_candidates(Path(sys.argv[2]))
    author = load_candidates(Path(sys.argv[3]))
    assert candidates == author
    assert len(candidates) == 1017
    candidate_set = set(candidates)
    for j in range(2, 7):
        a, b = sorted((matrix[0][j], matrix[1][j]))
        s = square_root(heron(D, a, b) // K)
        assert (a, b, s) in candidate_set

    oriented = 0
    extensions = 0
    for a, b, s in candidates:
        assert 1 <= a <= b <= B and a + b > D and b - a < D
        assert heron(D, a, b) == K * s * s
        for aa, bb in ((a, b), (b, a)) if a != b else ((a, b),):
            for sign in (-1, 1):
                oriented += 1
                candidate = (aa * aa - bb * bb + D * D, sign * s)
                if all(distance(candidate, point) is not None for point in points):
                    extensions += 1

    collinear = 0
    for x in itertools.chain(range(1, D), range(-(B - D), 0), range(D + 1, B + 1)):
        collinear += 1
        candidate = (2 * D * x, 0)
        if all(distance(candidate, point) is not None for point in points):
            extensions += 1

    # The two exterior extremes attain the inclusive distance bound. The
    # anchor endpoints themselves are coincidences and hence invalid.
    assert distance((2 * D * B, 0), points[0]) == B
    assert distance((-2 * D * (B - D), 0), points[1]) == B
    assert distance(points[0], points[0]) is None
    assert distance(points[1], points[1]) is None

    analytic_pairs = 0
    for total in range(D + 1, 2 * B + 1):
        cap = min(D - 1, total - 2, 2 * B - total)
        first = total & 1
        if first <= cap:
            analytic_pairs += (cap - first) // 2 + 1

    assert analytic_pairs == 1765966460
    boundary_b_pairs = sum(
        1 for a in range(1, B + 1) if a <= B and a + B > D and B - a < D
    )
    assert boundary_b_pairs == D
    assert oriented == 4068
    assert collinear == 169729
    assert extensions == 0
    print(f"analytic_triangle_pairs={analytic_pairs}")
    print(f"characteristic_candidates={len(candidates)}")
    print(f"oriented_candidates={oriented}")
    print(f"collinear_candidates={collinear}")
    print(f"raw_pairs_with_b_at_bound={boundary_b_pairs}")
    print("coincident_vertex_negative_controls=7")
    print(f"extensions={extensions}")
    print("AUDIT_METRIC_PASS")


if __name__ == "__main__":
    main()
