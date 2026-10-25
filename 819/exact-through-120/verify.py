#!/usr/bin/env python3
"""Dependency-free exact verifier for Erdős #819, N=81,...,120.

The search is exhaustive.  It does not call a SAT/MIP solver and it does not
import a ruler table.  A state consists of the increasing marks already
chosen, the bit set of their unordered pair sums (diagonal sums included),
and the exact number of repeated representations accumulated so far.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
import time


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def pair_sums(a: tuple[int, ...]) -> list[int]:
    return [a[i] + a[j] for i in range(len(a)) for j in range(i, len(a))]


def collision_excess(a: tuple[int, ...]) -> int:
    sums = pair_sums(a)
    return len(sums) - len(set(sums))


def score(n: int, a: tuple[int, ...]) -> int:
    return len({s for s in pair_sums(a) if s <= n})


def search_at_most(k: int, length: int, budget: int) -> dict[str, object]:
    """Find a normalized k-set in [0,length] with collision excess <= budget.

    Returning no witness exhausts every such increasing set, since the next
    mark is tried over its complete feasible integer interval.
    """
    marks = [0]
    nodes = 0
    leaves = 0
    answer: tuple[int, ...] | None = None

    def visit(start: int, used: int, defects: int) -> bool:
        nonlocal nodes, leaves, answer
        nodes += 1
        if len(marks) == k:
            leaves += 1
            answer = tuple(marks)
            return True

        remaining_after_choice = k - len(marks) - 1
        last_choice = length - remaining_after_choice
        for x in range(start, last_choice + 1):
            new_mask = 0
            for old in marks:
                new_mask |= 1 << (x + old)
            new_mask |= 1 << (2 * x)
            # The new sums are pairwise distinct: x+old values inherit the
            # strict order of old, and none equals 2x because old<x.
            require(
                new_mask.bit_count() == len(marks) + 1,
                "internal new-sum distinctness failure",
            )
            extra = (new_mask & used).bit_count()
            if defects + extra > budget:
                continue
            marks.append(x)
            if visit(x + 1, used | new_mask, defects + extra):
                return True
            marks.pop()
        return False

    exists = visit(1, 1, 0)  # bit 0 records 0+0
    if answer is not None:
        require(answer[0] == 0 and answer[-1] <= length, "bad witness range")
        require(collision_excess(answer) <= budget, "bad search witness")
    return {
        "k": k,
        "length": length,
        "budget": budget,
        "exists": exists,
        "nodes": nodes,
        "leaves": leaves,
        "witness": answer,
    }


def search_fixed_last(k: int, last: int, prefix_bound: int) -> dict[str, object]:
    """Exhaust Sidon k-sets with x_0=0, x_{k-1}=last, x_{k-2}<=bound."""
    marks = [0]
    nodes = 0
    prefixes = 0
    answer: tuple[int, ...] | None = None

    def visit(start: int, used: int) -> bool:
        nonlocal nodes, prefixes, answer
        nodes += 1
        if len(marks) == k - 1:
            prefixes += 1
            new_mask = 0
            for old in marks:
                new_mask |= 1 << (last + old)
            new_mask |= 1 << (2 * last)
            require(
                new_mask.bit_count() == len(marks) + 1,
                "internal fixed-last distinctness failure",
            )
            if new_mask & used:
                return False
            answer = tuple(marks + [last])
            return True

        remaining_after_choice = (k - 1) - len(marks) - 1
        last_choice = prefix_bound - remaining_after_choice
        for x in range(start, last_choice + 1):
            new_mask = 0
            for old in marks:
                new_mask |= 1 << (x + old)
            new_mask |= 1 << (2 * x)
            if new_mask & used:
                continue
            marks.append(x)
            if visit(x + 1, used | new_mask):
                return True
            marks.pop()
        return False

    exists = visit(1, 1)
    if answer is not None:
        require(answer[-1] == last, "bad fixed-last witness")
        require(answer[-2] <= prefix_bound, "bad prefix bound")
        require(collision_excess(answer) == 0, "fixed-last witness is not Sidon")
    return {
        "k": k,
        "last": last,
        "prefix_bound": prefix_bound,
        "exists": exists,
        "nodes": nodes,
        "prefixes": prefixes,
        "witness": answer,
    }


def literal_exists(k: int, length: int, budget: int) -> bool:
    for tail in combinations(range(1, length + 1), k - 1):
        if collision_excess((0,) + tail) <= budget:
            return True
    return False


def verify_small_search_kernel() -> int:
    checks = 0
    for k in range(1, 7):
        for length in range(max(0, k - 1), 13):
            for budget in range(3):
                got = bool(search_at_most(k, length, budget)["exists"])
                want = literal_exists(k, length, budget)
                require(got == want, f"small-k search mismatch {(k,length,budget)}")
                checks += 1
    return checks


def verify_table(witnesses: dict[str, tuple[int, ...]]) -> tuple[list[int], str]:
    expected_ranges = [
        (81, 81, 43),
        (82, 89, 44),
        (90, 99, 45),
        (100, 101, 53),
        (102, 111, 54),
        (112, 120, 55),
    ]
    values: list[int] = []
    for n in range(81, 121):
        if n == 81:
            witness = witnesses["k9_defect2"]
            claimed = 43
        elif n <= 89:
            witness = witnesses["k9_defect1"]
            claimed = 44
        elif n <= 99:
            witness = witnesses["k9_sidon"]
            claimed = 45
        elif n <= 101:
            witness = witnesses["k10_defect2"]
            claimed = 53
        elif n <= 111:
            witness = witnesses["k10_defect1"]
            claimed = 54
        else:
            witness = witnesses["k10_sidon"]
            claimed = 55
        require(len(witness) == int(n**0.5), f"wrong witness size at N={n}")
        require(witness[0] >= 1 and witness[-1] <= n, f"range failure at N={n}")
        require(score(n, witness) == claimed, f"score failure at N={n}")
        values.append(claimed)

    compressed: list[tuple[int, int, int]] = []
    lo = 81
    current = values[0]
    for n, value in enumerate(values[1:], 82):
        if value != current:
            compressed.append((lo, n - 1, current))
            lo, current = n, value
    compressed.append((lo, 120, current))
    require(compressed == expected_ranges, "compressed table mismatch")
    digest = sha256(",".join(map(str, values)).encode("ascii")).hexdigest()
    return values, digest


def main() -> None:
    started = time.perf_counter()
    small_checks = verify_small_search_kernel()

    searches = {
        "g0_8_lower": search_at_most(8, 33, 0),
        "g0_8_upper": search_at_most(8, 34, 0),
        "g0_9_lower": search_at_most(9, 43, 0),
        "g0_9_upper": search_at_most(9, 44, 0),
        "g1_9_lower": search_at_most(9, 39, 1),
        "g1_9_upper": search_at_most(9, 40, 1),
        "g0_10_lower": search_at_most(10, 54, 0),
        "g0_10_upper": search_at_most(10, 55, 0),
        "g1_10_lower": search_at_most(10, 49, 1),
        "g1_10_upper": search_at_most(10, 50, 1),
    }
    expected_existence = {
        "g0_8_lower": False,
        "g0_8_upper": True,
        "g0_9_lower": False,
        "g0_9_upper": True,
        "g1_9_lower": False,
        "g1_9_upper": True,
        "g0_10_lower": False,
        "g0_10_upper": True,
        "g1_10_lower": False,
        "g1_10_upper": True,
    }
    for name, expected in expected_existence.items():
        require(searches[name]["exists"] is expected, f"unexpected result: {name}")

    overflow = {
        "n81_L44": search_fixed_last(9, 44, 35),
        "n81_L45": search_fixed_last(9, 45, 34),
        "n101_L55": search_fixed_last(10, 55, 44),
    }
    for name, result in overflow.items():
        require(result["exists"] is False, f"overflow case survived: {name}")

    # Lower witnesses are kept explicit and checked from the live definition.
    normalized = {
        "k9_defect2": (0, 1, 4, 9, 12, 13, 19, 33, 35),
        "k9_defect1": (0, 1, 3, 10, 21, 26, 34, 38, 40),
        "k9_sidon": (0, 1, 5, 12, 25, 27, 35, 41, 44),
        "k10_defect2": (0, 1, 7, 11, 27, 29, 32, 41, 44, 46),
        "k10_defect1": (0, 1, 4, 12, 18, 28, 41, 43, 48, 50),
        "k10_sidon": (0, 1, 6, 10, 23, 26, 34, 41, 53, 55),
    }
    expected_defects = {
        "k9_defect2": 2,
        "k9_defect1": 1,
        "k9_sidon": 0,
        "k10_defect2": 2,
        "k10_defect1": 1,
        "k10_sidon": 0,
    }
    for name, witness in normalized.items():
        require(
            collision_excess(witness) == expected_defects[name],
            f"defect mismatch: {name}",
        )
    witnesses = {name: tuple(x + 1 for x in a) for name, a in normalized.items()}
    values, table_digest = verify_table(witnesses)

    # The lower searches must independently recover witnesses at the stated
    # sharp lengths; their particular lexicographic choices need not equal the
    # explicit witnesses above.
    sharp = {
        "g0(8)": 34,
        "g0(9)": 44,
        "g1(9)": 40,
        "g0(10)": 55,
        "g1(10)": 50,
    }
    record = {
        "problem": 819,
        "range": [81, 120],
        "exact_ranges": [
            [81, 81, 43],
            [82, 89, 44],
            [90, 99, 45],
            [100, 101, 53],
            [102, 111, 54],
            [112, 120, 55],
        ],
        "table_sha256": table_digest,
        "sharp_lengths": sharp,
        "small_literal_crosschecks": small_checks,
        "searches": searches,
        "overflow_checks": overflow,
        "witnesses": witnesses,
        "witness_defects": expected_defects,
        "seconds": round(time.perf_counter() - started, 6),
    }
    print(json.dumps(record, sort_keys=True, separators=(",", ":")))
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
