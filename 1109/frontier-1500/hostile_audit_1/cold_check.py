#!/usr/bin/env python3
"""Independent integrity, graph, log, and witness audit for Problem 1109."""

from __future__ import annotations

import argparse
import hashlib
import re
from math import isqrt
from pathlib import Path


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def squarefree_trial(n: int) -> bool:
    if n < 1:
        return False
    p = 2
    while p * p <= n:
        if n % (p * p) == 0:
            return False
        p += 1
    return True


def squarefree_sieve(limit: int) -> list[bool]:
    result = [True] * (limit + 1)
    result[0] = False
    for d in range(2, isqrt(limit) + 1):
        for n in range(d * d, limit + 1, d * d):
            result[n] = False
    return result


def parse_fields(line: str) -> dict[str, str]:
    return dict(token.split("=", 1) for token in line.split() if "=" in token)


def parse_external(path: Path) -> tuple[list[dict[str, object]], str]:
    lines = path.read_text(encoding="ascii").splitlines()
    result = []
    for line in lines:
        if not line.startswith("n="):
            continue
        f = parse_fields(line)
        witness_text = f["witness"].strip("{}")
        result.append(
            {
                "n": int(f["n"]),
                "target": int(f["target"]),
                "neighbors": int(f["neighbors"]),
                "edges": int(f["edges"]),
                "exists": f["exists"] == "True",
                "hash": f["graph_sha256"],
                "witness": tuple(map(int, witness_text.split(",")))
                if witness_text
                else (),
            }
        )
    claimed = [line.split("=", 1)[1] for line in lines if line.startswith("audit_sha256=")]
    conclusions = [line for line in lines if line.startswith("CONCLUSION ")]
    assert len(claimed) == len(conclusions) == 1
    return result, claimed[0]


def graph_for(n: int, eligible: list[int]) -> tuple[list[int], list[tuple[int, int]], str, str]:
    neighbors = [v for v in eligible if v < n and squarefree_trial(v + n)]
    edges = []
    for i, left in enumerate(neighbors):
        for j in range(i + 1, len(neighbors)):
            if squarefree_trial(left + neighbors[j]):
                edges.append((i + 1, j + 1))
    dimacs = f"p edge {len(neighbors)} {len(edges)}\n" + "".join(
        f"e {i} {j}\n" for i, j in edges
    )
    matrix = (
        "%%MatrixMarket matrix coordinate pattern symmetric\n"
        f"{len(neighbors)} {len(neighbors)} {len(edges)}\n"
        + "".join(f"{j} {i}\n" for i, j in edges)
    )
    return neighbors, edges, dimacs, matrix


def check_clique(values: tuple[int, ...] | list[int], maximum: int) -> None:
    assert values
    assert len(values) == len(set(values))
    assert min(values) >= 1 and max(values) == maximum
    for i, left in enumerate(values):
        for right in values[i:]:
            assert squarefree_trial(left + right), (maximum, left, right)


def canonical(records: list[dict[str, object]]) -> bytes:
    lines = []
    for r in records:
        witness = ",".join(map(str, r["witness"]))
        lines.append(
            f"{r['n']}:{r['target']}:{int(r['exists'])}:"
            f"{r['neighbors']}:{r['edges']}:{r['hash']}:{witness}\n"
        )
    return "".join(lines).encode("ascii")


def verify_manifest(bundle: Path) -> tuple[int, str]:
    manifest = bundle / "erdos1109_manifest_2026-08-11.sha256"
    assert digest(manifest.read_bytes()) == "cbd71d674a96c46a40b1a2a2a6b3ac7d9a18e05d255f4c8033b5233894bda7e9"
    lines = manifest.read_text(encoding="ascii").splitlines()
    seen = set()
    for line in lines:
        expected, rel = line.split("  ./", 1)
        assert rel not in seen and rel != manifest.name
        seen.add(rel)
        assert digest((bundle / rel).read_bytes()) == expected, rel
    actual = {
        str(path.relative_to(bundle))
        for path in bundle.rglob("*")
        if path.is_file() and path != manifest
    }
    assert seen == actual
    return len(lines), digest(manifest.read_bytes())


