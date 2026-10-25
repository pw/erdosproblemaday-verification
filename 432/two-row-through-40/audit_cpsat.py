#!/usr/bin/env python3
"""Independent CP-SAT audit of the new finite #432 thresholds.

This deliberately does not build a gcd compatibility graph and does not use
the branch-and-color code in audit_clique.cpp.  For each row gap d it factors
every candidate pair (v,v+d).  A family of pairs is valid exactly when each
prime occurs in at most one pair, so the audit is a 0/1 set-packing model.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import pathlib
import time

from ortools.sat.python import cp_model


ROWS = {
    11: (101, 12, [11,13,17,31,37,41,47,61,67,71,89]),
    12: (107, 6,  [11,23,31,41,43,53,61,65,73,83,97,101]),
    13: (127, 6,  [13,23,25,37,41,53,61,73,83,101,103,113,121]),
    14: (131, 18, [5,13,19,29,41,43,49,53,79,83,89,103,109,113]),
    15: (149, 10, [13,17,19,31,37,43,49,61,73,79,97,103,121,127,139]),
    16: (167, 10, [13,19,31,37,43,49,61,73,79,97,103,121,127,139,153,157]),
    17: (173, 10, [13,17,19,31,37,43,49,61,73,79,97,103,121,127,139,157,163]),
    18: (191, 10, [17,19,31,37,43,61,73,79,97,103,121,127,139,151,157,163,169,181]),
    19: (197, 18, [5,19,29,41,43,53,79,83,89,103,109,113,119,139,149,151,163,173,179]),
    20: (211, 18, [5,19,29,41,43,53,79,83,89,103,109,113,119,139,149,151,173,179,181,193]),
    21: (241, 12, [17,25,31,41,47,61,67,71,97,101,127,137,151,157,161,179,181,197,211,227,229]),
    22: (251, 18, [19,29,41,43,49,53,79,83,89,103,109,113,137,139,149,173,179,181,211,221,223,233]),
    23: (257, 18, [5,19,29,41,43,53,79,83,89,103,109,113,119,139,149,151,173,179,181,211,223,233,239]),
    24: (271, 30, [17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,173,181,193,199,227,233,239,241]),
    25: (281, 30, [17,23,31,41,59,67,73,83,101,107,109,121,127,149,167,173,181,193,199,227,233,239,241,247,251]),
    26: (307, 30, [17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,203,227,239,241,251,263,277]),
    27: (313, 30, [17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,203,227,239,241,263,277,281,283]),
    28: (347, 30, [17,23,31,41,59,67,73,83,101,107,109,121,127,149,167,181,193,199,227,239,241,247,263,281,283,301,307,317]),
    29: (361, 30, [7,17,23,31,41,59,67,73,79,83,101,107,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,319,331]),
    30: (367, 30, [7,17,23,31,41,59,67,73,79,83,101,107,127,139,149,167,181,193,199,227,239,241,263,277,281,283,317,319,331,337]),
    31: (379, 30, [17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,277,281,283,317,331,337,343,349]),
    32: (383, 30, [17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,277,281,283,317,331,337,343,349,353]),
    33: (389, 30, [17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,277,281,283,317,331,337,343,349,353,359]),
    34: (431, 30, [17,23,31,41,59,67,73,79,83,101,107,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,319,331,343,353,367,379,389,401]),
    35: (439, 30, [17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,367,389,401,409]),
    36: (449, 30, [17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,359,367,401,409,419]),
    37: (463, 30, [17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,359,367,409,419,431,433]),
    38: (487, 30, [17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,367,389,409,431,433,449,457]),
    39: (491, 30, [17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,367,389,401,409,433,449,457,461]),
    40: (509, 30, [17,23,31,41,59,67,73,79,83,101,107,121,127,139,149,167,181,193,199,227,239,241,263,281,283,307,317,331,343,349,353,359,367,401,409,419,433,457,461,479]),
}


def supports_through(limit: int) -> list[frozenset[int]]:
    result: list[frozenset[int]] = [frozenset() for _ in range(limit + 1)]
    for value in range(2, limit + 1):
        remaining = value
        factors: set[int] = set()
        divisor = 2
        while divisor * divisor <= remaining:
            if remaining % divisor == 0:
                factors.add(divisor)
                while remaining % divisor == 0:
                    remaining //= divisor
            divisor += 1
        if remaining > 1:
            factors.add(remaining)
        result[value] = frozenset(factors)
    return result


def validate_witness(n: int, threshold: int, gap: int, starts: list[int]) -> None:
    assert len(starts) == n == len(set(starts))
    values = [item for v in starts for item in (v, v + gap)]
    assert min(values) >= 2 and max(values) <= threshold
    assert len(values) == len(set(values))
    for i, a in enumerate(values):
        for b in values[:i]:
            assert math.gcd(a, b) == 1


def infeasible_at(limit: int, target: int, supports: list[frozenset[int]]) -> tuple[int, int]:
    total_candidates = 0
    total_prime_constraints = 0
    for gap in range(1, limit - 1):
        candidates: list[tuple[int, frozenset[int]]] = []
        for v in range(2, limit - gap + 1):
            if supports[v].isdisjoint(supports[v + gap]):
                candidates.append((v, supports[v] | supports[v + gap]))
        total_candidates += len(candidates)

        if len(candidates) < target:
            continue

        model = cp_model.CpModel()
        chosen = [model.new_bool_var(f"v_{v}") for v, _ in candidates]
        by_prime: dict[int, list] = {}
        for variable, (_, support) in zip(chosen, candidates):
            for prime in support:
                by_prime.setdefault(prime, []).append(variable)
        for variables in by_prime.values():
            if len(variables) > 1:
                model.add(sum(variables) <= 1)
                total_prime_constraints += 1
        model.add(sum(chosen) >= target)

        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.random_seed = 432
        solver.parameters.cp_model_presolve = True
        status = solver.solve(model)
        assert status == cp_model.INFEASIBLE, (limit, target, gap, status)
    return total_candidates, total_prime_constraints


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", type=int, choices=sorted(ROWS))
    args = parser.parse_args()

    selected = [args.only] if args.only is not None else sorted(ROWS)
    max_limit = max(ROWS[n][0] for n in selected)
    supports = supports_through(max_limit)
    started = time.monotonic()
    digest = hashlib.sha256()

    for n in selected:
        threshold, gap, starts = ROWS[n]
        validate_witness(n, threshold, gap, starts)
        candidates, constraints = infeasible_at(threshold - 1, n, supports)
        line = (
            f"n={n} threshold={threshold} witness=PASS below=INFEASIBLE "
            f"candidate_instances={candidates} prime_constraints={constraints}"
        )
        print(line, flush=True)
        digest.update((line + "\n").encode())

    print(f"audit_sha256={digest.hexdigest()}")
    print(f"elapsed_seconds={time.monotonic() - started:.6f}")
    print("INDEPENDENT CP-SAT PRIME-SUPPORT AUDIT PASS")


if __name__ == "__main__":
    main()
