#!/usr/bin/env python3
"""Exact verifier for the m=11 finite case of Erdos problem 1160."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BFILE = ROOT / "b000001_20260811.txt"
EXPECTED_BFILE_SHA256 = (
    "54358f9bf5875f13f2e56c89f55c5942f868cc96f7a7fa653e2b133d1ad5a0f3"
)
EXPECTED_TOTAL = 49_910_538_480
EXPECTED_G1024 = 49_487_367_289
EXPECTED_OTHER_ORDERS = 423_171_191
LOWER_BOUND_G2048 = 1_774_274_116_992_170
EXPECTED_GAP_MISSING = {
    2002: 8,
    2004: 10,
    2010: 12,
    2016: 6538,
    2020: 20,
    2024: 46,
    2025: 63,
    2028: 88,
    2030: 12,
    2034: 10,
    2040: 175,
    2044: 11,
    2046: 12,
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_pairs(path: Path) -> dict[int, int]:
    rows: dict[int, int] = {}
    for line_number, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split()
        assert len(fields) == 2, (path, line_number, raw)
        n, count = map(int, fields)
        assert n not in rows, (path, n)
        assert count >= 0, (path, n, count)
        rows[n] = count
    return rows


def parse_appendix_tail(path: Path) -> dict[int, int]:
    rows: dict[int, int] = {}
    wanted = {2000: 10, 2010: 10, 2020: 10, 2030: 10, 2040: 8}
    for raw in path.read_text().splitlines():
        fields = raw.split()
        if not fields or not fields[0].isdigit():
            continue
        base = int(fields[0])
        if base not in wanted:
            continue
        values = [int(value) for value in fields[1:]]
        if len(values) != wanted[base]:
            continue
        assert base not in rows
        rows.update({base + offset: value for offset, value in enumerate(values)})
    assert set(wanted).issubset(rows)
    return rows


def assert_live_gate() -> None:
    problem = (ROOT / "live_problem_1160_20260811.txt").read_text()
    discussion = (ROOT / "live_discussion_1160_20260811.txt").read_text()
    required_problem_markers = (
        "FETCHED: 2026-08-11 UTC",
        "OPEN",
        "0 claimed proofs for this problem",
        "Currently working on this problem\tNone",
        "Question 22.18",
        "perhaps even as soon as",
    )
    for marker in required_problem_markers:
        assert marker in problem, marker
    assert discussion.count("BorisAlexeev") == 2
    assert discussion.count("Thomas Bloom") == 1
    assert "All comments are the responsibility of the user" in discussion


def assert_site_absence() -> None:
    token = re.compile(r"(?<![0-9])1160(?![0-9])")
    for name in ("site_index_20260811.js", "site_ledger_data_20260811.js"):
        text = (ROOT / name).read_text()
        assert not token.search(text), f"exact decimal token 1160 occurs in {name}"


def assert_source_markers() -> None:
    conway = (ROOT / "conway_dietrich_obrien_2008.txt").read_text()
    burrell = (ROOT / "burrell_dissertation_2022.txt").read_text()
    eick = (ROOT / "eick_classification_recent.txt").read_text()
    assert "strictly exceeds 1774274116992170" in conway
    assert "The 423171191 groups of all the other orders < 2048" in conway
    assert "49,487,367,289, not 49,487,365,422" in burrell
    assert "only source of error in the original calculation" in burrell
    assert "49.487.367.289" in eick
    assert "f 2 (2048) = 1.774.274.116.992.170." in eick
    assert "f 2 (2048) \u2264 f (2048)" in eick


def main() -> None:
    assert sha256(BFILE) == EXPECTED_BFILE_SHA256
    counts = parse_pairs(BFILE)
    assert list(counts) == list(range(2048))
    assert counts[0] == 0
    assert counts[1024] == EXPECTED_G1024

    total = sum(counts[n] for n in range(2048))
    other_orders = total - counts[1024]
    assert total == EXPECTED_TOTAL
    assert other_orders == EXPECTED_OTHER_ORDERS

    expected_strong_truth = {
        0: True,
        1: True,
        2: False,
        3: False,
        4: False,
        5: False,
        6: False,
        7: True,
        8: True,
        9: True,
        10: True,
    }
    print("m  2^m  sum(n<2^m)  right_hand_side  strong_inequality")
    for m in range(11):
        power = 1 << m
        partial_sum = sum(counts[n] for n in range(power))
        passes = partial_sum <= counts[power]
        assert passes is expected_strong_truth[m]
        print(f"{m:2d} {power:5d} {partial_sum:14d} {counts[power]:15d} {passes}")

    gap_counts = parse_pairs(ROOT / "gap_available_counts_1_2047.txt")
    assert len(gap_counts) == 2034
    assert set(range(1, 2048)) - set(gap_counts) == set(EXPECTED_GAP_MISSING)
    assert all(counts[n] == value for n, value in gap_counts.items())

    appendix = parse_appendix_tail(ROOT / "conway_dietrich_obrien_2008.txt")
    assert {
        n: appendix[n] for n in EXPECTED_GAP_MISSING
    } == EXPECTED_GAP_MISSING
    reconstructed = sum(gap_counts.values()) + sum(EXPECTED_GAP_MISSING.values())
    assert reconstructed == total

    assert_source_markers()
    assert_live_gate()
    assert_site_absence()

    margin = LOWER_BOUND_G2048 - total
    assert margin == 1_774_224_206_453_690
    assert total < LOWER_BOUND_G2048
    print(
        f"11  2048 {total:14d} >={LOWER_BOUND_G2048:15d} True"
    )
    print(f"strict certified margin below published lower bound: {margin}")
    print("CONCLUSION: sum_{0<=n<2048} g(n) < g(2048).")
    print("Hence g(n) <= g(2048) for every 1 <= n <= 2048.")
    print("ALL EXACT CHECKS PASSED")


if __name__ == "__main__":
    main()
