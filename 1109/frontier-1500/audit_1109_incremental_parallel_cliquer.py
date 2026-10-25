#!/usr/bin/env python3
"""Parallel external-Cliquer audit of the new Problem 1109 frontier."""

from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import cache
from hashlib import sha256
from pathlib import Path
from subprocess import PIPE, run
from tempfile import TemporaryDirectory
from time import monotonic

BASE_N = 1103
MAX_N = 1500
BASE_OPTIMUM = 39
NEW_TRANSITIONS = (1255, 1277, 1293, 1335, 1407)
CLIQUER = "/usr/bin/cliquer"


@cache
def is_squarefree_trial(value):
    divisor = 2
    while divisor * divisor <= value:
        if value % (divisor * divisor) == 0:
            return False
        divisor += 1
    return value > 0


def check_witness(witness, target, maximum):
    assert len(witness) == len(set(witness)) == target
    assert min(witness) >= 1 and max(witness) <= maximum
    for left_index, left in enumerate(witness):
        for right in witness[left_index:]:
            assert is_squarefree_trial(left + right), (left, right)


def neighbor_graph(new_value, old_values):
    neighbors = [old for old in old_values if is_squarefree_trial(new_value + old)]
    edges = []
    for left_index, left in enumerate(neighbors):
        for right_index in range(left_index + 1, len(neighbors)):
            if is_squarefree_trial(left + neighbors[right_index]):
                edges.append((left_index + 1, right_index + 1))
    lines = [f"p edge {len(neighbors)} {len(edges)}\n"]
    lines.extend(f"e {left} {right}\n" for left, right in edges)
    return neighbors, edges, "".join(lines)


def parse_witness(output, target, neighbors):
    result_line = next(line for line in output.splitlines() if line.startswith("size="))
    prefix, indices_text = result_line.split(":", 1)
    assert prefix.startswith(f"size={target}, weight={target}")
    indices = [int(token) for token in indices_text.split()]
    assert len(indices) == target
    return [neighbors[index - 1] for index in indices]


def audit_one(new_value, target, old_values, temp_dir):
    neighbors, edges, dimacs = neighbor_graph(new_value, old_values)
    graph_path = Path(temp_dir) / f"neighbors_{new_value}.dimacs"
    graph_path.write_text(dimacs, encoding="ascii")
    command = [
        CLIQUER, "-u", "-m", str(target), "-M", str(target),
        "-r", "reverse", "-q", str(graph_path),
    ]
    started = monotonic()
    completed = run(command, stdout=PIPE, stderr=PIPE, text=True, check=True)
    seconds = monotonic() - started
    output = completed.stdout + completed.stderr
    exists = "No such clique found." not in output
    expected_exists = new_value in NEW_TRANSITIONS
    assert exists == expected_exists, (new_value, target, output)

    witness = []
    if exists:
        witness = parse_witness(output, target, neighbors) + [new_value]
        witness.sort()
        check_witness(witness, target + 1, new_value)

    graph_hash = sha256(dimacs.encode("ascii")).hexdigest()
    return {
        "new_value": new_value,
        "target": target,
        "neighbors": len(neighbors),
        "edges": len(edges),
        "exists": exists,
        "seconds": seconds,
        "graph_hash": graph_hash,
        "witness": witness,
    }


def main():
    parser = ArgumentParser()
    parser.add_argument("--jobs", type=int, default=8)
    args = parser.parse_args()
    assert args.jobs >= 1

    all_values = [
        value for value in range(1, MAX_N + 1)
        if is_squarefree_trial(2 * value)
    ]
    tasks = []
    for new_value in all_values:
        if new_value <= BASE_N:
            continue
        old_values = [value for value in all_values if value < new_value]
        target = BASE_OPTIMUM + sum(point < new_value for point in NEW_TRANSITIONS)
        tasks.append((new_value, target, old_values))

    results = []
    with TemporaryDirectory(prefix="erdos1109_parallel_cliquer_") as temp_dir:
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            futures = [
                executor.submit(audit_one, new_value, target, old_values, temp_dir)
                for new_value, target, old_values in tasks
            ]
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                print(
                    f"finished n={result['new_value']} target={result['target']} "
                    f"exists={result['exists']} seconds={result['seconds']:.3f}",
                    flush=True,
                )

    records = []
    for result in sorted(results, key=lambda item: item["new_value"]):
        witness_text = ",".join(map(str, result["witness"]))
        records.append(
            f"{result['new_value']}:{result['target']}:{int(result['exists'])}:"
            f"{result['neighbors']}:{result['edges']}:{result['graph_hash']}:"
            f"{witness_text}\n"
        )
        print(
            f"n={result['new_value']} target={result['target']} "
            f"neighbors={result['neighbors']} edges={result['edges']} "
            f"exists={result['exists']} graph_sha256={result['graph_hash']} "
            f"witness={{{witness_text}}}"
        )

    assert len(results) == sum(value > BASE_N for value in all_values) == 163
    assert [result["new_value"] for result in results if result["exists"]]
    assert sorted(result["new_value"] for result in results if result["exists"]) == list(
        NEW_TRANSITIONS
    )
    print("audit_sha256=" + sha256("".join(records).encode("ascii")).hexdigest())
    print(
        "CONCLUSION external Cliquer certifies every eligible last-vertex "
        "decision for 1104<=N<=1500"
    )


if __name__ == "__main__":
    main()
