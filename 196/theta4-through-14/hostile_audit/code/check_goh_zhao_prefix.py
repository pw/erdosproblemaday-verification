#!/usr/bin/env python3
"""Translate Goh-Zhao arXiv v2 Table 1 into theta_4 values."""

import csv
from math import factorial
from pathlib import Path
import re


BASE = Path("/home/exedev/erdos_scratch/audit_196_20260811")
TEX = BASE / "provenance/goh_zhao_v2_source/ap-permsout.tex"
EXPECTED = Path(
    "/home/exedev/erdos_scratch/fresh9_erdos196_20260811/bundle_ro/expected_counts.tsv"
)


def main():
    text = TEX.read_text()
    start = text.index(r"\centerline{\smallheader Table 1}")
    stop = text.index(r"\endinsert", start)
    table = text[start:stop]

    rows = {}
    for line in table.splitlines():
        match = re.match(r"\s*(\d+)\s*&(.+?)\\cr\s*$", line)
        if not match:
            continue
        n = int(match.group(1))
        values = [int(field.strip()) for field in match.group(2).split("&")]
        rows[n] = values

    assert sorted(rows) == list(range(1, 13))
    with EXPECTED.open(newline="") as handle:
        expected = {
            int(row["n"]): int(row["theta4"])
            for row in csv.DictReader(handle, delimiter="\t")
        }

    for n in range(1, 13):
        distribution = rows[n]
        assert sum(distribution) == factorial(n), (n, sum(distribution), factorial(n))
        theta4 = sum(distribution[:3])
        assert theta4 == expected[n], (n, theta4, expected[n])
        padded = distribution + [0] * (3 - len(distribution))
        print(
            f"n={n} f1={padded[0]} f2={padded[1]} f3={padded[2]} "
            f"theta4={theta4} author={expected[n]} match=1 row_sum={sum(distribution)}"
        )

    print("published_prefix_matches_through=12")
    print("search_limited_unpublished_candidates=13,14")


if __name__ == "__main__":
    main()
