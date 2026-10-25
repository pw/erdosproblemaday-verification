#!/usr/bin/env python3
"""Independent definition-level audit of the frozen N=71 certificate.

This does not share the C++ support builder.  It directly compares all
unordered square pairs, verifies the lower witness, validates the live gate,
prefix dependency, cube cover, and logs.
"""

from __future__ import annotations

import itertools
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
N = 71
TARGET = 34
CUBES = ("00", "010", "011", "100", "101", "110", "111")
WITNESS = (
    1, 4, 6, 7, 9, 10, 12, 13, 16, 18, 19, 22, 24, 28, 30, 34, 36,
    37, 39, 40, 43, 46, 49, 51, 52, 57, 58, 60, 64, 65, 67, 69, 70,
)


def direct_collision_supports() -> set[tuple[int, ...]]:
    pairs = [(i, j, i * i + j * j) for i in range(1, N + 1) for j in range(i, N + 1)]
    result: set[tuple[int, ...]] = set()
    for left in range(len(pairs)):
        i, j, left_sum = pairs[left]
        for right in range(left + 1, len(pairs)):
            k, ell, right_sum = pairs[right]
            if left_sum == right_sum:
                result.add(tuple(sorted({i, j, k, ell})))
    return result


def check_cube_cover() -> None:
    assignments: dict[str, str] = {}
    for bits in itertools.product("01", repeat=3):
        assignment = "".join(bits)
        matches = [cube for cube in CUBES if assignment.startswith(cube)]
        assert len(matches) == 1, (assignment, matches)
        assignments[assignment] = matches[0]
    assert len(assignments) == 8


def main() -> None:
    live = (ROOT / "live_gate.txt").read_text()
    comments = (ROOT / "live_comments.txt").read_text()
    assert "OPEN" in live
    assert "0 claimed proofs for this problem" in live
    assert "Interested in collaborating\tNone" in live
    assert "Currently working on this problem\tNone" in live
    assert "0 claimed proofs for this problem" in comments

    rows = []
    for line in (ROOT / "prefix_bounds_through_70.txt").read_text().splitlines():
        if line and not line.startswith("#"):
            rows.append(tuple(map(int, line.split())))
    assert [index for index, _ in rows] == list(range(1, 71))
    assert rows[-3:] == [(68, 32), (69, 32), (70, 33)]
    assert len(rows) == 70 and rows[0] == (1, 1)

    supports = direct_collision_supports()
    sizes = {size: sum(len(s) == size for s in supports) for size in (3, 4)}
    assert len(supports) == 764 and sizes == {3: 23, 4: 741}

    sums = [i * i + j * j for pos, i in enumerate(WITNESS) for j in WITNESS[pos:]]
    assert len(WITNESS) == 33
    assert len(sums) == 561 == len(set(sums))
    assert max(WITNESS) <= N

    check_cube_cover()
    expected_by_cube = {
        "00": {"nodes": 2, "prefix_prunes": 1, "blocked_prunes": 0,
               "color_calls": 1, "color_prunes": 0},
        "010": {"nodes": 2, "prefix_prunes": 1, "blocked_prunes": 0,
                 "color_calls": 1, "color_prunes": 0},
        "011": {"nodes": 2, "prefix_prunes": 1, "blocked_prunes": 0,
                 "color_calls": 1, "color_prunes": 0},
        "100": {"nodes": 14_391_515, "prefix_prunes": 457_087,
                 "blocked_prunes": 2_832, "color_calls": 13_931_596,
                 "color_prunes": 6_276_915},
        "101": {"nodes": 40_004_795, "prefix_prunes": 1_143_913,
                 "blocked_prunes": 9_389, "color_calls": 38_851_493,
                 "color_prunes": 17_652_449},
        "110": {"nodes": 26_162_953, "prefix_prunes": 695_538,
                 "blocked_prunes": 2_924, "color_calls": 25_464_491,
                 "color_prunes": 11_493_240},
        "111": {"nodes": 33_737_137, "prefix_prunes": 759_347,
                 "blocked_prunes": 4_826, "color_calls": 32_972_964,
                 "color_prunes": 14_974_799},
    }
    totals = {key: 0 for key in (
        "nodes", "prefix_prunes", "blocked_prunes", "color_calls", "color_prunes"
    )}
    for cube in CUBES:
        assert (ROOT / f"cube_{cube}.status").read_text().strip() == "20"
        log = (ROOT / f"cube_{cube}.log").read_text().strip()
        assert log.startswith("status=UNSATISFIABLE ")
        assert f"cube={cube}" in log and "color_slack=33" in log
        observed = {}
        for key in totals:
            match = re.search(rf"(?:^| ){key}=(\d+)(?: |$)", log)
            assert match, (cube, key)
            observed[key] = int(match.group(1))
            totals[key] += observed[key]
        assert observed == expected_by_cube[cube], (cube, observed)
    assert totals == {
        "nodes": 114_296_406,
        "prefix_prunes": 3_055_888,
        "blocked_prunes": 19_971,
        "color_calls": 111_220_547,
        "color_prunes": 50_397_403,
    }

    print("live gate OPEN/0/no worker/no collaborator: PASS")
    print("direct collision supports: 764 (23 triples, 741 quadruples)")
    print("witness size=33 unordered sums=561 all distinct: PASS")
    print("seven cubes cover all top-three assignments exactly once: PASS")
    print(f"frozen exhaustive counters: {totals}")
    print("DEFINITION-LEVEL AUDIT PASS")


if __name__ == "__main__":
    main()
