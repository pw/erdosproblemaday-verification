#!/usr/bin/env python3
"""Exact finite checks used in the Erdős problem #51 investigation.

The main routine ``min_inverse_phi`` is a multiplicative knapsack over the
divisors of a.  It is exact: if phi(n) = a and p^e || n, then

    phi(p^e) = (p - 1) p^(e - 1) | a,

so p - 1 | a.  Conversely, any choice of at most one exponent for each such
prime, whose totient contributions multiply to a, gives a preimage of a.

The optional dense scan uses a totient sieve.  A first occurrence encountered
while scanning n in increasing order is globally minimal, not just minimal
within the scan range.
"""

from __future__ import annotations

import argparse
from math import prod

from sympy import divisors, factorint, isprime, primerange, totient


def min_inverse_phi(a: int) -> int | None:
    """Return min {n >= 1: phi(n) = a}, or None if a is a nontotient."""
    if a < 1:
        raise ValueError("a must be positive")
    if a == 1:
        return 1

    # best[d] is the least product of processed prime powers whose totient
    # contributions multiply to d.
    best: dict[int, int] = {1: 1}
    for h in divisors(a):
        p = h + 1
        if not isprime(p):
            continue

        options: list[tuple[int, int]] = []
        contribution = h
        prime_power = p
        while a % contribution == 0:
            # p=2,e=1 has contribution 1 and only enlarges a candidate, so it
            # can never occur in the least preimage.
            if not (p == 2 and contribution == 1):
                options.append((contribution, prime_power))
            contribution *= p
            prime_power *= p

        # Snapshotting enforces "at most one exponent for this prime".
        old = list(best.items())
        for d, cost0 in old:
            for contribution, prime_power in options:
                new_d = d * contribution
                if a % new_d:
                    continue
                new_cost = cost0 * prime_power
                if new_cost < best.get(new_d, new_cost + 1):
                    best[new_d] = new_cost

    return best.get(a)


def print_primorial_phi_table(kmax: int = 15) -> None:
    """Test a_k=prod_{i<=k}(p_i-1), the tempting failed construction."""
    a = 1
    proposed_n = 1
    print("First-prime product construction")
    print("k p_k a_k proposed_n min_inverse min/a proposed/a")
    for k, p in enumerate(primerange(2, 10_000), start=1):
        if k > kmax:
            break
        a *= p - 1
        proposed_n *= p
        minimum = min_inverse_phi(a)
        assert minimum is not None
        assert int(totient(minimum)) == a
        print(
            k,
            p,
            a,
            proposed_n,
            minimum,
            f"{minimum / a:.12f}",
            f"{proposed_n / a:.12f}",
        )


def print_safe_marker_chain() -> None:
    """Verify a finite chain whose chosen preimage really is minimal."""
    chain = [3, 5, 17, 47, 347, 1187, 1367, 5387]
    print("\nFinite forced-marker chain")
    print("last_prime n phi(n) n/phi(n) exact_minimum")
    for k in range(2, len(chain) + 1):
        support = chain[:k]
        n = prod(support)
        a = prod(p - 1 for p in support)
        minimum = min_inverse_phi(a)
        print(support[-1], n, a, f"{n / a:.12f}", minimum)
        assert minimum == n
        assert int(totient(n)) == a

    n = prod(chain)
    a = int(totient(n))
    print("factor(n) =", factorint(n))
    print("factor(phi(n)) =", factorint(a))


def dense_record_scan(limit: int) -> None:
    """Print record ratios M(phi(n))/phi(n) for minimal n <= limit."""
    import numpy as np

    if limit >= 2**32:
        raise ValueError("the NumPy scan uses uint32 and needs limit < 2^32")

    phi = np.arange(limit + 1, dtype=np.uint32)
    for p in range(2, limit + 1):
        if phi[p] == p:
            multiples = phi[p::p]
            multiples -= multiples // p

    missing = np.iinfo(np.uint32).max
    first = np.full(limit + 1, missing, dtype=np.uint32)
    indices = np.arange(limit + 1, dtype=np.uint32)
    np.minimum.at(first, phi, indices)

    minimal_mask = first[phi] == indices
    candidate_n = np.flatnonzero(minimal_mask)
    candidate_n = candidate_n[candidate_n >= 1]
    ratios = candidate_n / phi[candidate_n]
    running_max = np.maximum.accumulate(ratios)
    record_mask = np.ones(len(candidate_n), dtype=bool)
    record_mask[1:] = ratios[1:] > running_max[:-1]

    print(f"\nDense exact scan through n={limit}")
    print("n phi(n) ratio factor(n) factor(phi(n))")
    for n0 in candidate_n[record_mask]:
        n = int(n0)
        a = int(phi[n])
        print(n, a, f"{n / a:.12f}", factorint(n), factorint(a))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scan-limit",
        type=int,
        default=0,
        help="also run the memory-intensive dense totient scan through this n",
    )
    args = parser.parse_args()

    print_primorial_phi_table()
    print_safe_marker_chain()
    if args.scan_limit:
        dense_record_scan(args.scan_limit)


if __name__ == "__main__":
    main()
