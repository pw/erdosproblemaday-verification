#!/usr/bin/env python3
"""Small independent audit of the exceptional N=17, B=(5,4) certificate.

The full upper-bound checker reduces every other normalized diameter branch to
at most 32 points by coloring certificates. Its only 33-point relaxation is
the no-high branch with diameter pair A=(0,0), B=(5,4). This script rebuilds
that branch from the geometric definition and checks the short final
certificate:

* the branch has 40 individually admissible candidates;
* its pair-incompatibility graph has 48 edges;
* nine displayed disjoint edges imply a compatible set has size at most 31;
* all 2^9 ways a compatible 31-set could meet that matching are exhausted;
* only two are pairwise compatible, and each contains a forbidden triple.

It also directly checks the published 32-point lower-bound witness. No
third-party package or floating-point arithmetic is used.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from itertools import combinations, combinations_with_replacement, product


Point = tuple[int, int]
N = 17
A: Point = (0, 0)
B: Point = (5, 4)
D2 = 41

WITNESS: tuple[Point, ...] = (
    (0, 0), (0, 1),
    (1, -1), (1, 0), (1, 1), (1, 2), (1, 3),
    (2, -1), (2, 0), (2, 1), (2, 2), (2, 3),
    (3, -1), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
    (4, -1), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4),
    (5, 0), (5, 1), (5, 2), (5, 3), (5, 4),
    (6, 1), (6, 2), (6, 3),
)

MATCHING: tuple[tuple[Point, Point], ...] = (
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

EXPECTED: dict[tuple[Point, ...], tuple[Point, Point, Point]] = {
    (
        (-1, 2), (-1, 3), (0, 4), (1, -1), (1, 5),
        (4, -1), (5, 0), (6, 1), (6, 2),
    ): ((0, 3), (3, -1), (4, 5)),
    (
        (-1, 2), (-1, 3), (0, 4), (1, 5), (4, -1),
        (4, 5), (5, 0), (6, 1), (6, 2),
    ): ((1, -1), (2, 5), (5, 1)),
}


def distance_squared(p: Point, q: Point) -> int:
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def twice_area(p: Point, q: Point, r: Point) -> int:
    return abs(
        p[0] * q[1] + q[0] * r[1] + r[0] * p[1]
        - p[1] * q[0] - q[1] * r[0] - r[1] * p[0]
    )


def gap(p: Point, q: Point, r: Point) -> int:
    a2 = twice_area(p, q, r)
    diameter2 = max(
        distance_squared(p, q),
        distance_squared(p, r),
        distance_squared(q, r),
    )
    return (a2 - 2 * N) ** 2 - 4 * diameter2


def is_avoiding(points: tuple[Point, ...]) -> bool:
    return all(gap(*triple) > 0 for triple in combinations_with_replacement(points, 3))


def witness_audit() -> dict[str, int | str]:
    assert len(WITNESS) == len(set(WITNESS)) == 32
    gaps = [gap(*triple) for triple in combinations_with_replacement(WITNESS, 3)]
    assert len(gaps) == math.comb(34, 3) == 5984
    assert min(gaps) == 5
    assert all(value > 0 for value in gaps)
    payload = json.dumps(list(WITNESS), separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("ascii")).hexdigest()
    assert digest == "d990dc0cc3a4dcdff1bf28adc3f5fba032cde647f940981e7a7a10f7810f2a39"
    return {"size": 32, "triples": len(gaps), "min_gap": min(gaps), "points_sha256": digest}


def exceptional_branch_audit() -> dict[str, object]:
    assert distance_squared(A, B) == D2

    base: list[Point] = []
    # Every lens point is within sqrt(41) of A, so this much larger box is
    # manifestly complete and avoids relying on a delicate coordinate bound.
    for x in range(-N, N + 1):
        for y in range(-N, N + 1):
            p = (x, y)
            if p in (A, B):
                continue
            if distance_squared(A, p) > D2 or distance_squared(B, p) > D2:
                continue
            if is_avoiding((A, B, p)):
                base.append(p)

    low = tuple(p for p in base if twice_area(A, B, p) < 2 * N)
    high = tuple(p for p in base if twice_area(A, B, p) > 2 * N)
    assert len(base) == len(low) + len(high)
    assert len(low) == 40 and not high
    pool = low
    pool_set = set(pool)
    assert len(pool_set) == 40

    incompatibility_edges = {
        tuple(sorted((p, q)))
        for p, q in combinations(pool, 2)
        if distance_squared(p, q) > D2 or not is_avoiding((A, B, p, q))
    }
    assert len(incompatibility_edges) == 48

    endpoints = [point for edge in MATCHING for point in edge]
    assert len(endpoints) == len(set(endpoints)) == 18
    assert set(endpoints) <= pool_set
    assert all(tuple(sorted(edge)) in incompatibility_edges for edge in MATCHING)

    covers: dict[tuple[Point, ...], tuple[Point, Point, Point]] = {}
    choices = 0
    for bits in product((0, 1), repeat=9):
        choices += 1
        omitted = frozenset(MATCHING[index][bit] for index, bit in enumerate(bits))
        assert len(omitted) == 9
        if any(p not in omitted and q not in omitted for p, q in incompatibility_edges):
            continue

        remaining = tuple(p for p in pool if p not in omitted)
        assert len(remaining) == 31
        assert all(
            distance_squared(p, q) <= D2 and is_avoiding((A, B, p, q))
            for p, q in combinations(remaining, 2)
        )
        bad = tuple(
            triple
            for triple in combinations_with_replacement(remaining, 3)
            if gap(*triple) <= 0
        )
        assert len(bad) == 1
        assert gap(*bad[0]) == -4
        covers[tuple(sorted(omitted))] = bad[0]

    assert choices == 512
    assert covers == EXPECTED

    record = {
        "N": N,
        "B": B,
        "pool": pool,
        "incompatibility_edges": sorted(incompatibility_edges),
        "matching": MATCHING,
        "covers": [
            {"omitted": omitted, "bad_triple": bad, "gap": gap(*bad)}
            for omitted, bad in sorted(covers.items())
        ],
    }
    encoded = json.dumps(record, sort_keys=True, separators=(",", ":")).encode("ascii")
    return {
        "pool_size": len(pool),
        "incompatibility_edges": len(incompatibility_edges),
        "matching_size": len(MATCHING),
        "choices_audited": choices,
        "vertex_covers": len(covers),
        "candidate_upper_bound": 30,
        "obstructions": record["covers"],
        "certificate_sha256": hashlib.sha256(encoded).hexdigest(),
    }


def main() -> None:
    started = time.perf_counter()
    result = {
        "witness": witness_audit(),
        "exceptional_branch": exceptional_branch_audit(),
    }
    result["seconds"] = time.perf_counter() - started
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    print("ALL N=17 MATCHING AUDITS PASSED")


if __name__ == "__main__":
    main()
