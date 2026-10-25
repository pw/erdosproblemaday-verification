#!/usr/bin/env python3
"""Differential fuzz test of PMC's Matrix Market k-clique mode."""

from pathlib import Path
from random import Random
import re
from subprocess import PIPE, run
from tempfile import TemporaryDirectory


HERE = Path(__file__).resolve().parent
PMC = HERE / "pmc_1109_audit"
SEED = 1109
CASES = 200


def brute_maximum(adjacency: list[int]) -> int:
    size = len(adjacency)
    best = 0
    for subset in range(1 << size):
        count = subset.bit_count()
        if count <= best:
            continue
        clique = True
        remaining = subset
        while remaining:
            vertex_bit = remaining & -remaining
            vertex = vertex_bit.bit_length() - 1
            remaining ^= vertex_bit
            if remaining & ~adjacency[vertex]:
                clique = False
                break
        if clique:
            best = count
    return best


def matrix_market(adjacency: list[int]) -> str:
    edges = []
    for right in range(len(adjacency)):
        for left in range(right):
            if adjacency[right] & (1 << left):
                edges.append((right + 1, left + 1))
    lines = [
        "%%MatrixMarket matrix coordinate pattern symmetric\n",
        f"{len(adjacency)} {len(adjacency)} {len(edges)}\n",
    ]
    lines.extend(f"{right} {left}\n" for right, left in edges)
    return "".join(lines)


def check_solver(graph: Path, adjacency: list[int], target: int, expected: bool) -> None:
    completed = run(
        [
            str(PMC), "-f", str(graph), "-a", "0", "-k", str(target),
            "-t", "1", "-o", "kcore", "-v",
        ],
        stdout=PIPE,
        stderr=PIPE,
        text=True,
        check=True,
    )
    output = completed.stdout + completed.stderr
    assert "Time limit expired" not in output
    explicit_negative = f"Clique of size {target} does not exist." in output
    core_bound_negative = "Heuristic found optimal solution." in output
    negative = explicit_negative or core_bound_negative
    reached = [
        int(value) for value in re.findall(
            r"\[pmc: upper bound reached\]  omega = (\d+)", output
        )
    ]
    positive = bool(reached)
    assert all(value >= target for value in reached)
    assert negative != positive, (target, expected, output)
    assert positive == expected, (target, expected, output)

    if positive:
        candidates = [
            line for line in output.splitlines()
            if line.startswith("Maximum clique:")
            and len(line.split()) >= target + 2
        ]
        assert candidates
        witness = [int(token) - 1 for token in candidates[-1].split(":", 1)[1].split()]
        assert len(witness) == len(set(witness)) >= target
        assert all(0 <= vertex < len(adjacency) for vertex in witness)
        for left_index, left in enumerate(witness):
            for right in witness[left_index + 1:]:
                assert adjacency[left] & (1 << right)


def main() -> None:
    random = Random(SEED)
    decisions = 0
    with TemporaryDirectory(prefix="pmc_solver_fuzz_") as temp_dir:
        for case_index in range(CASES):
            size = random.randrange(2, 15)
            threshold = random.random()
            adjacency = [0] * size
            for left in range(size):
                for right in range(left + 1, size):
                    if random.random() < threshold:
                        adjacency[left] |= 1 << right
                        adjacency[right] |= 1 << left

            exact = brute_maximum(adjacency)
            targets = {
                2,
                max(2, exact),
                min(size, exact + 1),
                random.randrange(2, size + 1),
            }
            graph = Path(temp_dir) / f"graph_{case_index}.mtx"
            graph.write_text(matrix_market(adjacency), encoding="ascii")
            for target in sorted(targets):
                check_solver(graph, adjacency, target, target <= exact)
                decisions += 1

    print(f"cases={CASES} decisions={decisions} seed={SEED} max_vertices=14")
    print("CONCLUSION PMC Matrix Market k-clique mode agrees with brute force")


if __name__ == "__main__":
    main()
