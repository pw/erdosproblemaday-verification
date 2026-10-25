#!/usr/bin/env python3
"""Directly check eight-mark maximal Sidon certificates through 136."""

from itertools import combinations_with_replacement


RULER = (0, 39, 47, 51, 52, 61, 67, 101)


def pair_sums(marks: tuple[int, ...]) -> list[int]:
    return [a + b for a, b in combinations_with_replacement(marks, 2)]


def blocked(marks: tuple[int, ...], candidate: int) -> bool:
    if candidate in marks:
        return True
    old = set(pair_sums(marks))
    return 2 * candidate in old or any(candidate + mark in old for mark in marks)


def component(marks: tuple[int, ...]) -> tuple[int, int]:
    lo, hi = min(marks), max(marks)
    assert all(blocked(marks, x) for x in range(lo, hi + 1))
    while blocked(marks, lo - 1):
        lo -= 1
    while blocked(marks, hi + 1):
        hi += 1
    return lo, hi


def main() -> None:
    sums = pair_sums(RULER)
    assert len(sums) == 36
    assert len(set(sums)) == len(sums)
    assert component(RULER) == (-16, 119)

    witnesses: dict[int, tuple[int, ...]] = {}
    for n in range(102, 137):
        shift = max(1, n - 119)
        marks = tuple(value + shift for value in RULER)
        assert 1 <= min(marks) and max(marks) <= n
        shifted_sums = pair_sums(marks)
        assert len(set(shifted_sums)) == 36
        assert all(blocked(marks, x) for x in range(1, n + 1))
        witnesses[n] = marks

    assert witnesses[102] == (1, 40, 48, 52, 53, 62, 68, 102)
    assert witnesses[128] == (9, 48, 56, 60, 61, 70, 76, 110)
    assert witnesses[136] == (17, 56, 64, 68, 69, 78, 84, 118)
    print(f"normalized ruler: {RULER}")
    print("blocked component: [-16,119] (length 136)")
    print("verified maximal eight-mark sets for every 102 <= n <= 136")
    print(f"n=102 witness: {witnesses[102]}")
    print(f"n=128 witness: {witnesses[128]}")
    print(f"n=136 witness: {witnesses[136]}")
    print("WITNESS CHECK PASSED")


if __name__ == "__main__":
    main()
