#!/usr/bin/env python3
"""Exact audit of the local-universality construction for Erdos #352.

This is finite evidence for a completely proved all-N lemma in REPORT.md.
All checks use integers; assertions must not be disabled.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from itertools import combinations, combinations_with_replacement

Point = tuple[int, int]


def egcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        g = abs(a)
        return g, (1 if a >= 0 else -1), 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def det(p: Point, q: Point) -> int:
    return p[0] * q[1] - p[1] * q[0]


def dot(p: Point, q: Point) -> int:
    return p[0] * q[0] + p[1] * q[1]


def sub(p: Point, q: Point) -> Point:
    return p[0] - q[0], p[1] - q[1]


def dist2(p: Point, q: Point) -> int:
    z = sub(p, q)
    return dot(z, z)


def twice_area(p: Point, q: Point, r: Point) -> int:
    return abs(det(sub(q, p), sub(r, p)))


def margin(n: int, p: Point, q: Point, r: Point) -> int:
    a2 = twice_area(p, q, r)
    diameter2 = max(dist2(p, q), dist2(p, r), dist2(q, r))
    return (a2 - 2 * n) ** 2 - 4 * diameter2


def construct(n: int, d: Point) -> tuple[tuple[Point, ...], int, int, int]:
    a, b = d
    s = dot(d, d)
    assert s > 0 and 10_000 * s <= n * n
    g, x, y = egcd(a, b)
    assert x * a + y * b == g == math.gcd(abs(a), abs(b))

    # k is exactly ceil(16 sqrt(s) / g), without floating point.
    k = math.isqrt((256 * s) // (g * g))
    while k * k * g * g < 256 * s:
        k += 1
    while k > 0 and (k - 1) * (k - 1) * g * g >= 256 * s:
        k -= 1
    t = k * g
    assert t * t >= 256 * s
    assert (t - g) * (t - g) < 256 * s

    # det((y,-x),d)=g.  Shift along d/g to put the dot product in
    # [0,s/g); this preserves the determinant.
    v = (k * y, -k * x)
    period = s // g
    shift = dot(v, d) // period
    v = (v[0] - shift * a // g, v[1] - shift * b // g)
    assert det(v, d) == t
    assert 0 <= dot(v, d) < period

    # M is exactly floor(n/(4 sqrt(s))).
    m = math.isqrt((n * n) // (16 * s))
    while 16 * (m + 1) * (m + 1) * s <= n * n:
        m += 1
    while 16 * m * m * s > n * n:
        m -= 1
    assert m >= 25

    # L is exactly floor(n/(20 sqrt(s))).  The complete construction has
    # H-jd, 1<=j<=L, as a clique of candidates in the fixed-high branch.
    ell = math.isqrt((n * n) // (400 * s))
    while 400 * (ell + 1) * (ell + 1) * s <= n * n:
        ell += 1
    while 400 * ell * ell * s > n * n:
        ell -= 1
    assert ell >= 5 and ell < m

    o = (0, 0)
    h = (m * a, m * b)
    big_b = (h[0] + v[0], h[1] + v[1])
    p = ((m - 2) * a, (m - 2) * b)
    q = ((m - 1) * a, (m - 1) * b)
    assert sub(q, p) == d
    return (o, big_b, h, p, q), m, ell, t


def audit_one(n: int, d: Point) -> dict[str, object]:
    points, m, ell, t = construct(n, d)
    o, b, h, p, q = points
    assert len(set(points)) == 5
    diameter2 = dist2(o, b)
    assert diameter2 == max(dist2(x, y) for x, y in combinations(points, 2))
    assert diameter2 < n * n

    gaps = [margin(n, x, y, z) for x, y, z in combinations_with_replacement(points, 3)]
    assert len(gaps) == 35 and min(gaps) > 0

    high_a2 = twice_area(o, b, h)
    assert high_a2 > 2 * n
    assert (high_a2 - 2 * n) ** 2 > 4 * diameter2

    # The largest within-cluster coefficient gap is ell and is low; the
    # smallest gap from O to that cluster is m-ell and is high.  Monotonicity
    # then checks the entire arithmetic-progression clique without expanding
    # it or trusting a graph routine.
    max_low_a2 = ell * t
    assert max_low_a2 < 2 * n
    assert (2 * n - max_low_a2) ** 2 > 4 * diameter2
    min_high_a2 = (m - ell) * t
    assert min_high_a2 > 2 * n
    assert (min_high_a2 - 2 * n) ** 2 > 4 * diameter2

    # P,Q are an actual compatible pair in the branch forced by O,B,H.
    forced = (o, b, h)
    assert all(margin(n, *triple) > 0 for triple in combinations_with_replacement(forced + (p,), 3))
    assert all(margin(n, *triple) > 0 for triple in combinations_with_replacement(forced + (q,), 3))
    assert all(margin(n, *triple) > 0 for triple in combinations_with_replacement(forced + (p, q), 3))

    return {
        "N": n,
        "d": d,
        "points": points,
        "diameter2": diameter2,
        "high_twice_area": high_a2,
        "min_margin": min(gaps),
        "progression_clique_size": ell,
    }


def main() -> None:
    records: list[dict[str, object]] = []
    deterministic = (100, 127, 251, 509, 1000, 4096, 10_000)
    for n in deterministic:
        radius = n // 100
        for a in range(-radius, radius + 1):
            for b in range(-radius, radius + 1):
                if (a, b) != (0, 0) and 10_000 * (a * a + b * b) <= n * n:
                    records.append(audit_one(n, (a, b)))

    rng = random.Random(352_100_016)
    random_cases = 10_000
    for _ in range(random_cases):
        n = rng.randrange(100, 1_000_001)
        radius = n // 100
        while True:
            d = (rng.randint(-radius, radius), rng.randint(-radius, radius))
            if d != (0, 0) and 10_000 * dot(d, d) <= n * n:
                break
        records.append(audit_one(n, d))

    digest = hashlib.sha256()
    for record in records:
        digest.update(json.dumps(record, sort_keys=True, separators=(",", ":")).encode("ascii") + b"\n")
    example = audit_one(100, (1, 0))
    print(f"deterministic_N={list(deterministic)} random_cases={random_cases}")
    print(f"total_cases={len(records)} trace_sha256={digest.hexdigest()}")
    print("example_N100_d10=" + json.dumps(example, separators=(",", ":")))
    print("ALL EXACT CHECKS PASSED")


if __name__ == "__main__":
    main()
