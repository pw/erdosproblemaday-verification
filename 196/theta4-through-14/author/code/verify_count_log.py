#!/usr/bin/env python3
"""Compare an optimized-enumerator log with the frozen finite table."""

import csv
from pathlib import Path
import re
import sys


COUNT_PATTERN = re.compile(r"^theta4\((\d+)\)=(\d+)\b")


def main():
    if len(sys.argv) != 4:
        raise SystemExit("usage: verify_count_log.py LOG EXPECTED_TSV MAX_N")

    log_path = Path(sys.argv[1])
    expected_path = Path(sys.argv[2])
    max_n = int(sys.argv[3])

    with expected_path.open(newline="") as handle:
        expected = {
            int(row["n"]): int(row["theta4"])
            for row in csv.DictReader(handle, delimiter="\t")
        }

    observed = {}
    for line in log_path.read_text().splitlines():
        match = COUNT_PATTERN.match(line)
        if match:
            n, value = map(int, match.groups())
            if n in observed:
                raise SystemExit(f"duplicate count for n={n}")
            observed[n] = value

    discrepancies = 0
    for n in range(1, max_n + 1):
        if n not in expected:
            print(f"n={n} expected_value=missing")
            discrepancies += 1
        elif observed.get(n) != expected[n]:
            print(f"n={n} expected={expected[n]} observed={observed.get(n)}")
            discrepancies += 1

    unexpected = sorted(set(observed) - set(range(1, max_n + 1)))
    if unexpected:
        print(f"unexpected_n_values={unexpected}")
        discrepancies += len(unexpected)

    print(f"counts_compared={max_n}")
    print(f"count_discrepancies={discrepancies}")
    raise SystemExit(discrepancies != 0)


if __name__ == "__main__":
    main()
