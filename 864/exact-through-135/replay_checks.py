#!/usr/bin/env python3
"""Hostile frozen-artifact checks, excluding the expensive enumerations."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def main() -> None:
    audit = read("audit_output.txt")
    audit_time = read("audit_time.txt")
    expected = {
        19: 0,
        18: 1297,
        17: 22271,
        16: 1920748,
        15: 1565022,
        14: 22183488,
    }
    audit_counts = {
        int(core): int(count)
        for core, count in re.findall(
            r"CASE (\d+) .* valid_cores=(\d+)", audit
        )
    }
    assert audit_counts == expected
    assert "CASE REDUCTION core sizes 14,15,16,17,18,19 PASS" in audit
    assert "EXHAUSTED: no valid 19-set has diameter <= 133" in audit
    assert "Exit status: 0" in audit_time

    controls = {}
    for core in range(14, 19):
        text = read(f"control18_core{core}.log")
        match = re.search(r"valid_cores=(\d+)", text)
        assert match and "found=0" in text
        controls[core] = int(match.group(1))
    assert controls == {
        18: 0,
        17: 105,
        16: 43399,
        15: 114112,
        14: 2837087,
    }

    sanitizer = read("sanitizer_output.txt")
    assert "negative_rc=0" in sanitizer
    assert "positive_rc=2" in sanitizer
    assert "WITNESS 0 4 5 7 17 33 44 52 58 67 76 82 90 101 117 127 129 130 134" in sanitizer
    assert "ERROR: AddressSanitizer" not in sanitizer
    assert "runtime error:" not in sanitizer

    debug = read("debug_positive_output.txt")
    assert "debug_positive_rc=2" in debug and "WITNESS" in debug

    gate = read("live_gate.txt")
    assert "OPEN" in gate
    assert "0 claimed proofs for this problem" in gate
    assert "Interested in collaborating\tNone" in gate
    assert "Currently working on this problem\tNone" in gate

    source = read("search_direct.cpp")
    assert "int max_lower = (exception - 1) / 2;" in source
    assert "int max_b = max_lower - orbits_needed + 1;" in source

    print("audit counts/final status: PASS")
    print("target-18 frozen-count regression: PASS")
    print("sanitizer/debug positive and negative controls: PASS")
    print("live gate OPEN/0/no worker/no collaborator: PASS")
    print("inclusive even-core endpoint source guard: PASS")


if __name__ == "__main__":
    main()
