#!/usr/bin/env python3
"""Gap-free audit of all solver logs used to exclude degrees 7 through 12."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path
import re


H_CASE = re.compile(r"^CASE .* case=(\d+)/(\d+) .* result=(\w+)")
PRODUCT = re.compile(r"^PAIR .* flat=(\d+)/(\d+) .* result=(\w+)")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_lines(paths: list[Path], pattern: re.Pattern[str], expected: int) -> None:
    seen: set[int] = set()
    totals: set[int] = set()
    done = 0
    for path in paths:
        for line in path.read_text().splitlines():
            match = pattern.match(line)
            if match:
                index, total, result = match.groups()
                index, total = int(index), int(total)
                assert index not in seen, (path, index)
                seen.add(index)
                totals.add(total)
                assert result == "False", (path, index, result)
            elif line.startswith("SHARD_DONE "):
                done += 1
    assert totals == {expected}, totals
    assert seen == set(range(expected)), (len(seen), expected)
    assert done == len(paths), (done, len(paths))


def audit_table(path: Path, expected: int) -> None:
    with path.open(newline="") as source:
        rows = list(csv.DictReader(source, delimiter="\t"))
    assert len(rows) == expected
    assert [int(row["case"]) for row in rows] == list(range(expected))
    assert all(row["result"] == "False" for row in rows)


def audit_d12_log(path: Path) -> None:
    seen = []
    for line in path.read_text().splitlines():
        match = re.search(r"(?:^| )case=(\d+)(?:/8)? .* result=False", line)
        if match:
            seen.append(int(match.group(1)))
    assert seen == list(range(8)), (path, seen)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_sweep_logs")
    parser.add_argument("prior_delta10")
    parser.add_argument("raw_hash_manifest")
    args = parser.parse_args()
    raw = Path(args.raw_sweep_logs)
    prior = Path(args.prior_delta10)

    expected_hashes = {}
    for line in Path(args.raw_hash_manifest).read_text().splitlines():
        match = re.match(r"^([0-9a-f]{64})  (d(?:7|8|9|10)_.+\.log)$", line)
        if match:
            value, name = match.groups()
            expected_hashes[name] = value
    assert len(expected_hashes) == 17
    for name, expected in expected_hashes.items():
        assert sha256(raw / name) == expected, name

    d7 = [raw / "d7_alpha3_cadical_s0.log"]
    d8 = [raw / f"d8_alpha3_cadical_s{shard}.log" for shard in range(2)]
    d9 = [raw / f"d9_double_cadical_s{shard}.log" for shard in range(7)]
    d10 = [raw / f"d10_double_cadical_s{shard}.log" for shard in range(7)]
    audit_lines(d7, H_CASE, 353)
    audit_lines(d8, H_CASE, 1829)
    audit_lines(d9, PRODUCT, 1566787)
    audit_lines(d10, PRODUCT, 616848)
    print("DEGREES_7_10 unique_indices=2185817 all_UNSAT=YES shards_done=17 hashes=PASS")

    audit_table(prior / "d11_all_cases.tsv", 403)
    audit_table(prior / "d11_kissat_all_cases.tsv", 403)
    audit_d12_log(prior / "d12_all_cases.log")
    audit_d12_log(prior / "d12_kissat.log")
    assert (prior / "census_n13.g6").read_bytes() == b""
    print("DEGREES_11_12 cadical_and_kissat_exact_case_coverage=411/411 all_UNSAT=YES")
    print("DEGREE_13_PLUS complete_neighbourhood_census_empty=YES")
    print("VERIFIED GAP-FREE DEGREE COVERAGE d=7..12; d>=13 census empty")


if __name__ == "__main__":
    main()
