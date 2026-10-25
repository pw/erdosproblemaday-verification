#!/usr/bin/env python3
"""Hostile, standalone audit of the proposed f(18)=34 certificate.

This intentionally does not import the producer.  It reconstructs the full
diameter-pair search, uses a set-based DSATUR coloring instead of the
producer's static degree-order bitset coloring, and handles the sole loose
branch as a vertex-cover problem in the incompatibility graph.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
import time
from itertools import combinations


N = 18
ORIGIN = (0, 0)

# The claimed 34-point lower witness.  It is copied as data only; every
# geometric assertion about it is recomputed below.
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


def norm2(p: tuple[int, int]) -> int:
    return p[0] * p[0] + p[1] * p[1]


def distance2(p: tuple[int, int], q: tuple[int, int]) -> int:
    # Polarization identity, independent of the producer's coordinate-
    # difference implementation.
    return norm2(p) + norm2(q) - 2 * (p[0] * q[0] + p[1] * q[1])


def double_area(p: tuple[int, int], q: tuple[int, int], r: tuple[int, int]) -> int:
    # Six-term shoelace formula.
    signed = (
        p[0] * q[1] + q[0] * r[1] + r[0] * p[1]
        - p[1] * q[0] - q[1] * r[0] - r[1] * p[0]
    )
    return abs(signed)


def exact_margin(p: tuple[int, int], q: tuple[int, int], r: tuple[int, int]) -> int:
    """Positive iff |area-N| > diameter, with no floating point."""
    delta2 = double_area(p, q, r) - 2 * N
    diameter2 = max(distance2(p, q), distance2(p, r), distance2(q, r))
    return delta2 * delta2 - 4 * diameter2


def all_triples_good(points: tuple[tuple[int, int], ...]) -> bool:
    # Deliberately explicit index loops rather than combinations_with_replacement.
    size = len(points)
    for i in range(size):
        for j in range(i, size):
            for k in range(j, size):
                if exact_margin(points[i], points[j], points[k]) <= 0:
                    return False
    return True


def witness_audit() -> dict[str, object]:
    require(len(WITNESS) == 34, "witness does not have 34 points")
    require(len(set(WITNESS)) == 34, "witness has duplicate points")
    margins: list[int] = []
    worst: list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]] = []
    for i in range(34):
        for j in range(i, 34):
            for k in range(j, 34):
                value = exact_margin(WITNESS[i], WITNESS[j], WITNESS[k])
                if not margins or value < min(margins):
                    worst = [(WITNESS[i], WITNESS[j], WITNESS[k])]
                elif value == min(margins):
                    worst.append((WITNESS[i], WITNESS[j], WITNESS[k]))
                margins.append(value)
    require(len(margins) == math.comb(36, 3), "wrong witness triple count")
    require(min(margins) > 0, f"invalid witness; minimum margin {min(margins)}")
    diameter2 = max(distance2(p, q) for p, q in combinations(WITNESS, 2))
    return {
        "points": len(WITNESS),
        "triples_with_repetition": len(margins),
        "minimum_margin": min(margins),
        "minimum_margin_multiplicity": margins.count(min(margins)),
        "minimum_margin_triples": worst,
        "diameter_squared": diameter2,
        "witness_sha256": hashlib.sha256(
            json.dumps(WITNESS, separators=(",", ":")).encode("ascii")
        ).hexdigest(),
    }


def canonical_direction(v: tuple[int, int]) -> tuple[int, int]:
    a, b = sorted((abs(v[0]), abs(v[1])), reverse=True)
    return (a, b)


def diameter_directions() -> tuple[tuple[int, int], ...]:
    # Generate all signed raw displacement vectors first, then quotient by D4.
    reps = {
        canonical_direction((x, y))
        for x in range(-(N - 1), N)
        for y in range(-(N - 1), N)
        if (x, y) != ORIGIN and x * x + y * y < N * N
    }
    ordered = tuple(sorted(reps, key=lambda p: (norm2(p), p)))

    # Separate orbit-size accounting catches axes/diagonals and a missing sign
    # or swap in the normalization argument.
    raw = [
        (x, y)
        for x in range(-(N - 1), N)
        for y in range(-(N - 1), N)
        if (x, y) != ORIGIN and x * x + y * y < N * N
    ]
    reconstructed = 0
    for x, y in ordered:
        reconstructed += 4 if (y == 0 or x == y) else 8
    require(reconstructed == len(raw), "D4 orbit accounting mismatch")
    require(all(x >= y >= 0 and 0 < norm2((x, y)) < N * N for x, y in ordered),
            "bad normalized direction")
    return ordered


def lens_candidates(b: tuple[int, int]) -> tuple[tuple[int, int], ...]:
    d2 = norm2(b)
    radius_box = math.isqrt(d2)
    candidates: list[tuple[int, int]] = []
    for x in range(-radius_box, radius_box + 1):
        for y in range(-radius_box, radius_box + 1):
            p = (x, y)
            if p == ORIGIN or p == b:
                continue
            if norm2(p) > d2 or distance2(p, b) > d2:
                continue
            if exact_margin(ORIGIN, b, p) > 0:
                candidates.append(p)
    require(len(candidates) == len(set(candidates)), f"duplicate candidate for B={b}")
    return tuple(candidates)


def pair_can_coexist(
    forced: tuple[tuple[int, int], ...],
    p: tuple[int, int],
    q: tuple[int, int],
    diameter2: int,
) -> bool:
    # Full enumeration over F union {p,q}; no optimized compatibility formula.
    return distance2(p, q) <= diameter2 and all_triples_good(forced + (p, q))


def branch_pool(
    base: tuple[tuple[int, int], ...],
    forced: tuple[tuple[int, int], ...],
    diameter2: int,
) -> tuple[tuple[int, int], ...]:
    forced_set = set(forced)
    out = []
    for p in base:
        if p in forced_set:
            continue
        if any(distance2(p, q) > diameter2 for q in forced):
            continue
        if all_triples_good(forced + (p,)):
            out.append(p)
    return tuple(out)


def compatibility_graph(
    forced: tuple[tuple[int, int], ...],
    pool: tuple[tuple[int, int], ...],
    diameter2: int,
) -> tuple[list[set[int]], frozenset[tuple[int, int]]]:
    adjacency = [set() for _ in pool]
    incompatibility: set[tuple[int, int]] = set()
    for i, j in combinations(range(len(pool)), 2):
        if pair_can_coexist(forced, pool[i], pool[j], diameter2):
            adjacency[i].add(j)
            adjacency[j].add(i)
        else:
            incompatibility.add((i, j))
    require(
        len(incompatibility) + sum(len(row) for row in adjacency) // 2
        == math.comb(len(pool), 2),
        "pair partition mismatch",
    )
    return adjacency, frozenset(incompatibility)


def dsatur(adjacency: list[set[int]]) -> tuple[int, ...]:
    """Dynamic saturation-degree greedy coloring using Python sets."""
    count = len(adjacency)
    colors = [-1] * count
    neighbor_colors = [set() for _ in adjacency]
    uncolored = set(range(count))
    while uncolored:
        vertex = max(
            uncolored,
            key=lambda v: (len(neighbor_colors[v]), len(adjacency[v]), -v),
        )
        color = 0
        while color in neighbor_colors[vertex]:
            color += 1
        colors[vertex] = color
        uncolored.remove(vertex)
        for neighbor in adjacency[vertex]:
            if colors[neighbor] < 0:
                neighbor_colors[neighbor].add(color)

    for i, j in combinations(range(count), 2):
        if j in adjacency[i]:
            require(colors[i] != colors[j], "DSATUR emitted an improper coloring")
    return tuple(colors)


def find_disjoint_edges(
    edges: frozenset[tuple[int, int]], target: int, vertex_count: int
) -> tuple[tuple[int, int], ...]:
    """Backtrack only until a target-size matching is found."""
    ordered = tuple(sorted(edges))

    def search(start: int, chosen: tuple[tuple[int, int], ...], used: frozenset[int]):
        if len(chosen) == target:
            return chosen
        need = target - len(chosen)
        if (vertex_count - len(used)) // 2 < need:
            return None
        for pos in range(start, len(ordered)):
            u, v = ordered[pos]
            if u in used or v in used:
                continue
            answer = search(pos + 1, chosen + ((u, v),), used | {u, v})
            if answer is not None:
                return answer
        return None

    result = search(0, (), frozenset())
    require(result is not None, f"failed to find matching of size {target}")
    return result


def exceptional_vertex_cover_audit(
    b: tuple[int, int],
    forced: tuple[tuple[int, int], ...],
    pool: tuple[tuple[int, int], ...],
    incompatibility: frozenset[tuple[int, int]],
) -> dict[str, object]:
    require(b == (5, 4), "wrong exceptional direction")
    require(len(pool) == 42, f"exceptional pool has {len(pool)} candidates, not 42")
    require(len(incompatibility) == 57,
            f"exceptional graph has {len(incompatibility)} incompatibility edges, not 57")

    matching = find_disjoint_edges(incompatibility, 9, len(pool))
    require(len({v for edge in matching for v in edge}) == 18,
            "purported matching is not disjoint")

    covers: list[tuple[int, ...]] = []
    endpoint_choices = 0
    for mask in range(1 << len(matching)):
        endpoint_choices += 1
        omitted = tuple(
            edge[(mask >> bit) & 1]
            for bit, edge in enumerate(matching)
        )
        omitted_set = set(omitted)
        if all(u in omitted_set or v in omitted_set for u, v in incompatibility):
            covers.append(tuple(sorted(omitted)))

    require(endpoint_choices == 512, "did not enumerate 512 endpoint covers")
    require(len(covers) == 2, f"expected two size-9 covers, found {len(covers)}")

    all_indices = set(range(len(pool)))
    killed_sets: list[dict[str, object]] = []
    for cover in sorted(covers):
        chosen_indices = tuple(sorted(all_indices - set(cover)))
        require(len(chosen_indices) == 33, "cover complement is not a 33-set")
        require(
            all((min(i, j), max(i, j)) not in incompatibility
                for i, j in combinations(chosen_indices, 2)),
            "cover complement is not pairwise compatible",
        )
        chosen_points = tuple(pool[i] for i in chosen_indices)
        bad = []
        for p, q, r in combinations(chosen_points, 3):
            margin = exact_margin(p, q, r)
            if margin <= 0:
                bad.append((p, q, r, margin))
        require(bad, "unobstructed 33-candidate extension found")
        require(all(item[3] == -15 for item in bad),
                f"unexpected exceptional bad margins: {bad}")
        killed_sets.append({
            "omitted_indices": cover,
            "omitted_points": tuple(pool[i] for i in cover),
            "chosen_points_sha256": hashlib.sha256(
                json.dumps(chosen_points, separators=(",", ":")).encode("ascii")
            ).hexdigest(),
            "bad_all_candidate_triples": bad,
        })

    # A 9-edge matching forces every independent set to omit at least nine
    # vertices.  The only ways to omit exactly nine are the two covers above,
    # and both are killed by a genuine three-candidate condition.  Hence an
    # avoiding extension has at most 32 candidates.
    return {
        "candidate_upper_bound": 32,
        "pool_size": len(pool),
        "incompatibility_edges": len(incompatibility),
        "matching_indices": matching,
        "matching_points": tuple((pool[u], pool[v]) for u, v in matching),
        "endpoint_covers_tested": endpoint_choices,
        "size9_vertex_covers": len(covers),
        "killed_33sets": killed_sets,
    }


def full_upper_audit() -> tuple[dict[str, object], dict[str, object]]:
    directions = diameter_directions()
    require(len(directions) == 140, f"expected 140 directions, found {len(directions)}")

    branch_digest = hashlib.sha256()
    diameter_digest = hashlib.sha256()
    branch_count = 0
    high_branches = 0
    directions_with_high = 0
    pool_memberships = 0
    max_pool = 0
    tight_directions: list[tuple[int, int]] = []
    global_upper = 0
    excessive_colorings: list[tuple[tuple[int, int], str, int, int]] = []
    exceptional: dict[str, object] | None = None

    for b in directions:
        d2 = norm2(b)
        base = lens_candidates(b)
        low = tuple(p for p in base if double_area(ORIGIN, b, p) < 2 * N)
        high = tuple(p for p in base if double_area(ORIGIN, b, p) > 2 * N)
        require(len(low) + len(high) == len(base), f"area=18 candidate for B={b}")
        if high:
            directions_with_high += 1

        direction_upper = 0
        branch_specs = [("low", (ORIGIN, b), low)]
        branch_specs.extend((f"high:{h[0]},{h[1]}", (ORIGIN, b, h), base) for h in high)

        for label, forced, source_pool in branch_specs:
            branch_count += 1
            if label.startswith("high:"):
                high_branches += 1
            pool = branch_pool(source_pool, forced, d2)
            pool_memberships += len(pool)
            max_pool = max(max_pool, len(pool))
            adjacency, incompatibility = compatibility_graph(forced, pool, d2)
            colors = dsatur(adjacency)
            color_count = max(colors, default=-1) + 1
            threshold = 34 - len(forced)
            candidate_bound = color_count

            if color_count > threshold:
                excessive_colorings.append((b, label, color_count, threshold))
                require(b == (5, 4) and label == "low" and color_count == 33,
                        f"unexpected loose coloring: B={b} {label} {color_count}>{threshold}")
                exceptional = exceptional_vertex_cover_audit(
                    b, forced, pool, incompatibility
                )
                candidate_bound = int(exceptional["candidate_upper_bound"])

            require(candidate_bound <= threshold,
                    f"uncertified branch B={b} {label}: {candidate_bound}>{threshold}")
            total_bound = len(forced) + candidate_bound
            direction_upper = max(direction_upper, total_bound)

            color_classes = []
            for color in range(color_count):
                color_classes.append(tuple(pool[i] for i, c in enumerate(colors) if c == color))
            record = {
                "B": b,
                "branch": label,
                "forced": forced,
                "pool_size": len(pool),
                "compatibility_edges": sum(len(row) for row in adjacency) // 2,
                "incompatibility_edges": len(incompatibility),
                "color_count": color_count,
                "candidate_bound": candidate_bound,
                "total_bound": total_bound,
                "color_classes": color_classes,
            }
            branch_digest.update(
                json.dumps(record, sort_keys=True, separators=(",", ":")).encode("ascii")
                + b"\n"
            )

        diameter_record = {
            "B": b,
            "diameter_squared": d2,
            "base_candidates": len(base),
            "low_candidates": len(low),
            "high_candidates": len(high),
            "upper_bound": direction_upper,
        }
        diameter_digest.update(
            json.dumps(diameter_record, sort_keys=True, separators=(",", ":")).encode("ascii")
            + b"\n"
        )
        if direction_upper > global_upper:
            global_upper = direction_upper
            tight_directions = [b]
        elif direction_upper == global_upper:
            tight_directions.append(b)

    require(branch_count == 12734, f"expected 12734 branches, found {branch_count}")
    require(high_branches == 12594, f"expected 12594 high branches, found {high_branches}")
    require(directions_with_high == 108,
            f"expected 108 directions with high candidates, found {directions_with_high}")
    require(pool_memberships == 446938,
            f"pool membership mismatch: {pool_memberships}")
    require(max_pool == 129, f"max pool mismatch: {max_pool}")
    require(excessive_colorings == [((5, 4), "low", 33, 32)],
            f"wrong loose-branch list: {excessive_colorings}")
    require(exceptional is not None, "exceptional branch was not audited")
    require(global_upper == 34, f"global upper bound is {global_upper}, not 34")

    summary = {
        "diameter_directions": len(directions),
        "directions_with_high": directions_with_high,
        "high_branches": high_branches,
        "all_branches": branch_count,
        "pool_memberships": pool_memberships,
        "max_pool": max_pool,
        "loose_colorings": excessive_colorings,
        "global_upper_bound": global_upper,
        "tight_directions": tight_directions,
        "branch_manifest_sha256": branch_digest.hexdigest(),
        "diameter_manifest_sha256": diameter_digest.hexdigest(),
    }
    return summary, exceptional


def main() -> None:
    started = time.perf_counter()
    witness = witness_audit()
    upper, exceptional = full_upper_audit()
    elapsed = time.perf_counter() - started
    result = {
        "audit": "erdos352-n18-hostile-independent-v1",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "witness": witness,
        "upper": upper,
        "exceptional_B_5_4": exceptional,
        "conclusion": "f(18)=34",
        "elapsed_seconds": elapsed,
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(canonical)
    print("RESULT_SHA256=" + hashlib.sha256(canonical.encode("ascii")).hexdigest())
    print(f"HOSTILE_AUDIT_PASS f(18)=34 elapsed_seconds={elapsed:.6f}")


if __name__ == "__main__":
    main()
