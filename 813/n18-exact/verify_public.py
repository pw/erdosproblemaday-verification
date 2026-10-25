#!/usr/bin/env python3
"""Self-contained audit of the compact Erdős #813 h(18)=5 bundle.

This checks the manifest, mathematical finite audit, graph6 census
definitions and filters, compact sweep summaries, the frozen d=11/d=12
two-solver tables, and one independently replayable d=10 DRAT spot proof.

It deliberately does not promote the complete sweeps to proof-certified:
their 269MB raw logs live in the separately hashed offline archive.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import itertools
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent

EXPECTED_CENSUSES = {
    "direct_n7.g6": (7, 578, "d9009414f9eea4baf919713c1431307476defb0113ed12893d6f4d711712294e"),
    "direct_n8.g6": (8, 3128, "75510632e58c7817029045bb13077d04f5e326a46f90d6fed79e88f03d208268"),
    "direct_n9.g6": (9, 11005, "36a71ed181bad51bc4758b3eb812298b2023e94cf7269071f8b6e949c54d8de5"),
    "direct_n10.g6": (10, 9133, "234be06b2b8dbadec010e95ec0f62fffbe936a21207654f521742c063321ff0c"),
}

EXPECTED_FILTERED = {
    "census_n7_alpha3.g6": (7, 353, "dcb9826f89febb23efdc2cce129faa588385a9f02211ac30a84e52906ee19739"),
    "census_n8_alpha3.g6": (8, 1829, "fff629fd92179ef4502f99548caed1481da39ac1239d3e99a78c6bbd3cba6df6"),
    "census_n9_alpha3.g6": (9, 8753, "c22b6fd0e5ebeea07afbf0396df30f153fbdc86c3374a95744d32100ffb9aa67"),
    "census_n10_alpha3.g6": (10, 8688, "4bfaf9ddb556254347a6dee7200b4852696686257427c107c6ab7cd2421177f0"),
}

EXPECTED_M = {
    "census_m7_canonical.g6": (7, 71, "64037dfeb6abc2f64fa92afc792e827d65325bc093434b8a7f9a906ae217bf29"),
    "census_m8_canonical.g6": (8, 179, "a7a0679d89af8f93e3008e4bc3ecb9f3f870a00fb5759720ddf617141b0e1e51"),
}


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def graph6_edges(line: bytes) -> tuple[int, set[tuple[int, int]]]:
    line = line.strip()
    assert line and line[0] != 126
    order = line[0] - 63
    assert 0 <= order <= 62
    bits: list[int] = []
    for char in line[1:]:
        value = char - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    pairs = [(u, v) for v in range(1, order) for u in range(v)]
    assert len(bits) >= len(pairs)
    return order, {pair for pair, bit in zip(pairs, bits) if bit}


def has_clique(order: int, edges: set[tuple[int, int]], size: int) -> bool:
    return any(
        all(tuple(sorted(pair)) in edges for pair in itertools.combinations(vertices, 2))
        for vertices in itertools.combinations(range(order), size)
    )


def has_independent(order: int, edges: set[tuple[int, int]], size: int) -> bool:
    return any(
        all(tuple(sorted(pair)) not in edges for pair in itertools.combinations(vertices, 2))
        for vertices in itertools.combinations(range(order), size)
    )


def has_triangle_free_seven(order: int, edges: set[tuple[int, int]]) -> bool:
    triangles = [
        frozenset(vertices)
        for vertices in itertools.combinations(range(order), 3)
        if all(tuple(sorted(pair)) in edges for pair in itertools.combinations(vertices, 2))
    ]
    return any(
        not any(triangle.issubset(seven) for triangle in triangles)
        for seven in map(frozenset, itertools.combinations(range(order), 7))
    )


def census_lines(path: Path) -> list[bytes]:
    return [line.strip() for line in path.read_bytes().splitlines() if line.strip()]


def verify_manifest() -> None:
    manifest = ROOT / "MANIFEST.sha256"
    assert manifest.exists()
    checked = 0
    for line in manifest.read_text().splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", 1)
        path = ROOT / relative.removeprefix("./")
        assert path.is_file(), path
        assert digest(path) == expected, path
        checked += 1
    print(f"MANIFEST verified_files={checked}")


def verify_upper_witness() -> None:
    checker = ROOT / "tools" / "verify_w18_upper.py"
    assert digest(checker) == "8ee0af91618b69113d49d54f3a7f24d6b043986b08e6e7252df622c60b940c1d"
    assert digest(ROOT / "w18.masks") == "3e1edce0c45327cb2ed9fb9addafdaadaa0467dece314df83ff5587924bbd1fe"
    result = subprocess.run(
        [sys.executable, str(checker), "--witness-only"],
        check=True, text=True, stdout=subprocess.PIPE,
    )
    assert "W18: n=18, edges=100, triangles=223, omega=5" in result.stdout
    assert "max triangle-free order=6" in result.stdout
    print("W18_UPPER omega=5 alpha3=6 definition_check=PASS")


def verify_neighbourhood_censuses() -> None:
    decoded_base: dict[int, list[tuple[bytes, set[tuple[int, int]]]]] = {}
    for name, (order, count, expected_hash) in EXPECTED_CENSUSES.items():
        path = ROOT / "censuses" / name
        assert digest(path) == expected_hash
        lines = census_lines(path)
        assert len(lines) == count and len(set(lines)) == count
        records = []
        for line in lines:
            actual_order, edges = graph6_edges(line)
            assert actual_order == order
            assert not has_clique(order, edges, 4)
            assert not has_triangle_free_seven(order, edges)
            records.append((line, edges))
        decoded_base[order] = records
        print(f"BASE_CENSUS order={order} count={count} definitions=PASS")

    for name, (order, count, expected_hash) in EXPECTED_FILTERED.items():
        path = ROOT / "censuses" / name
        assert digest(path) == expected_hash
        lines = census_lines(path)
        expected = [
            line for line, edges in decoded_base[order]
            if not has_independent(order, edges, 4)
        ]
        assert lines == expected and len(lines) == count
        print(f"FILTERED_H order={order} count={count} exact_sublist=PASS")


def verify_m_censuses(quick: bool) -> None:
    for name, (order, count, expected_hash) in EXPECTED_M.items():
        path = ROOT / "censuses" / name
        assert digest(path) == expected_hash
        lines = census_lines(path)
        assert len(lines) == count and len(set(lines)) == count
        for line in lines:
            actual_order, edges = graph6_edges(line)
            assert actual_order == order
            assert not has_clique(order, edges, 5)
            assert not has_independent(order, edges, 3)
        print(f"M_CENSUS order={order} count={count} definitions=PASS")

    assert digest(ROOT / "censuses" / "census_m8_canonical_shortg.g6") == (
        "7c760244e3efd2ef7549def2792490108155a1adcd8311ad4a2099c4d68799d8"
    )
    assert len(census_lines(ROOT / "censuses" / "census_m8_via_complements.g6")) == 179
    assert (ROOT / "censuses" / "census_m8_canonical_shortg.g6").read_bytes() == (
        ROOT / "censuses" / "census_m8_via_complements_shortg.g6"
    ).read_bytes()
    if not quick:
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / "verify_m7_census.py"),
             str(ROOT / "censuses" / "census_m7_canonical.g6")],
            check=True,
        )


def verify_sweep_summary() -> None:
    summary_path = ROOT / "SWEEP_SUMMARY.json"
    summary = json.loads(summary_path.read_text())
    assert "solver assertions" in summary["status"]
    expected = {
        7: (1, 353, 353),
        8: (1, 1829, 1829),
        9: (179, 8753, 1566787),
        10: (71, 8688, 616848),
    }
    audit_names = {
        7: "audit_d7_alpha3_census.log",
        8: "audit_d8_alpha3_census.log",
        9: "audit_d9_double_census.log",
        10: "audit_d10_double_census.log",
    }
    for row in summary["branches"]:
        degree = row["degree"]
        m_types, h_types, total = expected[degree]
        assert row["m_types"] == m_types and row["h_types"] == h_types
        assert m_types * h_types == total
        assert row["expected"] == row["observed_unique"] == row["unsat"] == total
        audit_path = ROOT / "audits" / audit_names[degree]
        assert digest(audit_path) == row["coverage_audit_sha256"]
        text = audit_path.read_text()
        assert "all_UNSAT=YES" in text and f"expected={total}" in text
    raw_hashes = ROOT / "OFFLINE_RAW_LOGS.sha256"
    hashes = re.findall(r"(?m)^([0-9a-f]{64})  (.+)$", raw_hashes.read_text())
    assert len(hashes) == 19 and len({name for _, name in hashes}) == 19
    assert summary["offline_archive"]["sha256"] == hashes[1][0]

    branch_hashes = re.findall(
        r"(?m)^([0-9a-f]{64})  branch_d(7|8|9|10)\.cnf$",
        (ROOT / "OFFLINE_BRANCH_CNFS.sha256").read_text(),
    )
    assert len(branch_hashes) == 4
    expected_branch_hashes = {
        "7": "7d470e3c43cea962ee11e5a48d1018b84043bff68a68c7bd852b63d602675347",
        "8": "c5d863bafbd97bd398bf7da5442740edb003441be90146f3e1b99ec5a2401b97",
        "9": "e1c692e377b797393a0acb09f5f74091f3c5f9357aa484ff118d9d3a76ecca6a",
        "10": "2a63c718792ce7fdce0161a664ef5b39411241789430fbe6dce5af0264197618",
    }
    assert {degree: value for value, degree in branch_hashes} == expected_branch_hashes
    for degree in (7, 8, 9, 10):
        text = (ROOT / "audits" / f"verify_branch_d{degree}_cnf.log").read_text()
        assert f"degree={degree}" in text
        assert "natural_clauses=43656 root_units=17" in text
        assert "degree_projection=EXACT exhaustive_assignments=131072" in text
    all_degrees = (ROOT / "audits" / "audit_all_d7_d12.log").read_text()
    assert "unique_indices=2185817 all_UNSAT=YES shards_done=17 hashes=PASS" in all_degrees
    assert "cadical_and_kissat_exact_case_coverage=411/411 all_UNSAT=YES" in all_degrees
    assert "VERIFIED GAP-FREE DEGREE COVERAGE d=7..12" in all_degrees
    print("SWEEP_SUMMARY exact_counts=PASS raw_logs_bound_by_SHA256=YES")


def verify_prior_delta10() -> None:
    prior = ROOT / "prior_delta10"
    for line in (prior / "MANIFEST.sha256").read_text().splitlines():
        expected, relative = line.split("  ", 1)
        assert digest(prior / relative) == expected

    for name in ("d11_all_cases.tsv", "d11_kissat_all_cases.tsv"):
        with (prior / name).open(newline="") as source:
            rows = list(csv.DictReader(source, delimiter="\t"))
        assert len(rows) == 403
        assert [int(row["case"]) for row in rows] == list(range(403))
        assert all(row["result"] == "False" for row in rows)
    for name in ("d12_all_cases.log", "d12_kissat.log"):
        lines = [line for line in (prior / name).read_text().splitlines()
                 if "case=" in line and "result=False" in line]
        assert len(lines) == 8
    assert len(census_lines(prior / "census_n11.g6")) == 403
    assert len(census_lines(prior / "census_n12.g6")) == 8
    assert len(census_lines(prior / "census_n13.g6")) == 0
    print("PRIOR_DELTA10 manifest=PASS d11_two_solver=403/403 d12_two_solver=8/8 d13=EMPTY")


def decompressed_hash(path: Path) -> str:
    with gzip.open(path, "rb") as source:
        return digest_bytes(source.read())


def verify_spot_proof(skip_drat: bool) -> None:
    cnf_gz = ROOT / "spot" / "d10_double_flat512188.cnf.gz"
    proof_gz = ROOT / "spot" / "d10_double_flat512188_kissat.drat.gz"
    assert decompressed_hash(cnf_gz) == "61c8846d263f71ce3f1dcd584ff30d53cb947b25c03e73dabec64bc71df47bd3"
    assert decompressed_hash(proof_gz) == "611f4be57e9eacd076042d42dd203a2b92e1415ab5d03c6ee6aadedbbdf98941"

    with tempfile.TemporaryDirectory(prefix="erdos813-public-") as directory:
        directory_path = Path(directory)
        full = directory_path / "spot.cnf"
        proof = directory_path / "spot.drat"
        with gzip.open(cnf_gz, "rb") as source:
            full.write_bytes(source.read())
        with gzip.open(proof_gz, "rb") as source:
            proof.write_bytes(source.read())

        comments = []
        clauses = []
        variables = declared = None
        for line in full.read_text().splitlines():
            if not line.strip():
                continue
            if line.startswith("c"):
                comments.append(line)
            elif line.startswith("p cnf"):
                _, _, variables_text, declared_text = line.split()
                variables, declared = int(variables_text), int(declared_text)
            else:
                clauses.append(line)
        assert variables == 2229 and declared == len(clauses) == 46205
        assert len(clauses) - 66 == 46139
        base = directory_path / "base.cnf"
        base.write_text(
            "c reconstructed exact d10 base prefix from published spot CNF\n"
            f"p cnf {variables} 46139\n" + "\n".join(clauses[:46139]) + "\n"
        )

        subprocess.run(
            [sys.executable, str(ROOT / "tools" / "verify_degree_branch_cnf.py"),
             "10", str(base)], check=True,
        )
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / "verify_double_census_case_cnf.py"),
             "10", "512188", str(base),
             str(ROOT / "censuses" / "census_m7_canonical.g6"),
             str(ROOT / "censuses" / "census_n10_alpha3.g6"), str(full)],
            check=True,
        )
        if not skip_drat:
            result = subprocess.run(
                [str(ROOT / "tools" / "drat-trim"), str(full), str(proof)],
                check=True, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            assert "s VERIFIED" in result.stdout
            print("SPOT_DRAT d10_flat512188=VERIFIED")
        else:
            print("SPOT_DRAT replay=SKIPPED compressed_hashes=PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true",
                        help="skip the exhaustive 2^21 labelled M7 orbit audit")
    parser.add_argument("--skip-drat", action="store_true",
                        help="skip the bundled x86-64 drat-trim replay")
    args = parser.parse_args()

    verify_manifest()
    verify_upper_witness()
    subprocess.run([sys.executable, str(ROOT / "tools" / "delta7_check.py")], check=True)
    verify_neighbourhood_censuses()
    verify_m_censuses(args.quick)
    verify_sweep_summary()
    verify_prior_delta10()
    verify_spot_proof(args.skip_drat)
    print("ALL COMPACT PUBLICATION CHECKS PASSED")
    print("STATUS: exhaustive solver assertions; not a full per-branch proof certificate")


if __name__ == "__main__":
    main()
