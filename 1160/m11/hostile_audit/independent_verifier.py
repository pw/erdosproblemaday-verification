#!/usr/bin/env python3
"""Independent hostile verifier for the finite m=11 result for Problem 1160."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


AUDIT = Path(__file__).resolve().parent
DEFAULT_SOURCE = Path("/home/exedev/erdos_scratch/erdos1160_m11_20260811")
SOURCE = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else DEFAULT_SOURCE
EXPECTED_MANIFEST_HASHES = {
    "erdos1160_m11_20260811": "2289951ca13d7a86e9878ac22b9f9d1d4185589545dca689e5ef1b403221525f",
    "erdos1160_m11_20260811_v2": "8cb5c802c759c3a2dc12fd3e203e00abb991bfaae5376e44ebaa71e48da6dd90",
}
EXPECTED_BFILE_HASH = "54358f9bf5875f13f2e56c89f55c5942f868cc96f7a7fa653e2b133d1ad5a0f3"
EXPECTED_TOTAL = 49_910_538_480
EXPECTED_G1024 = 49_487_367_289
EXPECTED_OTHER = 423_171_191
F2_2048 = 1_774_274_116_992_170


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest() -> None:
    manifest = SOURCE / "SHA256SUMS"
    assert digest(manifest) == EXPECTED_MANIFEST_HASHES[SOURCE.name]
    listed: dict[str, str] = {}
    for line in manifest.read_text().splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        assert match, line
        checksum, name = match.groups()
        assert name not in listed
        listed[name] = checksum
    actual = {
        str(path.relative_to(SOURCE))
        for path in SOURCE.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS"
    }
    assert set(listed) == actual
    for name, checksum in listed.items():
        assert digest(SOURCE / name) == checksum, name


def pairs(path: Path) -> dict[int, int]:
    result: dict[int, int] = {}
    for number, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split()
        assert len(fields) == 2, (path, number, raw)
        index, value = map(int, fields)
        assert index not in result and value >= 0
        result[index] = value
    return result


def appendix_tail() -> dict[int, int]:
    widths = {2000: 10, 2010: 10, 2020: 10, 2030: 10, 2040: 8}
    result: dict[int, int] = {}
    text = (SOURCE / "conway_dietrich_obrien_2008.txt").read_text()
    for raw in text.splitlines():
        fields = raw.split()
        if not fields or not fields[0].isdigit():
            continue
        base = int(fields[0])
        if base in widths and len(fields) == widths[base] + 1:
            assert not any(base + offset in result for offset in range(widths[base]))
            for offset, value in enumerate(fields[1:]):
                result[base + offset] = int(value)
    assert sorted(result) == list(range(2000, 2048))
    return result


def complete_2008_appendix() -> dict[int, int]:
    text = (SOURCE / "conway_dietrich_obrien_2008.txt").read_text()
    table = text.split("A   The number of groups for each order < 2048", 1)[1]
    result: dict[int, int] = {}
    for raw in table.splitlines():
        fields = raw.split()
        if not fields or not fields[0].isdigit():
            continue
        base = int(fields[0])
        if base % 10 or not 0 <= base <= 2040:
            continue
        width = 9 if base == 0 else 8 if base == 2040 else 10
        if len(fields) != width + 1:
            continue
        start = 1 if base == 0 else 0
        for offset, value in enumerate(fields[1:], start):
            index = base + offset
            assert index not in result
            result[index] = int(value)
    assert sorted(result) == list(range(1, 2048))
    return result


def source_checks() -> None:
    conway = (SOURCE / "conway_dietrich_obrien_2008.txt").read_text()
    burrell = (SOURCE / "burrell_dissertation_2022.txt").read_text()
    eick = (SOURCE / "eick_classification_recent.txt").read_text()

    assert re.search(r"gnu\(2048\).*?still not\s+precisely known", conway, re.S)
    assert re.search(
        r"exact number\s+of groups of order 2048 that have exponent-2 class 2",
        conway,
    )
    old = int(re.search(r"gnu\(1024\) = ([0-9]+)", conway).group(1))
    other = int(re.search(r"The ([0-9]+) groups of all the other orders < 2048", conway).group(1))
    assert old == 49_487_365_422 and other == EXPECTED_OTHER

    theorem = re.search(r"Theorem 3\.2\.1\. There are precisely ([0-9,]+) groups", burrell)
    assert theorem and int(theorem.group(1).replace(",", "")) == EXPECTED_G1024
    wrong, corrected = re.search(
        r"originally recorded as ([0-9]+) whereas the correct number is ([0-9]+)", burrell
    ).groups()
    assert (int(wrong), int(corrected)) == (933, 2800)
    assert old - int(wrong) + int(corrected) == EXPECTED_G1024
    assert "only source of error in the original calculation" in burrell

    assert "number f (n) of groups of order n" in eick
    lower = re.search(r"f 2 \(2048\) = ([0-9.]+)\.", eick)
    assert lower and int(lower.group(1).replace(".", "")) == F2_2048
    assert "f 2 (2048) ≤ f (2048)" in eick
    assert "f (2048) itself is not known" in eick
    assert "with lower p-central series of length 2" in eick


def main() -> None:
    assert len(sys.argv) <= 2, "usage: independent_verifier.py [bundle-directory]"
    verify_manifest()
    source_checks()

    bfile = SOURCE / "b000001_20260811.txt"
    assert digest(bfile) == EXPECTED_BFILE_HASH
    oeis = pairs(bfile)
    assert list(oeis) == list(range(2048)) and oeis[0] == 0

    printed_2008 = complete_2008_appendix()
    disagreements = [n for n in range(1, 2048) if printed_2008[n] != oeis[n]]
    assert disagreements == [1024]
    assert printed_2008[1024] == 49_487_365_422
    printed_2008[1024] = EXPECTED_G1024
    assert printed_2008 == {n: oeis[n] for n in range(1, 2048)}

    gap = pairs(AUDIT / "gap_414_counts.txt")
    missing = sorted(set(range(1, 2048)) - set(gap))
    assert missing == [2016, 2024, 2025, 2040]
    pinned_gap = pairs(AUDIT / "gap_412_counts.txt")
    pinned_missing = sorted(set(range(1, 2048)) - set(pinned_gap))
    assert pinned_missing == [
        2002, 2004, 2010, 2016, 2020, 2024, 2025,
        2028, 2030, 2034, 2040, 2044, 2046,
    ]
    assert all(pinned_gap[n] == oeis[n] for n in pinned_gap)
    tail = appendix_tail()
    rebuilt = dict(gap)
    rebuilt.update((n, tail[n]) for n in missing)
    assert sorted(rebuilt) == list(range(1, 2048))
    assert all(rebuilt[n] == oeis[n] for n in rebuilt)

    assert rebuilt[1024] == EXPECTED_G1024
    total = sum(rebuilt.values())
    assert total == EXPECTED_TOTAL
    assert total - rebuilt[1024] == EXPECTED_OTHER
    assert EXPECTED_OTHER + EXPECTED_G1024 == EXPECTED_TOTAL
    assert total < F2_2048

    # Every summand is nonnegative, so each proper-order count is at most the sum.
    assert all(oeis[n] <= total < F2_2048 for n in range(1, 2048))
    margin = F2_2048 - total
    print("bundle:", SOURCE)
    print("manifest: complete and valid")
    print("complete 2008 appendix cells parsed: 2047; sole stale cell: 1024")
    print("GAP 4.14 / SmallGrp 1.5.4 counts:", len(gap))
    print("pinned GAP 4.12 / SmallGrp 1.5.3 counts:", len(pinned_gap))
    print("appendix-only orders:", missing)
    print("g(1024):", rebuilt[1024])
    print("sum(1 <= n < 2048) g(n):", total)
    print("published subclass f_2(2048):", F2_2048)
    print("strict margin:", margin)
    print("VERIFIED: sum_{n<2^11} g(n) < f_2(2048) <= g(2048)")
    print("VERIFIED: g(n) < g(2048) for 1 <= n < 2048; equality at n=2048")


if __name__ == "__main__":
    main()
