#!/usr/bin/env python3
"""Independent structural and certificate audit for the frozen #1109 bundle."""

from hashlib import sha256
from pathlib import Path
import re


BUNDLE = Path("/home/exedev/erdos_scratch/erdos1109_exact_frontier_2026-08-11")
MANIFEST = BUNDLE / "erdos1109_manifest_2026-08-11.sha256"
CLIQUER_LOG = BUNDLE / "erdos1109_incremental_parallel_reverse_cliquer_2026-08-11.log"
PMC_LOG = BUNDLE / "erdos1109_incremental_pmc_2026-08-11.log"
PRIMARY_LOG = BUNDLE / "erdos1109_frontier_run_2026-08-11.log"
SANITIZER_LOG = BUNDLE / "erdos1109_frontier_sanitize_run_2026-08-11.log"
TRANSITIONS = (1255, 1277, 1293, 1335, 1407)
EXPECTED_INTERVALS = (
    (1103, 1254, 39),
    (1255, 1276, 40),
    (1277, 1292, 41),
    (1293, 1334, 42),
    (1335, 1406, 43),
    (1407, 1500, 44),
)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def mobius_table(limit):
    """Linear sieve; squarefree(n) iff mu[n] is nonzero."""
    least_prime = [0] * (limit + 1)
    mu = [0] * (limit + 1)
    primes = []
    mu[1] = 1
    for value in range(2, limit + 1):
        if least_prime[value] == 0:
            least_prime[value] = value
            primes.append(value)
            mu[value] = -1
        for prime in primes:
            product = value * prime
            if product > limit:
                break
            least_prime[product] = prime
            if value % prime == 0:
                mu[product] = 0
                break
            mu[product] = -mu[value]
    return mu


MU = mobius_table(3000)


def squarefree(value):
    return value > 0 and MU[value] != 0


def parse_record(line):
    fields = dict(field.split("=", 1) for field in line.split())
    witness_text = fields["witness"].strip("{}")
    return {
        "n": int(fields["n"]),
        "target": int(fields["target"]),
        "neighbors": int(fields["neighbors"]),
        "edges": int(fields["edges"]),
        "exists": fields["exists"] == "True",
        "graph_hash": fields["graph_sha256"],
        "witness": tuple(map(int, witness_text.split(","))) if witness_text else (),
    }


def parse_external(path):
    lines = path.read_text(encoding="ascii").splitlines()
    records = [parse_record(line) for line in lines if line.startswith("n=")]
    claimed = [line.split("=", 1)[1] for line in lines if line.startswith("audit_sha256=")]
    finished = [line for line in lines if line.startswith("finished n=")]
    conclusions = [line for line in lines if line.startswith("CONCLUSION ")]
    assert len(records) == len(finished) == 163
    assert len(claimed) == len(conclusions) == 1
    finished_keys = []
    for line in finished:
        match = re.fullmatch(r"finished n=(\d+) target=(\d+) exists=(True|False) seconds=([0-9.]+)", line)
        assert match, line
        finished_keys.append((int(match[1]), int(match[2]), match[3] == "True"))
        assert float(match[4]) < 3600
    assert sorted(finished_keys) == sorted(
        (record["n"], record["target"], record["exists"]) for record in records
    )
    return lines, records, claimed[0]


def graph_texts(new_value, all_values):
    old_values = [value for value in all_values if value < new_value]
    neighbors = [value for value in old_values if squarefree(new_value + value)]
    edges = []
    for left_index, left in enumerate(neighbors):
        for right_index in range(left_index + 1, len(neighbors)):
            if squarefree(left + neighbors[right_index]):
                edges.append((left_index + 1, right_index + 1))
    dimacs = f"p edge {len(neighbors)} {len(edges)}\n" + "".join(
        f"e {left} {right}\n" for left, right in edges
    )
    matrix = (
        "%%MatrixMarket matrix coordinate pattern symmetric\n"
        f"{len(neighbors)} {len(neighbors)} {len(edges)}\n"
        + "".join(f"{right} {left}\n" for left, right in edges)
    )
    return neighbors, edges, dimacs, matrix


def validate_witness(witness, expected_size, maximum):
    assert len(witness) == len(set(witness)) == expected_size
    assert tuple(sorted(witness)) == witness
    assert witness[-1] == maximum
    assert all(
        squarefree(left + right)
        for index, left in enumerate(witness)
        for right in witness[index:]
    )


