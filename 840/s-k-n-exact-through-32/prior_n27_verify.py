#!/usr/bin/env python3
"""From-scratch checks for the Erdős #840 wave w018 report.

The main computation is an exhaustive determination of

    s(k,n) = max{|A+A| : A is a k-subset of {1,...,n}}

for every n <= 27.  Translation lets us restrict to sets containing 0.
The depth-first recurrence

    Sigma(A union {x}) = Sigma(A) union (x+A) union {2x}

updates the sumset as a bit mask in one step.  Exactly 2^26 translated
subsets are visited for n=27.

The script also:
  * recomputes all displayed witnesses by ordinary Python set arithmetic;
  * cross-checks the recurrence against a separate combinations-based
    exhaustive search for n <= 13;
  * tests the reflected-Sidon construction on every small Sidon set; and
  * checks the telescoping Fourier coefficients and constants used in the
    analytic-method barrier.

Runtime on the exe.dev VM used for the report: about 36-45 seconds.
No third-party packages are required.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import math
import sys
import time


MAX_N = 27
EXPECTED_ROW_27 = [
    1, 3, 6, 10, 15, 21, 28, 34, 41, 47, 51, 53,
    53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53,
    53, 53, 53,
]


def elements_from_mask(mask: int, shift: int = 0) -> tuple[int, ...]:
    """Return the increasing elements represented by a nonnegative bit mask."""
    answer: list[int] = []
    while mask:
        bit = mask & -mask
        answer.append(bit.bit_length() - 1 + shift)
        mask ^= bit
    return tuple(answer)


def direct_sumset(values: tuple[int, ...]) -> set[int]:
    """Compute A+A independently, with no bit-mask recurrence."""
    return {a + b for a in values for b in values}


def direct_sumset_mask(mask: int) -> int:
    """Compute the sumset mask directly from the element mask."""
    result = 0
    rest = mask
    while rest:
        bit = rest & -rest
        x = bit.bit_length() - 1
        result |= mask << x
        rest ^= bit
    return result


def exhaustive_incremental(max_n: int = MAX_N):
    """Enumerate every translated nonempty subset through the DFS recurrence."""
    # Entry [d][k] concerns sets with minimum 0, maximum exactly d, and size k.
    best_by_diameter = [[-1] * (max_n + 1) for _ in range(max_n)]
    witness_by_diameter = [[0] * (max_n + 1) for _ in range(max_n)]
    nodes = 0
    sampled_recurrence_checks = 0

    def visit(
        next_x: int,
        element_mask: int,
        sumset_mask: int,
        cardinality: int,
        diameter: int,
    ) -> None:
        nonlocal nodes, sampled_recurrence_checks
        nodes += 1

        # A sparse, deterministic independent check of the recurrence state.
        if nodes == 1 or nodes % 1_000_003 == 0:
            assert sumset_mask == direct_sumset_mask(element_mask)
            sampled_recurrence_checks += 1

        score = sumset_mask.bit_count()
        if score > best_by_diameter[diameter][cardinality]:
            best_by_diameter[diameter][cardinality] = score
            witness_by_diameter[diameter][cardinality] = element_mask

        for x in range(next_x, max_n):
            # The old element mask shifted by x is x+A; 2x is the new diagonal.
            visit(
                x + 1,
                element_mask | (1 << x),
                sumset_mask | (element_mask << x) | (1 << (2 * x)),
                cardinality + 1,
                x,
            )

    visit(1, 1, 1, 1, 0)
    assert nodes == 1 << (max_n - 1)

    # Prefix over diameters: diameter <= n-1 is equivalent to fitting in [n].
    table = [[-1] * (max_n + 1) for _ in range(max_n + 1)]
    witnesses = [[0] * (max_n + 1) for _ in range(max_n + 1)]
    current_best = [-1] * (max_n + 1)
    current_witness = [0] * (max_n + 1)
    for diameter in range(max_n):
        for k in range(1, max_n + 1):
            candidate = best_by_diameter[diameter][k]
            if candidate > current_best[k]:
                current_best[k] = candidate
                current_witness[k] = witness_by_diameter[diameter][k]
        n = diameter + 1
        table[n] = current_best.copy()
        witnesses[n] = current_witness.copy()

    return table, witnesses, nodes, sampled_recurrence_checks


def exhaustive_direct_small(table, limit: int = 13) -> int:
    """Independent, slower check using itertools and Python sets."""
    candidate_count = 0
    for n in range(1, limit + 1):
        for k in range(1, n + 1):
            best = -1
            # Translation reduces to 0 plus k-1 elements selected from 1,...,n-1.
            for tail in combinations(range(1, n), k - 1):
                candidate_count += 1
                values = (0,) + tail
                best = max(best, len(direct_sumset(values)))
            assert best == table[n][k], (n, k, best, table[n][k])
    return candidate_count


def check_all_reported_witnesses(table, witnesses, n: int = MAX_N) -> None:
    """Recompute every extremal witness by ordinary set arithmetic."""
    for k in range(1, n + 1):
        zero_based = elements_from_mask(witnesses[n][k])
        one_based = tuple(x + 1 for x in zero_based)
        assert len(one_based) == k
        assert one_based[0] == 1 and one_based[-1] <= n
        assert len(direct_sumset(one_based)) == table[n][k]


def is_sidon(values: tuple[int, ...]) -> bool:
    sums = [values[i] + values[j]
            for i in range(len(values))
            for j in range(i, len(values))]
    return len(sums) == len(set(sums))


def check_reflected_sidon_formula(max_m: int = 8) -> int:
    """Test |(B union (N-B))+(B union (N-B))|=2|B|^2+1 exhaustively."""
    sidon_sets_checked = 0
    for interval_length in range(1, max_m + 1):
        universe = range(1, interval_length + 1)
        n = 3 * interval_length
        for size in range(1, interval_length + 1):
            for values in combinations(universe, size):
                if not is_sidon(values):
                    continue
                sidon_sets_checked += 1
                reflected = tuple(sorted(set(values) | {n - b for b in values}))
                assert len(reflected) == 2 * size
                assert len(direct_sumset(reflected)) == 2 * size * size + 1
    return sidon_sets_checked


def check_fourier_arithmetic() -> tuple[float, float, float]:
    """Check the exact coefficient sum and the two published constants."""
    for cutoff in (1, 2, 3, 10, 100, 1000):
        coefficient_sum = sum(
            (Fraction(2, 4 * m * m - 1) for m in range(1, cutoff + 1)),
            Fraction(0),
        )
        assert coefficient_sum == 1 - Fraction(1, 2 * cutoff + 1)

    certificate_cost = 1.0 + math.pi / 2.0
    pikhurko_constant = (
        Fraction(1, 4) + 1.0 / (math.pi + 2.0) ** 2
    ) ** -0.5
    reflected_constant = 2.0 / math.sqrt(3.0)

    # The two algebraically equivalent forms of Pikhurko's constant.
    equivalent = 2.0 / math.sqrt(1.0 + 1.0 / certificate_cost ** 2)
    assert math.isclose(pikhurko_constant, equivalent, rel_tol=0, abs_tol=1e-14)
    assert 1.8639 < pikhurko_constant < 1.8640
    assert 1.1547 < reflected_constant < 1.1548
    return certificate_cost, pikhurko_constant, reflected_constant


def thresholds(table, n: int) -> tuple[int, int]:
    """Largest Sidon k and smallest full-sumset k for a fixed n."""
    sidon_max = max(k for k in range(1, n + 1)
                    if table[n][k] == k * (k + 1) // 2)
    basis_min = min(k for k in range(1, n + 1)
                    if table[n][k] == 2 * n - 1)
    return sidon_max, basis_min


def main() -> None:
    started = time.perf_counter()
    table, witnesses, nodes, sampled = exhaustive_incremental()
    elapsed = time.perf_counter() - started

    assert table[MAX_N][1:MAX_N + 1] == EXPECTED_ROW_27
    check_all_reported_witnesses(table, witnesses)
    direct_candidates = exhaustive_direct_small(table)
    sidon_checks = check_reflected_sidon_formula()
    cost, upper_constant, lower_constant = check_fourier_arithmetic()

    print(f"enumerated translated subsets: {nodes:,}")
    print(f"incremental enumeration seconds: {elapsed:.3f}")
    print(f"sampled direct recurrence checks: {sampled}")
    print(f"independent small-search candidates: {direct_candidates:,}")
    print(f"small reflected Sidon sets checked: {sidon_checks:,}")
    print("s(k,27), k=1..27:")
    print(" ".join(map(str, table[MAX_N][1:MAX_N + 1])))

    print("critical witnesses (one-based):")
    for k in range(7, 13):
        values = elements_from_mask(witnesses[MAX_N][k], shift=1)
        print(f"  k={k:2d}, s={table[MAX_N][k]:2d}: {values}")

    sidon_max, basis_min = thresholds(table, MAX_N)
    print(f"largest Sidon cardinality in [27]: {sidon_max}")
    print(f"smallest k with A+A=[2,54]: {basis_min}")
    print("thresholds n : (largest Sidon k, smallest full-basis k)")
    print(" ".join(f"{n}:({thresholds(table, n)[0]},{thresholds(table, n)[1]})"
                   for n in range(1, MAX_N + 1)))

    print(f"Fourier certificate infimum cost: 1+pi/2 = {cost:.15f}")
    print(f"Pikhurko upper constant: {upper_constant:.15f}")
    print(f"reflected-Sidon lower constant: {lower_constant:.15f}")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"CHECK FAILED: {exc!r}", file=sys.stderr)
        raise
