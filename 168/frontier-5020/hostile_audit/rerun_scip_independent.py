#!/usr/bin/env python3
"""Independent selected-set SCIP rerun for frozen Problem 168 rows.

This is intentionally different from the bundle's minimum-cover generator:
it enumerates a bounded exponent rectangle, builds triples by multiplication,
creates variables in reverse order, maximizes selected vertices, and changes
SCIP's randomization settings.  SCIP still uses floating MIP arithmetic.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import pyscipopt
from pyscipopt import Model, quicksum


def smooth_prefix(count: int) -> list[tuple[int, int, int]]:
    candidates = sorted(
        (pow(2, a) * pow(3, b), a, b)
        for a in range(256)
        for b in range(192)
    )
    result = candidates[:count]
    assert pow(2, 256) > result[-1][0] and pow(3, 192) > result[-1][0]
    return result


def read_start(path: Path, points: list[tuple[int, int, int]]) -> set[int]:
    index = {(a, b): i for i, (_, a, b) in enumerate(points)}
    chosen = set()
    lines = path.read_text(encoding="ascii").splitlines()
    for line in lines:
        pair = tuple(map(int, line.split()))
        assert pair in index and index[pair] not in chosen
        chosen.add(index[pair])
    assert len(chosen) == len(lines)
    return chosen


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--witness", type=Path, required=True)
    parser.add_argument("--seconds", type=float, default=600)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()

    points = smooth_prefix(args.k)
    values = [value for value, _, _ in points]
    position = {value: i for i, value in enumerate(values)}
    edges = [
        (i, position[2 * value], position[3 * value])
        for i, value in enumerate(values)
        if 2 * value in position and 3 * value in position
    ]
    chosen = read_start(args.witness, points)
    assert all(not set(edge) <= chosen for edge in edges)

    model = Model(f"audit_direct_independent_k{args.k}")
    model.setIntParam("parallel/maxnthreads", 1)
    model.setIntParam("randomization/randomseedshift", 314159)
    model.setBoolParam("randomization/permutevars", True)
    model.setIntParam("randomization/permutationseed", 271828)
    model.setRealParam("limits/time", args.seconds)
    model.setLogfile(str(args.log))

    variables = {}
    for i in reversed(range(args.k)):
        variables[i] = model.addVar(vtype="B", name=f"selected_{i}")
    for anchor, east, north in reversed(edges):
        model.addCons(
            variables[anchor] + variables[east] + variables[north] <= 2
        )
    model.setObjective(quicksum(variables.values()), "maximize")
    start = model.createSol()
    for i in range(args.k):
        model.setSolVal(start, variables[i], int(i in chosen))
    assert model.addSol(start, free=True)

    began = time.monotonic()
    model.optimize()
    elapsed = time.monotonic() - began
    status = str(model.getStatus())
    result = {
        "k": args.k,
        "points": len(points),
        "edges": len(edges),
        "start_size": len(chosen),
        "status": status,
        "objective": model.getObjVal() if model.getNSols() else None,
        "dual_bound": model.getDualbound(),
        "gap": model.getGap(),
        "nodes": model.getNNodes(),
        "lp_iterations": model.getNLPIterations(),
        "elapsed": elapsed,
        "pyscipopt": pyscipopt.__version__,
        "scip": f"{model.getMajorVersion()}.{model.getMinorVersion()}.{model.getTechVersion()}",
        "floating_mip": True,
        "exact_mode": False,
    }
    if status == "optimal":
        extracted = {
            i for i in range(args.k) if model.getVal(variables[i]) > 0.5
        }
        assert len(extracted) == round(result["objective"])
        assert all(not set(edge) <= extracted for edge in edges)
    args.result.write_text(json.dumps(result, indent=2) + "\n", encoding="ascii")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
