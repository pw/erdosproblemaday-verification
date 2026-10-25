#!/usr/bin/env python3
"""Exact, dependency-free checker for the k(18) <= 35 certificate."""

from fractions import Fraction


K17_WITNESS = (
    17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 32, 33,
    34, 35, 36, 38, 39, 42, 43, 44, 45, 48, 50, 52, 54, 63, 1735650,
    68479214496,
)

K18_WITNESS = (
    18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
    34, 35, 36, 38, 39, 40, 42, 43, 44, 45, 48, 50, 52, 54, 63, 640,
    337280, 1735650, 68479214496,
)

REPLACEMENT = (31, 40, 640, 337280)


def unit_sum(denominators):
    return sum((Fraction(1, d) for d in denominators), Fraction(0))


def check_witness(name, denominators, minimum, count):
    total = unit_sum(denominators)
    increasing = all(a < b for a, b in zip(denominators, denominators[1:]))
    print(f"{name}_count={len(denominators)}")
    print(f"{name}_minimum={min(denominators)}")
    print(f"{name}_strictly_increasing={increasing}")
    print(f"{name}_sum={total.numerator}/{total.denominator}")
    assert len(denominators) == count
    assert min(denominators) >= minimum
    assert increasing
    assert total == 1


def main():
    check_witness("k17_source", K17_WITNESS, 17, 32)
    check_witness("k18_upper", K18_WITNESS, 18, 35)

    replacement_sum = unit_sum(REPLACEMENT)
    print(f"replacement_sum={replacement_sum.numerator}/{replacement_sum.denominator}")
    print(f"replacement_equals_1_over_17={replacement_sum == Fraction(1, 17)}")
    assert replacement_sum == Fraction(1, 17)
    assert set(REPLACEMENT).isdisjoint(set(K17_WITNESS) - {17})
    assert set(K18_WITNESS) == (set(K17_WITNESS) - {17}) | set(REPLACEMENT)

    harmonic_30 = unit_sum(range(18, 48))
    harmonic_31 = unit_sum(range(18, 49))
    print(f"harmonic_18_through_47={harmonic_30.numerator}/{harmonic_30.denominator}")
    print(f"harmonic_18_through_47_lt_1={harmonic_30 < 1}")
    print(f"harmonic_18_through_48={harmonic_31.numerator}/{harmonic_31.denominator}")
    print(f"harmonic_18_through_48_gt_1={harmonic_31 > 1}")
    assert harmonic_30 < 1 < harmonic_31

    print("all_checks=PASS")


if __name__ == "__main__":
    main()
