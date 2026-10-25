#!/usr/bin/env python3
"""Cold boundary/count audit against an SPF two-square classifier."""

import os
import random
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MAXIMUM = 1_000_000


def smallest_prime_factors(limit):
    spf = list(range(limit + 1))
    for p in range(2, int(limit**0.5) + 1):
        if spf[p] == p:
            for multiple in range(p * p, limit + 1, p):
                if spf[multiple] == multiple:
                    spf[multiple] = p
    return spf


SPF = smallest_prime_factors(MAXIMUM)


def represented(n):
    if n == 0:
        return True
    while n > 1:
        p = SPF[n]
        exponent = 0
        while n % p == 0:
            n //= p
            exponent += 1
        if p % 4 == 3 and exponent % 2:
            return False
    return True


def truth(lo, hi, threshold):
    values = [n for n in range(lo, hi + 1) if represented(n)]
    gaps = [(b - a, a, b) for a, b in zip(values, values[1:])]
    widest = (0, 0, 0)
    for gap in gaps:
        if gap[0] > widest[0]:
            widest = gap
    return {
        "REPRESENTED_COUNT": len(values),
        "FIRST": values[0] if values else 0,
        "LAST": values[-1] if values else 0,
        "MAX_GAP": widest[0],
        "MAX_GAP_LEFT": widest[1],
        "MAX_GAP_RIGHT": widest[2],
        "reported": [gap for gap in gaps if gap[0] >= threshold],
    }


def invoke(binary, lo, hi, chunk, threshold):
    env = dict(os.environ, OMP_NUM_THREADS="2")
    result = subprocess.run(
        [str(ROOT / binary), str(lo), str(hi), str(chunk), str(threshold)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=True,
        env=env,
    )
    fields, gaps = {}, []
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1].isdigit():
            fields[parts[0]] = int(parts[1])
        elif len(parts) == 4 and parts[0] == "GAP":
            gaps.append(tuple(map(int, parts[1:])))
    fields["reported"] = gaps
    return fields


def check_case(lo, hi, chunk, threshold, require_boundary_fields=True):
    expected = truth(lo, hi, threshold)
    for binary in ("primary_audit", "independent_audit"):
        got = invoke(binary, lo, hi, chunk, threshold)
        keys = ["REPRESENTED_COUNT", "MAX_GAP", "MAX_GAP_LEFT",
                "MAX_GAP_RIGHT", "reported"]
        if require_boundary_fields:
            keys += ["FIRST", "LAST"]
        for key in keys:
            assert got[key] == expected[key], (binary, lo, hi, chunk, key,
                                                got[key], expected[key])


def main():
    # Claimed-run geometry: both closed boundaries are represented.
    fixed = [
        (0, 500, 1, 3),
        (0, 10_000, 97, 10),
        (1, 100_000, 4093, 15),
        (25, 250_000, 8191, 15),
        (100, 1_000_000, 33331, 20),
    ]
    for case in fixed:
        assert represented(case[0]) and represented(case[1])
        check_case(*case)

    rng = random.Random(222_20260811)
    reps = [n for n in range(MAXIMUM + 1) if represented(n)]
    for _ in range(30):
        left_index = rng.randrange(len(reps) - 200)
        right_index = min(len(reps) - 1, left_index + rng.randrange(2, 200))
        lo, hi = reps[left_index], reps[right_index]
        width = hi - lo + 1
        chunk = rng.randrange(1, max(2, min(width, 5000)))
        threshold = rng.randrange(2, 20)
        check_case(lo, hi, chunk, threshold)

    # Arbitrary nonrepresented boundaries still preserve counts and gaps.
    check_case(3, 9973, 1, 10, require_boundary_fields=False)

    # Explicitly expose two output-only edge cases outside the frozen claim.
    primary = invoke("primary_audit", 3, 100, 1, 2)
    assert primary["REPRESENTED_COUNT"] > 0 and primary["FIRST"] == 0
    empty_lo, empty_hi = 685_542, 685_575
    assert not any(represented(n) for n in range(empty_lo, empty_hi + 1))
    independent = invoke("independent_audit", empty_lo, empty_hi, 7, 2)
    assert independent["REPRESENTED_COUNT"] == 0
    assert independent["NONREPRESENTED_RUN"] == 2**64 - 1

    print("SCANNER_HARNESS_PASS represented_endpoint_cases=35 arbitrary_boundary_cases=1")
    print("COUNTS_GAPS_BOUNDARIES_PASS methods=primary,independent truth=SPF_factor_criterion")
    print("SCOPED_DIAGNOSTIC primary_FIRST_is_0_when_first_chunk_empty")
    print("SCOPED_DIAGNOSTIC independent_NONREPRESENTED_RUN_underflows_on_empty_global_interval")
    print("CLAIM_IMPACT none: both frozen scans have represented LO and HI and many marks")


if __name__ == "__main__":
    main()
