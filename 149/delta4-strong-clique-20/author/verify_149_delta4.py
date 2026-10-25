#!/usr/bin/env python3
"""Exact checks for the Delta=4 strong-clique corollary for Problem 149."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parent
KMP_TEX = ROOT / "sources/2607.02698v1-source/line_graph.tex"
HSY_TEXT = ROOT / "sources/HSY2018/v25i3p31.txt"


def add_poly(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    size = max(len(left), len(right))
    result = [Fraction(0) for _ in range(size)]
    for i, value in enumerate(left):
        result[i] += value
    for i, value in enumerate(right):
        result[i] += value
    return result


def mul_poly(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    result = [Fraction(0) for _ in range(len(left) + len(right) - 1)]
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i + j] += x * y
    return result


def scale_poly(poly: list[Fraction], scalar: Fraction) -> list[Fraction]:
    return [scalar * value for value in poly]


def pow_poly(poly: list[Fraction], exponent: int) -> list[Fraction]:
    result = [Fraction(1)]
    for _ in range(exponent):
        result = mul_poly(result, poly)
    return result


def check_source_statements() -> None:
    tex = KMP_TEX.read_text()
    hsy = HSY_TEXT.read_text()

    required_tex = (
        "For a finite simple graph $G$",
        "For every graph $G$",
        r"\omega(L(G)^2)",
        r"\frac{2607}{1987}",
        r"\Delta(G)^2",
        r"\Delta(C_5^{(t)}) = 2t",
        r"complete graph of order $5t^2",
    )
    for fragment in required_tex:
        assert fragment in tex, f"missing KMP source fragment: {fragment}"

    # This is the v1 typo discussed in PROOF_AUDIT.md. Its presence is checked
    # so a silently changed source cannot make the audit stale.
    typo = r"\beta\in [0,1/4]"
    assert typo in tex, "expected beta-star interval typo is no longer present"

    assert "Theorem 2. For every graph G with maximum degree four" in hsy
    assert "21." in hsy


def check_exact_constant_algebra() -> None:
    beta = Fraction(620, 1987)
    coefficient = Fraction(2607, 1987)

    assert Fraction(1, 4) < beta < Fraction(1, 3)
    assert (1 + beta) / 4 == Fraction(2607, 7948)
    assert 4 * ((1 + beta) / 4) == coefficient
    assert coefficient < Fraction(21, 16)

    delta_four_bound = coefficient * 16
    assert delta_four_bound == Fraction(41712, 1987)
    assert 20 < delta_four_bound < 21
    assert 21 - delta_four_bound == Fraction(15, 1987)

    # Verify the exact sum-of-a-square decomposition in KMP Lemma 2.1.
    # Coefficients are stored in ascending powers of x.
    p_beta = [
        beta * beta,
        beta * (2 * beta - 1),
        beta * beta,
        2 * beta - 1,
        beta,
    ]
    square_base = [
        -Fraction(211, 1000),
        -Fraction(747, 1240),
        Fraction(1),
    ]
    square_term = scale_poly(mul_poly(square_base, square_base), beta)
    quadratic_term = [
        Fraction(510806838853, 6119661950000),
        Fraction(-1203303717450, 6119661950000),
        Fraction(708654527125, 6119661950000),
    ]
    assert p_beta == add_poly(square_term, quadratic_term)

    discriminant = (
        (-1203303717450) ** 2
        - 4 * 708654527125 * 510806838853
    )
    assert discriminant == -2478929365735048000
    assert discriminant < 0

    # Check the cleared-denominator identity used at the final induction step:
    # beta - F(t) = (1-t)^4 P_beta(t/(1-t)) /
    #               (t^2 + beta(1-t)^2).
    # The two numerator polynomials below must agree identically.
    one_minus_t = [Fraction(1), Fraction(-1)]
    denominator = add_poly(
        [Fraction(0), Fraction(0), Fraction(1)],
        scale_poly(mul_poly(one_minus_t, one_minus_t), beta),
    )
    t_one_minus_t = [Fraction(0), Fraction(1), Fraction(-1)]
    t2_one_minus_t2 = mul_poly(
        [Fraction(0), Fraction(0), Fraction(1)],
        mul_poly(one_minus_t, one_minus_t),
    )
    left_numerator = add_poly(
        scale_poly(denominator, beta),
        scale_poly(mul_poly(t_one_minus_t, denominator), -1),
    )
    left_numerator = add_poly(
        left_numerator,
        scale_poly(t2_one_minus_t2, -beta),
    )

    # Homogenize P_beta(x) at x=t/(1-t).
    right_numerator = [Fraction(0)]
    for power, value in enumerate(p_beta):
        term = mul_poly(
            [Fraction(0)] * power + [Fraction(1)],
            pow_poly(one_minus_t, 4 - power),
        )
        right_numerator = add_poly(
            right_numerator, scale_poly(term, value)
        )
    while left_numerator and left_numerator[-1] == 0:
        left_numerator.pop()
    while right_numerator and right_numerator[-1] == 0:
        right_numerator.pop()
    assert left_numerator == right_numerator


def cycle_blowup(t: int) -> tuple[list[int], list[tuple[int, int]]]:
    vertices = list(range(5 * t))
    edges: set[tuple[int, int]] = set()
    for part in range(5):
        next_part = (part + 1) % 5
        for a in range(t):
            for b in range(t):
                u = part * t + a
                v = next_part * t + b
                edges.add((min(u, v), max(u, v)))
    return vertices, sorted(edges)


def line_square_distance_histogram(
    edges: list[tuple[int, int]],
) -> Counter[int]:
    line_neighbors = [set() for _ in edges]
    for i, j in combinations(range(len(edges)), 2):
        if set(edges[i]) & set(edges[j]):
            line_neighbors[i].add(j)
            line_neighbors[j].add(i)

    distances: Counter[int] = Counter()
    for i, j in combinations(range(len(edges)), 2):
        if j in line_neighbors[i]:
            distances[1] += 1
        elif line_neighbors[i] & line_neighbors[j]:
            distances[2] += 1
        else:
            distances[3] += 1
    return distances


def check_blowups() -> tuple[str, Counter[int]]:
    delta_four_digest = ""
    delta_four_histogram: Counter[int] = Counter()

    for t in range(1, 9):
        vertices, edges = cycle_blowup(t)
        degrees = Counter()
        for u, v in edges:
            assert u != v
            degrees[u] += 1
            degrees[v] += 1

        assert len(vertices) == 5 * t
        assert len(edges) == 5 * t * t
        assert set(degrees) == set(vertices)
        assert set(degrees.values()) == {2 * t}
        assert len(edges) == Fraction(5, 4) * (2 * t) ** 2

        histogram = line_square_distance_histogram(edges)
        assert histogram[3] == 0
        assert histogram[1] + histogram[2] == len(edges) * (len(edges) - 1) // 2

        if t == 2:
            assert len(vertices) == 10
            assert len(edges) == 20
            assert histogram == Counter({2: 130, 1: 60})
            payload = "".join(f"{u} {v}\n" for u, v in edges).encode()
            delta_four_digest = sha256(payload).hexdigest()
            delta_four_histogram = histogram

    return delta_four_digest, delta_four_histogram


def main() -> None:
    check_source_statements()
    check_exact_constant_algebra()
    digest, histogram = check_blowups()

    beta = Fraction(620, 1987)
    coefficient = Fraction(2607, 1987)
    bound = coefficient * 16

    print("Erdos Problem 149: Delta=4 strong-clique audit")
    print("================================================")
    print(f"KMP beta = {beta}")
    print(f"KMP strong-clique coefficient = {coefficient}")
    print(f"Delta=4 rational upper bound = {bound}")
    print(f"distance below 21 = {21 - bound}")
    print("integer consequence: omega(L(G)^2) <= 20 when Delta(G) <= 4")
    print("C5^(2): |V|=10, Delta=4, |E|=20")
    print(f"C5^(2) line-graph distance histogram = {dict(sorted(histogram.items()))}")
    print(f"C5^(2) canonical edge SHA256 = {digest}")
    print("exact consequence: max omega(L(G)^2) over Delta<=4 equals 20")
    print("coloring consequence only: 20 <= max chi(L(G)^2) <= 21")
    print("SOURCE TYPO CONFIRMED: beta-star interval [0,1/4]; fixed-beta proof used")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
