#!/usr/bin/env python3
"""Independent exact-index audit of every assertion log used for #813."""

import argparse
from hashlib import sha256
from pathlib import Path
import re

parser = argparse.ArgumentParser()
parser.add_argument("bundle", type=Path)
args = parser.parse_args()
BUNDLE = args.bundle.resolve()
ROOT = BUNDLE
OLD = BUNDLE / "prior_delta10"


def graph6_edges(path):
    output = []
    for raw in path.read_bytes().splitlines():
        values = [byte - 63 for byte in raw]
        n = values[0]
        bits = []
        for value in values[1:]:
            bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
        output.append(sum(bits[:n * (n - 1) // 2]))
    return output


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def mark(seen, index):
    assert 0 <= index < len(seen)
    assert not seen[index], f"duplicate index {index}"
    seen[index] = 1


CASE = re.compile(
    r"^CASE sequence=(\d+)/(\d+) case=(\d+)/(\d+) edges=(\d+) "
    r"result=(\w+) conflicts_delta=(-?\d+) decisions_delta=(-?\d+) seconds=([0-9.]+)$"
)
DONE_CASE = re.compile(
    r"^SHARD_DONE shard=(\d+)/(\d+) cases=(\d+) unsat=(\d+) seconds=([0-9.]+)$"
)


def audit_degree(degree, shards):
    census = ROOT / "censuses" / f"census_n{degree}_alpha3.g6"
    edges = graph6_edges(census)
    seen = bytearray(len(edges))
    paths = [ROOT / "logs" / f"d{degree}_alpha3_cadical_s{s}.log"
             for s in range(shards)]
    for shard, path in enumerate(paths):
        lines = path.read_text().splitlines()
        assert lines[0].startswith("SETUP ") and "solver=cadical195" in lines[0]
        case_lines = lines[1:-1]
        expected_indices = list(range(shard, len(edges), shards))
        assert len(case_lines) == len(expected_indices)
        for expected_sequence, (line, expected_index) in enumerate(
            zip(case_lines, expected_indices), 1
        ):
            match = CASE.fullmatch(line)
            assert match, line
            sequence, assigned, case, total, edge_count, result, conflicts, decisions, seconds = match.groups()
            assert int(sequence) == expected_sequence
            assert int(assigned) == len(expected_indices)
            assert int(case) == expected_index and int(total) == len(edges)
            assert int(edge_count) == edges[expected_index]
            assert result == "False" and int(conflicts) >= 0 and int(decisions) >= 0
            assert float(seconds) >= 0
            mark(seen, expected_index)
        done = DONE_CASE.fullmatch(lines[-1])
        assert done
        s, k, cases, unsat, seconds = done.groups()
        assert (int(s), int(k)) == (shard, shards)
        assert int(cases) == int(unsat) == len(expected_indices)
        assert float(seconds) >= 0
    assert all(seen)
    print(f"ASSERT d={degree} solver=CaDiCaL logs={shards} cases={len(edges)} "
          f"unique_complete=PASS logset_sha={sha256(''.join(digest(p) for p in paths).encode()).hexdigest()}")


PAIR = re.compile(
    r"^PAIR sequence=(\d+)/(\d+) flat=(\d+)/(\d+) "
    r"m=(\d+)/(\d+) h=(\d+)/(\d+) result=(\w+) "
    r"conflicts_delta=(-?\d+)(?: decisions_delta=(-?\d+))? seconds=(-?[0-9.]+)$"
)
DONE_PAIR = re.compile(
    r"^SHARD_DONE(?: degree=(\d+))? shard=(\d+)/(\d+) pairs=(\d+) "
    r"unsat=(\d+) seconds=([0-9.]+)$"
)


def audit_product(degree, m_path, h_path, prefix, shards):
    m_count = len(m_path.read_bytes().splitlines())
    h_count = len(h_path.read_bytes().splitlines())
    total = m_count * h_count
    seen = bytearray(total)
    paths = [ROOT / "logs" / f"{prefix}_s{s}.log" for s in range(shards)]
    for shard, path in enumerate(paths):
        with path.open() as source:
            setup = next(source).strip()
            assert setup.startswith("SETUP ") and "solver=cadical195" in setup
            expected_count = len(range(shard, total, shards))
            sequence_seen = 0
            done_line = None
            for raw in source:
                line = raw.strip()
                if line.startswith("SHARD_DONE"):
                    assert done_line is None
                    done_line = line
                    continue
                assert done_line is None, "content after SHARD_DONE"
                match = PAIR.fullmatch(line)
                assert match, line
                sequence, assigned, flat, logged_total, m_case, logged_m, h_case, logged_h, result, conflicts, decisions, seconds = match.groups()
                sequence_seen += 1
                flat = int(flat)
                assert int(sequence) == sequence_seen
                assert int(assigned) == expected_count
                assert int(logged_total) == total
                assert flat == shard + (sequence_seen - 1) * shards
                assert (int(m_case), int(h_case)) == divmod(flat, h_count)
                assert (int(logged_m), int(logged_h)) == (m_count, h_count)
                assert result == "False" and int(conflicts) >= 0
                assert decisions is None or int(decisions) >= 0
                # Five sub-millisecond negative readings occur across 2.18M
                # calls, consistent with cross-CPU timer skew in this VM.
                assert float(seconds) > -0.001
                mark(seen, flat)
            assert sequence_seen == expected_count and done_line is not None
            done = DONE_PAIR.fullmatch(done_line)
            assert done
            logged_degree, s, k, pairs, unsat, seconds = done.groups()
            assert logged_degree is None or int(logged_degree) == degree
            assert (int(s), int(k)) == (shard, shards)
            assert int(pairs) == int(unsat) == expected_count
            assert float(seconds) >= 0
    assert all(seen)
    print(f"ASSERT d={degree} solver=CaDiCaL logs={shards} M={m_count} H={h_count} "
          f"pairs={total} unique_complete=PASS logset_sha={sha256(''.join(digest(p) for p in paths).encode()).hexdigest()}")


OLD_CASE = re.compile(
    r"^shard=(\d+)/(\d+) sequence=(\d+)/(\d+) case=(\d+)/(\d+) "
    r"edges=(\d+) result=(\w+) conflicts=(-?\d+) seconds=([0-9.]+)$"
)
OLD_DONE = re.compile(
    r"^SHARD_DONE shard=(\d+)/(\d+) degree=(\d+) cases=(\d+) unsat=(\d+) "
    r"unknown=(\d+) conflicts=(\d+) seconds=([0-9.]+)$"
)


def audit_old_shards(degree, solver, shards, prefix, census):
    edges = graph6_edges(census)
    seen = bytearray(len(edges))
    if shards == 1 and (OLD / f"{prefix}.log").exists():
        paths = [OLD / f"{prefix}.log"]
    else:
        paths = [OLD / f"{prefix}{s}.log" for s in range(shards)]
    for shard, path in enumerate(paths):
        lines = path.read_text().splitlines()
        expected_indices = list(range(shard, len(edges), shards))
        assert len(lines) == len(expected_indices) + 1
        for seq, (line, expected_index) in enumerate(zip(lines[:-1], expected_indices), 1):
            match = OLD_CASE.fullmatch(line)
            assert match, line
            s, k, sequence, assigned, case, total, edge_count, result, conflicts, seconds = match.groups()
            assert (int(s), int(k)) == (shard, shards)
            assert (int(sequence), int(assigned)) == (seq, len(expected_indices))
            assert (int(case), int(total)) == (expected_index, len(edges))
            assert int(edge_count) == edges[expected_index]
            assert result == "False" and float(seconds) >= 0
            if solver == "CaDiCaL":
                assert int(conflicts) >= 0
            mark(seen, expected_index)
        done = OLD_DONE.fullmatch(lines[-1])
        assert done
        s, k, d, cases, unsat, unknown, conflicts, seconds = done.groups()
        assert (int(s), int(k), int(d)) == (shard, shards, degree)
        assert int(cases) == int(unsat) == len(expected_indices)
        assert int(unknown) == 0 and int(conflicts) >= 0 and float(seconds) >= 0
    assert all(seen)
    print(f"ASSERT d={degree} solver={solver} logs={shards} cases={len(edges)} "
          f"unique_complete=PASS logset_sha={sha256(''.join(digest(p) for p in paths).encode()).hexdigest()}")


audit_degree(7, 1)
audit_degree(8, 2)
audit_product(9, ROOT / "censuses" / "census_m8_canonical.g6", ROOT / "censuses" / "census_n9_alpha3.g6", "d9_double_cadical", 7)
audit_product(10, ROOT / "censuses" / "census_m7_canonical.g6", ROOT / "censuses" / "census_n10_alpha3.g6", "d10_double_cadical", 7)
audit_old_shards(11, "Kissat", 12, "d11_kissat_shard", OLD / "census_n11.g6")
audit_old_shards(12, "Kissat", 1, "d12_kissat", OLD / "census_n12.g6")

# The first d11 CaDiCaL launch was interrupted near completion. Ten exact
# one-case reruns fill its gaps; audit their union without relying on the TSV.
edges11 = graph6_edges(OLD / "census_n11.g6")
seen11 = bytearray(len(edges11))
d11_paths = [OLD / f"d11_shard{s}.log" for s in range(8)]
d11_paths += sorted(OLD.glob("d11_case*.log"))
for path in d11_paths:
    for line in path.read_text().splitlines():
        if line.startswith("SHARD_DONE"):
            continue
        match = OLD_CASE.fullmatch(line)
        assert match, (path, line)
        s, k, sequence, assigned, case, total, edge_count, result, conflicts, seconds = match.groups()
        case = int(case)
        assert int(total) == len(edges11) and int(edge_count) == edges11[case]
        assert result == "False" and int(conflicts) >= 0 and float(seconds) >= 0
        mark(seen11, case)
assert all(seen11)
print(f"ASSERT d=11 solver=CaDiCaL logs={len(d11_paths)} cases=403 "
      f"unique_complete=PASS logset_sha={sha256(''.join(digest(p) for p in d11_paths).encode()).hexdigest()}")

# The independent d12 CaDiCaL run uses a compact non-sharded format.
edges12 = graph6_edges(OLD / "census_n12.g6")
lines12 = (OLD / "d12_all_cases.log").read_text().splitlines()
simple = re.compile(r"^case=(\d+) neighbourhood_edges=(\d+) result=(\w+) conflicts=(\d+) seconds=([0-9.]+)$")
assert len(lines12) == 9
for case, line in enumerate(lines12[:-1]):
    match = simple.fullmatch(line)
    assert match
    logged_case, edge_count, result, conflicts, seconds = match.groups()
    assert int(logged_case) == case and int(edge_count) == edges12[case]
    assert result == "False" and int(conflicts) >= 0 and float(seconds) >= 0
assert lines12[-1].startswith("VERIFIED: all 8 order-12 neighbourhood types are UNSAT")
print(f"ASSERT d=12 solver=CaDiCaL logs=1 cases=8 unique_complete=PASS "
      f"log_sha={digest(OLD / 'd12_all_cases.log')}")
