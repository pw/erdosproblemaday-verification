#!/usr/bin/env python3
"""Certified diameter split for the hard s(9,37)<=43 upper bound.

If a 9-set has at least 44 of its 45 possible unordered sums, it has at most
one sum collision.  Each sum collision accounts for at most two repetitions
among the 36 positive differences, so it has at least 34 distinct positive
differences.  Hence its diameter is at least 34.  Translation makes its
minimum zero, leaving exact diameters 34, 35, and 36.

For each diameter we use the generic definition-to-CNF encoding, require the
top endpoint, require primitivity (sound by dividing by the gcd), and choose
the reflection whose first gap is no larger than its last gap.
"""

from __future__ import annotations

import argparse
import gzip
from pathlib import Path
import shutil
import sys

from sat_audit import make_cnf, run, sha256, write_cnf


N = 37
K = 9
VALUE = 43
TARGET = 44
DIAMETERS = (34, 35, 36)


def primes_through(limit: int) -> list[int]:
    answer = []
    for candidate in range(2, limit + 1):
        if all(candidate % p for p in answer if p * p <= candidate):
            answer.append(candidate)
    return answer


def reduced_cnf(diameter: int):
    variables, clauses = make_cnf(N, K, TARGET)
    x = lambda value: value + 1

    clauses.append((x(diameter),))
    for value in range(diameter + 1, N):
        clauses.append((-x(value),))

    # Divide any witness by the gcd of its positive elements.  Thus it is
    # sound to demand at least one chosen nonmultiple of each possible prime.
    for prime in primes_through(diameter):
        clauses.append(tuple(x(value) for value in range(1, diameter + 1)
                             if value % prime != 0))

    # Reflection about the fixed top endpoint preserves all relevant data.
    # Choose the orientation first_gap <= last_gap.
    for first_gap in range(1, diameter):
        for last_gap in range(1, first_gap):
            clause = [-x(first_gap), -x(diameter - last_gap)]
            clause.extend(x(value) for value in range(1, first_gap))
            clause.extend(x(value) for value in range(diameter - last_gap + 1, diameter))
            clauses.append(tuple(clause))
    return variables, clauses


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cadical", type=Path,
                        default=Path("/home/exedev/MathDyad/erdos813/tools/cadical/build/cadical"))
    parser.add_argument("--kissat", type=Path,
                        default=Path("/home/exedev/MathDyad/erdos813/tools/kissat/build/kissat"))
    parser.add_argument("--drat", type=Path,
                        default=Path("/home/exedev/MathDyad/erdos813/tools/drat-trim/drat-trim"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for binary in (args.cadical, args.kissat, args.drat):
        assert binary.is_file()

    print(f"cadical_sha256={sha256(args.cadical)}")
    print(f"kissat_sha256={sha256(args.kissat)}")
    print(f"drat_trim_sha256={sha256(args.drat)}")
    for diameter in DIAMETERS:
        variables, clauses = reduced_cnf(diameter)
        stem = f"n37_k09_no_score_44_diameter_{diameter}"
        cnf = args.out / f"{stem}.cnf"
        proof = args.out / f"{stem}.drat"
        cadical_log = args.out / f"{stem}.cadical.log"
        kissat_log = args.out / f"{stem}.kissat.log"
        replay_log = args.out / f"{stem}.drat-trim.log"
        write_cnf(cnf, variables, clauses)
        print(
            f"diameter={diameter} vars={variables} clauses={len(clauses)} "
            f"cnf_sha256={sha256(cnf)}",
            flush=True,
        )
        rc = run([str(args.cadical), str(cnf), str(proof)], cadical_log)
        assert rc == 20, (diameter, "cadical", rc)
        rc = run([str(args.kissat), "--quiet", str(cnf)], kissat_log)
        assert rc == 20, (diameter, "kissat", rc)
        rc = run([str(args.drat), str(cnf), str(proof)], replay_log)
        assert rc == 0 and "VERIFIED" in replay_log.read_text(errors="replace")
        proof_hash = sha256(proof)
        with proof.open("rb") as source, gzip.open(str(proof) + ".gz", "wb", compresslevel=9) as sink:
            shutil.copyfileobj(source, sink)
        compressed = Path(str(proof) + ".gz")
        proof.unlink()
        print(
            f"diameter={diameter} CaDiCaL=UNSAT Kissat=UNSAT DRAT=VERIFIED "
            f"proof_sha256={proof_hash} proof_gz_bytes={compressed.stat().st_size}",
            flush=True,
        )
    print("K9 DIAMETER-SPLIT AUDIT PASSED", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"AUDIT FAILED: {exc!r}", file=sys.stderr)
        raise