def bfile_values(path: Path) -> list[int]:
    rows = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        left, right = map(int, line.split())
        rows.append((left, right))
    assert [left for left, _ in rows] == list(range(rows[0][0], rows[0][0] + len(rows)))
    return [right for _, right in rows]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args()
    bundle = args.bundle.resolve()

    count, manifest_hash = verify_manifest(bundle)
    sieve = squarefree_sieve(3000)
    assert all(sieve[n] == squarefree_trial(n) for n in range(3001))
    eligible = [n for n in range(1, 1501) if squarefree_trial(2 * n)]
    after_base = [n for n in eligible if n > 1103]
    assert len(eligible) == 610 and len(after_base) == 163

    cliquer, cliquer_claimed = parse_external(
        bundle / "erdos1109_incremental_parallel_reverse_cliquer_2026-08-11.log"
    )
    pmc, pmc_claimed = parse_external(bundle / "erdos1109_incremental_pmc_2026-08-11.log")
    assert len(cliquer) == len(pmc) == 163
    assert [r["n"] for r in cliquer] == [r["n"] for r in pmc] == after_base

    current = 39
    transitions = []
    for cr, pr in zip(cliquer, pmc):
        n = cr["n"]
        assert (cr["n"], cr["target"], cr["exists"]) == (
            pr["n"], pr["target"], pr["exists"]
        )
        assert cr["target"] == current
        neighbors, edges, dimacs, matrix = graph_for(n, eligible)
        for record, text in ((cr, dimacs), (pr, matrix)):
            assert record["neighbors"] == len(neighbors)
            assert record["edges"] == len(edges)
            assert record["hash"] == digest(text.encode("ascii"))
            if record["exists"]:
                assert len(record["witness"]) == current + 1
                check_clique(record["witness"], n)
            else:
                assert not record["witness"]
        if cr["exists"]:
            transitions.append(n)
            current += 1
    assert current == 44
    assert digest(canonical(cliquer)) == cliquer_claimed
    assert digest(canonical(pmc)) == pmc_claimed

    primary_text = (bundle / "erdos1109_frontier_run_2026-08-11.log").read_text(
        encoding="ascii"
    )
    primary_decisions = []
    for line in primary_text.splitlines():
        if line.startswith("decision n="):
            f = parse_fields(line)
            n = int(f["n"])
            if n > 1103:
                primary_decisions.append((n, int(f["target"]), bool(int(f["exists"]))))
    expected_decisions = [(r["n"], r["target"], r["exists"]) for r in cliquer]
    assert primary_decisions == expected_decisions

    primary_transitions = []
    primary_witnesses = {}
    for line in primary_text.splitlines():
        match = re.match(r"f=(\d+) first_N=(\d+) witness=\{([^}]*)\}", line)
        if not match:
            continue
        size, n = int(match.group(1)), int(match.group(2))
        witness = tuple(map(int, match.group(3).split(",")))
        assert len(witness) == size
        check_clique(witness, n)
        primary_transitions.append(n)
        primary_witnesses[n] = witness

    published = bfile_values(bundle / "oeis_A392165_bfile_accessed_2026-08-11.txt")
    assert len(published) == 39 and published[-1] == 1103
    assert primary_transitions[:39] == published
    assert primary_transitions[39:] == transitions
    assert all(len(primary_witnesses[n]) == size for size, n in enumerate(transitions, 40))

    print(f"manifest_payload_files={count}")
    print(f"manifest_sha256={manifest_hash}")
    print(f"eligible_vertices={len(eligible)} external_decisions={len(after_base)}")
    print(f"transitions={','.join(map(str, transitions))}")
    print(f"cliquer_digest={cliquer_claimed}")
    print(f"pmc_digest={pmc_claimed}")
    print("PASS independent manifest, arithmetic, graph, log, digest, induction, and witness checks")


if __name__ == "__main__":
    main()
