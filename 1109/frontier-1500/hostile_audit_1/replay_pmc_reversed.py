#!/usr/bin/env python3
"""One-core independent PMC replay using reversed graph vertex order."""

from __future__ import annotations

import argparse
import subprocess
from math import isqrt
from pathlib import Path
from tempfile import TemporaryDirectory


def squarefree(n: int) -> bool:
    return n > 0 and all(n % (d * d) for d in range(2, isqrt(n) + 1))


def check_witness(values: list[int], maximum: int, expected: int) -> None:
    assert len(values) == len(set(values)) == expected
    assert max(values) == maximum
    assert all(
        squarefree(left + right)
        for i, left in enumerate(values)
        for right in values[i:]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pmc", type=Path)
    args = parser.parse_args()
    pmc = args.pmc.resolve()
    assert pmc.is_file()

    eligible = [n for n in range(1, 1501) if squarefree(2 * n)]
    current = 39
    transitions = []
    decisions = 0
    with TemporaryDirectory(prefix="cold_1109_pmc_") as tmp:
        tmp = Path(tmp)
        for n in eligible:
            if n <= 1103:
                continue
            # Reverse the author's vertex order to change PMC's concrete search tree.
            neighbors = [v for v in reversed(eligible) if v < n and squarefree(v + n)]
            edges = []
            for i, left in enumerate(neighbors):
                for j in range(i + 1, len(neighbors)):
                    if squarefree(left + neighbors[j]):
                        edges.append((j + 1, i + 1))
            graph = tmp / f"n{n}.mtx"
            graph.write_text(
                "%%MatrixMarket matrix coordinate pattern symmetric\n"
                f"{len(neighbors)} {len(neighbors)} {len(edges)}\n"
                + "".join(f"{row} {col}\n" for row, col in edges),
                encoding="ascii",
            )
            command = [
                str(pmc), "-f", str(graph), "-a", "0", "-k", str(current),
                "-t", "1", "-o", "kcore", "-v",
            ]
            run = subprocess.run(command, text=True, capture_output=True, check=True)
            output = run.stdout + run.stderr
            no = f"Clique of size {current} does not exist." in output
            yes = f"[pmc: upper bound reached]  omega = {current}" in output
            assert no != yes, (n, current, output)
            if yes:
                lines = [line for line in output.splitlines() if line.startswith("Maximum clique:")]
                assert lines
                indices = [int(token) for token in lines[-1].split(":", 1)[1].split()]
                witness = sorted([neighbors[index - 1] for index in indices] + [n])
                check_witness(witness, n, current + 1)
                transitions.append(n)
                current += 1
            decisions += 1
            print(f"n={n} target={current - int(yes)} exists={int(yes)}", flush=True)

    assert decisions == 163 and current == 44
    print(f"decisions={decisions}")
    print("transitions=" + ",".join(map(str, transitions)))
    print("PASS rebuilt PMC independently reproduces all decisions in reversed vertex order")


if __name__ == "__main__":
    main()
