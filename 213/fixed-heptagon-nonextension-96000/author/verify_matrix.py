#!/usr/bin/env python3
"""Definition-level exact checker for the published heptagon metric."""

import itertools
import json
from math import isqrt
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "heptagon_matrix.json").read_text())
M = DATA["distance_matrix"]
D = DATA["diameter"]
K = DATA["characteristic"]


def heron(a: int, b: int, c: int) -> int:
    return (a + b + c) * (a + b - c) * (a - b + c) * (-a + b + c)


def squarefree_part(n: int) -> int:
    answer = 1
    p = 2
    while p * p <= n:
        parity = 0
        while n % p == 0:
            n //= p
            parity ^= 1
        if parity:
            answer *= p
        p = 3 if p == 2 else p + 2
    return answer * n


def determinant(matrix: list[list[int]]) -> int:
    """Fraction-free Bareiss determinant."""
    a = [row[:] for row in matrix]
    n = len(a)
    sign = 1
    previous = 1
    for col in range(n - 1):
        pivot = next((r for r in range(col, n) if a[r][col]), None)
        if pivot is None:
            return 0
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            sign = -sign
        value = a[col][col]
        for i in range(col + 1, n):
            for j in range(col + 1, n):
                a[i][j] = (a[i][j] * value - a[i][col] * a[col][j]) // previous
        previous = value
    return sign * a[-1][-1]


def reconstruct() -> list[tuple[int, int]]:
    points = [(0, 0), (2 * D * D, 0)]
    for j in range(2, 7):
        a, b = M[0][j], M[1][j]
        h = heron(D, a, b)
        assert h % K == 0
        s = isqrt(h // K)
        assert s * s == h // K
        points.append((a * a - b * b + D * D, s))

    x2, s2 = points[2]
    for j in range(3, 7):
        x, s = points[j]
        signs = []
        for sign in (-1, 1):
            numerator = (x - x2) ** 2 + K * (sign * s - s2) ** 2
            if numerator == 4 * D * D * M[2][j] ** 2:
                signs.append(sign)
        assert len(signs) == 1
        points[j] = (x, signs[0] * s)
    return points


def main() -> None:
    assert len(M) == 7 and all(len(row) == 7 for row in M)
    assert all(M[i][i] == 0 for i in range(7))
    assert all(M[i][j] == M[j][i] > 0 for i in range(7) for j in range(i + 1, 7))

    points = reconstruct()
    denominator = 4 * D * D
    edge_values = []
    for i, j in itertools.combinations(range(7), 2):
        dx = points[i][0] - points[j][0]
        ds = points[i][1] - points[j][1]
        assert dx * dx + K * ds * ds == denominator * M[i][j] ** 2
        edge_values.append(M[i][j])

    triangle_count = 0
    for i, j, ell in itertools.combinations(range(7), 3):
        h = heron(M[i][j], M[i][ell], M[j][ell])
        assert h > 0 and squarefree_part(h) == K
        xi, si = points[i]
        xj, sj = points[j]
        xl, sl = points[ell]
        assert (xj - xi) * (sl - si) != (xl - xi) * (sj - si)
        triangle_count += 1

    quadruple_count = 0
    for subset in itertools.combinations(range(7), 4):
        rows = []
        for i in subset:
            x, s = points[i]
            rows.append([x * x + K * s * s, x, s, 1])
        assert determinant(rows) != 0
        quadruple_count += 1

    print(f"matrix_pairs={len(edge_values)}")
    print(f"distinct_distances={len(set(edge_values))}")
    print(f"triangle_characteristic_2002={triangle_count}")
    print(f"noncollinear_triples={triangle_count}")
    print(f"nonconcyclic_quadruples={quadruple_count}")
    print("general_position=true")


if __name__ == "__main__":
    main()
