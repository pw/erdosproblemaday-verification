#!/usr/bin/env python3
"""Emit one Fermat two-square obstruction for every integer in the new gap."""

from sympy import factorint


LEFT = 133_858_454_292
RIGHT = 133_858_454_404


for n in range(LEFT + 1, RIGHT):
    factors = factorint(n)
    bad = [(p, exponent) for p, exponent in factors.items()
           if p % 4 == 3 and exponent % 2 == 1]
    if not bad:
        raise AssertionError(f"no two-square obstruction found for {n}")
    p, exponent = min(bad)
    print(f"[{n},{p},{exponent}]")
