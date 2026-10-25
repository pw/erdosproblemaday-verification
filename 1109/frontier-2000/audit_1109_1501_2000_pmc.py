#!/usr/bin/env python3
"""Independent exact-PMC audit of a Problem 1109 frontier extension."""

from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import cache
from hashlib import sha256
from pathlib import Path
from subprocess import PIPE, run
from tempfile import TemporaryDirectory
from time import monotonic

BASE_N = 1500
BASE_OPTIMUM = 44
PMC = str(Path(__file__).resolve().with_name("pmc_1109_audit"))


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

    # PMC's Matrix Market reader expects one-based lower-triangular entries.
    lines = [
        "%%MatrixMarket matrix coordinate pattern symmetric\n",
        f"{len(neighbors)} {len(neighbors)} {len(edges)}\n",
    ]
    lines.extend(f"{right} {left}\n" for left, right in edges)
    return neighbors, edges, "".join(lines)


def parse_witness(output, target, neighbors):
    result_line = next(
        line for line in output.splitlines() if line.startswith("Maximum clique:")
    )
    indices = [int(token) for token in result_line.split(":", 1)[1].split()]
    assert len(indices) == target
    assert all(1 <= index <= len(neighbors) for index in indices)
    return [neighbors[index - 1] for index in indices]


def audit_one(
    new_value, target, old_values, temp_dir, expected_transitions, strict
):
    neighbors, edges, matrix_market = neighbor_graph(new_value, old_values)
    graph_path = Path(temp_dir) / f"neighbors_{new_value}.mtx"
    graph_path.write_text(matrix_market, encoding="ascii")
    command = [
        PMC, "-f", str(graph_path), "-a", "0", "-k", str(target),
        "-t", "1", "-o", "kcore", "-v",
    ]
    started = monotonic()
    completed = run(command, stdout=PIPE, stderr=PIPE, text=True, check=True)
    seconds = monotonic() - started
    output = completed.stdout + completed.stderr

    no_result = f"Clique of size {target} does not exist." in output
    found_result = f"[pmc: upper bound reached]  omega = {target}" in output
    assert no_result != found_result, (new_value, target, output)
    exists = found_result
    expected_exists = new_value in expected_transitions
    if strict:
        assert exists == expected_exists, (new_value, target, output)

    witness = []
    if exists:
        witness = parse_witness(output, target, neighbors) + [new_value]
        witness.sort()
        check_witness(witness, target + 1, new_value)

    graph_hash = sha256(matrix_market.encode("ascii")).hexdigest()
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
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--max-n", type=int, default=2000)
    parser.add_argument("--start-n", type=int, default=BASE_N + 1)
    parser.add_argument("--transitions", required=True)
    parser.add_argument("--discover", action="store_true")
    args = parser.parse_args()
    assert args.jobs >= 1
    assert args.max_n > BASE_N
    assert BASE_N < args.start_n <= args.max_n
    assert Path(PMC).is_file()
    expected_transitions = tuple(
        int(value) for value in args.transitions.split(",") if value
    )
    assert expected_transitions == tuple(sorted(set(expected_transitions)))
    assert all(BASE_N < value <= args.max_n for value in expected_transitions)

    all_values = [
        value for value in range(1, args.max_n + 1)
        if is_squarefree_trial(2 * value)
    ]
    assert all(value in all_values for value in expected_transitions)
    tasks = []
    for new_value in all_values:
        if new_value < args.start_n:
            continue
        old_values = [value for value in all_values if value < new_value]
        target = BASE_OPTIMUM + sum(
            point < new_value for point in expected_transitions
        )
        tasks.append((new_value, target, old_values))

    results = []
    with TemporaryDirectory(prefix="erdos1109_pmc_") as temp_dir:
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            futures = [
                executor.submit(
                    audit_one,
                    new_value,
                    target,
                    old_values,
                    temp_dir,
                    expected_transitions,
                    not args.discover,
                )
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

    expected_count = sum(value >= args.start_n for value in all_values)
    assert len(results) == expected_count
    positives = sorted(result["new_value"] for result in results if result["exists"])
    if args.discover:
        print("discovered_positives=" + ",".join(map(str, positives)))
    else:
        expected_in_range = [
            value for value in expected_transitions if value >= args.start_n
        ]
        assert positives == expected_in_range
    print("audit_sha256=" + sha256("".join(records).encode("ascii")).hexdigest())
    print(
        "CONCLUSION external exact PMC certifies every eligible last-vertex "
        f"decision for {args.start_n}<=N<={args.max_n}"
    )


if __name__ == "__main__":
    main()
