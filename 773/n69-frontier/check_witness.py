#!/usr/bin/env python3
"""Standard-library verifier for an Erdős #773 square-Sidon witness."""

from __future__ import annotations

from itertools import combinations_with_replacement


WITNESS_N69: tuple[int, ...] = (
    3, 4, 6, 12, 13, 15, 17, 19, 23, 25, 28, 34, 35, 38, 42, 45,
    48, 49, 53, 54, 56, 57, 58, 60, 61, 62, 63, 64, 65, 66, 68, 69,
)

WITNESS_N70: tuple[int, ...] = (
    1, 4, 6, 7, 9, 10, 12, 13, 16, 18, 19, 22, 24, 28, 30, 34, 36,
    37, 39, 40, 43, 46, 49, 51, 52, 57, 58, 60, 64, 65, 67, 69, 70,
)


def check(indices: tuple[int, ...], n: int) -> None:
    assert tuple(sorted(set(indices))) == indices
    assert 1 <= indices[0] and indices[-1] <= n
    seen: dict[int, tuple[int, int]] = {}
    for i, j in combinations_with_replacement(indices, 2):
        value = i * i + j * j
        assert value not in seen, (value, seen[value], (i, j))
        seen[value] = (i, j)

    expected = len(indices) * (len(indices) + 1) // 2
    assert len(seen) == expected
    print(
        f"PASS: {len(indices)} indices in [1,{n}] produce "
        f"{expected} distinct unordered two-square sums"
    )


def main() -> None:
    assert len(WITNESS_N69) == 32
    assert len(WITNESS_N70) == 33
    check(WITNESS_N69, 69)
    check(WITNESS_N70, 70)



if __name__ == "__main__":
    main()
