#!/usr/bin/env python3
"""Controlled failures for the public convex-proof checker."""

from verify_convex_proof import VerificationError, pair_count_gap, validate_vector


def expect_rejection(label: str, action) -> None:
    try:
        action()
    except VerificationError:
        return
    raise RuntimeError(f"tamper accepted: {label}")


def main() -> None:
    expect_rejection("hexagon pair total", lambda: validate_vector(6, (6, 6, 4), 3))
    expect_rejection("regular even pair total", lambda: validate_vector(8, (8, 8, 8, 5), 4))
    expect_rejection("multiplicity above n", lambda: validate_vector(6, (7, 5, 3), 3))
    expect_rejection("missing distance class", lambda: validate_vector(7, (7, 7), 3))
    if pair_count_gap(5, 4) >= 0:
        raise RuntimeError("weakened pair-count premise still reported a contradiction")
    print("TAMPER_TESTS_PASS rejected=4 weakened_pair_count=detected")


if __name__ == "__main__":
    main()
