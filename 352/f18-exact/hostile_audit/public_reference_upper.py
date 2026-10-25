#!/usr/bin/env python3
"""Reference upper-bound search for the lattice N-avoiding problem.

AI usage disclosure:
    This solution and code were developed with assistance from Codex 5.5 using
    xhigh reasoning and ChatGPT 5.5 Pro.

Forum citations:
    - Erdős Problems #352 forum discussion:
      https://www.erdosproblems.com/forum/thread/352
    - Koizumi's forum comments introducing the discrete model:
      J_Koizumi_144, 17:37 on 24 Dec 2025.
      https://www.erdosproblems.com/forum/thread/352
    - Forum witness tables:
      BorisAlexeev, 03:17 on 28 Dec 2025;
      KentaKitamura, 07:43 on 31 May 2026.
      https://www.erdosproblems.com/forum/thread/352

This is a small, readable implementation of the proof strategy used in the
explanatory pages:

1. Normalize a diameter pair as A=(0,0), B=(a,b), with |B| < N.
2. Build the finite lens of possible extra points q.
3. Split candidates into no-high and high-side cases.
4. Use a compatibility graph coloring as an upper bound.

For small N this script can compute exact chromatic numbers by backtracking.
For larger N, use exported coloring certificates instead of asking this
reference script to solve every coloring problem from scratch.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Sequence


Point = tuple[int, int]
A: Point = (0, 0)


def popcount(value: int) -> int:
    return bin(value).count("1")


def dist2(p: Point, q: Point) -> int:
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def twice_area(p: Point, q: Point, r: Point) -> int:
    return abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]))


def triangle_diam2(p: Point, q: Point, r: Point) -> int:
    return max(dist2(p, q), dist2(p, r), dist2(q, r))


def is_forbidden_or_equal(n: int, p: Point, q: Point, r: Point) -> bool:
    a2 = twice_area(p, q, r)
    d2 = triangle_diam2(p, q, r)
    return (a2 - 2 * n) ** 2 <= 4 * d2


def forbidden_reason(n: int, p: Point, q: Point, r: Point) -> dict:
    a2 = twice_area(p, q, r)
    d2 = triangle_diam2(p, q, r)
    lhs = (a2 - 2 * n) ** 2
    rhs = 4 * d2
    return {
        "triangle": [list(p), list(q), list(r)],
        "twice_area": a2,
        "diameter_squared": d2,
        "lhs": lhs,
        "rhs": rhs,
        "forbidden_or_equal": lhs <= rhs,
    }


def normalized_diameter_vectors(n: int) -> list[Point]:
    vectors: list[Point] = [(d, 0) for d in range(1, n)]
    for a in range(1, n):
        for b in range(1, a + 1):
            if a * a + b * b < n * n:
                vectors.append((a, b))
    return sorted(vectors, key=lambda p: (dist2(A, p), p[0], p[1]))


def universe_for_vector(n: int, bvec: Point) -> list[Point]:
    d2 = dist2(A, bvec)
    radius = math.ceil(math.sqrt(d2))
    xmin = min(0, bvec[0]) - radius
    xmax = max(0, bvec[0]) + radius
    ymin = min(0, bvec[1]) - radius
    ymax = max(0, bvec[1]) + radius
    out: list[Point] = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            p = (x, y)
            if dist2(p, A) <= d2 and dist2(p, bvec) <= d2:
                if not is_forbidden_or_equal(n, A, bvec, p):
                    out.append(p)
    return sorted(out)


def lens_rows(n: int, bvec: Point) -> list[dict]:
    d2 = dist2(A, bvec)
    radius = math.ceil(math.sqrt(d2))
    xmin = min(0, bvec[0]) - radius
    xmax = max(0, bvec[0]) + radius
    ymin = min(0, bvec[1]) - radius
    ymax = max(0, bvec[1]) + radius
    rows: list[dict] = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            p = (x, y)
            da = dist2(p, A)
            db = dist2(p, bvec)
            if da <= d2 and db <= d2:
                a2 = twice_area(A, bvec, p)
                if p == A:
                    side = "A"
                elif p == bvec:
                    side = "B"
                elif is_forbidden_or_equal(n, A, bvec, p):
                    side = "band"
                elif is_high_side(n, bvec, d2, p):
                    side = "high"
                else:
                    side = "low"
                rows.append(
                    {
                        "point": list(p),
                        "dist_to_A_squared": da,
                        "dist_to_B_squared": db,
                        "twice_area_A_B_q": a2,
                        "area_A_B_q": a2 / 2,
                        "side": side,
                    }
                )
    return sorted(rows, key=lambda row: (-row["point"][1], row["point"][0]))


def is_high_side(n: int, bvec: Point, d2: int, p: Point) -> bool:
    a2 = twice_area(A, bvec, p)
    return a2 > 2 * n and (a2 - 2 * n) ** 2 > 4 * d2


def low_high_split(n: int, bvec: Point) -> tuple[list[Point], list[Point], list[Point]]:
    d2 = dist2(A, bvec)
    universe = universe_for_vector(n, bvec)
    low: list[Point] = []
    high: list[Point] = []
    for p in universe:
        if p in (A, bvec):
            continue
        if is_high_side(n, bvec, d2, p):
            high.append(p)
        else:
            low.append(p)
    return universe, low, high


def single_survivors(n: int, d2: int, forced: Sequence[Point], universe: Sequence[Point]) -> list[Point]:
    forced_set = set(forced)
    survivors: list[Point] = []
    for p in universe:
        if p in forced_set:
            continue
        if single_reject_reason(n, d2, forced, p) is None:
            survivors.append(p)
    return survivors


def single_reject_reason(n: int, d2: int, forced: Sequence[Point], p: Point) -> dict | None:
    for q in forced:
        d = dist2(p, q)
        if d > d2:
            return {
                "kind": "distance",
                "with": list(q),
                "distance_squared": d,
                "diameter_squared": d2,
            }

    for q in forced:
        if is_forbidden_or_equal(n, p, p, q):
            return {"kind": "triangle", **forbidden_reason(n, p, p, q)}
        if is_forbidden_or_equal(n, p, q, q):
            return {"kind": "triangle", **forbidden_reason(n, p, q, q)}

    for i, q in enumerate(forced):
        for r in forced[i:]:
            if is_forbidden_or_equal(n, p, q, r):
                return {"kind": "triangle", **forbidden_reason(n, p, q, r)}

    return None


def pair_conflict(n: int, d2: int, forced: Sequence[Point], p: Point, q: Point) -> bool:
    if dist2(p, q) > d2:
        return True
    if is_forbidden_or_equal(n, p, p, q) or is_forbidden_or_equal(n, p, q, q):
        return True
    for r in forced:
        if is_forbidden_or_equal(n, p, q, r):
            return True
    return False


def compatibility_graph(n: int, d2: int, forced: Sequence[Point], candidates: Sequence[Point]) -> list[int]:
    count = len(candidates)
    adj = [0 for _ in range(count)]
    for i, p in enumerate(candidates):
        for j in range(i + 1, count):
            q = candidates[j]
            if not pair_conflict(n, d2, forced, p, q):
                adj[i] |= 1 << j
                adj[j] |= 1 << i
    return adj


def greedy_coloring(adj: Sequence[int]) -> tuple[int, list[int]]:
    n = len(adj)
    colors = [-1] * n
    order = sorted(range(n), key=lambda i: (popcount(adj[i]), i), reverse=True)
    for i in order:
        used = {colors[j] for j in range(n) if colors[j] >= 0 and ((adj[i] >> j) & 1)}
        color = 0
        while color in used:
            color += 1
        colors[i] = color
    return max(colors, default=-1) + 1, colors


def exact_coloring(adj: Sequence[int], max_vertices: int) -> tuple[int, list[int], str]:
    n = len(adj)
    if n == 0:
        return 0, [], "exact"
    greedy_count, greedy_colors = greedy_coloring(adj)
    if n > max_vertices:
        return greedy_count, greedy_colors, "greedy"

    degrees = [popcount(adj[i]) for i in range(n)]

    def can_color(color_count: int) -> tuple[bool, list[int]]:
        colors = [-1] * n

        def saturation(i: int) -> int:
            return len({colors[j] for j in range(n) if colors[j] >= 0 and ((adj[i] >> j) & 1)})

        def rec(done: int) -> bool:
            if done == n:
                return True
            remaining = [i for i in range(n) if colors[i] < 0]
            i = max(remaining, key=lambda k: (saturation(k), degrees[k]))
            blocked = {colors[j] for j in range(n) if colors[j] >= 0 and ((adj[i] >> j) & 1)}
            for color in range(color_count):
                if color not in blocked:
                    colors[i] = color
                    if rec(done + 1):
                        return True
                    colors[i] = -1
            return False

        return rec(0), colors[:]

    for color_count in range(1, greedy_count + 1):
        ok, colors = can_color(color_count)
        if ok:
            return color_count, colors, "exact"
    return greedy_count, greedy_colors, "greedy"


def color_groups(candidates: Sequence[Point], colors: Sequence[int]) -> list[dict]:
    groups: dict[int, list[Point]] = {}
    for p, color in zip(candidates, colors):
        groups.setdefault(color + 1, []).append(p)
    return [
        {"color": color, "points": [list(p) for p in points]}
        for color, points in sorted(groups.items())
    ]


def branch_report(
    n: int,
    bvec: Point,
    forced: Sequence[Point],
    candidates: Sequence[Point],
    max_color_vertices: int,
) -> dict:
    d2 = dist2(A, bvec)
    adj = compatibility_graph(n, d2, forced, candidates)
    color_count, colors, mode = exact_coloring(adj, max_color_vertices)
    return {
        "forced": [list(p) for p in forced],
        "candidate_count": len(candidates),
        "candidates": [list(p) for p in candidates],
        "compatible_edge_count": sum(popcount(bits) for bits in adj) // 2,
        "coloring_mode": mode,
        "color_count": color_count,
        "colors": [color + 1 for color in colors],
        "color_groups": color_groups(candidates, colors),
    }


def case_report(n: int, bvec: Point, max_color_vertices: int, include_lens_rows: bool) -> dict:
    d2 = dist2(A, bvec)
    universe, low, high = low_high_split(n, bvec)
    rows = lens_rows(n, bvec) if include_lens_rows else None

    no_high = branch_report(n, bvec, [A, bvec], low, max_color_vertices)
    no_high["upper_total"] = 2 + no_high["color_count"]

    high_branches = []
    for h in high:
        survivors = single_survivors(n, d2, [A, bvec, h], universe)
        branch = branch_report(n, bvec, [A, bvec, h], survivors, max_color_vertices)
        branch["H"] = list(h)
        branch["upper_total"] = 3 + branch["color_count"]
        reject_kinds = Counter()
        reject_examples = []
        for p in universe:
            if p in (A, bvec, h):
                continue
            reason = single_reject_reason(n, d2, [A, bvec, h], p)
            if reason is not None:
                reject_kinds[reason["kind"]] += 1
                if len(reject_examples) < 5:
                    reject_examples.append({"point": list(p), "reason": reason})
        branch["single_reject_counts"] = dict(reject_kinds)
        branch["single_reject_examples"] = reject_examples
        high_branches.append(branch)

    high_upper = max((branch["upper_total"] for branch in high_branches), default=2)
    report = {
        "N": n,
        "B": list(bvec),
        "diameter_squared": d2,
        "universe_size_after_ABq_filter": len(universe),
        "candidate_count_after_A_B": len(low) + len(high),
        "low_candidate_count": len(low),
        "high_candidate_count": len(high),
        "low_candidates": [list(p) for p in low],
        "high_candidates": [list(p) for p in high],
        "no_high": no_high,
        "high_side": {
            "branch_count": len(high_branches),
            "branches": high_branches,
            "max_upper_total": high_upper,
        },
        "case_upper_total": max(no_high["upper_total"], high_upper),
    }
    if rows is not None:
        report["lens_size_before_ABq_filter"] = len(rows)
        report["lens_rows_before_ABq_filter"] = rows
    return report


def run_all_cases(n: int, max_color_vertices: int) -> dict:
    cases = [case_report(n, bvec, max_color_vertices, include_lens_rows=False) for bvec in normalized_diameter_vectors(n)]
    if not cases:
        return {
            "N": n,
            "case_count": 0,
            "max_case_upper_total": 1,
            "cases_with_high": 0,
            "cases": [],
        }
    return {
        "N": n,
        "case_count": len(cases),
        "max_case_upper_total": max(case["case_upper_total"] for case in cases),
        "cases_with_high": sum(1 for case in cases if case["high_candidate_count"] > 0),
        "cases": [
            {
                "B": case["B"],
                "diameter_squared": case["diameter_squared"],
                "low": case["low_candidate_count"],
                "high": case["high_candidate_count"],
                "no_high_upper_total": case["no_high"]["upper_total"],
                "high_side_upper_total": case["high_side"]["max_upper_total"],
                "case_upper_total": case["case_upper_total"],
            }
            for case in cases
        ],
    }


def parse_point(raw: str) -> Point:
    left, right = raw.split(",", 1)
    return int(left), int(right)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--case", type=parse_point, help="one normalized B vector, for example 6,3")
    parser.add_argument("--include-lens-rows", action="store_true")
    parser.add_argument("--max-color-vertices", type=int, default=24)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    if args.case:
        payload = case_report(args.n, args.case, args.max_color_vertices, args.include_lens_rows)
    else:
        payload = run_all_cases(args.n, args.max_color_vertices)

    text = json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
