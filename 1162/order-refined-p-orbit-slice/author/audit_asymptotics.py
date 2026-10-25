#!/usr/bin/env python3
"""Exact and numerical cross-checks for corrected equations (2)--(5)."""

from __future__ import annotations

import math
from pathlib import Path


def gaussian(n: int, r: int, p: int) -> int:
    if not 0 <= r <= n:
        return 0
    r = min(r, n - r)
    numerator = 1
    denominator = 1
    for index in range(r):
        numerator *= p ** (n - index) - 1
        denominator *= p ** (r - index) - 1
    assert numerator % denominator == 0
    return numerator // denominator


def full_support(m: int, r: int, p: int) -> int:
    return sum(
        (-1) ** omitted * math.comb(m, omitted) * gaussian(m - omitted, r, p)
        for omitted in range(m + 1)
    )


def framework(n: int, p: int) -> int:
    assert n % p == 0
    m = n // p
    denominator = math.factorial(m) * (p * (p - 1)) ** m
    assert math.factorial(n) % denominator == 0
    return math.factorial(n) // denominator


def check_rendered_operator() -> None:
    report = Path("REPORT.md").read_text()
    corrected = (
        "={}&\\frac{\\log_2p}{4p^2}n^2\n"
        "+\\left(1-\\frac1p\\right)n\\log_2 n"
    )
    assert corrected in report
    assert "n^2\n\\left(1-\\frac1p\\right)n\\log_2 n" not in report


def check_exponent_identities() -> None:
    for m in range(2, 101):
        r = m // 2
        assert r * (m - r) == (m * m) // 4
        if m % 2 == 0:
            s = m // 2
            for k in range(-s, s + 1):
                assert (s + k) * (s - k) == s * s - k * k
        else:
            s = m // 2
            for k in range(-s, s + 2):
                assert (s + k) * (s + 1 - k) == s * (s + 1) - k * (k - 1)

    assert math.log2(2) / (4 * 2**2) == 1 / 16
    assert 1 - 1 / 2 == 1 / 2
    assert math.log2(2 - 1) == 0


def residual(p: int, m: int) -> float:
    n = p * m
    r = m // 2
    exact = framework(n, p) * full_support(m, r, p)
    displayed = (
        math.log2(p) * n * n / (4 * p * p)
        + (1 - 1 / p) * n * math.log2(n)
        - ((1 - 1 / p) * math.log2(math.e) + math.log2(p - 1) / p) * n
    )
    return math.log2(exact) - displayed


def check_residuals() -> None:
    print("exact log2 residuals after all displayed terms in equation (2):")
    for p in (2, 3, 5):
        values = []
        for m in (40, 41, 80, 81):
            value = residual(p, m)
            assert math.isfinite(value) and abs(value) < 20
            values.append((m, value))
        rendered = ", ".join(f"m={m}: {value:.9f}" for m, value in values)
        print(f"  p={p}: {rendered}")


def check_finite_rank_laws() -> None:
    print("finite middle-rank ratios versus limiting theta weights:")
    for p, m in ((2, 40), (2, 41), (3, 30), (3, 31)):
        s = m // 2
        center = full_support(m, s, p)
        errors = []
        for k in range(-3, 4):
            r = s + k
            actual = full_support(m, r, p) / center
            exponent = k * k if m % 2 == 0 else k * (k - 1)
            expected = p ** (-exponent)
            errors.append(abs(actual - expected))
        maximum_error = max(errors)
        assert maximum_error < 0.001
        print(f"  p={p}, m={m}: max ratio error={maximum_error:.12g}")


def main() -> None:
    check_rendered_operator()
    check_exponent_identities()
    check_residuals()
    check_finite_rank_laws()
    print("ASYMPTOTIC SIGNS AND TERMS AUDIT PASSED")


if __name__ == "__main__":
    main()
