#!/usr/bin/env python3
"""Probe the sharp 2-by-4 van Doorn--Li--Tang construction for c_8.

The construction gives eight moduli whose full divisibility neighborhood in an
open interval of length twice the largest modulus consists of six points.  This
script builds a concrete instance, measures the valuation deficit after using
those six points, and checks whether two further interval points repair it.
"""

from __future__ import annotations

from math import gcd, lcm, prod


S = 2
T = 4
D = lcm(*range(1, S * T + 1))


def factor(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def merge_congruences(a: int, m: int, b: int, n: int) -> tuple[int, int]:
    """Return x mod lcm(m,n) satisfying x=a mod m and x=b mod n."""
    g = gcd(m, n)
    assert (b - a) % g == 0
    m1, n1 = m // g, n // g
    k = ((b - a) // g * pow(m1, -1, n1)) % n1
    modulus = m * n1
    return (a + m * k) % modulus, modulus


def forbidden_primes() -> set[int]:
    primes: set[int] = set()
    for q in (-1, 1):
        for r in range(-(T - 1), T):
            n = abs(q + r * D)
            primes.update(p for p in factor(n) if p > S * T)
    return primes


def choose_m() -> int:
    forbidden = forbidden_primes()
    for m in range(2 * S + 2 * T * D + 1, 100_000):
        if all(
            m % p not in {(-i - j * D) % p for i in range(1, S + 1) for j in range(1, T + 1)}
            for p in forbidden
        ):
            return m
    raise RuntimeError("no admissible M found")


def valuations(n: int, targets: dict[int, int]) -> tuple[int, ...]:
    result: list[int] = []
    for p, cap in targets.items():
        exponent = 0
        while exponent < cap and n % p == 0:
            exponent += 1
            n //= p
        result.append(exponent)
    return tuple(result)


def main() -> None:
    m = choose_m()
    moduli = [m + i + j * D for i in range(1, S + 1) for j in range(1, T + 1)]

    x0, modulus = 0, 1
    for i in range(1, S + 1):
        for j in range(1, T + 1):
            alpha = m + i + j * D
            x0, modulus = merge_congruences(x0, modulus, i, alpha)

    # Shift to a positive representative without changing any congruence.
    if x0 <= m:
        x0 += ((m - x0) // modulus + 1) * modulus

    maximum = max(moduli)
    left = [x0 - i for i in range(1, S + 1)]
    right = [x0 + m + j * D for j in range(1, T + 1)]
    neighborhood = left + right
    interval = range(x0 - m + 1, x0 - m + 2 * maximum)

    actual_neighbors = [n for n in interval if any(n % a == 0 for a in moduli)]
    assert actual_neighbors == sorted(neighborhood)

    target_product = prod(moduli)
    endpoint_product = prod(neighborhood)
    residual = target_product // gcd(target_product, endpoint_product)
    residual_factors = factor(residual)
    residual_vector = tuple(residual_factors.values())

    occupied = set(neighborhood)
    if residual == 1:
        padding = [n for n in interval if n not in occupied][:2]
        assert len(padding) == 2
        witness = padding[0], padding[1]
        vectors: list[tuple[int, ...]] = []
    else:
        candidates: dict[tuple[int, ...], int] = {}
        for n in interval:
            if n in occupied:
                continue
            vector = valuations(n, residual_factors)
            if any(vector):
                candidates.setdefault(vector, n)

        vectors = list(candidates)
        witness = None
        for idx, first in enumerate(vectors):
            for second in vectors[idx:]:
                if all(a + b >= need for a, b, need in zip(first, second, residual_vector)):
                    x, y = candidates[first], candidates[second]
                    if x != y:
                        witness = x, y
                        break
            if witness:
                break

    print(f"D={D}, M={m}, max(A)={maximum}")
    print("A=", moduli)
    print("factorizations=", [factor(a) for a in moduli])
    print("six-point neighborhood verified:", neighborhood)
    print("residual after six endpoints:", residual, residual_factors)
    print("distinct nonzero candidate vectors:", len(vectors))
    print("two-point repair/padding:", witness)
    if witness:
        cover = neighborhood + list(witness)
        assert len(set(cover)) == 8
        assert prod(cover) % target_product == 0
        print("eight-point product cover verified")


if __name__ == "__main__":
    main()
