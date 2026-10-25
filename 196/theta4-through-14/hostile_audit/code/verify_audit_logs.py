#!/usr/bin/env python3
"""Verify every frozen numerical result and required audit sentinel."""

from argparse import ArgumentParser
from pathlib import Path
import csv
import re


BASE = Path(__file__).resolve().parents[1]
LOGS = BASE / "logs"


def expected_counts():
    with (BASE / "expected_counts.tsv").open(newline="") as handle:
        return {
            int(row["n"]): int(row["theta4"])
            for row in csv.DictReader(handle, delimiter="\t")
        }


def parse_counts(path, pattern):
    text = Path(path).read_text()
    rows = [(int(match.group(1)), int(match.group(2))) for match in pattern.finditer(text)]
    return text, rows


def require_exact(label, rows, maximum, expected):
    wanted = [(n, expected[n]) for n in range(1, maximum + 1)]
    assert rows == wanted, f"{label}: got {rows!r}, wanted {wanted!r}"
    print(f"method={label} compared={maximum} discrepancies=0")


def verify_fresh(automaton_path, insertion_path, expected):
    pattern = re.compile(r"^n=(\d+).*\btheta4=(\d+)\b", re.MULTILINE)
    for label, path in (("fresh_automaton", automaton_path), ("fresh_insertion", insertion_path)):
        text, rows = parse_counts(path, pattern)
        require_exact(label, rows, 14, expected)
        assert "exit_status=0" in text, f"{label}: missing clean time sentinel"


def verify_frozen(expected):
    author_pattern = re.compile(r"^theta4\((\d+)\)=(\d+)\b", re.MULTILINE)
    general_pattern = re.compile(r"^n=(\d+).*\btheta4=(\d+)\b", re.MULTILINE)

    author_text, rows = parse_counts(LOGS / "author_reproduce_n14.log", author_pattern)
    require_exact("author_endpoint", rows, 14, expected)
    for sentinel in (
        "manifest_discrepancies=0",
        "crosscheck_mismatches=0",
        "verification_mismatches=0",
        "count_discrepancies=0",
        "reproduction_discrepancies=0",
        "outer_exit_status=0",
    ):
        assert sentinel in author_text, f"author reproduction missing {sentinel}"

    automaton_text, rows = parse_counts(LOGS / "automaton_n14.log", general_pattern)
    require_exact("subsequence_automaton", rows, 14, expected)
    assert "exit_status=0" in automaton_text

    insertion_text, rows = parse_counts(LOGS / "insertion_n14.log", general_pattern)
    require_exact("maximum_insertion", rows, 14, expected)
    assert "exit_status=0" in insertion_text

    exhaustive_text, rows = parse_counts(LOGS / "exhaustive_controls.log", general_pattern)
    require_exact("python_permutations", rows, 9, expected)
    assert "all_exhaustive_controls_passed=1" in exhaustive_text
    assert "negative_control_ascending_only_n4=23 expected_full=22" in exhaustive_text

    goh_text, rows = parse_counts(LOGS / "goh_zhao_prefix_check.log", general_pattern)
    require_exact("goh_zhao_v2_translation", rows, 12, expected)
    assert "published_prefix_matches_through=12" in goh_text

    thread_text = (LOGS / "author_thread_matrix_n12.log").read_text()
    cases = re.split(r"^THREAD_CASE=(\d+)\s*$", thread_text, flags=re.MULTILINE)
    seen = []
    for index in range(1, len(cases), 2):
        threads = int(cases[index])
        body = cases[index + 1]
        rows = [(int(m.group(1)), int(m.group(2))) for m in author_pattern.finditer(body)]
        require_exact(f"author_threads_{threads}", rows, 12, expected)
        assert f"threads={threads}" in body
        seen.append(threads)
    assert seen == [1, 2, 3, 7, 16], seen

    required_sentinels = {
        "author_strict_rebuild.log": "strict_vs_frozen_cmp_exit=0",
        "author_tar_integrity.log": "cleanup_after_readonly_extract=PASS",
        "site_collision_frozen_strict.log": "collision_total=0",
        "site_collision_current_final_strict.log": "collision_total=0",
        "audit_sanitizer_n9.log": "n=9 theta4=168864",
        "author_sanitizer_n10.log": "crosscheck_mismatches=0",
    }
    for name, sentinel in required_sentinels.items():
        assert sentinel in (LOGS / name).read_text(), f"{name}: missing {sentinel}"

    live = (BASE / "provenance/live_196_final_20260811.txt").read_text()
    for sentinel in (
        "OPEN",
        "0 claimed proofs for this problem",
        "Currently working on this problem\tNone",
    ):
        assert sentinel in live, f"live capture missing {sentinel!r}"

    print("frozen_audit_discrepancies=0")


def main():
    parser = ArgumentParser()
    parser.add_argument("--fresh", nargs=2, metavar=("AUTOMATON_LOG", "INSERTION_LOG"))
    args = parser.parse_args()
    expected = expected_counts()
    assert sorted(expected) == list(range(1, 15))
    if args.fresh:
        verify_fresh(*args.fresh, expected)
    else:
        verify_frozen(expected)


if __name__ == "__main__":
    main()
