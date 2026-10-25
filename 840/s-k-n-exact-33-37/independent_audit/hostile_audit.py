#!/usr/bin/env python3
"""Clean-room structural and mathematical audit of the #840 n=33..37 bundle."""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import gzip
import hashlib
from math import gcd
from pathlib import Path
import random
import re


BUNDLE = Path("/tmp/erdos840_n33_37_bundle")
PUBLISHED = Path("/home/exedev/ErdosProblemADay/verification/840/s-k-n-exact-through-32")

TERMINAL = [1, 3, 6, 10, 15, 21, 28, 36, 43, 51, 59, 64, 69] + [73] * 24
GENERIC = {10: 52, 11: 60, 12: 65, 13: 70}
DIAMETERS = (34, 35, 36)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def gzip_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with gzip.open(path, "rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_primary(path: Path, expected_nodes: int | None = None):
    row_pattern = re.compile(r"ROW n=(\d+):(.*)")
    witness_pattern = re.compile(r"WITNESS n=(\d+) k=(\d+) score=(\d+) A=\[(.*)\]")
    rows = {}
    witnesses = {}
    text = path.read_text()
    for line in text.splitlines():
        if found := row_pattern.fullmatch(line):
            rows[int(found.group(1))] = tuple(map(int, found.group(2).split()))
        elif found := witness_pattern.fullmatch(line):
            n, k, claimed = map(int, found.group(1, 2, 3))
            values = tuple(map(int, found.group(4).split(",")))
            witnesses[n, k] = claimed, values
    if expected_nodes is not None:
        assert f"NODES {expected_nodes}" in text
    assert text.rstrip().endswith("ALL CHECKS PASSED")
    return rows, witnesses


def sum_score(values) -> int:
    return len({a + b for a in values for b in values})


def check_primary_and_prefix():
    rows, witnesses = parse_primary(BUNDLE / "primary_output.txt", 1 << 36)
    old_rows, _ = parse_primary(PUBLISHED / "primary_output.txt", 1 << 31)
    for n in range(27, 33):
        assert rows[n] == old_rows[n], (n, rows[n], old_rows[n])
    assert list(rows[37]) == TERMINAL
    for n in range(33, 38):
        assert len(rows[n]) == n
        assert all(a <= b for a, b in zip(rows[n], rows[n][1:]))
        assert all(rows[n - 1][k - 1] <= rows[n][k - 1] for k in range(1, n))
        for k, value in enumerate(rows[n], 1):
            assert value <= min(k * (k + 1) // 2, 2 * n - 1)
        for k in range(7, 17):
            claimed, values = witnesses[n, k]
            assert len(values) == len(set(values)) == k
            assert 1 <= min(values) <= max(values) <= n
            assert claimed == rows[n][k - 1] == sum_score(values)
    print("primary transcript, direct witnesses, monotonicity, caps: PASS")
    print("rows 27..32 exactly match published frozen checkpoint: PASS")
    return rows


def parse_dimacs(path: Path):
    clauses = []
    variables = declared = None
    for line in path.read_text().splitlines():
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            _, kind, variables_text, declared_text = line.split()
            assert kind == "cnf"
            variables, declared = int(variables_text), int(declared_text)
            continue
        values = tuple(map(int, line.split()))
        assert values[-1] == 0 and 0 not in values[:-1]
        clauses.append(values[:-1])
    assert variables is not None and declared == len(clauses)
    assert all(abs(lit) <= variables for clause in clauses for lit in clause)
    return variables, clauses


def at_most(literals: list[int], bound: int, fresh: int):
    count = len(literals)
    if bound < 0:
        return [()], fresh
    if bound >= count:
        return [], fresh
    if bound == 0:
        return [(-literal,) for literal in literals], fresh

    marker = {}
    for prefix in range(1, count):
        for weight in range(1, bound + 1):
            marker[prefix, weight] = fresh
            fresh += 1
    clauses = []
    for prefix in range(1, count):
        clauses.append((-literals[prefix - 1], marker[prefix, 1]))
    for prefix in range(2, count):
        for weight in range(1, bound + 1):
            clauses.append((-marker[prefix - 1, weight], marker[prefix, weight]))
        for weight in range(2, bound + 1):
            clauses.append((-literals[prefix - 1], -marker[prefix - 1, weight - 1],
                            marker[prefix, weight]))
    for prefix in range(2, count + 1):
        clauses.append((-literals[prefix - 1], -marker[prefix - 1, bound]))
    return clauses, fresh


def direct_definition_cnf(n: int, k: int, target: int):
    # Numbering is reconstructed from the DIMACS contract, without importing
    # or executing any producer module.
    chosen = list(range(1, n + 1))
    fresh = n + 1
    representations = [[] for _ in range(2 * n - 1)]
    clauses = []
    for left in range(n):
        representations[2 * left].append(chosen[left])
        for right in range(left + 1, n):
            pair = fresh
            fresh += 1
            clauses += [(-pair, chosen[left]), (-pair, chosen[right]),
                        (-chosen[left], -chosen[right], pair)]
            representations[left + right].append(pair)
    present_sum = list(range(fresh, fresh + 2 * n - 1))
    fresh += 2 * n - 1
    for flag, reps in zip(present_sum, representations):
        clauses += [(-rep, flag) for rep in reps]
        clauses.append(tuple([-flag, *reps]))
    clauses.append((chosen[0],))
    extra, fresh = at_most(chosen, k, fresh)
    clauses += extra
    extra, fresh = at_most([-literal for literal in chosen], n - k, fresh)
    clauses += extra
    extra, fresh = at_most([-literal for literal in present_sum], len(present_sum) - target, fresh)
    clauses += extra
    return fresh - 1, clauses


def primes(limit: int):
    result = []
    for candidate in range(2, limit + 1):
        if all(candidate % divisor for divisor in range(2, int(candidate**0.5) + 1)):
            result.append(candidate)
    return result


def reduced_k9_cnf(diameter: int):
    variables, clauses = direct_definition_cnf(37, 9, 44)
    x = lambda value: value + 1
    clauses.append((x(diameter),))
    clauses.extend((-x(value),) for value in range(diameter + 1, 37))
    for prime in primes(diameter):
        clauses.append(tuple(x(value) for value in range(1, diameter + 1)
                             if value % prime))
    for first in range(1, diameter):
        for last in range(1, first):
            clauses.append(tuple([
                -x(first), -x(diameter - last),
                *(x(value) for value in range(1, first)),
                *(x(value) for value in range(diameter - last + 1, diameter)),
            ]))
    return variables, clauses


def compare_cnf(path: Path, expected_variables: int, expected_clauses):
    variables, clauses = parse_dimacs(path)
    assert variables == expected_variables
    assert Counter(clauses) == Counter(expected_clauses)
    return len(clauses)


def check_frozen_cnfs():
    for k, target in GENERIC.items():
        variables, expected = direct_definition_cnf(37, k, target)
        name = f"n37_k{k:02d}_no_score_{target}.cnf"
        count = compare_cnf(BUNDLE / "sat" / name, variables, expected)
        print(f"clean-room clause equality: generic k={k}, {variables} vars, {count} clauses: PASS")
    for diameter in DIAMETERS:
        variables, expected = reduced_k9_cnf(diameter)
        name = f"n37_k09_no_score_44_diameter_{diameter}.cnf"
        count = compare_cnf(BUNDLE / "sat_k9_split" / name, variables, expected)
        print(f"clean-room clause equality: k=9,d={diameter}, {variables} vars, {count} clauses: PASS")


def check_reductions():
    # Exhaust every minimum-zero set through 17 positions, then attack the
    # actual diameters with deterministic random 9-sets.
    examined = 0
    for n in range(1, 18):
        for mask in range(1 << (n - 1)):
            values = (0,) + tuple(i + 1 for i in range(n - 1) if mask >> i & 1)
            unordered = len({values[i] + values[j]
                             for i in range(len(values)) for j in range(i, len(values))})
            positive = len({a - b for a in values for b in values if a > b})
            sum_deficit = len(values) * (len(values) + 1) // 2 - unordered
            difference_deficit = len(values) * (len(values) - 1) // 2 - positive
            if sum_deficit <= 1:
                assert difference_deficit <= 2
            examined += 1

    rng = random.Random(840_033_037)
    for diameter in DIAMETERS:
        for _ in range(100_000):
            middle = rng.sample(range(1, diameter), 7)
            values = tuple(sorted((0, diameter, *middle)))
            reflected = tuple(sorted(diameter - value for value in values))
            first, last = values[1], diameter - values[-2]
            reflected_first = reflected[1]
            reflected_last = diameter - reflected[-2]
            assert (first <= last) or (reflected_first <= reflected_last)
            common = 0
            for value in values[1:]:
                common = gcd(common, value)
            if common > 1:
                scaled = tuple(value // common for value in values)
                assert len(set(scaled)) == 9 and sum_score(scaled) == sum_score(values)
    print(f"sum/difference deficit implication exhaustive on {examined:,} sets: PASS")
    print("300,000 actual-diameter reflection/scaling attacks: PASS")


def check_manifest_and_proof_hashes():
    entries = {}
    for line in (BUNDLE / "SHA256SUMS").read_text().splitlines():
        digest, relative = line.split("  ", 1)
        assert relative not in entries and re.fullmatch(r"[0-9a-f]{64}", digest)
        entries[relative] = digest
    actual = {str(path.relative_to(BUNDLE)) for path in BUNDLE.rglob("*")
              if path.is_file() and path.name != "SHA256SUMS" and "__pycache__" not in path.parts}
    assert set(entries) == actual
    for relative, digest in entries.items():
        assert sha256(BUNDLE / relative) == digest

    summaries = (BUNDLE / "sat_audit_output.txt").read_text() + (BUNDLE / "sat_k9_split_output.txt").read_text()
    proofs = sorted(BUNDLE.glob("sat*/*.drat.gz"))
    assert len(proofs) == 7
    for proof in proofs:
        payload = gzip_hash(proof)
        assert f"proof_sha256={payload}" in summaries
    print(f"closed manifest and seven uncompressed proof hashes: PASS ({len(entries)} files)")


def main():
    check_primary_and_prefix()
    check_reductions()
    check_frozen_cnfs()
    check_manifest_and_proof_hashes()
    print("HOSTILE STRUCTURAL AUDIT PASS")


if __name__ == "__main__":
    main()
