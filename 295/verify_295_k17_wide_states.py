#!/usr/bin/env python3
"""Independent certificate for the two wide terminal states in #295.

For a reduced remainder a/b, solutions of a/b = 1/x + 1/y with x < y
correspond to divisors q = ax-b of b^2 below b and congruent to -b modulo a.
This checker uses a meet-in-the-middle split by prime support, rather than the
recursive divisor traversal in verify_295_k17_independent.cpp.
"""

from bisect import bisect_left, bisect_right
from collections import defaultdict
from math import prod


STATES = (
    (
        2_511_623_003,
        219_060_189_739_591_200,
        63,
        (
            (2, 5), (3, 3), (5, 2), (7, 1), (11, 1), (13, 1),
            (17, 1), (19, 1), (23, 1), (29, 1), (31, 1),
            (37, 1), (41, 1),
        ),
    ),
    (
        133_025_383_151,
        9_419_588_158_802_421_600,
        77,
        (
            (2, 5), (3, 3), (5, 2), (7, 1), (11, 1), (13, 1),
            (17, 1), (19, 1), (23, 1), (29, 1), (31, 1),
            (37, 1), (41, 1), (43, 1),
        ),
    ),
)


def partial_divisors(factors):
    values = [1]
    for prime, exponent_in_b in factors:
        powers = [prime**j for j in range(2 * exponent_in_b + 1)]
        values = [value * power for value in values for power in powers]
    return values


def check_state(a, b, lower, factors):
    assert prod(prime**exponent for prime, exponent in factors) == b

    # The factor split is disjoint in prime support, so every divisor of b^2
    # has exactly one representation left_value * right_value.
    left = partial_divisors(factors[:5])
    right = sorted(partial_divisors(factors[5:]))
    right_by_residue = defaultdict(list)
    for value in right:
        right_by_residue[value % a].append(value)

    minimum_q = max(1, a * lower - b)
    target_residue = (-b) % a
    divisors_below_b = 0
    matches = []

    for left_value in left:
        divisors_below_b += bisect_right(right, (b - 1) // left_value)

        # gcd(left_value,a)=1 because gcd(a,b)=1 and left_value divides b^2.
        right_residue = (
            target_residue * pow(left_value, -1, a)
        ) % a
        candidates = right_by_residue.get(right_residue, ())
        lower_right = (minimum_q + left_value - 1) // left_value
        upper_right = (b - 1) // left_value
        first = bisect_left(candidates, lower_right)
        last = bisect_right(candidates, upper_right)
        matches.extend(left_value * value for value in candidates[first:last])

    tau_b_squared = prod(2 * exponent + 1 for _, exponent in factors)
    expected_below_b = (tau_b_squared - 1) // 2
    assert divisors_below_b == expected_below_b
    assert not matches
    return tau_b_squared, divisors_below_b, minimum_q, target_residue


def main():
    for a, b, lower, factors in STATES:
        tau, count, minimum_q, residue = check_state(a, b, lower, factors)
        print(f"a={a} b={b} lower={lower}")
        print(
            f"factor_product_ok=True tau_b2={tau} "
            f"divisors_strictly_below_b={count}"
        )
        print(
            f"q_interval=[{minimum_q},{b - 1}] "
            f"residue={residue} mod {a} matches=[]"
        )
    print("WIDE STATES VERIFIED: no two-term completion")


if __name__ == "__main__":
    main()
