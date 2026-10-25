#!/usr/bin/env python3
"""Independent exact checker for a finite result related to Erdos problem #352.

This script proves, by finite exhaustive certificates, that Koizumi's lattice
quantity satisfies

    f(8..21) = 14,16,18,21,23,24,26,28,32,32,34,38,39,41.

Here a finite S subset Z^2 is N-avoiding when every triple, with repetitions
allowed, obeys

    |area(triangle) - N| > diameter(triangle).

The lower bounds are explicit witnesses embedded below.  For each upper bound
the program:

  * normalizes a diameter pair to A=(0,0), B=(b_x,b_y);
  * exhausts the finite two-disc lens containing every other point;
  * splits candidates below/above the forbidden area band;
  * exhausts the "no high point" branch and every possible fixed high point;
  * greedily colors a pair-compatibility graph.

A greedy coloring is enough: every actual avoiding extension is a clique, so
it uses at most one vertex of each color.  The checker then audits each color
class directly with a second determinant formula and full triple enumeration;
it does not trust optimality of the greedy algorithm (none is needed).

Only the Python standard library is used.  All geometric comparisons use exact
integer arithmetic.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from collections import defaultdict
from itertools import combinations, combinations_with_replacement
from typing import Iterable, Sequence


Point = tuple[int, int]
A: Point = (0, 0)


# Previously posted lower-bound witnesses, independently rechecked here.
WITNESSES: dict[int, tuple[Point, ...]] = {
    8: (
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2), (1, 3),
        (2, 0), (2, 1), (2, 2), (2, 3),
        (3, 1), (3, 2), (3, 3),
    ),
    9: (
        (0, 0), (0, 1),
        (1, -1), (1, 0), (1, 1), (1, 2),
        (2, -1), (2, 0), (2, 1), (2, 2),
        (3, -1), (3, 0), (3, 1), (3, 2),
        (4, 0), (4, 1),
    ),
    10: (
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2), (1, 3),
        (2, 0), (2, 1), (2, 2), (2, 3),
        (3, 0), (3, 1), (3, 2), (3, 3),
        (4, 1), (4, 2), (4, 3),
    ),
    11: (
        (0, 0), (0, 1), (0, 2),
        (1, -1), (1, 0), (1, 1), (1, 2), (1, 3),
        (2, -1), (2, 0), (2, 1), (2, 2), (2, 3),
        (3, -1), (3, 0), (3, 1), (3, 2), (3, 3),
        (4, 0), (4, 1), (4, 2),
    ),
    12: (
        (0, 0), (0, 1), (0, 2), (0, 3),
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
        (4, 1), (4, 2), (4, 3), (4, 4),
    ),
    13: (
        (0, 0), (0, 1),
        (1, -1), (1, 0), (1, 1), (1, 2),
        (2, -1), (2, 0), (2, 1), (2, 2),
        (3, -1), (3, 0), (3, 1), (3, 2),
        (4, -1), (4, 0), (4, 1), (4, 2),
        (5, -1), (5, 0), (5, 1), (5, 2),
        (6, 0), (6, 1),
    ),
    14: (
        (0, 0), (0, 1),
        (1, -1), (1, 0), (1, 1), (1, 2), (1, 3),
        (2, -1), (2, 0), (2, 1), (2, 2), (2, 3),
        (3, -1), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
        (4, 0), (4, 1), (4, 2), (4, 3), (4, 4),
        (5, 1), (5, 2), (5, 3),
    ),
    15: (
        (0, 0), (0, 1), (0, 2), (0, 3),
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
        (4, 0), (4, 1), (4, 2), (4, 3), (4, 4),
        (5, 1), (5, 2), (5, 3), (5, 4),
    ),
    16: (
        (0, 0), (0, 1), (0, 2), (0, 3),
        (1, -1), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
        (2, -1), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
        (3, -1), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
        (4, -1), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4),
        (5, 0), (5, 1), (5, 2), (5, 3),
    ),
    17: (
        (0, 0),
        (6, 3), (6, 2), (6, 1),
        (5, 4), (5, 3), (5, 2), (5, 1), (5, 0),
        (4, 4), (4, 3), (4, 2), (4, 1), (4, 0), (4, -1),
        (3, 4), (3, 3), (3, 2), (3, 1), (3, 0), (3, -1),
        (2, 3), (2, 2), (2, 1), (2, 0), (2, -1),
        (1, 3), (1, 2), (1, 1), (1, 0), (1, -1),
        (0, 1),
    ),
    18: (
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2), (1, 3),
        (2, -1), (2, 0), (2, 1), (2, 2), (2, 3),
        (3, -1), (3, 0), (3, 1), (3, 2), (3, 3),
        (4, -1), (4, 0), (4, 1), (4, 2), (4, 3),
        (5, -1), (5, 0), (5, 1), (5, 2), (5, 3),
        (6, 0), (6, 1), (6, 2), (6, 3),
        (7, 0), (7, 1), (7, 2),
    ),
    19: (
        (0, 0), (0, 1), (0, 2), (0, 3),
        (1, -1), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
        (2, -1), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
        (3, -1), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
        (4, -1), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4),
        (5, -1), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4),
        (6, 0), (6, 1), (6, 2), (6, 3),
    ),
    20: (
        (0, 0), (0, 1), (0, 2), (1, -1), (1, 0), (1, 1),
        (1, 2), (1, 3), (1, 4), (2, -1), (2, 0), (2, 1),
        (2, 2), (2, 3), (2, 4), (3, -1), (3, 0), (3, 1),
        (3, 2), (3, 3), (3, 4), (3, 5), (4, -1), (4, 0),
        (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (5, 0),
        (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (6, 1),
        (6, 2), (6, 3), (6, 4),
    ),
    21: (
        (0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1),
        (1, 2), (1, 3), (1, 4), (1, 5), (2, -1), (2, 0),
        (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (3, -1),
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
        (4, -1), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4),
        (4, 5), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4),
        (5, 5), (6, 1), (6, 2), (6, 3), (6, 4),
    ),
}

EXPECTED = {n: len(points) for n, points in WITNESSES.items()}


# ---------- Producer arithmetic ----------


def dist2(p: Point, q: Point) -> int:
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def twice_area(p: Point, q: Point, r: Point) -> int:
    return abs(
        (q[0] - p[0]) * (r[1] - p[1])
        - (q[1] - p[1]) * (r[0] - p[0])
    )


def gap(n: int, p: Point, q: Point, r: Point) -> int:
    """Positive exactly when the N-avoiding inequality holds."""

    a2 = twice_area(p, q, r)
    d2 = max(dist2(p, q), dist2(p, r), dist2(q, r))
    return (a2 - 2 * n) ** 2 - 4 * d2


def avoids_fast(n: int, points: Sequence[Point]) -> bool:
    return all(
        gap(n, p, q, r) > 0
        for p, q, r in combinations_with_replacement(points, 3)
    )


# ---------- Independent audit arithmetic ----------


def dist2_audit(p: Point, q: Point) -> int:
    # Dot-product expansion, rather than the producer's difference-of-squares.
    return (
        p[0] * p[0] + p[1] * p[1]
        + q[0] * q[0] + q[1] * q[1]
        - 2 * (p[0] * q[0] + p[1] * q[1])
    )


def twice_area_audit(p: Point, q: Point, r: Point) -> int:
    # Shoelace formula, rather than the producer's based-vector determinant.
    return abs(
        p[0] * q[1] + q[0] * r[1] + r[0] * p[1]
        - p[1] * q[0] - q[1] * r[0] - r[1] * p[0]
    )


def gap_audit(n: int, p: Point, q: Point, r: Point) -> int:
    a2 = twice_area_audit(p, q, r)
    d2 = max(dist2_audit(p, q), dist2_audit(p, r), dist2_audit(q, r))
    return (a2 - 2 * n) ** 2 - 4 * d2


def avoids_audit(n: int, points: Sequence[Point]) -> bool:
    return all(
        gap_audit(n, p, q, r) > 0
        for p, q, r in combinations_with_replacement(points, 3)
    )


def witness_stats(n: int, points: Sequence[Point]) -> dict[str, int]:
    assert len(points) == len(set(points)), f"duplicate point in N={n} witness"
    minimum: int | None = None
    maximum_d2 = 0
    maximum_a2 = 0
    count = 0
    for p, q, r in combinations_with_replacement(points, 3):
        g = gap_audit(n, p, q, r)
        assert g > 0, f"invalid N={n} witness triple {(p, q, r)}: gap={g}"
        minimum = g if minimum is None else min(minimum, g)
        maximum_d2 = max(
            maximum_d2,
            dist2_audit(p, q),
            dist2_audit(p, r),
            dist2_audit(q, r),
        )
        maximum_a2 = max(maximum_a2, twice_area_audit(p, q, r))
        count += 1
    assert count == math.comb(len(points) + 2, 3)
    assert minimum is not None
    return {
        "triples": count,
        "min_gap": minimum,
        "max_diameter_squared": maximum_d2,
        "max_twice_area": maximum_a2,
    }


# ---------- Exhaustive diameter-pair reduction ----------


def normalized_vectors(n: int) -> tuple[Point, ...]:
    """One representative of every nonzero D4 orbit with squared norm < N^2."""

    vectors = [
        (x, y)
        for x in range(1, n)
        for y in range(0, x + 1)
        if x * x + y * y < n * n
    ]
    return tuple(sorted(vectors, key=lambda p: (dist2(A, p), p[0], p[1])))


def normalized_vectors_audit(n: int) -> tuple[Point, ...]:
    """Construct the same orbit set by normalizing every signed raw vector."""

    representatives: set[Point] = set()
    for x in range(-(n - 1), n):
        for y in range(-(n - 1), n):
            if (x, y) == A or x * x + y * y >= n * n:
                continue
            ax, ay = abs(x), abs(y)
            representatives.add((max(ax, ay), min(ax, ay)))
    return tuple(
        sorted(
            representatives,
            key=lambda p: (dist2_audit(A, p), p[0], p[1]),
        )
    )


def base_candidates(n: int, b: Point) -> tuple[Point, ...]:
    """All possible third points after fixing A,B as a diameter pair."""

    diameter2 = dist2(A, b)
    out: list[Point] = []
    # Any q in the lens has |q-A| <= |B-A| < N, hence each coordinate
    # lies in this complete finite interval.
    for x in range(-(n - 1), n):
        for y in range(-(n - 1), n):
            p = (x, y)
            if p in (A, b):
                continue
            if dist2(A, p) > diameter2 or dist2(b, p) > diameter2:
                continue
            if gap(n, A, b, p) > 0:
                out.append(p)
    return tuple(out)


def base_candidates_audit(n: int, b: Point) -> tuple[Point, ...]:
    diameter2 = dist2_audit(A, b)
    out: list[Point] = []
    for x in range(-(n - 1), n):
        for y in range(-(n - 1), n):
            p = (x, y)
            if p in (A, b):
                continue
            if (
                dist2_audit(A, p) <= diameter2
                and dist2_audit(b, p) <= diameter2
                and avoids_audit(n, (A, b, p))
            ):
                out.append(p)
    return tuple(out)


def extension_safe_fast(
    n: int,
    diameter2: int,
    forced: Sequence[Point],
    p: Point,
) -> bool:
    if any(dist2(p, q) > diameter2 for q in forced):
        return False
    return avoids_fast(n, tuple(forced) + (p,))


def extension_safe_audit(
    n: int,
    diameter2: int,
    forced: Sequence[Point],
    p: Point,
) -> bool:
    if any(dist2_audit(p, q) > diameter2 for q in forced):
        return False
    return avoids_audit(n, tuple(forced) + (p,))


def pair_compatible_fast(
    n: int,
    diameter2: int,
    forced: Sequence[Point],
    p: Point,
    q: Point,
) -> bool:
    """Whether two individually safe candidates may coexist with forced."""

    if dist2(p, q) > diameter2:
        return False
    if gap(n, p, p, q) <= 0 or gap(n, p, q, q) <= 0:
        return False
    return all(gap(n, p, q, r) > 0 for r in forced)


# ---------- Coloring-certificate production and direct audit ----------


def greedy_certificate(
    n: int,
    diameter2: int,
    forced: Sequence[Point],
    pool: Sequence[Point],
) -> tuple[int, ...]:
    size = len(pool)
    adjacency = [0] * size
    for i, p in enumerate(pool):
        for j in range(i + 1, size):
            if pair_compatible_fast(n, diameter2, forced, p, pool[j]):
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i

    colors = [-1] * size
    order = sorted(
        range(size),
        key=lambda i: (adjacency[i].bit_count(), i),
        reverse=True,
    )
    for i in order:
        used = 0
        neighbors = adjacency[i]
        while neighbors:
            lowbit = neighbors & -neighbors
            j = lowbit.bit_length() - 1
            if colors[j] >= 0:
                used |= 1 << colors[j]
            neighbors ^= lowbit
        color = 0
        while used & (1 << color):
            color += 1
        colors[i] = color
    return tuple(colors)


def audit_certificate(
    *,
    n: int,
    b: Point,
    branch: str,
    forced: tuple[Point, ...],
    pool: tuple[Point, ...],
    expected_pool: tuple[Point, ...],
    colors: tuple[int, ...],
    digest: hashlib._Hash,
) -> dict[str, int]:
    diameter2 = dist2_audit(A, b)
    assert avoids_audit(n, forced), (n, b, branch, "forced set is not avoiding")
    assert max(
        (dist2_audit(p, q) for p, q in combinations(forced, 2)),
        default=0,
    ) <= diameter2
    assert pool == expected_pool, (n, b, branch, "candidate-pool mismatch")
    assert len(pool) == len(colors)
    assert len(pool) == len(set(pool))
    for p in pool:
        assert extension_safe_audit(n, diameter2, forced, p)

    if colors:
        color_count = max(colors) + 1
        assert min(colors) == 0
        assert set(colors) == set(range(color_count))
    else:
        color_count = 0

    groups: dict[int, list[Point]] = defaultdict(list)
    for p, color in zip(pool, colors):
        groups[color].append(p)

    checked_pairs = 0
    for group in groups.values():
        for p, q in combinations(group, 2):
            # Same-color vertices must be incompatible.  This full audit
            # enumerates all triples of forced union {p,q}, independently of
            # the optimized compatibility predicate used by the producer.
            assert (
                dist2_audit(p, q) > diameter2
                or not avoids_audit(n, forced + (p, q))
            ), (
                n,
                b,
                branch,
                p,
                q,
                "same-color pair is compatible and respects the fixed diameter",
            )
            checked_pairs += 1

    record = {
        "N": n,
        "B": b,
        "branch": branch,
        "forced": forced,
        "pool": pool,
        "colors": colors,
    }
    digest.update(
        json.dumps(record, sort_keys=True, separators=(",", ":")).encode("ascii")
        + b"\n"
    )
    return {
        "color_count": color_count,
        "pool_size": len(pool),
        "same_color_pairs_checked": checked_pairs,
    }


def audit_n17_tight_low_branch(
    pool: tuple[Point, ...],
    digest: hashlib._Hash,
) -> dict[str, object]:
    """Close the sole branch where pair-coloring alone loses one point.

    For N=17 and diameter vector B=(5,4), the low pool has 40 points.  Its
    incompatibility graph has a matching of size nine.  If 31 pool points
    were pairwise compatible, the omitted nine points would be a vertex
    cover and would have to choose exactly one endpoint of each matching
    edge.  We audit all 2^9 choices.  Only two cover all incompatibility
    edges, and each remaining 31-set contains a forbidden triple.
    """

    n = 17
    b = (5, 4)
    forced = (A, b)
    diameter2 = dist2_audit(A, b)
    assert len(pool) == 40 and len(set(pool)) == 40

    incompatible: set[frozenset[Point]] = set()
    for p, q in combinations(pool, 2):
        if (
            dist2_audit(p, q) > diameter2
            or not avoids_audit(n, forced + (p, q))
        ):
            incompatible.add(frozenset((p, q)))
    assert len(incompatible) == 48

    matching: tuple[tuple[Point, Point], ...] = (
        ((-1, 2), (4, 0)),
        ((-1, 3), (3, 0)),
        ((0, 3), (4, -1)),
        ((0, 4), (2, -1)),
        ((1, -1), (4, 5)),
        ((1, 4), (6, 1)),
        ((1, 5), (5, 1)),
        ((2, 5), (5, 0)),
        ((3, 5), (6, 2)),
    )
    endpoints = [p for edge in matching for p in edge]
    assert len(endpoints) == len(set(endpoints)) == 18
    assert all(p in pool for p in endpoints)
    assert all(frozenset(edge) in incompatible for edge in matching)

    covers: list[tuple[Point, ...]] = []
    survivors: list[tuple[Point, ...]] = []
    bad_triples: list[tuple[Point, Point, Point, int]] = []
    for mask in range(1 << len(matching)):
        cover = frozenset(
            edge[(mask >> i) & 1]
            for i, edge in enumerate(matching)
        )
        assert len(cover) == 9
        if not all(edge & cover for edge in incompatible):
            continue
        chosen = tuple(p for p in pool if p not in cover)
        assert len(chosen) == 31
        # The cover condition directly rechecks pairwise compatibility.
        assert all(
            frozenset((p, q)) not in incompatible
            for p, q in combinations(chosen, 2)
        )
        bad = [
            (p, q, r, gap_audit(n, p, q, r))
            for p, q, r in combinations(chosen, 3)
            if gap_audit(n, p, q, r) <= 0
        ]
        assert len(bad) == 1 and bad[0][3] == -4
        covers.append(tuple(sorted(cover)))
        survivors.append(chosen)
        bad_triples.extend(bad)

    expected_bad = {
        frozenset(((0, 3), (3, -1), (4, 5))),
        frozenset(((1, -1), (2, 5), (5, 1))),
    }
    assert len(covers) == 2
    assert {frozenset(t[:3]) for t in bad_triples} == expected_bad

    record = {
        "N": n,
        "B": b,
        "branch": "no-high-tight-cover",
        "pool": pool,
        "incompatible_edges": sorted(tuple(sorted(e)) for e in incompatible),
        "matching": matching,
        "covers": covers,
        "bad_triples": bad_triples,
    }
    digest.update(
        json.dumps(record, sort_keys=True, separators=(",", ":")).encode("ascii")
        + b"\n"
    )
    return {
        "pool_size": len(pool),
        "incompatible_edges": len(incompatible),
        "matching_size": len(matching),
        "endpoint_choices": 1 << len(matching),
        "surviving_covers": len(covers),
        "bad_triples": len(bad_triples),
        "candidate_cap": 30,
    }


def audit_n18_tight_low_branch(
    pool: tuple[Point, ...],
    digest: hashlib._Hash,
) -> dict[str, object]:
    """Close the sole N=18 branch where pair-coloring loses one point.

    For B=(5,4), the no-high pool has 42 points.  Its incompatibility graph
    contains a matching of size nine.  Any pairwise-compatible 33-subset
    would omit a nine-vertex cover and hence exactly one endpoint of every
    matching edge.  Of the 2^9 endpoint choices only two are vertex covers;
    both surviving 33-sets contain forbidden triples.
    """

    n = 18
    b = (5, 4)
    forced = (A, b)
    diameter2 = dist2_audit(A, b)
    assert len(pool) == 42 and len(set(pool)) == 42

    incompatible: set[frozenset[Point]] = set()
    for p, q in combinations(pool, 2):
        if (
            dist2_audit(p, q) > diameter2
            or not avoids_audit(n, forced + (p, q))
        ):
            incompatible.add(frozenset((p, q)))
    assert len(incompatible) == 57

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
    endpoints = [p for edge in matching for p in edge]
    assert len(endpoints) == len(set(endpoints)) == 18
    assert all(p in pool for p in endpoints)
    assert all(frozenset(edge) in incompatible for edge in matching)

    covers: list[tuple[Point, ...]] = []
    bad_triples: list[tuple[Point, Point, Point, int]] = []
    for mask in range(1 << len(matching)):
        cover = frozenset(
            edge[(mask >> i) & 1]
            for i, edge in enumerate(matching)
        )
        assert len(cover) == 9
        if not all(edge & cover for edge in incompatible):
            continue
        chosen = tuple(p for p in pool if p not in cover)
        assert len(chosen) == 33
        assert all(
            frozenset((p, q)) not in incompatible
            for p, q in combinations(chosen, 2)
        )
        bad = [
            (p, q, r, gap_audit(n, p, q, r))
            for p, q, r in combinations(chosen, 3)
            if gap_audit(n, p, q, r) <= 0
        ]
        assert len(bad) == 2
        assert all(item[3] == -15 for item in bad)
        covers.append(tuple(sorted(cover)))
        bad_triples.extend(bad)

    expected_bad = {
        frozenset(((1, -1), (1, 4), (6, 1))),
        frozenset(((1, -1), (1, 4), (6, 2))),
        frozenset(((-1, 2), (4, 0), (4, 5))),
        frozenset(((-1, 3), (4, 0), (4, 5))),
    }
    assert len(covers) == 2
    assert {frozenset(t[:3]) for t in bad_triples} == expected_bad

    record = {
        "N": n,
        "B": b,
        "branch": "no-high-tight-cover",
        "pool": pool,
        "incompatible_edges": sorted(tuple(sorted(e)) for e in incompatible),
        "matching": matching,
        "covers": covers,
        "bad_triples": bad_triples,
    }
    digest.update(
        json.dumps(record, sort_keys=True, separators=(",", ":")).encode("ascii")
        + b"\n"
    )
    return {
        "pool_size": len(pool),
        "incompatible_edges": len(incompatible),
        "matching_size": len(matching),
        "endpoint_choices": 1 << len(matching),
        "surviving_covers": len(covers),
        "bad_triples": len(bad_triples),
        "candidate_cap": 32,
    }


def prove_one_n(n: int) -> dict[str, object]:
    started = time.perf_counter()
    witness = WITNESSES[n]
    lower_stats = witness_stats(n, witness)
    target = len(witness)

    vectors = normalized_vectors(n)
    assert vectors == normalized_vectors_audit(n)

    digest = hashlib.sha256()
    global_upper = 1
    tight_vectors: list[Point] = []
    high_cases = 0
    certificate_count = 0
    high_branch_count = 0
    pool_memberships = 0
    same_color_pairs = 0
    max_pool = 0
    tight_cover_audit: dict[str, object] | None = None

    for b in vectors:
        diameter2 = dist2(A, b)
        assert diameter2 < n * n

        base = base_candidates(n, b)
        base_check = base_candidates_audit(n, b)
        assert base == base_check, (n, b, "base-candidate mismatch")

        low = tuple(p for p in base if twice_area(A, b, p) < 2 * n)
        high = tuple(p for p in base if twice_area(A, b, p) > 2 * n)
        low_check = tuple(p for p in base_check if twice_area_audit(A, b, p) < 2 * n)
        high_check = tuple(p for p in base_check if twice_area_audit(A, b, p) > 2 * n)
        assert low == low_check and high == high_check
        assert len(low) + len(high) == len(base)
        if high:
            high_cases += 1

        forced_low = (A, b)
        pool_low = tuple(
            p
            for p in low
            if extension_safe_fast(n, diameter2, forced_low, p)
        )
        expected_low = tuple(
            p
            for p in low_check
            if extension_safe_audit(n, diameter2, forced_low, p)
        )
        colors_low = greedy_certificate(n, diameter2, forced_low, pool_low)
        audit = audit_certificate(
            n=n,
            b=b,
            branch="no-high",
            forced=forced_low,
            pool=pool_low,
            expected_pool=expected_low,
            colors=colors_low,
            digest=digest,
        )
        certificate_count += 1
        pool_memberships += audit["pool_size"]
        same_color_pairs += audit["same_color_pairs_checked"]
        max_pool = max(max_pool, audit["pool_size"])
        case_upper = 2 + audit["color_count"]
        if n == 17 and b == (5, 4):
            assert case_upper == 33
            tight_cover_audit = audit_n17_tight_low_branch(pool_low, digest)
            case_upper = 2 + int(tight_cover_audit["candidate_cap"])
        elif n == 18 and b == (5, 4):
            assert case_upper == 35
            tight_cover_audit = audit_n18_tight_low_branch(pool_low, digest)
            case_upper = 2 + int(tight_cover_audit["candidate_cap"])

        # Every avoiding set containing at least one high candidate appears in
        # at least one of these branches; we deliberately enumerate all H.
        assert len(set(high)) == len(high)
        for h in high:
            forced_high = (A, b, h)
            pool_high = tuple(
                p
                for p in base
                if p != h
                and extension_safe_fast(n, diameter2, forced_high, p)
            )
            expected_high = tuple(
                p
                for p in base_check
                if p != h
                and extension_safe_audit(n, diameter2, forced_high, p)
            )
            colors_high = greedy_certificate(
                n,
                diameter2,
                forced_high,
                pool_high,
            )
            audit = audit_certificate(
                n=n,
                b=b,
                branch=f"high:{h[0]},{h[1]}",
                forced=forced_high,
                pool=pool_high,
                expected_pool=expected_high,
                colors=colors_high,
                digest=digest,
            )
            certificate_count += 1
            high_branch_count += 1
            pool_memberships += audit["pool_size"]
            same_color_pairs += audit["same_color_pairs_checked"]
            max_pool = max(max_pool, audit["pool_size"])
            case_upper = max(case_upper, 3 + audit["color_count"])

        if case_upper > global_upper:
            global_upper = case_upper
            tight_vectors = [b]
        elif case_upper == global_upper:
            tight_vectors.append(b)

    assert global_upper == target, (
        f"N={n}: certificate upper bound {global_upper} "
        f"does not match witness size {target}"
    )
    elapsed = time.perf_counter() - started
    return {
        "N": n,
        "f(N)": target,
        "witness_triples": lower_stats["triples"],
        "witness_min_gap": lower_stats["min_gap"],
        "diameter_cases": len(vectors),
        "cases_with_high": high_cases,
        "high_branches": high_branch_count,
        "certificates": certificate_count,
        "pool_memberships": pool_memberships,
        "same_color_pairs_audited": same_color_pairs,
        "max_branch_pool": max_pool,
        "tight_vectors": tight_vectors,
        "tight_cover_audit": tight_cover_audit,
        "certificate_sha256": digest.hexdigest(),
        "seconds": elapsed,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reverify exact Koizumi-model values for Erdos #352."
    )
    parser.add_argument("--min-n", type=int, default=8)
    parser.add_argument("--max-n", type=int, default=21)
    parser.add_argument(
        "--json",
        action="store_true",
        help="print one canonical JSON result per N",
    )
    args = parser.parse_args()

    available = sorted(WITNESSES)
    if args.min_n > args.max_n:
        parser.error("--min-n must not exceed --max-n")
    requested = list(range(args.min_n, args.max_n + 1))
    missing = [n for n in requested if n not in WITNESSES]
    if missing:
        parser.error(f"no embedded witness for N={missing}; available range is {available}")

    total_started = time.perf_counter()
    results = []
    for n in requested:
        result = prove_one_n(n)
        results.append(result)
        if args.json:
            print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        else:
            tight = ";".join(f"{x},{y}" for x, y in result["tight_vectors"])
            print(
                f"N={n:2d} f(N)={result['f(N)']:2d} "
                f"witness_triples={result['witness_triples']:4d} "
                f"min_gap={result['witness_min_gap']:3d} "
                f"B_cases={result['diameter_cases']:3d} "
                f"high_branches={result['high_branches']:5d} "
                f"certs={result['certificates']:5d} "
                f"same_color_pairs={result['same_color_pairs_audited']:6d} "
                f"tight_B={tight} "
                f"sha256={result['certificate_sha256']} "
                f"seconds={result['seconds']:.3f}"
            )

    total = time.perf_counter() - total_started
    expected_table = [EXPECTED[n] for n in requested]
    observed_table = [int(result["f(N)"]) for result in results]
    assert observed_table == expected_table
    print(
        f"ALL CHECKS PASSED for N={args.min_n}..{args.max_n}; "
        f"exact table={observed_table}; total_seconds={total:.3f}"
    )


if __name__ == "__main__":
    main()
