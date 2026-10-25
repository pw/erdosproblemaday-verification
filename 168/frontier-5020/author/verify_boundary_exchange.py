#!/usr/bin/env python3
"""Verify the five-point coloring exchange giving f(5000) >= 3335."""

from __future__ import annotations

import heapq


def points_prefix(count: int) -> list[tuple[int, int]]:
    heap = [(1, 0, 0)]
    seen = {1}
    points: list[tuple[int, int]] = []
    while len(points) < count:
        value, a, b = heapq.heappop(heap)
        points.append((a, b))
        for child, aa, bb in ((2 * value, a + 1, b), (3 * value, a, b + 1)):
            if child not in seen:
                seen.add(child)
                heapq.heappush(heap, (child, aa, bb))
    return points


def main() -> None:
    points = points_prefix(5000)
    point_set = set(points)
    color_counts = [sum((a + 2 * b) % 3 == c for a, b in points) for c in range(3)]
    if color_counts != [1667, 1667, 1666]:
        raise AssertionError(f"unexpected color counts {color_counts}")

    chosen = {(a, b) for a, b in points if (a + 2 * b) % 3 != 2}
    added = {(122, 0), (121, 2), (123, 1)}
    removed = {(121, 1), (123, 0)}
    if not added | removed <= point_set:
        raise AssertionError("exchange point lies outside the prefix")
    if added & chosen or not removed <= chosen:
        raise AssertionError("exchange colors are inconsistent")
    chosen = (chosen - removed) | added
    if len(chosen) != 3335:
        raise AssertionError(f"wrong witness size {len(chosen)}")

    corners = []
    for a, b in points:
        corner = {(a, b), (a + 1, b), (a, b + 1)}
        if corner <= point_set:
            corners.append(corner)
            if corner <= chosen:
                raise AssertionError(f"forbidden corner survives: {corner}")
    print(
        "PASS: colors="
        f"{color_counts}; delete color 2, remove={sorted(removed)}, "
        f"add={sorted(added)}; size={len(chosen)}; checked {len(corners)} corners"
    )


if __name__ == "__main__":
    main()
