#!/usr/bin/env python3
"""Independent SAT audit for the exact Erdős #425 extension through 61.

This code deliberately does not import the primary Python hypergraph/search
checker.  It generates obstruction clauses by inspecting every four-subset,
adds a Sinz sequential at-most counter for the deleted vertices, and asks two
independent SAT engines to reject every claimed upper-bound violation.
"""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import hashlib
import os
import subprocess
import sys


HERE = Path(__file__).resolve().parent
CADICAL = Path(os.environ.get("CADICAL", "/bin/cadical"))
KISSAT = Path(os.environ.get("KISSAT", "/usr/local/bin/kissat"))
DRAT_TRIM = Path(os.environ.get("DRAT_TRIM", "/usr/local/bin/drat-trim"))
UPPER_DECISIONS = ((50, 26), (51, 26), (55, 28), (58, 29), (60, 30))


def obstruction_edges(n: int) -> list[tuple[int, int, int, int]]:
    edges = []
    for a, b, c, d in combinations(range(1, n + 1), 4):
        if a * b == c * d or a * c == b * d or a * d == b * c:
            edges.append((a, b, c, d))
    return edges


def at_most_sinz(inputs: list[int], k: int, next_var: int):
    """Return (clauses, largest_var) for sum(inputs) <= k."""
    n = len(inputs)
    if k < 0:
        return [tuple()], next_var - 1
    if k >= n:
        return [], next_var - 1
    if k == 0:
        return [(-x,) for x in inputs], next_var - 1

    s = {}
    for i in range(1, n):
        for j in range(1, k + 1):
            s[i, j] = next_var
            next_var += 1

    clauses = []
    for i in range(1, n):
        clauses.append((-inputs[i - 1], s[i, 1]))
    for i in range(2, n):
        for j in range(1, k + 1):
            clauses.append((-s[i - 1, j], s[i, j]))
        for j in range(2, k + 1):
            clauses.append((-inputs[i - 1], -s[i - 1, j - 1], s[i, j]))
    for i in range(2, n + 1):
        clauses.append((-inputs[i - 1], -s[i - 1, k]))
    return clauses, next_var - 1


def make_cnf(n: int, value: int) -> tuple[int, list[tuple[int, ...]], int]:
    # y_v means that v is deleted from A.  Every multiplicative rectangle
    # needs a deleted vertex, and an A of size >= value+1 deletes <=n-value-1.
    budget = n - value - 1
    edges = obstruction_edges(n)
    clauses: list[tuple[int, ...]] = [tuple(edge) for edge in edges]
    counter, largest = at_most_sinz(list(range(1, n + 1)), budget, n + 1)
    clauses.extend(counter)
    return max(n, largest), clauses, len(edges)


def write_cnf(path: Path, variables: int, clauses: list[tuple[int, ...]]) -> None:
    with path.open("w", encoding="ascii") as out:
        out.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            out.write(" ".join(map(str, clause)) + " 0\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_solver(command: list[str], log: Path) -> int:
    with log.open("wb") as out:
        completed = subprocess.run(command, stdout=out, stderr=subprocess.STDOUT)
    return completed.returncode


def main() -> None:
    assert CADICAL.is_file() and KISSAT.is_file() and DRAT_TRIM.is_file()
    print(f"cadical_sha256={sha256(CADICAL)}")
    print(f"kissat_sha256={sha256(KISSAT)}")
    print(f"drat_trim_sha256={sha256(DRAT_TRIM)}")

    for n, value in UPPER_DECISIONS:
        variables, clauses, edge_count = make_cnf(n, value)
        cnf = HERE / f"upper_n{n}_F{value}.cnf"
        write_cnf(cnf, variables, clauses)
        print(
            f"n={n} target_size={value + 1} edges={edge_count} "
            f"vars={variables} clauses={len(clauses)} cnf_sha256={sha256(cnf)}",
            flush=True,
        )

        proof = HERE / f"upper_n{n}_F{value}.drat"
        cadical_log = HERE / f"upper_n{n}_cadical.log"
        kissat_log = HERE / f"upper_n{n}_kissat.log"
        replay_log = HERE / f"upper_n{n}_drat_trim.log"

        # SAT competition convention: exit 20 means UNSAT.
        rc1 = run_solver([str(CADICAL), str(cnf), str(proof)], cadical_log)
        assert rc1 == 20, (n, rc1, cadical_log)
        rc2 = run_solver([str(KISSAT), str(cnf)], kissat_log)
        assert rc2 == 20, (n, rc2, kissat_log)
        rc3 = run_solver([str(DRAT_TRIM), str(cnf), str(proof)], replay_log)
        assert rc3 == 0, (n, rc3, replay_log)
        replay_text = replay_log.read_text(errors="replace")
        assert "VERIFIED" in replay_text
        print(
            f"n={n} CaDiCaL=UNSAT Kissat=UNSAT DRAT=VERIFIED "
            f"proof_bytes={proof.stat().st_size} proof_sha256={sha256(proof)}",
            flush=True,
        )

    print("INDEPENDENT SAT AUDIT PASSED", flush=True)


if __name__ == "__main__":
    main()
