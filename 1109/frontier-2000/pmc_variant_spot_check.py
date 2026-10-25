#!/usr/bin/env python3
"""Spot-check #1109 boundaries through PMC's separate exact algorithm 1."""

from pathlib import Path
from subprocess import PIPE, run
from tempfile import TemporaryDirectory
from time import monotonic

from cold_check_extension import TRANSITIONS, graph_for, squarefree


PMC = Path(__file__).resolve().with_name("pmc_1109_audit")
CASES = (
    (1501, 44, False),
    (1509, 44, True),
    (1533, 45, False),
    (1535, 45, True),
    (1997, 53, False),
    (1999, 53, True),
)


def main():
    all_values = [value for value in range(1, 2001) if squarefree(2 * value)]
    with TemporaryDirectory(prefix="erdos1109_variant_") as temp_dir:
        for new_value, target, expected in CASES:
            neighbors, edges, matrix = graph_for(new_value, all_values)
            graph = Path(temp_dir) / f"neighbors_{new_value}.mtx"
            graph.write_text(matrix, encoding="ascii")
            command = [
                str(PMC), "-f", str(graph), "-a", "1", "-k", str(target),
                "-t", "1", "-o", "deg", "-v",
            ]
            started = monotonic()
            completed = run(command, stdout=PIPE, stderr=PIPE, text=True, check=True)
            elapsed = monotonic() - started
            output = completed.stdout + completed.stderr
            assert "Time limit expired" not in output
            negative = f"Clique of size {target} does not exist." in output
            positive = f"[pmc: upper bound reached]  omega = {target}" in output
            assert negative != positive
            exists = positive
            assert exists == expected, (new_value, output)

            witness = []
            if exists:
                line = next(
                    line for line in output.splitlines()
                    if line.startswith("Maximum clique:") and len(line.split()) == target + 2
                )
                indices = [int(token) for token in line.split(":", 1)[1].split()]
                witness = sorted([neighbors[index - 1] for index in indices] + [new_value])
                assert len(witness) == target + 1
                assert len(set(witness)) == len(witness)
                assert all(
                    squarefree(left + right)
                    for left_index, left in enumerate(witness)
                    for right in witness[left_index:]
                )

            print(
                f"n={new_value} target={target} neighbors={len(neighbors)} "
                f"edges={len(edges)} exists={exists} seconds={elapsed:.3f} "
                f"witness={{{','.join(map(str, witness))}}}",
                flush=True,
            )

    expected_positives = (TRANSITIONS[0], TRANSITIONS[1], TRANSITIONS[-1])
    assert tuple(value for value, _, exists in CASES if exists) == expected_positives
    print("CONCLUSION PMC exact algorithm 1 agrees on six boundary decisions")


if __name__ == "__main__":
    main()
