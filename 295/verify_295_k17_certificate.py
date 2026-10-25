#!/usr/bin/env python3
"""Small exact checks for the upper certificate and elementary lower cut."""

from fractions import Fraction
from math import lcm


DENOMINATORS = (
    17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
    32, 33, 34, 35, 36, 38, 39, 42, 43, 44, 45, 48, 50, 52,
    54, 63, 1_735_650, 68_479_214_496,
)


def main() -> None:
    assert len(DENOMINATORS) == len(set(DENOMINATORS)) == 32
    assert DENOMINATORS == tuple(sorted(DENOMINATORS))
    assert DENOMINATORS[0] == 17

    common = lcm(*DENOMINATORS)
    numerator = sum(common // d for d in DENOMINATORS)
    assert common == 200_301_702_400_800
    assert numerator == common
    assert sum((Fraction(1, d) for d in DENOMINATORS), Fraction()) == 1

    harmonic_28 = sum((Fraction(1, d) for d in range(17, 45)), Fraction())
    assert harmonic_28 == Fraction(
        9_344_202_253_751_673_739,
        9_419_588_158_802_421_600,
    )
    assert harmonic_28 < 1

    print(f"terms={len(DENOMINATORS)} minimum={DENOMINATORS[0]}")
    print(f"lcm={common} scaled_sum={numerator}")
    print(f"maximal_28_term_sum={harmonic_28}")
    print("CERTIFICATE CHECKS PASSED")


if __name__ == "__main__":
    main()
