#!/usr/bin/env python3
"""Independent small-n checks for the Erdos #196 finite enumeration."""

from itertools import permutations
from math import factorial


EXPECTED = [1, 2, 6, 22, 102, 564, 3336, 22266, 168864]


def progressions(n):
    return [
        (a, a + d, a + 2 * d, a + 3 * d)
        for d in range(1, n)
        for a in range(n - 3 * d)
    ]


def monotone_count(permutation, aps):
    position = [0] * len(permutation)
    for index, value in enumerate(permutation):
        position[value] = index
    total = 0
    for a, b, c, d in aps:
        pa, pb, pc, pd = position[a], position[b], position[c], position[d]
        total += (pa < pb < pc < pd) or (pa > pb > pc > pd)
    return total


def verify_n(n):
    aps = progressions(n)
    avoiding = 0
    incidence_total = 0
    for permutation in permutations(range(n)):
        occurrences = monotone_count(permutation, aps)
        avoiding += occurrences == 0
        incidence_total += occurrences

    # Each fixed four-term AP has 4! relative orders, exactly two monotone.
    expected_incidence = factorial(n) * len(aps) // 12 if n >= 4 else 0
    assert incidence_total == expected_incidence, (n, incidence_total, expected_incidence)
    assert avoiding == EXPECTED[n - 1], (n, avoiding, EXPECTED[n - 1])
    return avoiding, len(aps), incidence_total


def main():
    for n in range(1, len(EXPECTED) + 1):
        avoiding, ap_count, incidence_total = verify_n(n)
        print(
            f"n={n} theta4={avoiding} four_aps={ap_count} "
            f"incidence_total={incidence_total}"
        )
    print("verification_mismatches=0")


if __name__ == "__main__":
    main()
