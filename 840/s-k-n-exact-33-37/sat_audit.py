#!/usr/bin/env python3
"""Independent SAT/DRAT audit for finite s(k,n) rows in primary output.

This program does not import or reproduce the producer's subset traversal.
For every nontrivial table cell it constructs a Boolean model directly from
the definition of A+A and rejects the existence of a set scoring one better.
Triangular and interval-size caps are checked arithmetically.  Every displayed
lower-bound witness is recomputed with ordinary Python sets.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


DEFAULT_CADICAL = Path("/home/exedev/MathDyad/erdos813/tools/cadical/build/cadical")
DEFAULT_KISSAT = Path("/home/exedev/MathDyad/erdos813/tools/kissat/build/kissat")
DEFAULT_DRAT = Path("/home/exedev/MathDyad/erdos813/tools/drat-trim/drat-trim")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def parse_output(path: Path):
    rows: dict[int, list[int]] = {}
    witnesses: dict[tuple[int, int], tuple[int, tuple[int, ...]]] = {}
    row_re = re.compile(r"ROW n=(\d+):(.*)")
    witness_re = re.compile(r"WITNESS n=(\d+) k=(\d+) score=(\d+) A=\[(.*)\]")
    for line in path.read_text().splitlines():
        if match := row_re.fullmatch(line):
            n = int(match.group(1))
            values = [int(v) for v in match.group(2).split()]
            assert len(values) == n
            rows[n] = values
        elif match := witness_re.fullmatch(line):
            n, k, score = map(int, match.group(1, 2, 3))
            values = tuple(int(v) for v in match.group(4).split(",") if v)
            witnesses[n, k] = score, values
    return rows, witnesses


def direct_score(values: tuple[int, ...]) -> int:
    return len({a + b for a in values for b in values})


def at_most_sinz(inputs: list[int], bound: int, next_var: int):
    """CNF for sum(input literals) <= bound; return clauses and new top id."""
    count = len(inputs)
    if bound < 0:
        return [tuple()], next_var - 1
    if bound >= count:
        return [], next_var - 1
    if bound == 0:
        return [(-literal,) for literal in inputs], next_var - 1

    counter: dict[tuple[int, int], int] = {}
    for i in range(1, count):
        for j in range(1, bound + 1):
            counter[i, j] = next_var
            next_var += 1

    clauses: list[tuple[int, ...]] = []
    for i in range(1, count):
        clauses.append((-inputs[i - 1], counter[i, 1]))
    for i in range(2, count):
        for j in range(1, bound + 1):
            clauses.append((-counter[i - 1, j], counter[i, j]))
        for j in range(2, bound + 1):
            clauses.append((-inputs[i - 1], -counter[i - 1, j - 1], counter[i, j]))
    for i in range(2, count + 1):
        clauses.append((-inputs[i - 1], -counter[i - 1, bound]))
    return clauses, next_var - 1


def make_cnf(n: int, k: int, target: int):
    """Encode: min(A)=0, |A|=k, and |A+A| >= target."""
    next_var = 1
    x = list(range(next_var, next_var + n))
    next_var += n

    # Each off-diagonal z_(i,j) is equivalent to x_i AND x_j.
    pair_literals: list[list[int]] = [[] for _ in range(2 * n - 1)]
    clauses: list[tuple[int, ...]] = []
    for i in range(n):
        pair_literals[2 * i].append(x[i])
        for j in range(i + 1, n):
            z = next_var
            next_var += 1
            clauses.extend(((-z, x[i]), (-z, x[j]), (-x[i], -x[j], z)))
            pair_literals[i + j].append(z)

    # y_s is equivalent to the OR of all selected pairs with sum s.
    y = list(range(next_var, next_var + 2 * n - 1))
    next_var += 2 * n - 1
    for sum_value, pair_vars in enumerate(pair_literals):
        assert pair_vars
        for pair_var in pair_vars:
            clauses.append((-pair_var, y[sum_value]))
        clauses.append(tuple([-y[sum_value], *pair_vars]))

    clauses.append((x[0],))
    equal_upper, top = at_most_sinz(x, k, next_var)
    clauses.extend(equal_upper)
    equal_lower, top = at_most_sinz([-v for v in x], n - k, top + 1)
    clauses.extend(equal_lower)
    score_lower, top = at_most_sinz([-v for v in y], len(y) - target, top + 1)
    clauses.extend(score_lower)
    return max(top, max(y)), clauses


def write_cnf(path: Path, variables: int, clauses: list[tuple[int, ...]]) -> None:
    with path.open("w", encoding="ascii") as out:
        out.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            out.write(" ".join(map(str, clause)) + " 0\n")


def run(command: list[str], log: Path) -> int:
    with log.open("wb") as out:
        return subprocess.run(command, stdout=out, stderr=subprocess.STDOUT).returncode


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("primary_output", type=Path)
    parser.add_argument("--out", type=Path, default=Path("sat_certificates"))
    parser.add_argument("--min-n", type=int, default=28)
    parser.add_argument("--max-n", type=int, default=10**9)
    parser.add_argument("--min-k", type=int, default=1)
    parser.add_argument("--max-k", type=int, default=10**9)
    parser.add_argument("--cadical", type=Path, default=DEFAULT_CADICAL)
    parser.add_argument("--kissat", type=Path, default=DEFAULT_KISSAT)
    parser.add_argument("--drat", type=Path, default=DEFAULT_DRAT)
    parser.add_argument("--keep-cnf", action="store_true")
    args = parser.parse_args()

    for binary in (args.cadical, args.kissat, args.drat):
        assert binary.is_file(), binary
    args.out.mkdir(parents=True, exist_ok=True)
    rows, witnesses = parse_output(args.primary_output)
    chosen = [n for n in sorted(rows) if args.min_n <= n <= args.max_n]
    assert chosen

    print(f"cadical_sha256={sha256(args.cadical)}")
    print(f"kissat_sha256={sha256(args.kissat)}")
    print(f"drat_trim_sha256={sha256(args.drat)}")
    cases = 0
    trivial = 0
    for n in chosen:
        row = rows[n]
        assert row[0] == 1
        assert all(a <= b for a, b in zip(row, row[1:]))
        first_full = next(k for k, score in enumerate(row, 1) if score == 2 * n - 1)
        for k, score in enumerate(row, 1):
            if not args.min_k <= k <= args.max_k:
                continue
            assert score <= min(k * (k + 1) // 2, 2 * n - 1)
            if k <= 16 and (n, k) in witnesses:
                claimed_score, values = witnesses[n, k]
                assert claimed_score == score
                assert len(values) == k and len(set(values)) == k
                assert min(values) >= 1 and max(values) <= n
                assert direct_score(values) == score

            cap = min(k * (k + 1) // 2, 2 * n - 1)
            if score == cap:
                trivial += 1
                continue

            # All nontrivial cells here have stored producer witnesses.
            assert (n, k) in witnesses, (n, k, score)
            variables, clauses = make_cnf(n, k, score + 1)
            stem = f"n{n:02d}_k{k:02d}_no_score_{score + 1}"
            cnf = args.out / f"{stem}.cnf"
            proof = args.out / f"{stem}.drat"
            cadical_log = args.out / f"{stem}.cadical.log"
            kissat_log = args.out / f"{stem}.kissat.log"
            replay_log = args.out / f"{stem}.drat-trim.log"
            write_cnf(cnf, variables, clauses)
            cnf_hash = sha256(cnf)

            rc = run([str(args.cadical), str(cnf), str(proof)], cadical_log)
            assert rc == 20, (stem, "cadical", rc)
            rc = run([str(args.kissat), "--quiet", str(cnf)], kissat_log)
            assert rc == 20, (stem, "kissat", rc)
            rc = run([str(args.drat), str(cnf), str(proof)], replay_log)
            assert rc == 0 and "VERIFIED" in replay_log.read_text(errors="replace"), stem

            proof_hash = sha256(proof)
            with proof.open("rb") as source, gzip.open(str(proof) + ".gz", "wb", compresslevel=9) as sink:
                shutil.copyfileobj(source, sink)
            compressed = Path(str(proof) + ".gz")
            proof.unlink()
            if not args.keep_cnf:
                cnf.unlink()
            cases += 1
            print(
                f"n={n} k={k} value={score} target={score + 1} "
                f"vars={variables} clauses={len(clauses)} cnf_sha256={cnf_hash} "
                f"CaDiCaL=UNSAT Kissat=UNSAT DRAT=VERIFIED "
                f"proof_sha256={proof_hash} proof_gz_bytes={compressed.stat().st_size}",
                flush=True,
            )
        assert all(score == 2 * n - 1 for score in row[first_full - 1 :])

    print(f"ROWS {chosen[0]}..{chosen[-1]}")
    print(f"NONTRIVIAL_SAT_CASES {cases}")
    print(f"TRIVIAL_CAP_CASES {trivial}")
    print("INDEPENDENT SAT/DRAT AUDIT PASSED")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"AUDIT FAILED: {exc!r}", file=sys.stderr)
        raise
