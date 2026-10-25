#!/usr/bin/env python3
"""Solver-free consistency checks for the Problem 168 frontier artifacts.

This verifies all constructive witnesses and the logical propagation between
solver rows.  For upper bounds at flat rows it checks, but cannot replace,
the retained SCIP optimality transcripts.
"""

from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import re
from pathlib import Path


EXPECTED_BFILE_SHA256 = (
    "bba41cd187052c20e638c539893f16f73d23956f9900caa882e06778256b15ea"
)


def smooth_prefix(count: int) -> tuple[list[int], list[tuple[int, int]]]:
    heap = [(1, 0, 0)]
    seen = {1}
    values: list[int] = []
    points: list[tuple[int, int]] = []
    while len(values) < count:
        value, a, b = heapq.heappop(heap)
        values.append(value)
        points.append((a, b))
        for child, aa, bb in ((2 * value, a + 1, b), (3 * value, a, b + 1)):
            if child not in seen:
                seen.add(child)
                heapq.heappush(heap, (child, aa, bb))
    return values, points


def edges_for(points: list[tuple[int, int]]) -> list[tuple[int, int, int]]:
    index = {point: i for i, point in enumerate(points)}
    edges: list[tuple[int, int, int]] = []
    for i, (a, b) in enumerate(points):
        if (a + 1, b) in index and (a, b + 1) in index:
            edges.append((i, index[(a + 1, b)], index[(a, b + 1)]))
    return edges


def read_witness(path: Path, points: list[tuple[int, int]]) -> set[int]:
    index = {point: i for i, point in enumerate(points)}
    chosen: set[int] = set()
    lines = path.read_text(encoding="ascii").splitlines()
    for line in lines:
        fields = line.split()
        if len(fields) != 2:
            raise AssertionError(f"malformed witness line in {path}: {line!r}")
        point = tuple(map(int, fields))
        if point not in index:
            raise AssertionError(f"point {point} is outside prefix for {path}")
        chosen.add(index[point])
    if len(chosen) != len(lines):
        raise AssertionError(f"duplicate witness point in {path}")
    return chosen


def transcript_bound(text: str, label: str) -> float:
    match = re.search(rf"^{re.escape(label)}\s*:\s*([+0-9.eE-]+)", text, re.MULTILINE)
    if not match:
        raise AssertionError(f"missing {label!r} in SCIP transcript")
    return float(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bfile", type=Path, required=True)
    parser.add_argument("--artifacts", type=Path, required=True)
    args = parser.parse_args()

    bfile_hash = hashlib.sha256(args.bfile.read_bytes()).hexdigest()
    if bfile_hash != EXPECTED_BFILE_SHA256:
        raise AssertionError(f"unexpected b-file SHA-256 {bfile_hash}")

    data = json.loads((args.artifacts / "results.json").read_text(encoding="ascii"))
    rows = data["rows"]
    if not rows or rows[0]["k"] != 5000:
        raise AssertionError("frontier does not start at k=5000")
    through = int(rows[-1]["k"])
    if [row["k"] for row in rows] != list(range(5000, through + 1)):
        raise AssertionError("frontier rows are not consecutive")

    values, all_points = smooth_prefix(through)
    solver_rows: list[int] = []
    previous_f: int | None = None
    for row in rows:
        k = int(row["k"])
        f = int(row["f"])
        points = all_points[:k]
        edges = edges_for(points)
        if row["smooth_value"] != str(values[k - 1]):
            raise AssertionError(f"k={k}: wrong smooth value")
        if row["exponents"] != list(points[-1]):
            raise AssertionError(f"k={k}: wrong exponent pair")
        if int(row["corners"]) != len(edges):
            raise AssertionError(f"k={k}: wrong corner count")

        chosen = read_witness(args.artifacts / row["witness"], points)
        if len(chosen) != f:
            raise AssertionError(f"k={k}: witness size {len(chosen)} != f={f}")
        for edge in edges:
            if all(i in chosen for i in edge):
                raise AssertionError(f"k={k}: witness contains corner {edge}")

        if previous_f is not None:
            increment = f - previous_f
            if increment not in (0, 1) or row["increment"] != increment:
                raise AssertionError(f"k={k}: invalid increment")
        else:
            increment = None
            if row["increment"] is not None:
                raise AssertionError("baseline increment must be null")

        solver = row["solver"]
        if solver is None:
            if increment != 1:
                raise AssertionError(f"k={k}: non-solver row is not a +1 step")
            if row["method"] != "witness plus f(k)<=f(k-1)+1":
                raise AssertionError(f"k={k}: wrong propagation method")
        else:
            solver_rows.append(k)
            if solver["status"] != "optimal" or float(solver["gap"]) != 0.0:
                raise AssertionError(f"k={k}: result does not record zero-gap optimum")
            cover_size = k - f
            if int(solver["objective"]) != cover_size:
                raise AssertionError(f"k={k}: wrong cover objective")
            transcript = (args.artifacts / solver["log"]).read_text(encoding="ascii")
            if "problem is solved [optimal solution found]" not in transcript:
                raise AssertionError(f"k={k}: transcript lacks optimal status")
            primal = transcript_bound(transcript, "Primal Bound")
            dual = transcript_bound(transcript, "Dual Bound")
            if round(primal) != cover_size or round(dual) != cover_size:
                raise AssertionError(f"k={k}: transcript bounds disagree with objective")
        previous_f = f

    if solver_rows != list(map(int, data["solved_prefixes"])):
        raise AssertionError("solved-prefix index is inconsistent")
    expected_solver_rows = [rows[0]["k"]] + [
        row["k"] for row in rows[1:] if row["increment"] == 0
    ]
    if solver_rows != expected_solver_rows:
        raise AssertionError("a flat step lacks a solver certificate")

    print(
        f"PASS: k=5000..{through}; {len(rows)} witnesses; "
        f"{sum(int(row['corners']) for row in rows)} corner checks; "
        f"SCIP transcripts at {solver_rows}; final f={previous_f}"
    )


if __name__ == "__main__":
    main()
