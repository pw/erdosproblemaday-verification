#!/usr/bin/env python3
"""Independent hostile audit for the Erdős #352 local-universality lemma.

This deliberately does not import the producer.  It builds the Bézout
solution by a separate iterative routine, materializes the full progression
on a deterministic test grid, checks every pair and every repeated triple,
and separately tests the endpoint inequalities on much larger signed cases.
Assertions must remain enabled.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import random

Point = tuple[int, int]


def xgcd_signed(a: int, b: int) -> tuple[int, int, int]:
    """Return positive gcd and signed Bézout coefficients, iteratively."""
    aa, bb = abs(a), abs(b)
    old_r, r = aa, bb
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    sx = old_s if a >= 0 else -old_s
    sy = old_t if b >= 0 else -old_t
    assert old_r > 0 and sx * a + sy * b == old_r
    return old_r, sx, sy


def dot(a: Point, b: Point) -> int:
    return a[0] * b[0] + a[1] * b[1]


def det(a: Point, b: Point) -> int:
    return a[0] * b[1] - a[1] * b[0]


def minus(a: Point, b: Point) -> Point:
    return a[0] - b[0], a[1] - b[1]


def d2(a: Point, b: Point) -> int:
    return dot(minus(a, b), minus(a, b))


def area2(a: Point, b: Point, c: Point) -> int:
    # Shoelace path, rather than the producer's based-vector determinant.
    return abs(a[0] * b[1] + b[0] * c[1] + c[0] * a[1]
               - a[1] * b[0] - b[1] * c[0] - c[1] * a[0])


def good(n: int, a: Point, b: Point, c: Point) -> bool:
    twice_error = abs(area2(a, b, c) - 2 * n)
    diam2 = max(d2(a, b), d2(a, c), d2(b, c))
    return twice_error * twice_error > 4 * diam2


def floor_ratio_sqrt(numer: int, denom: int) -> int:
    """floor(sqrt(numer/denom)) for positive integers."""
    q = math.isqrt(numer // denom)
    assert q * q * denom <= numer < (q + 1) * (q + 1) * denom
    return q


def make(n: int, d: Point) -> dict[str, object]:
    dx, dy = d
    norm2 = dot(d, d)
    assert norm2 and 10_000 * norm2 <= n * n

    g, bx, by = xgcd_signed(dx, dy)
    # Minimal k with (kg)^2 >= 256 |d|^2.
    root = math.isqrt(256 * norm2)
    k = (root + g - 1) // g
    while (k * g) ** 2 < 256 * norm2:
        k += 1
    while k > 1 and ((k - 1) * g) ** 2 >= 256 * norm2:
        k -= 1
    t = k * g

    # det((by,-bx),d)=g.  Euclidean divmod gives the normalized dot.
    raw_v = (k * by, -k * bx)
    period = norm2 // g
    shift, residue = divmod(dot(raw_v, d), period)
    v = (raw_v[0] - shift * dx // g,
         raw_v[1] - shift * dy // g)
    assert det(v, d) == t
    assert dot(v, d) == residue and 0 <= residue < period

    m = floor_ratio_sqrt(n * n, 16 * norm2)
    ell = floor_ratio_sqrt(n * n, 400 * norm2)
    assert m >= 25 and 5 <= ell < m

    o = (0, 0)
    h = (m * dx, m * dy)
    b = (h[0] + v[0], h[1] + v[1])
    cluster = tuple(((m - j) * dx, (m - j) * dy)
                    for j in range(1, ell + 1))
    points = (o, b, h) + cluster
    return {
        "d": d, "g": g, "t": t, "v": v, "m": m, "ell": ell,
        "o": o, "b": b, "h": h, "cluster": cluster, "points": points,
    }


def endpoint_audit(n: int, d: Point) -> dict[str, int | Point]:
    z = make(n, d)
    g, t, v = int(z["g"]), int(z["t"]), z["v"]
    m, ell = int(z["m"]), int(z["ell"])
    o, b, h = z["o"], z["b"], z["h"]
    norm2 = dot(d, d)
    vd = dot(v, d)
    diameter2 = d2(o, b)

    # Exact forms of every radical bound used in the prose proof.
    assert t * t >= 256 * norm2
    assert (t - g) * (t - g) < 256 * norm2
    assert g * g <= norm2
    assert 0 <= vd < norm2 // g
    assert norm2 * dot(v, v) == vd * vd + t * t
    assert 10_000 * diameter2 < 1849 * n * n       # D < 0.43 N
    assert diameter2 < n * n

    # O,B remain a diameter pair for every progression vertex: the squared
    # B-distance is f(j)=|jd+v|^2 and f is nondecreasing for j>=0.
    assert d2(o, h) <= diameter2
    for j in (0, 1, ell):
        x = ((m - j) * d[0], (m - j) * d[1])
        assert d2(b, x) <= diameter2
        assert d2(o, x) <= diameter2

    max_low_a2 = ell * t
    min_high_a2 = (m - ell) * t
    high_a2 = m * t
    assert max_low_a2 < 2 * n
    assert (2 * n - max_low_a2) ** 2 > 4 * diameter2
    assert min_high_a2 > 2 * n
    assert (min_high_a2 - 2 * n) ** 2 > 4 * diameter2
    assert high_a2 > 2 * n
    assert (high_a2 - 2 * n) ** 2 > 4 * diameter2

    q, p = z["cluster"][0], z["cluster"][1]
    assert minus(q, p) == d
    return {"N": n, "d": d, "D2": diameter2, "M": m,
            "L": ell, "t": t}


def materialized_audit(n: int, d: Point) -> dict[str, int | Point]:
    z = make(n, d)
    points = z["points"]
    assert len(points) == len(set(points))
    diameter2 = d2(z["o"], z["b"])
    pairs = 0
    for a, b in itertools.combinations(points, 2):
        pairs += 1
        assert d2(a, b) <= diameter2
    triples = 0
    min_margin = None
    for a, b, c in itertools.combinations_with_replacement(points, 3):
        triples += 1
        e2 = (area2(a, b, c) - 2 * n) ** 2
        dd = max(d2(a, b), d2(a, c), d2(b, c))
        margin = e2 - 4 * dd
        assert margin > 0
        min_margin = margin if min_margin is None else min(min_margin, margin)
    assert area2(z["o"], z["b"], z["h"]) > 2 * n
    assert minus(z["cluster"][0], z["cluster"][1]) == d
    return {"N": n, "d": d, "points": len(points), "pairs": pairs,
            "triples": triples, "min_margin": int(min_margin)}


def main() -> None:
    trace = hashlib.sha256()
    endpoint_cases = 0
    materialized_cases = 0
    materialized_triples = 0

    # All signed admissible vectors for boundary-rich deterministic N values.
    for n in (100, 101, 127, 199, 251, 509, 997, 2000):
        r = n // 100
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                if (dx or dy) and 10_000 * (dx * dx + dy * dy) <= n * n:
                    rec = endpoint_audit(n, (dx, dy))
                    endpoint_cases += 1
                    # Materialize the whole AP clique, including all repeated
                    # triples.  This expressly covers all sign quadrants.
                    full = materialized_audit(n, (dx, dy))
                    materialized_cases += 1
                    materialized_triples += int(full["triples"])
                    trace.update(json.dumps(full, sort_keys=True,
                                            separators=(",", ":")).encode())
                    trace.update(b"\n")

    # Large cases audit the proof endpoints without expanding huge cliques.
    rng = random.Random(0x352BADC0DE)
    for _ in range(50_000):
        n = rng.randrange(100, 10_000_001)
        r = n // 100
        while True:
            d = (rng.randint(-r, r), rng.randint(-r, r))
            if d != (0, 0) and 10_000 * dot(d, d) <= n * n:
                break
        rec = endpoint_audit(n, d)
        endpoint_cases += 1
        trace.update(json.dumps(rec, sort_keys=True,
                                separators=(",", ":")).encode())
        trace.update(b"\n")

    # Deliberately exercise axes, primitive/nonprimitive vectors, every sign,
    # equality 100|d|=N when integral, and the smallest N=100 boundary.
    special = [(100, (1, 0)), (100, (-1, 0)), (100, (0, 1)),
               (100, (0, -1)), (500, (3, 4)), (500, (-3, 4)),
               (500, (3, -4)), (500, (-3, -4)), (1000, (6, 8)),
               (1300, (5, 12)), (10_000, (1, -1))]
    for n, d in special:
        rec = materialized_audit(n, d)
        materialized_cases += 1
        materialized_triples += int(rec["triples"])
        endpoint_audit(n, d)
        endpoint_cases += 1
        trace.update(json.dumps(rec, sort_keys=True,
                                separators=(",", ":")).encode())
        trace.update(b"\n")

    print(f"endpoint_cases={endpoint_cases}")
    print(f"materialized_cases={materialized_cases}")
    print(f"materialized_repeated_triples={materialized_triples}")
    print(f"hostile_trace_sha256={trace.hexdigest()}")
    print("ALL INDEPENDENT CHECKS PASSED")


if __name__ == "__main__":
    main()
