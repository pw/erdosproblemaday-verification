#!/usr/bin/env python3
"""Exact certificate for the p-orbit subgroup slice in Erdos problem 1162.

For n = p*m + q, this checks the formula for subgroups H <= S_n having
exactly q fixed points, m nontrivial orbits of size p, and |H| = p^r.
Only Python's standard library is used.
"""

from __future__ import annotations

import argparse
import itertools
import math
from collections.abc import Iterator


def gaussian_binomial(n: int, k: int, p: int) -> int:
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    numerator = 1
    denominator = 1
    for i in range(k):
        numerator *= p ** (n - i) - 1
        denominator *= p ** (k - i) - 1
    assert numerator % denominator == 0
    return numerator // denominator


def full_support_subspaces(m: int, r: int, p: int) -> int:
    """Number of r-spaces in F_p^m contained in no coordinate hyperplane."""
    return sum(
        (-1) ** j * math.comb(m, j) * gaussian_binomial(m - j, r, p)
        for j in range(m + 1)
    )


def framework_count(n: int, p: int, m: int) -> int:
    """Conjugates of C_p^m with m p-orbits and n-pm fixed points."""
    q = n - p * m
    if q < 0:
        return 0
    denominator = math.factorial(q) * math.factorial(m) * (p * (p - 1)) ** m
    assert math.factorial(n) % denominator == 0
    return math.factorial(n) // denominator


def exact_slice_count(n: int, p: int, m: int, r: int) -> int:
    return framework_count(n, p, m) * full_support_subspaces(m, r, p)


def rref_bases(m: int, r: int, p: int) -> Iterator[tuple[tuple[int, ...], ...]]:
    """Generate every r-dimensional subspace of F_p^m by its unique RREF."""
    if not 0 <= r <= m:
        return
    for pivots in itertools.combinations(range(m), r):
        pivot_set = set(pivots)
        free_positions = [
            (row, col)
            for row, pivot in enumerate(pivots)
            for col in range(pivot + 1, m)
            if col not in pivot_set
        ]
        for values in itertools.product(range(p), repeat=len(free_positions)):
            rows = [[0] * m for _ in range(r)]
            for row, pivot in enumerate(pivots):
                rows[row][pivot] = 1
            for (row, col), value in zip(free_positions, values):
                rows[row][col] = value
            yield tuple(tuple(row) for row in rows)


def has_full_support(basis: tuple[tuple[int, ...], ...], m: int) -> bool:
    return all(any(row[col] for row in basis) for col in range(m))


def direct_subspace_count(m: int, r: int, p: int) -> int:
    return sum(has_full_support(basis, m) for basis in rref_bases(m, r, p))


def check_gaussian_recurrence(limit: int, primes: tuple[int, ...]) -> None:
    for p in primes:
        for n in range(1, limit + 1):
            for k in range(n + 1):
                lhs = gaussian_binomial(n, k, p)
                rhs = gaussian_binomial(n - 1, k, p)
                if k:
                    rhs += p ** (n - k) * gaussian_binomial(n - 1, k - 1, p)
                assert lhs == rhs, (p, n, k, lhs, rhs)


def check_direct_subspaces(cases: tuple[tuple[int, int], ...]) -> None:
    for p, m in cases:
        total = 0
        for r in range(m + 1):
            formula = full_support_subspaces(m, r, p)
            direct = direct_subspace_count(m, r, p)
            assert formula == direct, (p, m, r, formula, direct)
            total += formula
        print(f"direct RREF audit p={p}, m={m}: {total} full-support subspaces")


def print_main_table(max_n: int) -> None:
    print("\nfixed-order slice for p=2, n even, r=floor(n/4)")
    print("n\tr\tfull_support_spaces\tpairings\texact_subgroups\tlog2(count)")
    for n in range(4, max_n + 1, 2):
        m = n // 2
        r = m // 2
        spaces = full_support_subspaces(m, r, 2)
        pairings = framework_count(n, 2, m)
        count = spaces * pairings
        print(f"{n}\t{r}\t{spaces}\t{pairings}\t{count}\t{math.log2(count):.12f}")


def check_asymptotic_residual(max_n: int) -> None:
    residuals = []
    for n in range(4, max_n + 1, 2):
        m = n // 2
        r = m // 2
        count = exact_slice_count(n, 2, m, r)
        main = n * n / 16 + n * math.log2(n) / 2 - math.log2(math.e) * n / 2
        residuals.append((n, math.log2(count) - main))
    assert all(math.isfinite(value) for _, value in residuals)
    print("\np=2 asymptotic residual log2(count)-[n^2/16+(n/2)log2(n)-(n/2)log2(e)]")
    for n, value in residuals[-5:]:
        print(f"n={n}: {value:.12f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=40)
    args = parser.parse_args()
    if args.max_n < 4 or args.max_n % 2:
        parser.error("--max-n must be even and at least 4")

    check_gaussian_recurrence(16, (2, 3, 5, 7))
    print("Gaussian-binomial recurrence: PASS")
    check_direct_subspaces(((2, 6), (3, 4), (5, 3)))

    # Exact spot checks used in the report.
    assert full_support_subspaces(10, 5, 2) == 80189094
    assert framework_count(20, 2, 10) == 654729075
    assert exact_slice_count(20, 2, 10, 5) == 52502131339708050

    print_main_table(args.max_n)
    check_asymptotic_residual(max(200, args.max_n))
    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()
