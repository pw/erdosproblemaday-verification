#!/usr/bin/env python3
"""Exact checks for the elementary part of the convex-position proof."""

from collections import Counter
from math import comb


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def cyclic_step_counts(order: int, deleted: int | None = None) -> Counter[int]:
    require(order >= 3, f"invalid polygon order: {order}")
    require(deleted is None or 0 <= deleted < order, "invalid deleted vertex")
    vertices = [vertex for vertex in range(order) if vertex != deleted]
    counts: Counter[int] = Counter()
    for position, left in enumerate(vertices):
        for right in vertices[position + 1 :]:
            delta = (right - left) % order
            counts[min(delta, order - delta)] += 1
    return counts


def pair_count_gap(n: int, minimum_non_diameter_multiplicity: int) -> int:
    require(n >= 5, f"invalid point count: {n}")
    forced = (n // 2) * minimum_non_diameter_multiplicity + 1
    return forced - comb(n, 2)


def validate_vector(n: int, vector: tuple[int, ...], expected_classes: int) -> None:
    require(len(vector) == expected_classes, f"wrong class count for n={n}")
    require(len(vector) >= 2, f"too few distances for n={n}")
    require(all(isinstance(value, int) and value > 0 for value in vector),
            f"invalid multiplicity for n={n}")
    require(sum(vector) == comb(n, 2), f"pair total mismatch for n={n}")
    require(max(vector) <= n, f"multiplicity exceeds n for n={n}")


def check_pair_count_contradiction(limit: int = 10_000) -> int:
    checked = 0
    for n in range(5, limit + 1):
        gap = pair_count_gap(n, n + 1)
        expected = n + 1 if n % 2 == 0 else (n + 1) // 2
        require(gap == expected and gap > 0, f"bad pair-count gap for n={n}")
        checked += 1
    return checked


def check_regular_models(limit: int = 500) -> tuple[int, int]:
    regular_checked = 0
    deleted_checked = 0
    for n in range(5, limit + 1):
        counts = tuple(sorted(cyclic_step_counts(n).values(), reverse=True))
        if n % 2:
            expected = (n,) * ((n - 1) // 2)
        else:
            expected = (n,) * (n // 2 - 1) + (n // 2,)
        require(counts == expected, f"regular polygon mismatch for n={n}")
        validate_vector(n, counts, n // 2)
        regular_checked += 1

    for n in range(8, limit + 1, 2):
        counts = tuple(sorted(cyclic_step_counts(n + 1, deleted=0).values(),
                              reverse=True))
        expected = (n - 1,) * (n // 2)
        require(counts == expected, f"deleted-vertex mismatch for n={n}")
        validate_vector(n, counts, n // 2)
        deleted_checked += 1
    return regular_checked, deleted_checked


def check_hexagon_vectors() -> int:
    vectors = ((6, 6, 3), (5, 5, 5))
    for vector in vectors:
        validate_vector(6, vector, 3)
    return len(vectors)


def main() -> None:
    pair_counts = check_pair_count_contradiction()
    regular, deleted = check_regular_models()
    hexagons = check_hexagon_vectors()
    print(
        "CONVEX_PROOF_PASS "
        f"pair_counts={pair_counts} regular_models={regular} "
        f"deleted_models={deleted} hexagon_vectors={hexagons}"
    )


if __name__ == "__main__":
    main()
