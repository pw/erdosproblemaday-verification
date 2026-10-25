#!/usr/bin/env python3
"""Literal small-instance cross-check of the producer's fixed-last search.

Usage:
    python3 fixed_last_literal_check.py /path/to/verify.py

The literal side enumerates every internal-mark combination and evaluates
pair-sum collisions from the definition.  It does not reuse the producer's
recursive search logic.
"""

from __future__ import annotations

import importlib.util
from itertools import combinations
from pathlib import Path
import sys


def load_producer(path: Path):
    spec = importlib.util.spec_from_file_location("erdos819_producer", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load producer: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def literal_sidon(marks: tuple[int, ...]) -> bool:
    pair_sums = [
        marks[i] + marks[j]
        for i in range(len(marks))
        for j in range(i, len(marks))
    ]
    return len(pair_sums) == len(set(pair_sums))


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: fixed_last_literal_check.py /path/to/verify.py")
    producer = load_producer(Path(sys.argv[1]))
    checks = 0
    for k in range(2, 7):
        for last in range(k - 1, 14):
            for bound in range(k - 2, last):
                got = bool(
                    producer.search_fixed_last(k, last, bound)["exists"]
                )
                want = any(
                    literal_sidon((0,) + middle + (last,))
                    for middle in combinations(range(1, bound + 1), k - 2)
                )
                if got != want:
                    raise RuntimeError(
                        f"fixed-last mismatch: {(k, last, bound, got, want)}"
                    )
                checks += 1
    print(f"fixed-last literal checks {checks}")
    print("ALL FIXED-LAST KERNEL CROSSCHECKS PASSED")


if __name__ == "__main__":
    main()
