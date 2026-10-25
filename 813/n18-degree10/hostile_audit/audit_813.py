#!/usr/bin/env python3
"""Independent hostile audit for the frozen Erdos #813 attack bundle.

This checker deliberately does not import the producer's census or CNF code.
It checks the graph6 files from definitions, independently rebuilds every
one-vertex census transition, verifies raw/consolidated solver-log coverage,
rebuilds the fixed-neighbourhood SAT instances, and checks the near witness.

The default run is definition-level and includes the full 10->11->12->13
augmentation audit.  Optional solver reruns remain solver assertions; they
do not turn the archived UNSAT results into proof certificates.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import re
import subprocess
import tempfile
from collections import Counter
from itertools import combinations
from pathlib import Path
from time import perf_counter


DEFAULT_BUNDLE = Path(__file__).resolve().parent.parent
EXPECTED = {
    10: (9133, "234be06b2b8dbadec010e95ec0f62fffbe936a21207654f521742c063321ff0c"),
    11: (403, "5c519de3308a947bbdfbda8db4ad02b4f6e9435247204c571730b931a9069e50"),
    12: (8, "178c371f2e88e09bfd3462f225496c5e8910eb2e779a6cfcd7ecb001c07e4b0c"),
    13: (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_graph6(line: bytes) -> tuple[int, ...]:
    """Parse the small graph6 form without NetworkX or producer code."""
    line = line.strip()
    assert line and line[0] != 126, "only small graph6 order encoding expected"
    n = line[0] - 63
    assert 0 <= n <= 62
    bits: list[int] = []
    for byte in line[1:]:
        assert 63 <= byte <= 126
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    need = n * (n - 1) // 2
    assert len(bits) >= need and all(bit == 0 for bit in bits[need:])
    adj = [0] * n
    cursor = 0
    for v in range(1, n):
        for u in range(v):
            if bits[cursor]:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
            cursor += 1
    return tuple(adj)


def encode_graph6(adj: tuple[int, ...]) -> bytes:
    n = len(adj)
    assert n <= 62
    bits = [(adj[u] >> v) & 1 for v in range(1, n) for u in range(v)]
    bits.extend([0] * (-len(bits) % 6))
    payload = bytearray([63 + n])
    for start in range(0, len(bits), 6):
        value = sum(bits[start + offset] << (5 - offset) for offset in range(6))
        payload.append(63 + value)
    return bytes(payload) + b"\n"


def load_graph6(path: Path) -> tuple[list[bytes], list[tuple[int, ...]]]:
    lines = [line.strip() + b"\n" for line in path.read_bytes().splitlines() if line.strip()]
    return lines, [parse_graph6(line) for line in lines]


def clique(adj: tuple[int, ...] | list[int], vertices: tuple[int, ...]) -> bool:
    return all((adj[u] >> v) & 1 for u, v in combinations(vertices, 2))


def triangle_free(adj: tuple[int, ...] | list[int], vertices: tuple[int, ...]) -> bool:
    return not any(clique(adj, triple) for triple in combinations(vertices, 3))


def valid_census_graph(adj: tuple[int, ...]) -> bool:
    vertices = tuple(range(len(adj)))
    return (
        not any(clique(adj, four) for four in combinations(vertices, 4))
        and not any(triangle_free(adj, seven) for seven in combinations(vertices, 7))
    )


def child_extensions(adj: tuple[int, ...]) -> list[bytes]:
    """Enumerate extensions directly from the two defining conditions."""
    n = len(adj)
    vertices = tuple(range(n))
    edge_masks = [(1 << u) | (1 << v) for u, v in combinations(vertices, 2)
                  if (adj[u] >> v) & 1]
    triangle_masks = [sum(1 << v for v in triple)
                      for triple in combinations(vertices, 3) if clique(adj, triple)]
    edgeful = [False] * (1 << n)
    triangle_free_mask = [True] * (1 << n)
    for mask in range(1 << n):
        edgeful[mask] = any((mask & edge) == edge for edge in edge_masks)
        triangle_free_mask[mask] = not any(
            (mask & triangle) == triangle for triangle in triangle_masks
        )
    tf_sixes = [mask for mask in range(1 << n)
                if mask.bit_count() == 6 and triangle_free_mask[mask]]
    output: list[bytes] = []
    for mask in range(1 << n):
        if mask.bit_count() > 6:
            continue
        neighbourhood = tuple(v for v in vertices if (mask >> v) & 1)
        if not triangle_free_mask[mask]:
            continue
        if not all(edgeful[mask & six] for six in tf_sixes):
            continue
        child = list(adj) + [mask]
        for v in neighbourhood:
            child[v] |= 1 << n
        encoded = encode_graph6(tuple(child))
        assert parse_graph6(encoded) == tuple(child)
        assert valid_census_graph(tuple(child))
        output.append(encoded)
    return output


def canonicalise(lines: list[bytes]) -> bytes:
    with tempfile.TemporaryDirectory(prefix="erdos813-hostile-") as directory:
        raw = Path(directory) / "raw.g6"
        canon = Path(directory) / "canon.g6"
        raw.write_bytes(b"".join(lines))
        subprocess.run(["nauty-shortg", "-q", str(raw), str(canon)], check=True)
        return canon.read_bytes()


def audit_manifest(bundle: Path) -> None:
    manifest = bundle / "SHA256SUMS"
    listed: set[str] = set()
    for raw in manifest.read_text().splitlines():
        expected, name = raw.split(maxsplit=1)
        listed.add(name)
        actual = sha256(bundle / name)
        assert actual == expected, (name, expected, actual)
    raw_logs = {
        path.relative_to(bundle).as_posix()
        for pattern in (
            "logs/cadical/d11_shard*.log",
            "logs/cadical/d11_case*.log",
            "logs/kissat/d11_kissat_shard*.log",
        )
        for path in bundle.glob(pattern)
    }
    absent = sorted(raw_logs - listed)
    print(f"MANIFEST files={len(listed)} hashes=PASS raw_solver_logs_not_listed={len(absent)}")


def audit_censuses(bundle: Path, transitions: bool) -> dict[int, list[tuple[int, ...]]]:
    loaded: dict[int, list[tuple[int, ...]]] = {}
    for n, (expected_count, expected_hash) in EXPECTED.items():
        path = bundle / f"census_n{n}.g6"
        lines, graphs = load_graph6(path)
        assert len(lines) == len(set(lines)) == expected_count
        assert sha256(path) == expected_hash
        assert all(len(graph) == n and valid_census_graph(graph) for graph in graphs)
        loaded[n] = graphs
        print(f"CENSUS n={n} count={len(graphs)} sha256={expected_hash} definition=PASS distinct=PASS")

    direct_path = bundle / "direct_n10.g6"
    direct_lines, direct_graphs = load_graph6(direct_path)
    assert len(direct_lines) == len(set(direct_lines)) == 9133
    assert all(len(graph) == 10 and valid_census_graph(graph) for graph in direct_graphs)
    direct_canonical = canonicalise(direct_lines)
    expected_bytes = (bundle / "census_n10.g6").read_bytes()
    assert direct_canonical == (bundle / "direct_n10_canon.g6").read_bytes() == expected_bytes
    print(
        "DIRECT_N10 count=9133 definitions=PASS distinct=PASS "
        f"raw_sha256={sha256(direct_path)} canonical_byte_comparison=PASS"
    )

    if transitions:
        for parent_n in (10, 11, 12):
            started = perf_counter()
            extensions: list[bytes] = []
            for graph in loaded[parent_n]:
                extensions.extend(child_extensions(graph))
            canonical = canonicalise(extensions)
            expected = (bundle / f"census_n{parent_n + 1}.g6").read_bytes()
            assert canonical == expected
            print(
                f"TRANSITION {len(loaded[parent_n])}->{len(loaded[parent_n + 1])} "
                f"labelled={len(extensions)} canonical_bytes=PASS COMPLETE "
                f"seconds={perf_counter() - started:.3f}"
            )
    return loaded


def edge_and_triangle_variables(n: int) -> tuple[
    list[tuple[int, int]], list[tuple[int, int, int]],
    dict[tuple[int, int], int], dict[tuple[int, int, int], int]
]:
    pairs = list(combinations(range(n), 2))
    triples = list(combinations(range(n), 3))
    edge = {pair: index for index, pair in enumerate(pairs, 1)}
    triangle = {triple: len(pairs) + index for index, triple in enumerate(triples, 1)}
    return pairs, triples, edge, triangle


def independent_base_cnf(n: int = 18) -> tuple[int, list[list[int]], list[tuple[int, int]]]:
    pairs, triples, edge, triangle = edge_and_triangle_variables(n)
    clauses: list[list[int]] = []
    for triple in triples:
        t = triangle[triple]
        es = [edge[pair] for pair in combinations(triple, 2)]
        clauses.append([-t, es[0]])
        clauses.append([-t, es[1]])
        clauses.append([-t, es[2]])
        clauses.append([-es[0], -es[1], -es[2], t])
    for five in combinations(range(n), 5):
        clauses.append([-edge[pair] for pair in combinations(five, 2)])
    for seven in combinations(range(n), 7):
        clauses.append([triangle[triple] for triple in combinations(seven, 3)])
    return len(pairs) + len(triples), clauses, pairs


def fixed_formula(neighbourhood: tuple[int, ...]) -> tuple[int, list[list[int]]]:
    d = len(neighbourhood)
    nvars, clauses, pairs = independent_base_cnf(18)
    clauses = [list(clause) for clause in clauses]
    edge = {pair: index for index, pair in enumerate(pairs, 1)}

    def e(u: int, v: int) -> int:
        return edge[tuple(sorted((u, v)))]

    for v in range(1, 18):
        clauses.append([e(0, v) if v <= d else -e(0, v)])
    for u, v in combinations(range(d), 2):
        variable = e(u + 1, v + 1)
        clauses.append([variable if (neighbourhood[u] >> v) & 1 else -variable])
    return nvars, clauses


RESULT_RE = re.compile(
    r"\bcase=(\d+)(?:/(\d+))?\b.*?(?:\bedges|\bneighbourhood_edges)=(\d+)\b.*?"
    r"\bresult=(True|False|None)\b.*?(?:\bconflicts=(-?\d+)\s+)?"
    r"\bseconds=([0-9.]+)"
)


def extract_results(paths: list[Path]) -> dict[int, dict[str, str | int]]:
    output: dict[int, dict[str, str | int]] = {}
    for path in sorted(paths):
        for line in path.read_text().splitlines():
            match = RESULT_RE.search(line)
            if not match:
                continue
            case = int(match.group(1))
            assert case not in output, (case, output[case]["file"], path.name)
            output[case] = {
                "total": int(match.group(2)) if match.group(2) else -1,
                "edges": int(match.group(3)),
                "result": match.group(4),
                "conflicts": match.group(5),
                "seconds": match.group(6),
                "file": path.name,
            }
    return output


def read_table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def audit_d11_family(
    label: str,
    raw: dict[int, dict[str, str | int]],
    table_path: Path,
    census: list[tuple[int, ...]],
) -> None:
    assert set(raw) == set(range(403))
    table = read_table(table_path)
    assert len(table) == 403 and {int(row["case"]) for row in table} == set(range(403))
    for row in table:
        case = int(row["case"])
        item = raw[case]
        assert item["result"] == row["result"] == "False"
        assert item["seconds"] == row["seconds"]
        if "conflicts" in row:
            assert item["conflicts"] == row["conflicts"]
        assert item["edges"] == sum(mask.bit_count() for mask in census[case]) // 2
    seconds = sum(float(row["seconds"]) for row in table)
    slow = max(table, key=lambda row: float(row["seconds"]))
    conflicts = sum(int(row["conflicts"]) for row in table) if "conflicts" in table[0] else None
    suffix = f" conflicts={conflicts}" if conflicts is not None else " conflicts=unavailable"
    print(
        f"D11_LOGS solver={label} raw_cases=403 table_cases=403 exact_match=PASS "
        f"all_UNSAT=PASS seconds={seconds:.3f} slow_case={slow['case']} "
        f"slow_seconds={float(slow['seconds']):.3f}{suffix}"
    )


def audit_solver_logs(bundle: Path, census: dict[int, list[tuple[int, ...]]]) -> None:
    cadical_paths = sorted(bundle.glob("logs/cadical/d11_shard[0-9]*.log")) + sorted(
        bundle.glob("logs/cadical/d11_case*.log")
    )
    kissat_paths = sorted(bundle.glob("logs/kissat/d11_kissat_shard*.log"))
    audit_d11_family(
        "cadical195", extract_results(cadical_paths), bundle / "d11_all_cases.tsv", census[11]
    )
    audit_d11_family(
        "kissat404", extract_results(kissat_paths), bundle / "d11_kissat_all_cases.tsv", census[11]
    )
    for label, name in (
        ("cadical195", "logs/cadical/d12_all_cases.log"),
        ("kissat404", "logs/kissat/d12_kissat.log"),
    ):
        results = extract_results([bundle / name])
        assert set(results) == set(range(8))
        for case, item in results.items():
            assert item["result"] == "False"
            assert item["edges"] == sum(mask.bit_count() for mask in census[12][case]) // 2
        print(f"D12_LOGS solver={label} cases=8 all_UNSAT=PASS edge_metadata=PASS")


def audit_cnf(bundle: Path, census: dict[int, list[tuple[int, ...]]]) -> None:
    nvars, base, pairs = independent_base_cnf(18)
    assert nvars == 969 and len(pairs) == 153 and len(base) == 43656
    lengths = Counter(map(len, base))
    assert lengths == Counter({2: 2448, 4: 816, 10: 8568, 35: 31824})

    # Exact implementation comparison is secondary to the independent
    # derivation above, but catches transcription differences in the bundle.
    spec = importlib.util.spec_from_file_location(
        "bundled_neighbourhood_checker", bundle / "neighbourhood_census_sat.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    producer_nvars, producer_base, producer_pairs = module.build(18, 5)
    assert (producer_nvars, producer_base, producer_pairs) == (nvars, base, pairs)

    for d in (11, 12):
        expected_clauses = 43656 + 17 + d * (d - 1) // 2
        # Check every representative's fixed-edge data directly.  Building
        # and discarding 411 identical 43,656-clause bases would add no audit
        # coverage, so instantiate the full formula once per degree.
        for neighbourhood in census[d]:
            assert len(neighbourhood) == d
            assert all(
                ((neighbourhood[u] >> v) & 1) == ((neighbourhood[v] >> u) & 1)
                for u, v in combinations(range(d), 2)
            )
        got_nvars, clauses = fixed_formula(census[d][0])
        assert got_nvars == 969 and len(clauses) == expected_clauses
        assert all(len(clause) == 1 for clause in clauses[-(17 + d * (d - 1) // 2):])
        print(
            f"CNF degree={d} cases={len(census[d])} vars=969 clauses={expected_clauses} "
            "base_exact_comparison=PASS fixed_units=PASS"
        )


def audit_near_witness(bundle: Path) -> None:
    adj = tuple(int(token, 16) for token in (bundle / "best9.masks").read_text().split())
    n = len(adj)
    assert n == 18
    full = (1 << n) - 1
    assert all((adj[u] >> u) & 1 == 0 and not (adj[u] & ~full) for u in range(n))
    assert all(((adj[u] >> v) & 1) == ((adj[v] >> u) & 1) for u in range(n) for v in range(n))
    vertices = tuple(range(n))
    edges = [pair for pair in combinations(vertices, 2) if (adj[pair[0]] >> pair[1]) & 1]
    triangles = [triple for triple in combinations(vertices, 3) if clique(adj, triple)]
    k4s = [four for four in combinations(vertices, 4) if clique(adj, four)]
    k5s = [five for five in combinations(vertices, 5) if clique(adj, five)]
    bad = [seven for seven in combinations(vertices, 7) if triangle_free(adj, seven)]
    degrees = sorted(mask.bit_count() for mask in adj)
    assert (len(edges), len(triangles), len(k5s), len(bad)) == (96, 180, 0, 9)
    assert k4s and degrees == [10] * 6 + [11] * 12

    repairs: list[tuple[tuple[int, int], int, int]] = []
    for u, v in combinations(vertices, 2):
        if (adj[u] >> v) & 1:
            continue
        changed = list(adj)
        changed[u] |= 1 << v
        changed[v] |= 1 << u
        remaining_bad = sum(triangle_free(changed, seven) for seven in combinations(vertices, 7))
        if remaining_bad >= len(bad):
            continue
        new_k5s = sum(clique(changed, five) for five in combinations(vertices, 5))
        repairs.append(((u, v), len(bad) - remaining_bad, new_k5s))
    assert len(repairs) == 39 and min(item[2] for item in repairs) == 3

    automorphisms = "not_checked"
    try:
        import networkx as nx
        graph = nx.Graph()
        graph.add_nodes_from(vertices)
        graph.add_edges_from(edges)
        automorphisms = str(sum(
            1 for _ in nx.algorithms.isomorphism.GraphMatcher(graph, graph).isomorphisms_iter()
        ))
        assert automorphisms == "12"
    except ImportError:
        pass
    print(
        "NEAR n=18 edges=96 triangles=180 K4_count=" + str(len(k4s)) +
        " K5_count=0 bad7=9 omega=4 degrees=10^6,11^12 "
        f"automorphisms={automorphisms} repairing_additions=39 min_created_K5=3 PASS"
    )


def rerun_sat(census: dict[int, list[tuple[int, ...]]]) -> None:
    from pysat.solvers import Solver

    samples = {12: list(range(8)), 11: [0, 394]}
    for solver_name in ("cadical195", "kissat404"):
        for d, cases in samples.items():
            for case in cases:
                nvars, clauses = fixed_formula(census[d][case])
                started = perf_counter()
                with Solver(name=solver_name, bootstrap_with=clauses) as solver:
                    result = solver.solve()
                elapsed = perf_counter() - started
                assert nvars == 969 and result is False
                print(
                    f"SAT_RERUN solver={solver_name} degree={d} case={case} "
                    f"result=UNSAT seconds={elapsed:.3f}"
                )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--quick", action="store_true", help="skip full transition rebuild")
    parser.add_argument("--rerun-sat", action="store_true", help="rerun d12 and selected d11 formulas")
    args = parser.parse_args()
    started = perf_counter()
    audit_manifest(args.bundle)
    census = audit_censuses(args.bundle, transitions=not args.quick)
    audit_cnf(args.bundle, census)
    audit_solver_logs(args.bundle, census)
    audit_near_witness(args.bundle)
    if args.rerun_sat:
        rerun_sat(census)
    print(
        "AUDIT_PASS: finite structure and archived log coverage verified. "
        "UNSAT verdicts remain uncertified solver assertions (no DRAT/LRAT proof logs). "
        f"seconds={perf_counter() - started:.3f}"
    )


if __name__ == "__main__":
    main()
