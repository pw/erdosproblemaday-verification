#!/usr/bin/env python3
"""Independent focused audit of the exceptional N=18 branch for #352."""

from itertools import combinations, combinations_with_replacement
import math


Point = tuple[int, int]
N = 18
A = (0, 0)
B = (5, 4)

WITNESS: tuple[Point, ...] = (
    (0, 0), (0, 1), (0, 2),
    (1, 0), (1, 1), (1, 2), (1, 3),
    (2, -1), (2, 0), (2, 1), (2, 2), (2, 3),
    (3, -1), (3, 0), (3, 1), (3, 2), (3, 3),
    (4, -1), (4, 0), (4, 1), (4, 2), (4, 3),
    (5, -1), (5, 0), (5, 1), (5, 2), (5, 3),
    (6, 0), (6, 1), (6, 2), (6, 3),
    (7, 0), (7, 1), (7, 2),
)


def squared_distance(p: Point, q: Point) -> int:
    return (
        p[0] * p[0] + p[1] * p[1]
        + q[0] * q[0] + q[1] * q[1]
        - 2 * p[0] * q[0] - 2 * p[1] * q[1]
    )


def doubled_area(p: Point, q: Point, r: Point) -> int:
    return abs(
        p[0] * q[1] + q[0] * r[1] + r[0] * p[1]
        - p[1] * q[0] - q[1] * r[0] - r[1] * p[0]
    )


def margin(p: Point, q: Point, r: Point) -> int:
    area2 = doubled_area(p, q, r)
    diameter2 = max(
        squared_distance(p, q),
        squared_distance(p, r),
        squared_distance(q, r),
    )
    return (area2 - 2 * N) ** 2 - 4 * diameter2


def avoiding(points: tuple[Point, ...]) -> bool:
    return all(
        margin(p, q, r) > 0
        for p, q, r in combinations_with_replacement(points, 3)
    )


def main() -> None:
    assert len(WITNESS) == len(set(WITNESS)) == 34
    witness_margins = [
        margin(p, q, r)
        for p, q, r in combinations_with_replacement(WITNESS, 3)
    ]
    assert len(witness_margins) == math.comb(36, 3) == 7140
    assert min(witness_margins) == 21

    diameter2 = squared_distance(A, B)
    assert diameter2 == 41
    pool = tuple(
        p
        for x in range(-(N - 1), N)
        for y in range(-(N - 1), N)
        if (p := (x, y)) not in (A, B)
        and squared_distance(A, p) <= diameter2
        and squared_distance(B, p) <= diameter2
        and doubled_area(A, B, p) < 2 * N
        and avoiding((A, B, p))
    )
    assert len(pool) == 42 and len(pool) == len(set(pool))

    bad_pairs = {
        frozenset((p, q))
        for p, q in combinations(pool, 2)
        if squared_distance(p, q) > diameter2
        or not avoiding((A, B, p, q))
    }
    assert len(bad_pairs) == 57

    matching: tuple[tuple[Point, Point], ...] = (
        ((-1, 2), (6, 2)),
        ((-1, 3), (2, -1)),
        ((0, 1), (3, -2)),
        ((0, 4), (3, -1)),
        ((1, -1), (4, 5)),
        ((1, 5), (4, -1)),
        ((2, 5), (5, 0)),
        ((2, 6), (5, 3)),
        ((3, 5), (6, 1)),
    )
    endpoints = tuple(p for edge in matching for p in edge)
    assert len(endpoints) == len(set(endpoints)) == 18
    assert all(frozenset(edge) in bad_pairs for edge in matching)

    covers: list[tuple[Point, ...]] = []
    violations: list[tuple[Point, Point, Point, int]] = []
    for mask in range(512):
        cover = frozenset(
            edge[(mask >> index) & 1]
            for index, edge in enumerate(matching)
        )
        assert len(cover) == 9
        if not all(edge & cover for edge in bad_pairs):
            continue
        survivor = tuple(p for p in pool if p not in cover)
        assert len(survivor) == 33
        assert all(
            frozenset((p, q)) not in bad_pairs
            for p, q in combinations(survivor, 2)
        )
        bad = [
            (p, q, r, margin(p, q, r))
            for p, q, r in combinations(survivor, 3)
            if margin(p, q, r) <= 0
        ]
        assert len(bad) == 2 and {row[3] for row in bad} == {-15}
        covers.append(tuple(sorted(cover)))
        violations.extend(bad)

    expected = {
        frozenset(((1, -1), (1, 4), (6, 1))),
        frozenset(((1, -1), (1, 4), (6, 2))),
        frozenset(((-1, 2), (4, 0), (4, 5))),
        frozenset(((-1, 3), (4, 0), (4, 5))),
    }
    assert len(covers) == 2
    assert {frozenset(row[:3]) for row in violations} == expected

    print("N=18 WITNESS PASS points=34 triples=7140 min_gap=21")
    print("B=(5,4) LOW POOL PASS vertices=42 incompatibility_edges=57")
    print("MATCHING AUDIT PASS edges=9 choices=512 covers=2")
    for index, cover in enumerate(covers):
        print(f"cover[{index}]={cover}")
    for p, q, r, value in violations:
        print(f"forbidden_triple={p},{q},{r} margin={value}")
    print("EXCEPTIONAL BRANCH CAP PASS candidates<=32 total_points<=34")
    print("ALL FOCUSED N=18 CHECKS PASSED")


if __name__ == "__main__":
    main()
