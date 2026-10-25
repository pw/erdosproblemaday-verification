#!/usr/bin/env python3
"""Cold, solver-independent parser/checker for the #1109 N=2000 PMC log."""

from hashlib import sha256
from pathlib import Path
import re


BASE_N = 1500
BASE_F = 44
MAX_N = 2000
TRANSITIONS = (1509, 1535, 1595, 1707, 1735, 1779, 1835, 1919, 1991, 1999)
HERE = Path(__file__).resolve().parent
PMC_LOG = HERE / "pmc_1501_2000_strict.log"
PMC_TIME = HERE / "pmc_1501_2000_strict.time"


def smallest_prime_factors(limit: int) -> list[int]:
    spf = list(range(limit + 1))
    spf[0] = 0
    spf[1] = 1
    for prime in range(2, limit + 1):
        if spf[prime] != prime:
            continue
        for multiple in range(prime * prime, limit + 1, prime):
            if spf[multiple] == multiple:
                spf[multiple] = prime
    return spf


SPF = smallest_prime_factors(2 * MAX_N)


def squarefree(value: int) -> bool:
    if value < 1:
        return False
    while value > 1:
        prime = SPF[value]
        value //= prime
        if value % prime == 0:
            return False
        while value > 1 and value % prime == 0:
            value //= prime
    return True


def parse_record(line: str) -> dict:
    match = re.fullmatch(
        r"n=(\d+) target=(\d+) neighbors=(\d+) edges=(\d+) "
        r"exists=(True|False) graph_sha256=([0-9a-f]{64}) witness=\{([^}]*)\}",
        line,
    )
    assert match, line
    witness_text = match.group(7)
    return {
        "n": int(match.group(1)),
        "target": int(match.group(2)),
        "neighbors": int(match.group(3)),
        "edges": int(match.group(4)),
        "exists": match.group(5) == "True",
        "graph_hash": match.group(6),
        "witness": tuple(map(int, witness_text.split(","))) if witness_text else (),
    }


def graph_for(new_value: int, all_values: list[int]):
    neighbors = [
        old for old in all_values
        if old < new_value and squarefree(old + new_value)
    ]
    edges = []
    for left_index, left in enumerate(neighbors):
        for right_index in range(left_index + 1, len(neighbors)):
            if squarefree(left + neighbors[right_index]):
                edges.append((left_index + 1, right_index + 1))
    lines = [
        "%%MatrixMarket matrix coordinate pattern symmetric\n",
        f"{len(neighbors)} {len(neighbors)} {len(edges)}\n",
    ]
    lines.extend(f"{right} {left}\n" for left, right in edges)
    return neighbors, edges, "".join(lines)


def main() -> None:
    log_text = PMC_LOG.read_text(encoding="ascii")
    lines = log_text.splitlines()
    records = [parse_record(line) for line in lines if line.startswith("n=")]
    claimed_digests = [
        line.split("=", 1)[1] for line in lines if line.startswith("audit_sha256=")
    ]
    conclusions = [line for line in lines if line.startswith("CONCLUSION ")]
    assert claimed_digests == ["aaaeea014ef1cc96993416d05f49e692359166b6f17e7be24211779353a3a549"]
    assert len(conclusions) == 1

    all_values = [value for value in range(1, MAX_N + 1) if squarefree(2 * value)]
    expected_values = [value for value in all_values if value > BASE_N]
    assert len(all_values) == 811
    assert len(expected_values) == len(records) == 201
    assert [record["n"] for record in records] == expected_values
    assert all(value % 2 == 1 and squarefree(value) for value in all_values)

    finished = {}
    for line in lines:
        match = re.fullmatch(
            r"finished n=(\d+) target=(\d+) exists=(True|False) seconds=([0-9.]+)",
            line,
        )
        if match:
            n = int(match.group(1))
            assert n not in finished
            finished[n] = (int(match.group(2)), match.group(3) == "True", float(match.group(4)))
    assert set(finished) == set(expected_values)
    assert max(item[2] for item in finished.values()) < 3600

    digest_rows = []
    checked_sums = 0
    for record in records:
        n = record["n"]
        target = BASE_F + sum(point < n for point in TRANSITIONS)
        expected_exists = n in TRANSITIONS
        assert record["target"] == target
        assert record["exists"] == expected_exists
        assert finished[n][:2] == (target, expected_exists)

        neighbors, edges, matrix_market = graph_for(n, all_values)
        graph_hash = sha256(matrix_market.encode("ascii")).hexdigest()
        assert record["neighbors"] == len(neighbors)
        assert record["edges"] == len(edges)
        assert record["graph_hash"] == graph_hash

        witness = record["witness"]
        if expected_exists:
            assert tuple(sorted(witness)) == witness
            assert len(witness) == len(set(witness)) == target + 1
            assert witness[-1] == n
            assert all(1 <= value <= n for value in witness)
            for left_index, left in enumerate(witness):
                for right in witness[left_index:]:
                    assert squarefree(left + right), (n, left, right)
                    checked_sums += 1
        else:
            assert not witness

        witness_text = ",".join(map(str, witness))
        digest_rows.append(
            f"{n}:{target}:{int(expected_exists)}:{len(neighbors)}:{len(edges)}:"
            f"{graph_hash}:{witness_text}\n"
        )

    digest = sha256("".join(digest_rows).encode("ascii")).hexdigest()
    assert digest == claimed_digests[0]
    assert "Exit status: 0" in PMC_TIME.read_text(encoding="ascii")
    assert [record["n"] for record in records if record["exists"]] == list(TRANSITIONS)
    assert BASE_F + len(TRANSITIONS) == 54

    intervals = []
    starts = (BASE_N + 1,) + TRANSITIONS
    values = (BASE_F,) + tuple(range(BASE_F + 1, BASE_F + len(TRANSITIONS) + 1))
    ends = tuple(point - 1 for point in TRANSITIONS) + (MAX_N,)
    for start, end, value in zip(starts, ends, values):
        intervals.append(f"{start}-{end}:{value}")

    print(f"eligible_total={len(all_values)} extension_decisions={len(records)}")
    print(f"positive_decisions={','.join(map(str, TRANSITIONS))}")
    print(f"checked_positive_sums={checked_sums}")
    print(f"slowest_pmc_seconds={max(item[2] for item in finished.values()):.3f}")
    print(f"audit_sha256={digest}")
    print("intervals=" + ";".join(intervals))
    print("CONCLUSION cold graph/hash/witness/quantifier audit passed; f(2000)=54 modulo exact PMC negatives")


if __name__ == "__main__":
    main()
