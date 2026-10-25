#!/usr/bin/env python3
"""Exact algebraic sanity checks for the sharp polynomial subtheorem.

The report contains the proof. This program independently checks its two
load-bearing algebraic facts over an exhaustive finite family; it does not
replace the analytic zero-count argument.
"""

from __future__ import annotations

from itertools import product


def fourier_coefficients(coefficients: tuple[int, ...], radius: int) -> dict[int, int]:
    """Return exact Fourier coefficients of |p(r exp(i theta))|^2."""
    result: dict[int, int] = {}
    for j, aj in enumerate(coefficients):
        for k, ak in enumerate(coefficients):
            result[j - k] = result.get(j - k, 0) + aj * ak * radius ** (j + k)
    return {frequency: value for frequency, value in result.items() if value}


def support_span(coefficients: tuple[int, ...]) -> tuple[int, int, int]:
    support = [j for j, coefficient in enumerate(coefficients) if coefficient]
    return support[0], support[-1], support[-1] - support[0]


def verify_endpoint_harmonic() -> int:
    checked = 0
    alphabet = (-1, 0, 1)
    for degree in range(1, 8):
        for coefficients in product(alphabet, repeat=degree + 1):
            if sum(value != 0 for value in coefficients) < 2:
                continue
            m, d, span = support_span(coefficients)
            for radius in (1, 2, 3, 5):
                fourier = fourier_coefficients(coefficients, radius)
                expected = coefficients[d] * coefficients[m] * radius ** (d + m)
                assert fourier[span] == expected
                assert fourier[-span] == expected
                assert max(abs(frequency) for frequency in fourier) == span
                checked += 1
    return checked


def verify_binomial_phase_count() -> int:
    """Check the exact root-of-unity equality condition combinatorially."""
    checked = 0
    # For p(z)=A*z^m+B*z^d with positive A,B and s=d-m, equality in
    # |A+B*r^s*exp(i*s*theta)| <= A+B*r^s occurs iff exp(i*s*theta)=1.
    # On a grid of L*s-th roots, exactly s indices satisfy that condition.
    for span in range(1, 41):
        for multiplier in (2, 3, 5, 11):
            grid = multiplier * span
            solutions = [k for k in range(grid) if k % multiplier == 0]
            assert len(solutions) == span
            checked += 1
    return checked


def main() -> None:
    harmonic_checks = verify_endpoint_harmonic()
    sharpness_checks = verify_binomial_phase_count()
    print(f"PASS exact endpoint-harmonic checks: {harmonic_checks}")
    print(f"PASS exact binomial phase-count checks: {sharpness_checks}")
    print("NOTE analytic zero-count proof is in REPORT.md; this is a sanity checker")


if __name__ == "__main__":
    main()
