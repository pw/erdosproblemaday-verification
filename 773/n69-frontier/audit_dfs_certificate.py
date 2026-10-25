#!/usr/bin/env python3
"""Audit the conditional exhaustive certificate for a(69)=32 and a(70)=33."""

from __future__ import annotations

import hashlib
import itertools
import re
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BFILE_SHA256 = "dce8e0faa57f6373f1f9fa7e33afe1b1819723cf3a3535b1e4d94ad62d056916"
SOURCE_SHA256 = "eb21d0f429881f61dd5148ab2a41da3fb6b57d1513ea2db656ae3ae69883e933"
BINARY_SHA256 = "e9d471fb6df395f0807c21efc2fffbda64403511cd92b8098bb9100eaaa5655a"
CUBES = ("00", "010", "011", "100", "101", "110", "111")
WITNESS_69 = (3, 4, 6, 12, 13, 15, 17, 19, 23, 25, 28, 34, 35, 38,
              42, 45, 48, 49, 53, 54, 56, 57, 58, 60, 61, 62, 63, 64,
              65, 66, 68, 69)
WITNESS_70 = (1, 4, 6, 7, 9, 10, 12, 13, 16, 18, 19, 22, 24, 28, 30,
              34, 36, 37, 39, 40, 43, 46, 49, 51, 52, 57, 58, 60, 64,
              65, 67, 69, 70)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_witness(witness: tuple[int, ...], limit: int) -> int:
    assert len(witness) == len(set(witness))
    assert all(1 <= value <= limit for value in witness)
    sums: dict[int, tuple[int, int]] = {}
    for position, first in enumerate(witness):
        for second in witness[position:]:
            value = first * first + second * second
            assert value not in sums, (value, sums[value], (first, second))
            sums[value] = (first, second)
    return len(sums)


def check_bfile() -> list[int]:
    path = ROOT / "oeis_A390813_b390813.txt"
    assert digest(path) == BFILE_SHA256
    rows: dict[int, int] = {}
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        index_text, value_text = line.split()
        rows[int(index_text)] = int(value_text)
    assert sorted(rows) == list(range(1, 69))
    values = [0] + [rows[index] for index in range(1, 69)]
    assert values[66:] == [31, 32, 32]
    assert all(values[index] <= values[index + 1] <= values[index] + 1
               for index in range(1, 68))
    return values


def check_collision_model() -> tuple[int, int, int]:
    representations: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for first in range(1, 70):
        for second in range(first, 70):
            representations[first * first + second * second].append((first, second))
    supports: set[frozenset[int]] = set()
    for pairs in representations.values():
        for first, second in itertools.combinations(pairs, 2):
            supports.add(frozenset((*first, *second)))
    triples = sum(len(edge) == 3 for edge in supports)
    quadruples = sum(len(edge) == 4 for edge in supports)
    assert len(supports) == 712
    assert (triples, quadruples) == (21, 691)
    assert all(len(edge) in (3, 4) for edge in supports)
    return len(supports), triples, quadruples


def check_rebuild() -> None:
    source = ROOT / "dfs_hypergraph_coloring.cpp"
    binary = ROOT / "dfs_hypergraph_coloring"
    assert digest(source) == SOURCE_SHA256
    assert digest(binary) == BINARY_SHA256
    with tempfile.TemporaryDirectory(prefix="erdos773-rebuild-") as directory:
        rebuilt = Path(directory) / "dfs_hypergraph_coloring"
        subprocess.run(
            [
                "g++", "-O3", "-DNDEBUG", "-std=c++20", "-Wall", "-Wextra",
                "-pedantic", str(source), "-o", str(rebuilt),
            ],
            check=True,
            cwd=ROOT,
        )
        assert digest(rebuilt) == BINARY_SHA256


def check_cube_logs() -> int:
    total_nodes = 0
    for cube in CUBES:
        log = (ROOT / f"dfs_color_cube_{cube}.log").read_text(encoding="ascii")
        timing = (ROOT / f"dfs_color_cube_{cube}.time").read_text(encoding="ascii")
        match = re.fullmatch(
            r"status=UNSATISFIABLE nodes=(\d+) seconds=([0-9.e+-]+) "
            r"prefix_prunes=(\d+) blocked_prunes=(\d+) color_calls=(\d+) "
            rf"color_prunes=(\d+) color_slack=32 cube={cube}\n",
            log,
        )
        assert match, (cube, log)
        nodes = int(match.group(1))
        assert nodes > 0
        total_nodes += nodes
        assert 'Command being timed: "./dfs_hypergraph_coloring"' in timing
        assert re.search(r"^\s*Exit status: 20$", timing, re.MULTILINE)

    assignments = tuple("".join(bits) for bits in itertools.product("01", repeat=3))
    for assignment in assignments:
        covering = [cube for cube in CUBES if assignment.startswith(cube)]
        assert len(covering) == 1, (assignment, covering)
    for first, second in itertools.combinations(CUBES, 2):
        assert not first.startswith(second) and not second.startswith(first)
    return total_nodes


def main() -> None:
    values = check_bfile()
    supports, triples, quadruples = check_collision_model()
    check_rebuild()
    total_nodes = check_cube_logs()
    sums_69 = check_witness(WITNESS_69, 69)
    sums_70 = check_witness(WITNESS_70, 70)

    print(f"PASS bfile_sha256={BFILE_SHA256} rows=68 a68={values[68]}")
    print(f"PASS source_sha256={SOURCE_SHA256}")
    print(f"PASS binary_sha256={BINARY_SHA256} deterministic_rebuild")
    print(f"PASS supports={supports} triples={triples} quadruples={quadruples}")
    print(f"PASS cubes={','.join(CUBES)} exhaustive_disjoint total_nodes={total_nodes}")
    print(f"PASS witness_N69_size={len(WITNESS_69)} sums={sums_69}")
    print(f"PASS witness_N70_size={len(WITNESS_70)} sums={sums_70}")
    print("CERTIFIED conditional_on_frozen_A390813_prefix a69=32 a70=33")


if __name__ == "__main__":
    main()
