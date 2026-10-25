#!/usr/bin/env python3
"""Exhaustively compare three Sidon/blocking formulations on small rulers."""

from itertools import combinations, combinations_with_replacement


def sums(marks: tuple[int, ...]) -> list[int]:
    return [a + b for a, b in combinations_with_replacement(marks, 2)]


def differences(marks: tuple[int, ...]) -> list[int]:
    return [b - a for a, b in combinations(marks, 2)]


def blocked_sum(marks: tuple[int, ...], x: int) -> bool:
    if x in marks:
        return True
    old = set(sums(marks))
    return 2 * x in old or any(x + a in old for a in marks)


def blocked_difference(marks: tuple[int, ...], x: int) -> bool:
    if x in marks:
        return True
    old = set(differences(marks))
    new = [abs(x - a) for a in marks]
    return len(set(new)) != len(new) or any(value in old for value in new)


def blocked_direct(marks: tuple[int, ...], x: int) -> bool:
    if x in marks:
        return True
    extended = tuple(sorted((*marks, x)))
    all_sums = sums(extended)
    return len(set(all_sums)) != len(all_sums)


def main() -> None:
    rulers = 0
    candidates = 0
    for maximum in range(6, 31):
        for interior in combinations(range(1, maximum), 5):
            marks = (0, *interior, maximum)
            sum_sidon = len(set(sums(marks))) == 28
            difference_sidon = len(set(differences(marks))) == 21
            assert sum_sidon == difference_sidon
            if not sum_sidon:
                continue
            rulers += 1
            for x in range(-maximum - 1, 2 * maximum + 2):
                candidates += 1
                values = {
                    blocked_sum(marks, x),
                    blocked_difference(marks, x),
                    blocked_direct(marks, x),
                }
                assert len(values) == 1, (marks, x, values)
    print(f"Sidon rulers checked: {rulers}")
    print(f"candidate insertions checked: {candidates}")
    assert rulers > 0 and candidates > 0
    print("SMALL FORMULATION CROSSCHECK PASSED")


if __name__ == "__main__":
    main()
