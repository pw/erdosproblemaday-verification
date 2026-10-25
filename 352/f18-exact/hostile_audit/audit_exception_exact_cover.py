#!/usr/bin/env python3
"""From-scratch exact vertex-cover audit of the exceptional N=18 branch."""

from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
import math


N = 18
A = (0, 0)
B = (5, 4)


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


def margin(p, q, r):
    a2 = twice_area(p, q, r)
    d2 = max(distance2(p, q), distance2(p, r), distance2(q, r))
    return (a2 - 2 * N) ** 2 - 4 * d2


def avoiding(points):
    return all(margin(*triple) > 0 for triple in combinations_with_replacement(points, 3))


def main() -> None:
    diameter2 = distance2(A, B)
    radius_box = math.isqrt(diameter2)
    pool = tuple(
        (x, y)
        for x in range(-radius_box, radius_box + 1)
        for y in range(-radius_box, radius_box + 1)
        if (x, y) not in (A, B)
        and distance2(A, (x, y)) <= diameter2
        and distance2(B, (x, y)) <= diameter2
        and twice_area(A, B, (x, y)) < 2 * N
        and avoiding((A, B, (x, y)))
    )
    require(len(pool) == len(set(pool)) == 42, f"wrong pool size: {len(pool)}")

    edges = {
        (i, j)
        for i, j in combinations(range(len(pool)), 2)
        if distance2(pool[i], pool[j]) > diameter2
        or not avoiding((A, B, pool[i], pool[j]))
    }
    require(len(edges) == 57, f"wrong incompatibility edge count: {len(edges)}")

    best = None
    covers = []

    def search(chosen: frozenset[int]) -> None:
        nonlocal best, covers
        if best is not None and len(chosen) > best:
            return
        uncovered = next(
            ((u, v) for u, v in edges if u not in chosen and v not in chosen),
            None,
        )
        if uncovered is None:
            if best is None or len(chosen) < best:
                best = len(chosen)
                covers = []
            if len(chosen) == best:
                covers.append(chosen)
            return
        u, v = uncovered
        search(chosen | {u})
        search(chosen | {v})

    search(frozenset())
    unique_covers = set(covers)
    require(best == 9, f"minimum cover size is {best}, not 9")
    require(len(unique_covers) == 2, f"minimum cover count is {len(unique_covers)}, not 2")

    transcript = []
    all_indices = set(range(len(pool)))
    for cover in sorted(unique_covers, key=lambda item: tuple(sorted(item))):
        survivor = tuple(pool[i] for i in sorted(all_indices - set(cover)))
        require(len(survivor) == 33, "wrong survivor size")
        bad = [
            (p, q, r, margin(p, q, r))
            for p, q, r in combinations(survivor, 3)
            if margin(p, q, r) <= 0
        ]
        require(len(bad) == 2, f"expected two bad triples, found {len(bad)}")
        require({row[3] for row in bad} == {-15}, f"wrong bad margins: {bad}")
        transcript.append({
            "cover": tuple(pool[i] for i in sorted(cover)),
            "survivor_sha256": sha256(
                json.dumps(survivor, separators=(",", ":")).encode("ascii")
            ).hexdigest(),
            "bad": bad,
        })

    digest = sha256(json.dumps(transcript, sort_keys=True, separators=(",", ":")).encode("ascii")).hexdigest()
    print(f"pool_size={len(pool)} incompatibility_edges={len(edges)}")
    print(f"exact_minimum_vertex_cover={best} minimum_covers={len(unique_covers)}")
    for index, record in enumerate(transcript):
        print(f"cover[{index}]={record['cover']}")
        print(f"survivor[{index}]_sha256={record['survivor_sha256']}")
        for row in record["bad"]:
            print(f"bad_triple={row[0]},{row[1]},{row[2]} margin={row[3]}")
    print(f"transcript_sha256={digest}")
    print("EXACT_COVER_AUDIT_PASS candidate_cap=32 total_cap=34")


if __name__ == "__main__":
    main()
