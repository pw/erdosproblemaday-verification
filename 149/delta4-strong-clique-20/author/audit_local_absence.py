#!/usr/bin/env python3
"""Check exact local absence and disclose the related Problem 934 source overlap."""

from __future__ import annotations

import re
from pathlib import Path


HOME = Path("/home/exedev")
INDEX = HOME / "ErdosProblemADay/src/index.js"
LEDGER = HOME / "ErdosProblemADay/src/ledger_data.js"


def referenced_numbers(text: str) -> set[int]:
    numbers = {int(n) for n in re.findall(r"\bproblemNum\s*:\s*(\d+)", text)}
    numbers.update(
        int(n)
        for n in re.findall(
            r"\bn\s*:\s*(\d+)\s*,\s*(?:verdict|problem)\s*:", text
        )
    )
    return numbers


def main() -> None:
    index = INDEX.read_text()
    ledger = LEDGER.read_text()
    combined = index + "\n" + ledger
    used = referenced_numbers(combined)

    assert 149 not in used
    assert "arXiv:2607.02698" in ledger
    assert r"\frac{2607}{1987}" not in combined
    assert "2607/1987" not in combined

    print(f"referenced problem numbers found: {len(used)}")
    print("PASS exact-number gate: Problem 149 is absent")
    print("PASS exact-result gate: the KMP coefficient 2607/1987 is absent")
    print("DISCLOSURE: ledger Problem 934 cites arXiv:2607.02698")
    print("DISCLOSURE: #934 audits the paper's h_3 / L(G)^3 section, not this L(G)^2 theorem")
    print("LOCAL ABSENCE AUDIT PASSED WITH DISCLOSED SAME-PAPER OVERLAP")


if __name__ == "__main__":
    main()
