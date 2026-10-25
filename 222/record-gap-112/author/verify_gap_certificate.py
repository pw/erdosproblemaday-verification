#!/usr/bin/env python3
"""Dependency-free independent checker for the explicit gap certificate."""

import ast
from pathlib import Path


LEFT = 133_858_454_292
RIGHT = 133_858_454_404
CERTIFICATE = Path(__file__).with_name("gap_133858454292_133858454404.cert")


def is_prime_64(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


rows = [ast.literal_eval(line) for line in CERTIFICATE.read_text().splitlines()]
assert len(rows) == RIGHT - LEFT - 1
for expected, row in enumerate(rows, LEFT + 1):
    n, p, exponent = row
    assert n == expected
    assert p % 4 == 3 and exponent % 2 == 1 and is_prime_64(p)
    exact_exponent = 0
    quotient = n
    while quotient % p == 0:
        exact_exponent += 1
        quotient //= p
    assert exact_exponent == exponent

assert 49_986**2 + 362_436**2 == LEFT
assert 35_298**2 + 364_160**2 == RIGHT
print(f"PYTHON_CERTIFICATE_PASS rows={len(rows)} endpoints={LEFT},{RIGHT} "
      f"gap={RIGHT - LEFT}")