def check_external(records, expected_values, graph_kind):
    assert [record["n"] for record in records] == expected_values
    digest_lines = []
    semantic_lines = []
    optimum = 39
    for record in records:
        new_value = record["n"]
        assert record["target"] == optimum
        neighbors, edges, dimacs, matrix = graph_texts(new_value, ALL_VALUES)
        assert record["neighbors"] == len(neighbors)
        assert record["edges"] == len(edges)
        graph_text = dimacs if graph_kind == "dimacs" else matrix
        assert record["graph_hash"] == sha256(graph_text.encode("ascii")).hexdigest()
        if record["exists"]:
            validate_witness(record["witness"], optimum + 1, new_value)
            optimum += 1
        else:
            assert not record["witness"]
        witness_text = ",".join(map(str, record["witness"]))
        digest_lines.append(
            f"{new_value}:{record['target']}:{int(record['exists'])}:"
            f"{len(neighbors)}:{len(edges)}:{record['graph_hash']}:{witness_text}\n"
        )
        semantic_lines.append(
            f"{new_value}:" + ",".join(map(str, neighbors)) + ":" +
            ",".join(f"{left}-{right}" for left, right in edges) + "\n"
        )
    assert optimum == 44
    return (
        sha256("".join(digest_lines).encode("ascii")).hexdigest(),
        sha256("".join(semantic_lines).encode("ascii")).hexdigest(),
    )


def parse_primary_transitions(lines):
    result = []
    pattern = re.compile(r"f=(\d+) first_N=(\d+) witness=\{([^}]*)\}")
    for line in lines:
        match = pattern.fullmatch(line)
        if match:
            witness = tuple(map(int, match[3].split(",")))
            result.append((int(match[1]), int(match[2]), witness))
    return result


def deterministic_frontier_lines(path):
    return [
        line for line in path.read_text(encoding="ascii").splitlines()
        if line.startswith(("decision ", "Erdos Problem", "MAX_N=", "f=", "CONCLUSION "))
    ]


def check_manifest():
    assert digest(MANIFEST) == "cbd71d674a96c46a40b1a2a2a6b3ac7d9a18e05d255f4c8033b5233894bda7e9"
    entries = []
    for line in MANIFEST.read_text(encoding="ascii").splitlines():
        claimed, relative = line.split("  ", 1)
        path = BUNDLE / relative.removeprefix("./")
        assert path.is_file()
        assert digest(path) == claimed
        entries.append(relative.removeprefix("./"))
    actual = sorted(
        str(path.relative_to(BUNDLE))
        for path in BUNDLE.rglob("*")
        if path.is_file() and path != MANIFEST
    )
    assert len(entries) == len(set(entries)) == 70
    assert sorted(entries) == actual

    nested_root = BUNDLE / "erdos1109_cliquer_order_races_2026-08-11"
    nested_manifest = nested_root / "MANIFEST.sha256"
    nested_entries = []
    for line in nested_manifest.read_text(encoding="ascii").splitlines():
        claimed, relative = line.split("  ", 1)
        path = BUNDLE / relative
        assert path.is_file() and digest(path) == claimed
        nested_entries.append(str(path.relative_to(nested_root)))
    nested_actual = sorted(
        str(path.relative_to(nested_root))
        for path in nested_root.rglob("*")
        if path.is_file() and path != nested_manifest
    )
    assert sorted(nested_entries) == nested_actual


ALL_VALUES = [value for value in range(1, 1501) if squarefree(2 * value)]


