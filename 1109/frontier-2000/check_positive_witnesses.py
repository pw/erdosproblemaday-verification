#!/usr/bin/env python3
"""Minimal direct checker for the ten #1109 extension witnesses."""

from hashlib import sha256
from math import isqrt
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "pmc_positive_witnesses.txt"
TRANSITIONS = (1509, 1535, 1595, 1707, 1735, 1779, 1835, 1919, 1991, 1999)


def squarefree(value: int) -> bool:
    return value > 0 and all(
        value % (divisor * divisor) != 0
        for divisor in range(2, isqrt(value) + 1)
    )


def main() -> None:
    text = CERTIFICATE.read_text(encoding="ascii")
    pattern = re.compile(
        r"n=(\d+) target=(\d+) neighbors=\d+ edges=\d+ exists=True "
        r"graph_sha256=[0-9a-f]{64} witness=\{([0-9,]+)\}"
    )
    records = []
    checked_sums = 0
    for line in text.splitlines():
        match = pattern.fullmatch(line)
        assert match, line
        n = int(match.group(1))
        target = int(match.group(2))
        witness = tuple(map(int, match.group(3).split(",")))
        records.append((n, target, witness))

    assert tuple(n for n, _, _ in records) == TRANSITIONS
    assert tuple(target for _, target, _ in records) == tuple(range(44, 54))
    for n, target, witness in records:
        assert tuple(sorted(witness)) == witness
        assert len(witness) == len(set(witness)) == target + 1
        assert witness[-1] == n
        assert all(1 <= value <= n for value in witness)
        for left_index, left in enumerate(witness):
            for right in witness[left_index:]:
                assert squarefree(left + right), (n, left, right)
                checked_sums += 1

    print(f"certificate_sha256={sha256(CERTIFICATE.read_bytes()).hexdigest()}")
    print(f"witnesses={len(records)} checked_sums={checked_sums}")
    print("CONCLUSION all ten diagonal-inclusive lower certificates are valid")


if __name__ == "__main__":
    main()
