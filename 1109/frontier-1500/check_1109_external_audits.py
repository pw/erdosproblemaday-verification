#!/usr/bin/env python3
"""Cold log/hash/witness checker for the two external Problem 1109 audits."""

from hashlib import sha256
from math import isqrt
from pathlib import Path

BASE_N = 1103
MAX_N = 1500
BASE_OPTIMUM = 39
TRANSITIONS = (1255, 1277, 1293, 1335, 1407)
CLIQUER_LOG = Path("erdos1109_incremental_parallel_reverse_cliquer_2026-08-11.log")
PMC_LOG = Path("erdos1109_incremental_pmc_2026-08-11.log")
PRIMARY_LOG = Path("erdos1109_frontier_run_2026-08-11.log")


def squarefree(value):
    return value > 0 and all(
        value % (divisor * divisor)
        for divisor in range(2, isqrt(value) + 1)
    )


def parse_record(line):
    fields = dict(field.split("=", 1) for field in line.split())
    witness = fields["witness"].strip("{}")
    return {
        "n": int(fields["n"]),
        "target": int(fields["target"]),
        "neighbors": int(fields["neighbors"]),
        "edges": int(fields["edges"]),
        "exists": fields["exists"] == "True",
        "graph_hash": fields["graph_sha256"],
        "witness": tuple(map(int, witness.split(","))) if witness else (),
    }


def parse_audit(path):
    lines = path.read_text(encoding="ascii").splitlines()
    records = [parse_record(line) for line in lines if line.startswith("n=")]
    digest_lines = [line.split("=", 1)[1] for line in lines if line.startswith("audit_sha256=")]
    conclusions = [line for line in lines if line.startswith("CONCLUSION ")]
    assert len(records) == 163
    assert len(digest_lines) == len(conclusions) == 1
    return records, digest_lines[0]


def graph_texts(new_value, all_values):
    old_values = [value for value in all_values if value < new_value]
    neighbors = [
        old for old in old_values if squarefree(new_value + old)
    ]
    edges = []
    for left_index, left in enumerate(neighbors):
        for right_index in range(left_index + 1, len(neighbors)):
            if squarefree(left + neighbors[right_index]):
                edges.append((left_index + 1, right_index + 1))

    dimacs_lines = [f"p edge {len(neighbors)} {len(edges)}\n"]
    dimacs_lines.extend(f"e {left} {right}\n" for left, right in edges)

    matrix_lines = [
        "%%MatrixMarket matrix coordinate pattern symmetric\n",
        f"{len(neighbors)} {len(neighbors)} {len(edges)}\n",
    ]
    matrix_lines.extend(f"{right} {left}\n" for left, right in edges)
    return neighbors, edges, "".join(dimacs_lines), "".join(matrix_lines)


def check_records(records, expected_values, graph_kind):
    assert [record["n"] for record in records] == expected_values
    digest_records = []
    for record in records:
        new_value = record["n"]
        target = BASE_OPTIMUM + sum(point < new_value for point in TRANSITIONS)
        assert record["target"] == target
        assert record["exists"] == (new_value in TRANSITIONS)

        neighbors, edges, dimacs, matrix_market = graph_texts(new_value, ALL_VALUES)
        assert record["neighbors"] == len(neighbors)
        assert record["edges"] == len(edges)
        graph_text = dimacs if graph_kind == "dimacs" else matrix_market
        assert record["graph_hash"] == sha256(graph_text.encode("ascii")).hexdigest()

        witness = record["witness"]
        if record["exists"]:
            assert len(witness) == target + 1
            assert len(set(witness)) == len(witness)
            assert max(witness) == new_value
            assert all(
                squarefree(left + right)
                for left_index, left in enumerate(witness)
                for right in witness[left_index:]
            )
        else:
            assert not witness

        witness_text = ",".join(map(str, witness))
        digest_records.append(
            f"{new_value}:{target}:{int(record['exists'])}:"
            f"{len(neighbors)}:{len(edges)}:{record['graph_hash']}:"
            f"{witness_text}\n"
        )
    return sha256("".join(digest_records).encode("ascii")).hexdigest()


ALL_VALUES = [value for value in range(1, MAX_N + 1) if squarefree(2 * value)]


def main():
    expected_values = [value for value in ALL_VALUES if value > BASE_N]
    assert len(expected_values) == 163

    cliquer_records, cliquer_claimed_digest = parse_audit(CLIQUER_LOG)
    pmc_records, pmc_claimed_digest = parse_audit(PMC_LOG)
    cliquer_digest = check_records(cliquer_records, expected_values, "dimacs")
    pmc_digest = check_records(pmc_records, expected_values, "matrix")
    assert cliquer_digest == cliquer_claimed_digest
    assert pmc_digest == pmc_claimed_digest

    cliquer_decisions = [
        (record["n"], record["target"], record["exists"])
        for record in cliquer_records
    ]
    pmc_decisions = [
        (record["n"], record["target"], record["exists"])
        for record in pmc_records
    ]
    assert cliquer_decisions == pmc_decisions

    primary_decisions = []
    for line in PRIMARY_LOG.read_text(encoding="ascii").splitlines():
        if not line.startswith("decision n="):
            continue
        fields = dict(field.split("=", 1) for field in line.split()[1:])
        new_value = int(fields["n"])
        if new_value > BASE_N:
            primary_decisions.append(
                (new_value, int(fields["target"]), bool(int(fields["exists"])))
            )
    assert primary_decisions == cliquer_decisions

    print(f"eligible_decisions={len(expected_values)}")
    print(f"cliquer_audit_sha256={cliquer_digest}")
    print(f"pmc_audit_sha256={pmc_digest}")
    print("positive_decisions={" + ",".join(map(str, TRANSITIONS)) + "}")
    print("CONCLUSION external logs, graphs, witnesses, and primary decisions agree")


if __name__ == "__main__":
    main()
