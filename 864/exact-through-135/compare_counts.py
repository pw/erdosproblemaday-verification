#!/usr/bin/env python3
"""Cross-check valid-core counts between the independent implementations."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DIRECT_VALID = re.compile(
    r"RESULT cap=133 core=(\d+) .* valid_cores=(\d+)"
)
AUDIT = re.compile(r"CASE (\d+) .* valid_cores=(\d+)")


def main() -> None:
    direct: dict[int, int] = {}
    for core in range(15, 20):
        text = (ROOT / f"direct_core{core}.log").read_text(encoding="utf-8")
        match = DIRECT_VALID.search(text)
        assert match and int(match.group(1)) == core
        direct[core] = int(match.group(2))

    core14 = (ROOT / "direct_core14_slices.log").read_text(encoding="utf-8")
    matches = [
        (int(core), int(count))
        for core, count in DIRECT_VALID.findall(core14)
    ]
    assert len(matches) == 85 and all(core == 14 for core, _ in matches)
    direct[14] = sum(count for _, count in matches)

    audit = {
        int(core): int(count)
        for core, count in AUDIT.findall(
            (ROOT / "audit_output.txt").read_text(encoding="utf-8")
        )
    }
    expected = {
        19: 0,
        18: 1297,
        17: 22271,
        16: 1920748,
        15: 1565022,
        14: 22183488,
    }
    assert direct == audit == expected
    for core in range(19, 13, -1):
        print(f"core={core} valid_cores={expected[core]}")
    print("DIRECT/AUDIT VALID-CORE COUNTS: MATCH")


if __name__ == "__main__":
    main()
