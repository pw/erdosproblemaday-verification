#!/usr/bin/env python3
"""Compute rigorous density intervals and expose A386439's tail off-by-one.

For ordered 3-smooth numbers d_k and increments epsilon_k of f(k),

    alpha = (1/3) sum_k epsilon_k / d_k.

After a certified prefix K, 0 <= epsilon_k <= 1 gives an upper tail.  The
total reciprocal mass of all 3-smooth numbers is exactly 3, so the width is

    (1/3) * (3 - sum_{k<=K} 1/d_k).
"""

from __future__ import annotations

import argparse
import hashlib
import heapq
import json
from fractions import Fraction
from pathlib import Path


EXPECTED_BFILE_SHA256 = (
    "bba41cd187052c20e638c539893f16f73d23956f9900caa882e06778256b15ea"
)


def smooth_numbers(count: int) -> list[int]:
    heap = [1]
    seen = {1}
    values: list[int] = []
    while len(values) < count:
        value = heapq.heappop(heap)
        values.append(value)
        for child in (2 * value, 3 * value):
            if child not in seen:
                seen.add(child)
                heapq.heappush(heap, child)
    return values


def outward_decimal(value: Fraction, places: int, upper: bool) -> str:
    scale = 10**places
    scaled = value.numerator * scale
    integer = (scaled + value.denominator - 1) // value.denominator if upper else scaled // value.denominator
    digits = str(integer).rjust(places + 1, "0")
    return f"{digits[:-places]}.{digits[-places:]}"


def interval(
    values: list[int], increment_positions: set[int], through: int, places: int
) -> dict[str, object]:
    lower = sum(
        (Fraction(1, 3 * values[k - 1]) for k in increment_positions if k <= through),
        Fraction(0),
    )
    reciprocal_prefix = sum(
        (Fraction(1, value) for value in values[:through]), Fraction(0)
    )
    width = (Fraction(3) - reciprocal_prefix) / 3
    upper = lower + width
    return {
        "through": through,
        "last_smooth": str(values[through - 1]),
        "known_increments": sum(k <= through for k in increment_positions),
        "lower_outward": outward_decimal(lower, places, upper=False),
        "upper_outward": outward_decimal(upper, places, upper=True),
        "width_upper": outward_decimal(width, places, upper=True),
        "lower_fraction": f"{lower.numerator}/{lower.denominator}",
        "upper_fraction": f"{upper.numerator}/{upper.denominator}",
        "width_fraction": f"{width.numerator}/{width.denominator}",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bfile", type=Path, required=True)
    parser.add_argument("--frontier", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--places", type=int, default=60)
    args = parser.parse_args()

    raw = args.bfile.read_bytes()
    bfile_hash = hashlib.sha256(raw).hexdigest()
    if bfile_hash != EXPECTED_BFILE_SHA256:
        raise AssertionError(f"unexpected b-file SHA-256 {bfile_hash}")
    published_increments = {
        int(line.split()[1])
        for line in raw.decode("ascii").splitlines()
        if line and not line.startswith("#")
    }
    if len(published_increments) != 3335 or max(published_increments) != 5000:
        raise AssertionError("unexpected published endpoint")

    frontier = json.loads(args.frontier.read_text(encoding="ascii"))
    rows = frontier["rows"]
    if rows[0]["k"] != 5000 or rows[-1]["k"] < 5001:
        raise AssertionError("frontier does not extend the published endpoint")
    extended_increments = set(published_increments)
    extended_increments.update(
        int(row["k"]) for row in rows if row["k"] > 5000 and row["increment"] == 1
    )
    through = int(rows[-1]["k"])
    values = smooth_numbers(through + 1)

    published = interval(values, published_increments, 5000, args.places)
    extended = interval(values, extended_increments, through, args.places)

    published_lower = sum(
        (Fraction(1, 3 * values[k - 1]) for k in published_increments), Fraction(0)
    )
    bug_tail = Fraction(1) - sum(
        (Fraction(1, 3 * value) for value in values[:5001]), Fraction(0)
    )
    bug_upper = published_lower + bug_tail
    omitted = Fraction(1, 3 * values[5000])
    correct_upper = Fraction(
        int(published["upper_fraction"].split("/")[0]),
        int(published["upper_fraction"].split("/")[1]),
    )
    if bug_upper + omitted != correct_upper:
        raise AssertionError("off-by-one reconstruction failed")

    result = {
        "formula": "alpha=(1/3)*sum epsilon_k/d_k",
        "total_reciprocal_mass": "sum_{a,b>=0} 1/(2^a*3^b)=3",
        "bfile_sha256": bfile_hash,
        "published_5000_corrected": published,
        "extended": extended,
        "a386439_source_bug": {
            "description": (
                "the loop subtracts the k=5001 term before breaking, so its "
                "printed upper endpoint is smaller than the justified upper bound"
            ),
            "d_5001": str(values[5000]),
            "omitted_tail_term_fraction": f"{omitted.numerator}/{omitted.denominator}",
            "omitted_tail_term_upper": outward_decimal(omitted, args.places, upper=True),
            "source_bug_upper_outward": outward_decimal(bug_upper, args.places, upper=True),
            "correct_upper_outward": outward_decimal(correct_upper, args.places, upper=True),
        },
    }
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="ascii")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
