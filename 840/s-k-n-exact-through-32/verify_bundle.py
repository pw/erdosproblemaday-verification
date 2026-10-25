#!/usr/bin/env python3
"""Standalone definition-level checker for the Erdős #840 n<=32 bundle."""

from __future__ import annotations

import argparse
import gzip
import hashlib
from itertools import combinations
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
EXPECTED_ROWS = {
    27: [1, 3, 6, 10, 15, 21, 28, 34, 41, 47, 51, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53],
    28: [1, 3, 6, 10, 15, 21, 28, 34, 41, 47, 51, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55],
    29: [1, 3, 6, 10, 15, 21, 28, 35, 41, 47, 53, 56, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57],
    30: [1, 3, 6, 10, 15, 21, 28, 35, 42, 49, 53, 57, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59],
    31: [1, 3, 6, 10, 15, 21, 28, 35, 42, 51, 54, 59, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61, 61],
    32: [1, 3, 6, 10, 15, 21, 28, 35, 42, 51, 55, 59, 62, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63],
}
SAT_CASES = {
    (32, 8): 36,
    (32, 9): 43,
    (32, 10): 52,
    (32, 11): 56,
    (32, 12): 60,
    (32, 13): 63,
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def check_manifest() -> None:
    entries: dict[str, str] = {}
    for line in (HERE / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        assert re.fullmatch(r"[0-9a-f]{64}", digest)
        assert name not in entries
        entries[name] = digest
    actual_names = sorted(
        str(path.relative_to(HERE))
        for path in HERE.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS" and "__pycache__" not in path.parts
    )
    assert sorted(entries) == actual_names, (sorted(entries), actual_names)
    for name, expected in entries.items():
        assert sha256(HERE / name) == expected, name
    print(f"manifest: PASS ({len(entries)} files)")


def parse_primary(path: Path):
    rows: dict[int, list[int]] = {}
    witnesses: dict[tuple[int, int], tuple[int, tuple[int, ...]]] = {}
    row_re = re.compile(r"ROW n=(\d+):(.*)")
    witness_re = re.compile(r"WITNESS n=(\d+) k=(\d+) score=(\d+) A=\[(.*)\]")
    text = path.read_text()
    for line in text.splitlines():
        if match := row_re.fullmatch(line):
            rows[int(match.group(1))] = [int(v) for v in match.group(2).split()]
        elif match := witness_re.fullmatch(line):
            n, k, score = map(int, match.group(1, 2, 3))
            values = tuple(int(v) for v in match.group(4).split(",") if v)
            witnesses[n, k] = score, values
    assert "LIMIT 32" in text
    assert "NODES 2147483648" in text
    assert text.rstrip().endswith("ALL CHECKS PASSED")
    assert rows == EXPECTED_ROWS
    return rows, witnesses


def direct_score(values: tuple[int, ...]) -> int:
    return len({a + b for a in values for b in values})


def check_all_lower_witnesses(rows, witnesses) -> None:
    for n, row in rows.items():
        if n == 27:
            continue  # frozen baseline from the preceding certified package
        for (wn, k), (score, values) in witnesses.items():
            if wn != n:
                continue
            assert len(values) == k == len(set(values))
            assert min(values) >= 1 and max(values) <= n
            assert direct_score(values) == score == row[k - 1]

        first_full = next(k for k, score in enumerate(row, 1) if score == 2 * n - 1)
        full_values = witnesses[n, first_full][1]
        sidon_values = witnesses[n, 7][1]
        for k, claimed in enumerate(row, 1):
            cap = min(k * (k + 1) // 2, 2 * n - 1)
            assert claimed <= cap
            if (n, k) in witnesses:
                values = witnesses[n, k][1]
            elif k < 7:
                values = sidon_values[:k]
            elif k > first_full:
                chosen = set(full_values)
                for value in range(1, n + 1):
                    if len(chosen) == k:
                        break
                    chosen.add(value)
                values = tuple(sorted(chosen))
            else:
                raise AssertionError((n, k, "missing witness"))
            assert len(values) == k
            assert direct_score(values) == claimed, (n, k, values, claimed)
    print("definition-level lower witnesses for every n=28..32 cell: PASS")


def direct_small_table(limit: int = 13) -> None:
    """Independent combinations/set implementation, unrelated to bit masks."""
    candidates = 0
    for n in range(1, limit + 1):
        for k in range(1, n + 1):
            best = -1
            for tail in combinations(range(1, n), k - 1):
                candidates += 1
                best = max(best, direct_score((0,) + tail))
            assert 1 <= best <= min(k * (k + 1) // 2, 2 * n - 1)
    assert candidates == 8191
    print("independent direct-definition small search: PASS (8,191 candidates)")


def normalize_output(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if not line.startswith("SECONDS "))


def normalize_prior_output(text: str) -> str:
    return "\n".join(
        "incremental enumeration seconds: <timing>"
        if line.startswith("incremental enumeration seconds:") else line
        for line in text.splitlines()
    )


def check_prior_baseline() -> None:
    frozen = (HERE / "prior_n27_fresh_output.txt").read_text()
    for sentinel in (
        "enumerated translated subsets: 67,108,864",
        "sampled direct recurrence checks: 68",
        "independent small-search candidates: 8,191",
        "s(k,27), k=1..27:\n"
        "1 3 6 10 15 21 28 34 41 47 51 53 53 53 53 53 53 53 53 53 53 53 53 53 53 53 53",
        "ALL CHECKS PASSED",
    ):
        assert sentinel in frozen, sentinel
    print("frozen prior n<=27 baseline transcript: PASS")


def rerun_prior_baseline() -> None:
    completed = subprocess.run(
        [sys.executable, str(HERE / "prior_n27_verify.py")],
        check=True,
        text=True,
        capture_output=True,
    )
    frozen = (HERE / "prior_n27_fresh_output.txt").read_text()
    assert normalize_prior_output(completed.stdout) == normalize_prior_output(frozen)
    print("fresh prior n<=27 Python replay: PASS")


def rerun_primary() -> None:
    compiler = shutil.which("g++")
    assert compiler, "g++ is required unless --quick is used"
    with tempfile.TemporaryDirectory(prefix="erdos840-primary-") as raw:
        binary = Path(raw) / "primary_exact"
        subprocess.run(
            [compiler, "-O3", "-std=c++20", "-Wall", "-Wextra", "-pedantic",
             str(HERE / "primary_exact.cpp"), "-o", str(binary)],
            check=True,
        )
        completed = subprocess.run([str(binary)], check=True, text=True, capture_output=True)
    frozen = (HERE / "primary_output.txt").read_text()
    assert normalize_output(completed.stdout) == normalize_output(frozen)
    print("fresh 2^31-subset primary rerun: PASS")


def check_sat_artifacts() -> None:
    selftest = (HERE / "sat_encoding_selftest_output.txt").read_text()
    assert "instances checked: 94" in selftest
    assert "SAT ENCODING SELF-TEST PASSED" in selftest
    for (n, k), target in SAT_CASES.items():
        stem = f"n{n:02d}_k{k:02d}_no_score_{target}"
        cnf = HERE / "sat" / f"{stem}.cnf"
        header = cnf.read_text().splitlines()[0]
        assert re.fullmatch(r"p cnf \d+ \d+", header), header
        cadical = (HERE / "sat" / f"{stem}.cadical.log").read_text(errors="replace")
        kissat = (HERE / "sat" / f"{stem}.kissat.log").read_text(errors="replace")
        replay = (HERE / "sat" / f"{stem}.drat-trim.log").read_text(errors="replace")
        assert "UNSATISFIABLE" in cadical, stem
        assert "UNSATISFIABLE" in kissat, stem
        assert "VERIFIED" in replay, stem
        assert (HERE / "sat" / f"{stem}.drat.gz").stat().st_size > 0
    summary = (HERE / "sat_audit_output.txt").read_text()
    assert "NONTRIVIAL_SAT_CASES 6" in summary
    assert "INDEPENDENT SAT/DRAT AUDIT PASSED" in summary
    print("independent n=32 SAT/Kissat/DRAT records: PASS (6 cases)")


def replay_drat(drat_trim: Path) -> None:
    assert drat_trim.is_file()
    for (n, k), target in SAT_CASES.items():
        stem = f"n{n:02d}_k{k:02d}_no_score_{target}"
        cnf = HERE / "sat" / f"{stem}.cnf"
        with tempfile.TemporaryDirectory(prefix="erdos840-drat-") as raw:
            proof = Path(raw) / "proof.drat"
            with gzip.open(HERE / "sat" / f"{stem}.drat.gz", "rb") as source, proof.open("wb") as sink:
                shutil.copyfileobj(source, sink)
            result = subprocess.run([str(drat_trim), str(cnf), str(proof)], text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        assert result.returncode == 0 and "VERIFIED" in result.stdout, stem
        print(f"fresh DRAT replay {stem}: PASS")


def check_live_gate() -> None:
    gate = (HERE / "live_gate_2026-08-12.txt").read_text()
    for sentinel in (
        "OPEN",
        "0 claimed proofs for this problem",
        "Interested in collaborating\tNone",
        "Currently working on this problem\tNone",
        "accessed 2026-08-12",
    ):
        assert sentinel in gate, sentinel
    print("live no-collision gate transcript: PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="skip the fresh 2^31-node C++ rerun")
    parser.add_argument("--replay-drat", action="store_true")
    parser.add_argument("--drat-trim", type=Path,
                        default=Path("/home/exedev/MathDyad/erdos813/tools/drat-trim/drat-trim"))
    args = parser.parse_args()

    check_manifest()
    check_live_gate()
    check_prior_baseline()
    rows, witnesses = parse_primary(HERE / "primary_output.txt")
    check_all_lower_witnesses(rows, witnesses)
    direct_small_table()
    check_sat_artifacts()
    if not args.quick:
        rerun_prior_baseline()
        rerun_primary()
    if args.replay_drat:
        replay_drat(args.drat_trim)
    print("ALL BUNDLE CHECKS PASSED")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"CHECK FAILED: {exc!r}", file=sys.stderr)
        raise
