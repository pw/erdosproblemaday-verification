#!/usr/bin/env python3
"""Cross-check strict integer predicate against the literal radical inequality."""

from decimal import Decimal, getcontext
from hashlib import sha256
from itertools import combinations_with_replacement
import importlib.util
import json
from pathlib import Path
import sys
import time

SOURCE = str(Path(__file__).with_name("audit_352_n17.py"))
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("audit352", SOURCE)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

getcontext().prec = 80


def literal(p, q, r):
    diameter2 = max(module.distance2(p, q), module.distance2(p, r), module.distance2(q, r))
    left = abs(Decimal(module.double_area(p, q, r)) / 2 - Decimal(module.N))
    return left > Decimal(diameter2).sqrt()


def check(triple):
    exact = module.exact_margin(*triple)
    if literal(*triple) != (exact > 0):
        raise RuntimeError(f"predicate disagreement: {triple}, margin={exact}")
    return exact


def main():
    started = time.perf_counter()
    witness_checks = 0
    for triple in combinations_with_replacement(module.WITNESS, 3):
        check(triple)
        witness_checks += 1

    lens_checks = 0
    zero_margins = []
    closest_nonzero = None
    for b in module.diameter_directions():
        radius2 = module.norm2(b)
        for x in range(-16, 17):
            for y in range(-16, 17):
                p = (x, y)
                if p in (module.ORIGIN, b):
                    continue
                if module.norm2(p) > radius2 or module.distance2(p, b) > radius2:
                    continue
                triple = (module.ORIGIN, b, p)
                value = check(triple)
                lens_checks += 1
                if value == 0:
                    zero_margins.append(triple)
                elif closest_nonzero is None or abs(value) < abs(closest_nonzero):
                    closest_nonzero = value

    result = {
        "witness_literal_checks": witness_checks,
        "lens_literal_checks": lens_checks,
        "zero_margin_base_triples": len(zero_margins),
        "zero_margin_examples": zero_margins[:20],
        "closest_nonzero_base_margin": closest_nonzero,
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(canonical)
    print("STRICT_PREDICATE_SHA256=" + sha256(canonical.encode("ascii")).hexdigest())
    print(f"STRICT_PREDICATE_PASS elapsed_seconds={time.perf_counter()-started:.6f}")


if __name__ == "__main__":
    main()
