#!/usr/bin/env python3
"""Independent reconstruction of the Erdos 1160 m=11 arithmetic."""

from __future__ import annotations

import re
from pathlib import Path


HERE = Path(__file__).resolve().parent


def read_two_column(path: Path) -> dict[int, int]:
    answer: dict[int, int] = {}
    for raw in path.read_text().splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        a, b = raw.split()
        key, value = int(a), int(b)
        if key in answer:
            raise AssertionError(f"duplicate key {key} in {path.name}")
        answer[key] = value
    return answer


def appendix_rows() -> dict[int, int]:
    text = (HERE / "conway_dietrich_obrien_2008.txt").read_text()
    widths = {2000: 10, 2010: 10, 2020: 10, 2030: 10, 2040: 8}
    answer: dict[int, int] = {}
    for line in text.splitlines():
        fields = line.split()
        if not fields or not fields[0].isdigit():
            continue
        base = int(fields[0])
        if base not in widths or len(fields) != widths[base] + 1:
            continue
        answer.update(
            (base + offset, int(value))
            for offset, value in enumerate(fields[1:])
        )
    if len(answer) != 48:
        raise AssertionError(f"parsed {len(answer)} appendix-tail cells, expected 48")
    return answer


def extract_published_numbers() -> tuple[int, int, int]:
    conway = (HERE / "conway_dietrich_obrien_2008.txt").read_text()
    burrell = (HERE / "burrell_dissertation_2022.txt").read_text()
    eick = (HERE / "eick_classification_recent.txt").read_text()

    other_match = re.search(
        r"The ([0-9]+) groups of all the other orders < 2048", conway
    )
    corrected_match = re.search(
        r"Theorem 3\.2\.1\. There are precisely ([0-9,]+) groups", burrell
    )
    lower_match = re.search(
        r"f 2 \(2048\) = ([0-9.]+)\.", eick
    )
    assert other_match and corrected_match and lower_match
    other = int(other_match.group(1))
    corrected = int(corrected_match.group(1).replace(",", ""))
    lower = int(lower_match.group(1).replace(".", ""))
    return other, corrected, lower


def main() -> None:
    gap = read_two_column(HERE / "gap_available_counts_1_2047.txt")
    absent = sorted(set(range(1, 2048)) - set(gap))
    assert len(gap) == 2034 and len(absent) == 13

    tail = appendix_rows()
    assert all(n in tail for n in absent)
    reconstructed = dict(gap)
    reconstructed.update((n, tail[n]) for n in absent)
    assert sorted(reconstructed) == list(range(1, 2048))
    total_without_oeis = sum(reconstructed.values())

    other_published, g1024_published, lower_bound = extract_published_numbers()
    assert reconstructed[1024] == g1024_published
    assert total_without_oeis - reconstructed[1024] == other_published
    assert other_published + g1024_published == total_without_oeis

    oeis = read_two_column(HERE / "b000001_20260811.txt")
    assert oeis[0] == 0 and sorted(oeis) == list(range(2048))
    disagreements = [n for n in range(1, 2048) if oeis[n] != reconstructed[n]]
    assert not disagreements
    assert sum(oeis.values()) == total_without_oeis
    assert total_without_oeis < lower_bound

    print(f"GAP-covered orders: {len(gap)}")
    print(f"appendix-supplied orders: {absent}")
    print(f"all non-1024 orders from reconstruction: {other_published}")
    print(f"corrected g(1024): {g1024_published}")
    print(f"reconstructed sum below 2048: {total_without_oeis}")
    print(f"published lower bound for g(2048): {lower_bound}")
    print(f"strict margin: {lower_bound - total_without_oeis}")
    print("INDEPENDENT RECONSTRUCTION PASSED")


if __name__ == "__main__":
    main()
