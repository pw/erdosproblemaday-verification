#!/usr/bin/env python3
"""Check complete, unique center coverage and total the core-14 logs."""

import re
from pathlib import Path


PATTERN = re.compile(
    r"RESULT cap=133 core=14 t_range=(\d+)\.\.(\d+) found=(\d+) "
    r"orbit_nodes=(\d+) complete_cores=(\d+) valid_cores=(\d+) "
    r"extension_nodes=(\d+) "
    r"seconds=([0-9.e+-]+)"
)


def main() -> None:
    path = Path(__file__).with_name("direct_core14_slices.log")
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = PATTERN.fullmatch(line)
        if match:
            rows.append(
                tuple(map(int, match.groups()[:7]))
                + (float(match.group(8)),)
            )
    centers = [row[0] for row in rows]
    assert len(rows) == 85
    assert len(set(centers)) == 85
    assert set(centers) == set(range(49, 134))
    assert all(row[0] == row[1] and row[2] == 0 for row in rows)
    print("core14_slices=85 centers=49..133 unique_coverage=PASS")
    print(
        "orbit_nodes=%d valid_cores=%d extension_nodes=%d cpu_seconds=%.6f"
        % (
            sum(row[3] for row in rows),
            sum(row[5] for row in rows),
            sum(row[6] for row in rows),
            sum(row[7] for row in rows),
        )
    )


if __name__ == "__main__":
    main()
