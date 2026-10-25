#!/usr/bin/env python3
"""Emit independent CBC feasibility models for claimed flat frontier steps.

Variables select a corner-free set directly.  At a flat step k with prior
optimum q, a counterexample must select the new vertex and at least q+1 total
vertices.  Thus infeasibility is the desired upper-bound result.
"""

from __future__ import annotations

import argparse
from pathlib import Path


FLATS = {
    5001: 3335,
    5004: 3337,
    5006: 3338,
    5009: 3340,
    5011: 3341,
    5013: 3342,
    5016: 3344,
    5020: 3347,
}


def enumerate_smooth(count: int) -> list[int]:
    candidates = sorted(
        pow(2, a) * pow(3, b) for a in range(256) for b in range(192)
    )
    answer = candidates[:count]
    assert len(set(answer)) == count
    assert pow(2, 256) > answer[-1] and pow(3, 192) > answer[-1]
    return answer


def wrap_sum(variables: list[str], indent: str = "  ") -> str:
    chunks = []
    width = 18
    for start in range(0, len(variables), width):
        prefix = indent if start == 0 else indent + "+ "
        chunks.append(prefix + " + ".join(variables[start : start + width]))
    return "\n".join(chunks)


def write_model(path: Path, k: int, prior: int, values: list[int]) -> None:
    position = {value: i for i, value in enumerate(values[:k])}
    edges = []
    for i, value in enumerate(values[:k]):
        if 2 * value in position and 3 * value in position:
            edges.append((i, position[2 * value], position[3 * value]))
    variables = [f"x{i}" for i in range(k)]
    with path.open("w", encoding="ascii") as out:
        out.write("\\ Independent direct-set feasibility model\n")
        out.write("Maximize\n")
        out.write(" objective: 0 x0\n")
        out.write("Subject To\n")
        for number, (anchor, east, north) in enumerate(edges):
            out.write(f" corner_{number}: x{anchor} + x{east} + x{north} <= 2\n")
        out.write(f" force_new: x{k - 1} = 1\n")
        out.write(" target:\n")
        out.write(wrap_sum(variables, indent="  "))
        out.write(f" >= {prior + 1}\n")
        out.write("Binary\n")
        for start in range(0, len(variables), 24):
            out.write(" " + " ".join(variables[start : start + 24]) + "\n")
        out.write("End\n")


def exponent_pair(value: int) -> tuple[int, int]:
    a = b = 0
    while value % 2 == 0:
        value //= 2
        a += 1
    while value % 3 == 0:
        value //= 3
        b += 1
    assert value == 1
    return a, b


def write_baseline(out_dir: Path, values: list[int]) -> None:
    k = 5000
    position = {value: i for i, value in enumerate(values[:k])}
    edges = [
        (i, position[2 * value], position[3 * value])
        for i, value in enumerate(values[:k])
        if 2 * value in position and 3 * value in position
    ]
    variables = [f"x{i}" for i in range(k)]
    model_path = out_dir / "baseline_k5000_maximum.lp"
    with model_path.open("w", encoding="ascii") as out:
        out.write("\\ Independent direct-set baseline maximization model\n")
        out.write("Maximize\n")
        out.write(" objective:\n")
        out.write(wrap_sum(variables, indent="  "))
        out.write("\nSubject To\n")
        for number, (anchor, east, north) in enumerate(edges):
            out.write(f" corner_{number}: x{anchor} + x{east} + x{north} <= 2\n")
        out.write("Binary\n")
        for start in range(0, len(variables), 24):
            out.write(" " + " ".join(variables[start : start + 24]) + "\n")
        out.write("End\n")

    selected = set()
    for i, value in enumerate(values[:k]):
        a, b = exponent_pair(value)
        if (a + 2 * b) % 3 != 2:
            selected.add(i)
    by_pair = {exponent_pair(value): i for i, value in enumerate(values[:k])}
    selected.difference_update({by_pair[(121, 1)], by_pair[(123, 0)]})
    selected.update({by_pair[(121, 2)], by_pair[(122, 0)], by_pair[(123, 1)]})
    assert len(selected) == 3335
    start_path = out_dir / "baseline_k5000.mipstart"
    with start_path.open("w", encoding="ascii") as out:
        out.write("independent coloring exchange, objective 3335\n")
        for i, variable in enumerate(variables):
            out.write(f"{i} {variable} {int(i in selected)}\n")
    print(model_path)
    print(start_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--only", type=int, action="append")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    selected = sorted(args.only or FLATS)
    assert set(selected) <= set(FLATS)
    values = enumerate_smooth(max(selected))
    if not args.only:
        write_baseline(args.out, values)
    for k in selected:
        path = args.out / f"flat_k{k}_counterexample.lp"
        write_model(path, k, FLATS[k], values)
        print(path)


if __name__ == "__main__":
    main()
