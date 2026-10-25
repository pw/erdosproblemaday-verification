#!/usr/bin/env python3
"""Standalone checks for the Erdős #840 exact extension n=33..37."""

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
    32: [1, 3, 6, 10, 15, 21, 28, 35, 42, 51, 55, 59, 62, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63],
    33: [1, 3, 6, 10, 15, 21, 28, 35, 42, 51, 56, 61, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65],
    34: [1, 3, 6, 10, 15, 21, 28, 35, 42, 51, 56, 61, 65, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67],
    35: [1, 3, 6, 10, 15, 21, 28, 36, 42, 51, 57, 63, 67, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69],
    36: [1, 3, 6, 10, 15, 21, 28, 36, 43, 51, 57, 63, 68, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71],
    37: [1, 3, 6, 10, 15, 21, 28, 36, 43, 51, 59, 64, 69, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73],
}
SAT_CASES = {
    (37, 10): 52,
    (37, 11): 60,
    (37, 12): 65,
    (37, 13): 70,
}
K9_DIAMETERS = (34, 35, 36)
SOLVER_HASHES = {
    "cadical": "544dbba6f5338c9d65cf99494fe73ab51892dcc2d9a2b2a3b1933a53e4378d2b",
    "kissat": "cc867d71737c6a79c6cc03d292c971f643bf8782c426a76900a94ca287eebdc5",
    "drat_trim": "f8d971dc5956a73fa37e655a44ba8f6d128976acfedff7129f2ed251b234af1a",
}
K9_HASHES = {
    34: (
        "9c6281ec44021a715b50e3914417289e34c6cd952c8bc50583fb36656b74f550",
        "805146202ebc3d4e7c31f31e7600833f57da125748338ee5383d5d338cb6a02e",
    ),
    35: (
        "2be555dc42b9b5c6ef869593cb3cb58a1bf96505a3122b6cbb801e9ebdf70a8b",
        "c8e77c5beb22d230c4812e75af5400da022a8e08d6e8e7be1d16a1fcfebcca3d",
    ),
    36: (
        "3fdd7b1190526cb9b94a550c9f7ceececebd98f37b6fd6a8f5aa388011fa36b1",
        "2d6103b4f110d0712b137d247499fd9c83732f610207a143cfe102f14e5d288e",
    ),
}
SAT_HASHES = {
    (37, 10): (
        "a1a654009790721430a832e3a69e023f1db7bfe1ff93f78f2e6cea34300b68a3",
        "3e2388dd1fe82c43ae56a1bbadfe10e599d2ec4dfaf2a9dc1c740786cad78a11",
    ),
    (37, 11): (
        "cf2606de9afb257a60c58fef03c3fe7b4bdf5b11ac8e7ac7083209ed3f3efacb",
        "9b193936cdb76eb9f527480caa774bf47f6e71092820a3e3033336f36515f756",
    ),
    (37, 12): (
        "33973c969af644719bf3f05cf873b61df01732a05d0c1cddcd7efcb6b701503c",
        "680daccc06090307e792839d803ecdd3c6bc4368549da7f725a5b2b07004f6be",
    ),
    (37, 13): (
        "e66288208a75cae1f070e29c4c453c1fba8ccb21d502b1df1d9098b2fe874797",
        "108903a7e0433e6cca386b9ea81004e42f027e8aef3b9c48c773d201469346dd",
    ),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def gzip_payload_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with gzip.open(path, "rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def check_solver_hash_records(text: str) -> None:
    for name, digest in SOLVER_HASHES.items():
        assert f"{name}_sha256={digest}" in text


def check_manifest() -> None:
    entries: dict[str, str] = {}
    for line in (HERE / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        assert re.fullmatch(r"[0-9a-f]{64}", digest)
        assert name not in entries
        entries[name] = digest
    actual = sorted(
        str(path.relative_to(HERE))
        for path in HERE.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS" and "__pycache__" not in path.parts
    )
    assert sorted(entries) == actual
    for name, digest in entries.items():
        assert sha256(HERE / name) == digest, name
    print(f"closed manifest: PASS ({len(entries)} files)")


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
    assert "LIMIT 37" in text
    assert "NODES 68719476736" in text
    assert text.rstrip().endswith("ALL CHECKS PASSED")
    for n, expected in EXPECTED_ROWS.items():
        assert rows[n] == expected, n
    return rows, witnesses


def direct_score(values: tuple[int, ...]) -> int:
    return len({a + b for a in values for b in values})


def check_lower_witnesses(rows, witnesses) -> None:
    for n in range(33, 38):
        row = rows[n]
        first_full = next(k for k, score in enumerate(row, 1) if score == 2 * n - 1)
        full_values = witnesses[n, first_full][1]
        sidon = witnesses[n, 7][1]
        for k, claimed in enumerate(row, 1):
            assert claimed <= min(k * (k + 1) // 2, 2 * n - 1)
            if (n, k) in witnesses:
                recorded, values = witnesses[n, k]
                assert recorded == claimed
            elif k < 7:
                values = sidon[:k]
            elif k > first_full:
                chosen = set(full_values)
                for value in range(1, n + 1):
                    if len(chosen) == k:
                        break
                    chosen.add(value)
                values = tuple(sorted(chosen))
            else:
                raise AssertionError((n, k, "missing lower witness"))
            assert len(values) == k == len(set(values))
            assert 1 <= min(values) <= max(values) <= n
            assert direct_score(values) == claimed, (n, k, values, claimed)
    print("definition-level lower witness for every extension cell: PASS")


def direct_small_search(limit: int = 13) -> None:
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


def normalize_primary(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if not line.startswith("SECONDS "))


def rerun_primary() -> None:
    compiler = shutil.which("g++")
    assert compiler
    with tempfile.TemporaryDirectory(prefix="erdos840-n37-") as raw:
        binary = Path(raw) / "primary"
        subprocess.run(
            [compiler, "-O3", "-std=c++20", "-Wall", "-Wextra", "-pedantic",
             str(HERE / "primary_exact_u128.cpp"), "-o", str(binary)],
            check=True,
        )
        completed = subprocess.run([str(binary)], text=True, capture_output=True, check=True)
    frozen = (HERE / "primary_output.txt").read_text()
    assert normalize_primary(completed.stdout) == normalize_primary(frozen)
    print("fresh 2^36-node primary rerun: PASS")


def check_sat_records() -> None:
    selftest = (HERE / "sat_encoding_selftest_output.txt").read_text()
    assert "instances checked: 94" in selftest
    assert "SAT ENCODING SELF-TEST PASSED" in selftest
    diameter_selftest = (HERE / "diameter_reduction_selftest_output.txt").read_text()
    assert "sum/difference sets checked: 8191" in diameter_selftest
    assert "DIAMETER REDUCTION SELF-TEST PASSED" in diameter_selftest

    split_summary = (HERE / "sat_k9_split_output.txt").read_text()
    check_solver_hash_records(split_summary)
    for diameter in K9_DIAMETERS:
        stem = f"n37_k09_no_score_44_diameter_{diameter}"
        cnf = HERE / "sat_k9_split" / f"{stem}.cnf"
        proof_gz = HERE / "sat_k9_split" / f"{stem}.drat.gz"
        expected_cnf, expected_proof = K9_HASHES[diameter]
        assert re.fullmatch(r"p cnf \d+ \d+", cnf.read_text().splitlines()[0])
        assert sha256(cnf) == expected_cnf
        assert gzip_payload_sha256(proof_gz) == expected_proof
        assert f"cnf_sha256={expected_cnf}" in split_summary
        assert f"proof_sha256={expected_proof}" in split_summary
        cadical = (HERE / "sat_k9_split" / f"{stem}.cadical.log").read_text(errors="replace")
        kissat = (HERE / "sat_k9_split" / f"{stem}.kissat.log").read_text(errors="replace")
        replay = (HERE / "sat_k9_split" / f"{stem}.drat-trim.log").read_text(errors="replace")
        assert "UNSATISFIABLE" in cadical
        assert "UNSATISFIABLE" in kissat
        assert "VERIFIED" in replay
        assert proof_gz.stat().st_size > 0
    assert "K9 DIAMETER-SPLIT AUDIT PASSED" in split_summary
    print("terminal n=37 k=9 diameter split and hashes: PASS (3 dual-solver/proof cases)")

    summary = (HERE / "sat_audit_output.txt").read_text()
    check_solver_hash_records(summary)
    for (n, k), target in SAT_CASES.items():
        stem = f"n{n:02d}_k{k:02d}_no_score_{target}"
        cnf = HERE / "sat" / f"{stem}.cnf"
        proof_gz = HERE / "sat" / f"{stem}.drat.gz"
        expected_cnf, expected_proof = SAT_HASHES[n, k]
        assert re.fullmatch(r"p cnf \d+ \d+", cnf.read_text().splitlines()[0])
        assert sha256(cnf) == expected_cnf
        assert gzip_payload_sha256(proof_gz) == expected_proof
        assert f"cnf_sha256={expected_cnf}" in summary
        assert f"proof_sha256={expected_proof}" in summary
        cadical = (HERE / "sat" / f"{stem}.cadical.log").read_text(errors="replace")
        kissat = (HERE / "sat" / f"{stem}.kissat.log").read_text(errors="replace")
        replay = (HERE / "sat" / f"{stem}.drat-trim.log").read_text(errors="replace")
        assert "UNSATISFIABLE" in cadical
        assert "UNSATISFIABLE" in kissat
        assert "VERIFIED" in replay
        assert proof_gz.stat().st_size > 0
    assert "NONTRIVIAL_SAT_CASES 4" in summary
    assert "INDEPENDENT SAT/DRAT AUDIT PASSED" in summary
    print("terminal n=37 generic CaDiCaL/Kissat/DRAT records and hashes: PASS (4 cases)")


def replay_drat(checker: Path) -> None:
    assert checker.is_file()
    for diameter in K9_DIAMETERS:
        stem = f"n37_k09_no_score_44_diameter_{diameter}"
        with tempfile.TemporaryDirectory(prefix="erdos840-proof-") as raw:
            proof = Path(raw) / "proof.drat"
            with gzip.open(HERE / "sat_k9_split" / f"{stem}.drat.gz", "rb") as source, proof.open("wb") as sink:
                shutil.copyfileobj(source, sink)
            result = subprocess.run(
                [str(checker), str(HERE / "sat_k9_split" / f"{stem}.cnf"), str(proof)],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
        assert result.returncode == 0 and "VERIFIED" in result.stdout, stem
        print(f"fresh DRAT replay {stem}: PASS")

    for (n, k), target in SAT_CASES.items():
        stem = f"n{n:02d}_k{k:02d}_no_score_{target}"
        with tempfile.TemporaryDirectory(prefix="erdos840-proof-") as raw:
            proof = Path(raw) / "proof.drat"
            with gzip.open(HERE / "sat" / f"{stem}.drat.gz", "rb") as source, proof.open("wb") as sink:
                shutil.copyfileobj(source, sink)
            result = subprocess.run(
                [str(checker), str(HERE / "sat" / f"{stem}.cnf"), str(proof)],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            )
        assert result.returncode == 0 and "VERIFIED" in result.stdout, stem
        print(f"fresh DRAT replay {stem}: PASS")


def check_live_gate() -> None:
    text = (HERE / "live_gate_2026-08-12.txt").read_text()
    for sentinel in (
        "OPEN",
        "0 claimed proofs for this problem",
        "Interested in collaborating\tNone",
        "Currently working on this problem\tNone",
        "accessed 2026-08-12",
    ):
        assert sentinel in text
    print("live no-collision transcript: PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rerun-primary", action="store_true",
                        help="repeat the roughly 5.5-minute 2^36-node traversal")
    parser.add_argument("--replay-drat", action="store_true")
    parser.add_argument("--drat-trim", type=Path,
                        default=Path("/home/exedev/MathDyad/erdos813/tools/drat-trim/drat-trim"))
    args = parser.parse_args()

    check_manifest()
    check_live_gate()
    rows, witnesses = parse_primary(HERE / "primary_output.txt")
    check_lower_witnesses(rows, witnesses)
    direct_small_search()
    check_sat_records()
    if args.rerun_primary:
        rerun_primary()
    if args.replay_drat:
        replay_drat(args.drat_trim)
    print("ALL EXTENSION CHECKS PASSED")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"CHECK FAILED: {exc!r}", file=sys.stderr)
        raise
