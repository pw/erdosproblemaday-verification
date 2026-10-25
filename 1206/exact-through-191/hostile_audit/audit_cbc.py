#!/usr/bin/env python3
"""Independent CBC integer-program audit of all lower endpoints for #1206."""

from __future__ import annotations

import hashlib
import itertools
import pathlib
import re
import subprocess
import time
from collections import defaultdict


CBC = "/home/exedev/.local/bin/cbc"
ENDPOINTS = (
    (132, 21), (134, 22), (138, 23), (144, 24),
    (156, 25), (161, 26), (165, 27), (166, 28),
    (172, 29), (174, 30), (180, 31), (186, 32),
)


def collision_edges(n: int) -> tuple[tuple[int, ...], ...]:
    sums: dict[int, list[tuple[int, int]]] = defaultdict(list)
    # Reverse order and hashed grouping differ from the frozen C++ builder.
    for right in range(n, 0, -1):
        for left in range(right, 0, -1):
            sums[left**3 + right**3].append((left, right))
    edges = {
        tuple(sorted(set(one) | set(two)))
        for representations in sums.values()
        for one, two in itertools.combinations(representations, 2)
    }
    return tuple(sorted(edges))


def canonical_digest(edges) -> str:
    raw = "\n".join(",".join(map(str, e)) for e in edges).encode()
    return hashlib.sha256(raw).hexdigest()


def write_lp(path: pathlib.Path, n: int, edges) -> None:
    with path.open("w", encoding="ascii", newline="\n") as out:
        out.write("Minimize\n")
        for start in range(1, n + 1, 12):
            out.write(" obj: " if start == 1 else " + ")
            out.write(" + ".join(f"x{v}" for v in range(start, min(n + 1, start + 12))))
            out.write("\n")
        out.write("Subject To\n")
        for index, edge in enumerate(edges):
            out.write(f" edge{index}: ")
            out.write(" + ".join(f"x{v}" for v in edge))
            out.write(" >= 1\n")
        out.write("Binary\n")
        for start in range(1, n + 1, 20):
            out.write(" ")
            out.write(" ".join(f"x{v}" for v in range(start, min(n + 1, start + 20))))
            out.write("\n")
        out.write("End\n")


def direct_sidon(n: int, cover: set[int]) -> int:
    kept = [v for v in range(1, n + 1) if v not in cover]
    sums = set()
    for i, a in enumerate(kept):
        for b in kept[i:]:
            value = a**3 + b**3
            assert value not in sums
            sums.add(value)
    assert len(sums) == len(kept) * (len(kept) + 1) // 2
    return len(kept)


def main() -> None:
    root = pathlib.Path("/tmp/erdos1206_exact_132_191_hostile/cbc")
    root.mkdir(parents=True, exist_ok=True)
    total_start = time.monotonic()
    for n, expected_tau in ENDPOINTS:
        edges = collision_edges(n)
        lp = root / f"n{n}.lp"
        solution = root / f"n{n}.sol"
        log = root / f"n{n}.log"
        write_lp(lp, n, edges)
        start = time.monotonic()
        run = subprocess.run(
            [CBC, str(lp), "-randomCbcSeed=1206", "-threads=1",
             "-solve", f"-solution={solution}"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            check=True,
        )
        elapsed = time.monotonic() - start
        log.write_text(run.stdout, encoding="utf-8")
        assert "Result - Optimal solution found" in run.stdout
        match = re.search(r"Objective value:\s+([0-9.]+)", run.stdout)
        assert match
        objective = float(match.group(1))
        assert objective == expected_tau, (n, objective, expected_tau)

        cover: set[int] = set()
        first, *lines = solution.read_text().splitlines()
        assert first.startswith("Optimal - objective value ")
        assert float(first.rsplit(maxsplit=1)[1]) == expected_tau
        for line in lines:
            fields = line.split()
            if len(fields) >= 3 and fields[1].startswith("x"):
                value = float(fields[2])
                assert value in (0.0, 1.0)
                if value == 1.0:
                    cover.add(int(fields[1][1:]))
        assert len(cover) == expected_tau
        assert all(cover.intersection(edge) for edge in edges)
        retained = direct_sidon(n, cover)
        print(
            f"N={n}: OPTIMAL tau={expected_tau}, g3={retained}, "
            f"edges={len(edges)}, edge_sha256={canonical_digest(edges)}, "
            f"seconds={elapsed:.6f}",
            flush=True,
        )
    print(
        f"CBC INDEPENDENT INTEGER OPTIMA PASS at all 12 lower endpoints; "
        f"seconds={time.monotonic()-total_start:.6f}",
        flush=True,
    )


if __name__ == "__main__":
    main()
