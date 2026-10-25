#!/usr/bin/env python3
"""Cross-check both annulus scanners using the two-square factor criterion."""

from array import array
from pathlib import Path


LIMIT = 1_000_000
ROOT = Path(__file__).resolve().parent


def smallest_prime_factors(limit: int) -> array:
    spf = array("I", [0]) * (limit + 1)
    p = 2
    while p * p <= limit:
        if spf[p] == 0:
            for multiple in range(p * p, limit + 1, p):
                if spf[multiple] == 0:
                    spf[multiple] = p
        p += 1
    return spf


def is_sum_of_two_squares(n: int, spf: array) -> bool:
    if n == 0:
        return True
    remaining = n
    while remaining > 1:
        prime = spf[remaining] or remaining
        exponent = 0
        while remaining % prime == 0:
            remaining //= prime
            exponent += 1
        if prime % 4 == 3 and exponent % 2 == 1:
            return False
    return True


def parse_summary(filename: str) -> dict[str, int]:
    result = {}
    for line in (ROOT / filename).read_text().splitlines():
        fields = line.split()
        if len(fields) == 2 and fields[1].isdigit():
            result[fields[0]] = int(fields[1])
    return result


spf = smallest_prime_factors(LIMIT)
values = [n for n in range(LIMIT + 1) if is_sum_of_two_squares(n, spf)]
gaps = [(right - left, left, right) for left, right in zip(values, values[1:])]
widest = max(gaps, key=lambda gap: gap[0])
expected = {
    "REPRESENTED_COUNT": len(values),
    "FIRST": values[0],
    "LAST": values[-1],
    "MAX_GAP": widest[0],
    "MAX_GAP_LEFT": widest[1],
    "MAX_GAP_RIGHT": widest[2],
    "NONREPRESENTED_RUN": widest[0] - 1,
}

for filename in ("smoke_0_1e6.out", "independent_smoke.out"):
    observed = parse_summary(filename)
    for key, value in expected.items():
        assert observed[key] == value, (filename, key, observed[key], value)

assert expected == {
    "REPRESENTED_COUNT": 216_342,
    "FIRST": 0,
    "LAST": 1_000_000,
    "MAX_GAP": 35,
    "MAX_GAP_LEFT": 685_541,
    "MAX_GAP_RIGHT": 685_576,
    "NONREPRESENTED_RUN": 34,
}
print(
    "SMALL_FRONTIER_PASS method=spf_factor_criterion range=0..1000000 "
    "represented=216342 max_gap=35 endpoints=685541,685576 scanners=2"
)
