#!/usr/bin/env python3
"""Literal-radical audit of the strict N=18 predicate used for Erdős #352."""

from decimal import Decimal, getcontext
from hashlib import sha256
from itertools import combinations_with_replacement
import json
import math


N = 18
ORIGIN = (0, 0)
WITNESS = (
    (0, 0), (0, 1), (0, 2),
    (1, 0), (1, 1), (1, 2), (1, 3),
    (2, -1), (2, 0), (2, 1), (2, 2), (2, 3),
    (3, -1), (3, 0), (3, 1), (3, 2), (3, 3),
    (4, -1), (4, 0), (4, 1), (4, 2), (4, 3),
    (5, -1), (5, 0), (5, 1), (5, 2), (5, 3),
    (6, 0), (6, 1), (6, 2), (6, 3),
    (7, 0), (7, 1), (7, 2),
)


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def distance2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def twice_area(p, q, r):
    return abs(
        p[0] * (q[1] - r[1])
        + q[0] * (r[1] - p[1])
        + r[0] * (p[1] - q[1])
    )


def values(p, q, r):
    a2 = twice_area(p, q, r)
    d2 = max(distance2(p, q), distance2(p, r), distance2(q, r))
    integer = (a2 - 2 * N) ** 2 - 4 * d2
    literal = abs(Decimal(a2) / 2 - Decimal(N)) - Decimal(d2).sqrt()
    return integer, literal


def main() -> None:
    getcontext().prec = 100
    transcript = []

    minimum_literal = None
    witness_checks = 0
    for triple in combinations_with_replacement(WITNESS, 3):
        integer, literal = values(*triple)
        require((literal > 0) == (integer > 0), f"sign mismatch for {triple}")
        require(integer > 0, f"witness failure for {triple}: {integer}")
        minimum_literal = literal if minimum_literal is None else min(minimum_literal, literal)
        witness_checks += 1
    require(witness_checks == 7140, f"wrong witness check count: {witness_checks}")

    raw_vectors = {
        (x, y)
        for x in range(-(N - 1), N)
        for y in range(-(N - 1), N)
        if (x, y) != ORIGIN and x * x + y * y < N * N
    }
    directions = {
        tuple(sorted((abs(x), abs(y)), reverse=True))
        for x, y in raw_vectors
    }
    require(len(directions) == 140, f"wrong direction count: {len(directions)}")
    require(
        sum(4 if y == 0 or x == y else 8 for x, y in directions) == len(raw_vectors),
        "D4 orbit accounting mismatch",
    )

    lens_checks = 0
    zero_margin = []
    closest_nonzero = None
    for b in sorted(directions, key=lambda p: (distance2(ORIGIN, p), p)):
        diameter2 = distance2(ORIGIN, b)
        radius_box = math.isqrt(diameter2)
        for x in range(-radius_box, radius_box + 1):
            for y in range(-radius_box, radius_box + 1):
                p = (x, y)
                if p in (ORIGIN, b):
                    continue
                if distance2(ORIGIN, p) > diameter2 or distance2(b, p) > diameter2:
                    continue
                integer, literal = values(ORIGIN, b, p)
                require((literal > 0) == (integer > 0), f"sign mismatch for B={b}, p={p}")
                if integer == 0:
                    zero_margin.append((b, p, twice_area(ORIGIN, b, p), diameter2))
                else:
                    absolute = abs(integer)
                    closest_nonzero = absolute if closest_nonzero is None else min(closest_nonzero, absolute)
                lens_checks += 1

    require(lens_checks == 26680, f"wrong lens check count: {lens_checks}")
    require(len(zero_margin) == 96, f"wrong zero-margin count: {len(zero_margin)}")
    require(closest_nonzero == 3, f"wrong closest nonzero margin: {closest_nonzero}")
    transcript.extend(zero_margin)
    digest = sha256(json.dumps(transcript, separators=(",", ":")).encode("ascii")).hexdigest()
    print(f"witness_literal_checks={witness_checks}")
    print(f"witness_minimum_literal_gap={minimum_literal}")
    print(f"diameter_directions={len(directions)} raw_vectors={len(raw_vectors)}")
    print(f"base_lens_literal_checks={lens_checks}")
    print(f"zero_margin_base_triples={len(zero_margin)}")
    print(f"closest_nonzero_integer_margin={closest_nonzero}")
    print(f"zero_margin_transcript_sha256={digest}")
    print("STRICT_PREDICATE_AUDIT_PASS")


if __name__ == "__main__":
    main()
