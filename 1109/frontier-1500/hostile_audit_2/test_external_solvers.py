#!/usr/bin/env python3
"""Deterministic small-graph checks of the exact Cliquer and PMC commands."""

from hashlib import sha256
from pathlib import Path
from random import Random
from subprocess import PIPE, run
from tempfile import TemporaryDirectory


CLIQUER = "/usr/bin/cliquer"
PMC = "/home/exedev/erdos_scratch/erdos1109_exact_frontier_2026-08-11/pmc_1109_audit"


def maximum_clique(adjacency):
    best = []

    def search(pool, chosen):
        nonlocal best
        if len(chosen) + pool.bit_count() <= len(best):
            return
        if not pool:
            best = chosen[:]
            return
        bit = pool & -pool
        vertex = bit.bit_length() - 1
        search((pool ^ bit) & adjacency[vertex], chosen + [vertex])
        search(pool ^ bit, chosen)

    search((1 << len(adjacency)) - 1, [])
    return tuple(best)


def degeneracy(adjacency):
    remaining = set(range(len(adjacency)))
    result = 0
    while remaining:
        vertex = min(
            remaining,
            key=lambda item: sum((adjacency[item] >> other) & 1 for other in remaining),
        )
        degree = sum((adjacency[vertex] >> other) & 1 for other in remaining)
        result = max(result, degree)
        remaining.remove(vertex)
    return result


def edge_list(adjacency):
    return [
        (left + 1, right + 1)
        for left in range(len(adjacency))
        for right in range(left + 1, len(adjacency))
        if adjacency[left] & (1 << right)
    ]


def validate(indices, target, adjacency):
    assert len(indices) == len(set(indices)) == target
    assert all(0 <= vertex < len(adjacency) for vertex in indices)
    assert all(
        adjacency[left] & (1 << right)
        for position, left in enumerate(indices)
        for right in indices[position + 1:]
    )


def check_case(case_number, adjacency, temp_dir):
    edges = edge_list(adjacency)
    n = len(adjacency)
    optimum_witness = maximum_clique(adjacency)
    optimum = len(optimum_witness)
    validate(optimum_witness, optimum, adjacency)
    core_upper = degeneracy(adjacency) + 1
    targets = [optimum]
    if core_upper > optimum:
        targets.append(optimum + 1)

    dimacs = f"p edge {n} {len(edges)}\n" + "".join(
        f"e {left} {right}\n" for left, right in edges
    )
    matrix = (
        "%%MatrixMarket matrix coordinate pattern symmetric\n"
        f"{n} {n} {len(edges)}\n"
        + "".join(f"{right} {left}\n" for left, right in edges)
    )
    dimacs_path = Path(temp_dir) / f"case_{case_number}.dimacs"
    matrix_path = Path(temp_dir) / f"case_{case_number}.mtx"
    dimacs_path.write_text(dimacs, encoding="ascii")
    matrix_path.write_text(matrix, encoding="ascii")

    records = []
    for target in targets:
        expected = optimum >= target
        cliquer = run(
            [CLIQUER, "-u", "-m", str(target), "-M", str(target),
             "-r", "reverse", "-q", str(dimacs_path)],
            stdout=PIPE, stderr=PIPE, text=True, check=True, timeout=10,
        )
        cliquer_output = cliquer.stdout + cliquer.stderr
        cliquer_exists = "No such clique found." not in cliquer_output
        assert cliquer_exists == expected
        if cliquer_exists:
            result_line = next(line for line in cliquer_output.splitlines() if line.startswith("size="))
            prefix, indices_text = result_line.split(":", 1)
            assert prefix.startswith(f"size={target}, weight={target}")
            validate(tuple(int(token) - 1 for token in indices_text.split()), target, adjacency)

        pmc = run(
            [PMC, "-f", str(matrix_path), "-a", "0", "-k", str(target),
             "-t", "1", "-o", "kcore", "-v"],
            stdout=PIPE, stderr=PIPE, text=True, check=True, timeout=10,
        )
        pmc_output = pmc.stdout + pmc.stderr
        pmc_no = f"Clique of size {target} does not exist." in pmc_output
        pmc_yes = f"[pmc: upper bound reached]  omega = {target}" in pmc_output
        assert pmc_no != pmc_yes
        assert pmc_yes == expected
        if pmc_yes:
            result_line = next(line for line in pmc_output.splitlines() if line.startswith("Maximum clique:"))
            validate(
                tuple(int(token) - 1 for token in result_line.split(":", 1)[1].split()),
                target,
                adjacency,
            )
        records.append(f"{case_number}:{n}:{len(edges)}:{optimum}:{core_upper}:{target}:{int(expected)}\n")
    return records


def main():
    random = Random(0x1109A392165)
    graphs = []
    for trial in range(64):
        n = 10 + trial % 7
        threshold = 48 + (trial * 29) % 160
        adjacency = [0] * n
        for left in range(n):
            for right in range(left + 1, n):
                if random.randrange(256) < threshold:
                    adjacency[left] |= 1 << right
                    adjacency[right] |= 1 << left
        adjacency[0] |= 1 << 1
        adjacency[1] |= 1
        graphs.append(adjacency)

    records = []
    with TemporaryDirectory(prefix="audit1109_solver_smoke_") as temp_dir:
        for case_number, adjacency in enumerate(graphs):
            records.extend(check_case(case_number, adjacency, temp_dir))
    result_digest = sha256("".join(records).encode("ascii")).hexdigest()
    print(f"PASS external exact solver smoke cases={len(graphs)} decisions={len(records)}")
    print(f"solver_smoke_sha256={result_digest}")


if __name__ == "__main__":
    main()