def main():
    check_manifest()
    assert len(ALL_VALUES) == 610
    assert all(squarefree(2 * value) == (value % 2 == 1 and squarefree(value)) for value in range(1, 1501))
    expected_values = [value for value in ALL_VALUES if value > 1103]
    assert len(expected_values) == 163
    assert expected_values[0] == 1105 and expected_values[-1] == 1499
    assert not squarefree(2 * 1104) and not squarefree(2 * 1500)

    cliquer_lines, cliquer_records, cliquer_claimed = parse_external(CLIQUER_LOG)
    pmc_lines, pmc_records, pmc_claimed = parse_external(PMC_LOG)
    cliquer_digest, semantic_digest_1 = check_external(cliquer_records, expected_values, "dimacs")
    pmc_digest, semantic_digest_2 = check_external(pmc_records, expected_values, "matrix")
    assert cliquer_digest == cliquer_claimed == "6583a40e338f7bddbfe7eb666b3e1996c1c55bf7e325ce4ca9070a4baa856b84"
    assert pmc_digest == pmc_claimed == "cce1073c81456eb675be5adea58cf4fd2caa08f84bfa344465b38eadd5596dc3"
    assert semantic_digest_1 == semantic_digest_2
    cliquer_decisions = [(r["n"], r["target"], r["exists"]) for r in cliquer_records]
    pmc_decisions = [(r["n"], r["target"], r["exists"]) for r in pmc_records]
    assert cliquer_decisions == pmc_decisions
    assert tuple(record["n"] for record in cliquer_records if record["exists"]) == TRANSITIONS
    assert "### Time limit expired" not in "\n".join(pmc_lines)

    raw_hash = digest(CLIQUER_LOG)
    assert raw_hash == "eb871ca90a7830424f82a9f77c90bd3a6a8eada181fb80d9595c1170966ec973"
    certificate = BUNDLE / "erdos1109_cliquer_certificate_2026-08-11.log"
    certificate_lines = certificate.read_text(encoding="ascii").splitlines()
    certificate_records = [parse_record(line) for line in certificate_lines if line.startswith("n=")]
    assert certificate_records == cliquer_records
    assert f"raw_log_sha256={raw_hash}" in certificate_lines
    assert digest(certificate) == "30047bb3157b037a8122c56162e6fb89367f261aa7234604bb30fadb2aefd5ba"

    for record in cliquer_records:
        retained = BUNDLE / "erdos1109_cliquer_order_races_2026-08-11" / "graphs" / f"neighbors_{record['n']}.dimacs"
        if retained.exists():
            _, _, dimacs, _ = graph_texts(record["n"], ALL_VALUES)
            assert retained.read_text(encoding="ascii") == dimacs

    primary_lines = PRIMARY_LOG.read_text(encoding="ascii").splitlines()
    decision_pattern = re.compile(r"decision n=(\d+) target=(\d+) exists=([01]) nodes=(\d+)")
    primary_decisions = []
    for line in primary_lines:
        match = decision_pattern.fullmatch(line)
        if match:
            primary_decisions.append((int(match[1]), int(match[2]), bool(int(match[3]))))
    assert primary_decisions[0] == (1103, 38, True)
    assert primary_decisions[1:] == cliquer_decisions
    assert [n for n, _, _ in primary_decisions] == [value for value in ALL_VALUES if value >= 1103]

    transitions = parse_primary_transitions(primary_lines)
    assert len(transitions) == 44
    witness_lines = []
    for size, point, witness in transitions:
        assert size == len(witness)
        validate_witness(witness, size, point)
        witness_lines.append(f"{size}:{point}:" + ",".join(map(str, witness)) + "\n")
    transition_points = tuple(point for _, point, _ in transitions)
    frozen_oeis = tuple(
        int(line.split()[1])
        for line in (BUNDLE / "oeis_A392165_bfile_accessed_2026-08-11.txt").read_text(encoding="ascii").splitlines()
        if line and not line.startswith("#")
    )
    assert transition_points[:39] == frozen_oeis
    assert transition_points[39:] == TRANSITIONS

    values = [0] * 1501
    optimum = 0
    transition_iter = iter(transition_points)
    next_transition = next(transition_iter)
    for n in range(1, 1501):
        if n == next_transition:
            optimum += 1
            next_transition = next(transition_iter, None)
        values[n] = optimum
    intervals = []
    for start in range(1103, 1501):
        if start == 1103 or values[start] != values[start - 1]:
            end = start
            while end < 1500 and values[end + 1] == values[start]:
                end += 1
            intervals.append((start, end, values[start]))
    assert tuple(intervals) == EXPECTED_INTERVALS

    assert deterministic_frontier_lines(PRIMARY_LOG) == deterministic_frontier_lines(SANITIZER_LOG)
    sanitizer_text = SANITIZER_LOG.read_text(encoding="ascii")
    assert "ERROR: AddressSanitizer" not in sanitizer_text
    assert "runtime error:" not in sanitizer_text
    assert sanitizer_text.count("Exit status: 0") == 1
    assert "-fsanitize=address,undefined" in (BUNDLE / "erdos1109_frontier_sanitize_compile_2026-08-11.log").read_text(encoding="ascii")

    assert digest(BUNDLE / "verify_1109_frontier") == "84ebeca91559cfa6caaff408059731d9a35f74f6f446edde0aa807895e93bdb8"
    assert digest(BUNDLE / "pmc_1109_audit") == "e64c831e961bd18242e3cdd8b167dafc3322d667c3d90907eafc75720493f62d"

    print("PASS independent artifact/certificate check")
    print(f"manifest_sha256={digest(MANIFEST)} entries=70")
    print(f"eligible_vertices={len(ALL_VALUES)} post_1103_decisions={len(expected_values)}")
    print(f"semantic_graphs_sha256={semantic_digest_1}")
    print(f"cliquer_audit_sha256={cliquer_digest}")
    print(f"pmc_audit_sha256={pmc_digest}")
    print("transitions={" + ",".join(map(str, TRANSITIONS)) + "}")
    print("intervals=" + ";".join(f"{a}-{b}:{v}" for a, b, v in EXPECTED_INTERVALS))
    print("all_primary_witnesses_sha256=" + sha256("".join(witness_lines).encode("ascii")).hexdigest())
    print("sanitizer_deterministic_output_match=YES diagnostics=NONE")


if __name__ == "__main__":
    main()
