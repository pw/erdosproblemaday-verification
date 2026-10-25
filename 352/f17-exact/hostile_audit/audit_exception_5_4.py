#!/usr/bin/env python3
"""Small, certificate-style audit of the exceptional N=17, B=(5,4) branch."""

from decimal import Decimal, getcontext
from hashlib import sha256
from itertools import combinations
import json
import math
import time

N = 17
A = (0, 0)
B = (5, 4)
R2 = 41

# A fixed nine-edge matching, stated geometrically rather than by indices.
MATCHING = (
    ((-1, 2), (2, -1)),
    ((-1, 3), (3, 0)),
    ((0, 3), (4, -1)),
    ((0, 4), (3, -1)),
    ((1, -1), (4, 5)),
    ((1, 4), (6, 1)),
    ((1, 5), (5, 1)),
    ((2, 5), (5, 0)),
    ((3, 5), (6, 2)),
)


def d2(p, q):
    dx, dy = p[0] - q[0], p[1] - q[1]
    return dx * dx + dy * dy


def area2(p, q, r):
    return abs((q[0] - p[0]) * (r[1] - p[1])
               - (q[1] - p[1]) * (r[0] - p[0]))


def margin(p, q, r):
    diameter2 = max(d2(p, q), d2(p, r), d2(q, r))
    return (area2(p, q, r) - 34) ** 2 - 4 * diameter2


def good_tuple(points):
    for i in range(len(points)):
        for j in range(i, len(points)):
            for k in range(j, len(points)):
                if margin(points[i], points[j], points[k]) <= 0:
                    return False
    return True


def compatible(p, q):
    return d2(p, q) <= R2 and good_tuple((A, B, p, q))


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"))
                  .encode("ascii")).hexdigest()


def main():
    started = time.perf_counter()
    pool = []
    for x in range(-16, 17):
        for y in range(-16, 17):
            p = (x, y)
            if p in (A, B):
                continue
            if d2(A, p) > R2 or d2(B, p) > R2:
                continue
            if not good_tuple((A, B, p)):
                continue
            if area2(A, B, p) < 34:
                pool.append(p)
    assert len(pool) == 40 and len(pool) == len(set(pool))
    index = {p: i for i, p in enumerate(pool)}

    bad_edges = []
    for p, q in combinations(pool, 2):
        if not compatible(p, q):
            bad_edges.append((p, q))
    bad_edge_set = {frozenset(edge) for edge in bad_edges}
    assert len(bad_edges) == 48

    endpoints = [point for edge in MATCHING for point in edge]
    assert len(endpoints) == len(set(endpoints)) == 18
    assert all(frozenset(edge) in bad_edge_set for edge in MATCHING)

    covers = []
    for mask in range(512):
        omitted = frozenset(edge[(mask >> bit) & 1]
                            for bit, edge in enumerate(MATCHING))
        if all(p in omitted or q in omitted for p, q in bad_edges):
            covers.append(omitted)
    assert len(covers) == 2

    # Cross-check the squared predicate against the literal inequality at
    # 80-decimal precision on every triple involved in the two 31-sets.
    getcontext().prec = 80
    killed = []
    decimal_checks = 0
    for omitted in sorted(covers, key=lambda c: sorted(c)):
        chosen = tuple(p for p in pool if p not in omitted)
        assert len(chosen) == 31
        assert all(compatible(p, q) for p, q in combinations(chosen, 2))
        failures = []
        for p, q, r in combinations(chosen, 3):
            m = margin(p, q, r)
            diameter2 = max(d2(p, q), d2(p, r), d2(q, r))
            literal = abs(Decimal(area2(p, q, r)) / 2 - Decimal(N)) \
                      > Decimal(diameter2).sqrt()
            assert literal == (m > 0)
            decimal_checks += 1
            if m <= 0:
                failures.append((p, q, r, m, area2(p, q, r), diameter2))
        assert len(failures) == 1 and failures[0][3:] == (-4, 22, 37)
        killed.append({
            "omitted": sorted(omitted),
            "chosen_sha256": digest(chosen),
            "failure": failures[0],
        })

    canonical_edges = sorted((min(p, q), max(p, q)) for p, q in bad_edges)
    result = {
        "N": N,
        "B": B,
        "candidate_count": len(pool),
        "candidate_sha256": digest(pool),
        "incompatibility_edge_count": len(bad_edges),
        "incompatibility_edge_sha256": digest(canonical_edges),
        "matching": MATCHING,
        "matching_sha256": digest(MATCHING),
        "endpoint_covers_tested": 512,
        "size9_covers": len(covers),
        "decimal_triple_checks": decimal_checks,
        "killed_31sets": killed,
        "candidate_upper_bound": 30,
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(canonical)
    print("EXCEPTION_CERT_SHA256=" + sha256(canonical.encode("ascii")).hexdigest())
    print(f"EXCEPTION_AUDIT_PASS elapsed_seconds={time.perf_counter()-started:.6f}")


if __name__ == "__main__":
    main()
