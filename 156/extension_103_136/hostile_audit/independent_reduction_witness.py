#!/usr/bin/env python3
"""Independent exact checks of the reduction and all 102..136 witnesses."""

from itertools import combinations, combinations_with_replacement


RULER = (0, 39, 47, 51, 52, 61, 67, 101)


def sums(marks: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a + b for a, b in combinations_with_replacement(marks, 2))


def differences(marks: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(b - a for a, b in combinations(marks, 2))


def is_sidon(marks: tuple[int, ...]) -> bool:
    values = sums(marks)
    return len(values) == len(set(values))


def blocked_by_literal_insertion(marks: tuple[int, ...], candidate: int) -> bool:
    if candidate in marks:
        return True
    return not is_sidon(tuple(sorted((*marks, candidate))))


def blocked_by_sums(marks: tuple[int, ...], candidate: int) -> bool:
    if candidate in marks:
        return True
    old = set(sums(marks))
    return 2 * candidate in old or any(candidate + mark in old for mark in marks)


def blocked_by_differences(marks: tuple[int, ...], candidate: int) -> bool:
    if candidate in marks:
        return True
    old = set(differences(marks))
    fresh = tuple(abs(candidate - mark) for mark in marks)
    return len(fresh) != len(set(fresh)) or any(value in old for value in fresh)


def check_formulations() -> tuple[int, int]:
    rulers = 0
    insertions = 0
    for size in range(1, 8):
        for marks in combinations(range(11), size):
            if marks[0] != 0 or not is_sidon(marks):
                continue
            rulers += 1
            assert len(differences(marks)) == len(set(differences(marks)))
            for candidate in range(-12, 23):
                answers = {
                    blocked_by_literal_insertion(marks, candidate),
                    blocked_by_sums(marks, candidate),
                    blocked_by_differences(marks, candidate),
                }
                assert len(answers) == 1, (marks, candidate, answers)
                insertions += 1
    return rulers, insertions


def check_interval_converse() -> int:
    checks = 0
    for n in range(102, 137):
        for length in range(n):
            for lo in range(-40, 1):
                for hi in range(max(length, lo + n - 1), 141):
                    left = max(lo, length - n + 1)
                    right = min(0, hi - n + 1)
                    assert left <= right
                    domain_lo = left
                    domain_hi = domain_lo + n - 1
                    assert lo <= domain_lo <= 0 <= length <= domain_hi <= hi
                    checks += 1
    return checks


def check_witnesses() -> tuple[int, int]:
    assert is_sidon(RULER)
    assert len(sums(RULER)) == 36
    assert all(
        blocked_by_literal_insertion(RULER, candidate)
        for candidate in range(-16, 120)
    )
    assert not blocked_by_literal_insertion(RULER, -17)
    assert not blocked_by_literal_insertion(RULER, 120)

    outside_insertions = 0
    for n in range(102, 137):
        shift = max(1, n - 119)
        marks = tuple(mark + shift for mark in RULER)
        assert len(marks) == 8 and 1 <= marks[0] < marks[-1] <= n
        assert is_sidon(marks)
        for candidate in range(1, n + 1):
            if candidate in marks:
                continue
            assert blocked_by_literal_insertion(marks, candidate), (n, candidate)
            outside_insertions += 1
    return 35, outside_insertions


def main() -> None:
    rulers, insertions = check_formulations()
    interval_checks = check_interval_converse()
    witness_count, outside_insertions = check_witnesses()
    print(f"small normalized Sidon rulers: {rulers}")
    print(f"three-way insertion comparisons: {insertions}")
    print(f"normalization converse interval checks: {interval_checks}")
    print(f"eight-mark witnesses checked: {witness_count}")
    print(f"literal outside insertions rejected: {outside_insertions}")
    print("INDEPENDENT_REDUCTION_AND_WITNESSES=PASS")


if __name__ == "__main__":
    main()
