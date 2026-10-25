#!/usr/bin/env python3
"""Certify an exact A057561 frontier with one-worker SCIP solves.

The first k 3-smooth numbers are represented by exponent pairs (a,b), for
2**a * 3**b.  A forbidden triple is the lattice corner

    (a,b), (a+1,b), (a,b+1).

The complement of a corner-free set is a vertex cover of these 3-edges.  We
solve the minimum-cover ILP at k=5000 and thereafter only when a constructive
lower bound is flat.  At an increasing step exactness follows from
f(k) <= f(k-1)+1.

This script needs PySCIPOpt.  It intentionally restricts SCIP to one thread.
"""

from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import platform
import time
from pathlib import Path

import pyscipopt
from pyscipopt import Model, quicksum


HERE = Path(__file__).resolve().parent
DEFAULT_BFILE = HERE / "b004059.txt"


Point = tuple[int, int]
Edge = tuple[int, int, int]


def smooth_prefix(count: int) -> tuple[list[int], list[Point]]:
    """Return the first count 3-smooth values and their exponent pairs."""
    heap: list[tuple[int, int, int]] = [(1, 0, 0)]
    seen = {1}
    values: list[int] = []
    points: list[Point] = []
    while len(values) < count:
        value, a, b = heapq.heappop(heap)
        values.append(value)
        points.append((a, b))
        for child, child_a, child_b in (
            (2 * value, a + 1, b),
            (3 * value, a, b + 1),
        ):
            if child not in seen:
                seen.add(child)
                heapq.heappush(heap, (child, child_a, child_b))
    return values, points


def edges_for(points: list[Point]) -> list[Edge]:
    index = {point: i for i, point in enumerate(points)}
    edges: list[Edge] = []
    for i, (a, b) in enumerate(points):
        east = index.get((a + 1, b))
        north = index.get((a, b + 1))
        if east is not None and north is not None:
            edges.append((i, east, north))
    return edges


def read_bfile(path: Path) -> tuple[list[int], str]:
    raw = path.read_bytes()
    increments: list[int] = []
    for line in raw.decode("ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        n, k = map(int, line.split())
        if n != len(increments) + 1:
            raise ValueError(f"nonconsecutive b-file row {n}")
        increments.append(k)
    if increments != sorted(set(increments)):
        raise ValueError("b-file second column is not strictly increasing")
    return increments, hashlib.sha256(raw).hexdigest()


def verify_independent(vertex_count: int, edges: list[Edge], chosen: set[int]) -> None:
    if not all(0 <= i < vertex_count for i in chosen):
        raise AssertionError("invalid independent-set vertex indices")
    for edge in edges:
        if all(i in chosen for i in edge):
            raise AssertionError(f"witness contains corner {edge}")


def verify_cover(size: int, edges: list[Edge], cover: set[int]) -> None:
    if not all(0 <= i < size for i in cover):
        raise AssertionError("invalid cover vertex indices")
    for edge in edges:
        if not any(i in cover for i in edge):
            raise AssertionError(f"cover misses corner {edge}")


def quiet_deterministic_model(name: str) -> Model:
    model = Model(name)
    model.setIntParam("parallel/maxnthreads", 1)
    model.setIntParam("randomization/randomseedshift", 0)
    model.setIntParam("display/verblevel", 0)
    return model


def boundary_witness(points: list[Point], edges: list[Edge]) -> set[int]:
    """Optimize exchanges around the boundary of each mod-3 coloring.

    Coloring (a,b) by a+2b mod 3 assigns all three colors to every corner.
    Deleting one color is therefore independent.  We allow deleted-color
    boundary vertices (incidence degree below three) back in, while changing
    only their incident base vertices.  This is a small exact auxiliary ILP;
    its result is merely a lower-bound witness, not an upper-bound proof.
    """
    incidence: list[list[Edge]] = [[] for _ in points]
    for edge in edges:
        for i in edge:
            incidence[i].append(edge)

    best: set[int] = set()
    for deleted_color in range(3):
        base = {
            i for i, (a, b) in enumerate(points)
            if (a + 2 * b) % 3 != deleted_color
        }
        candidates = {
            i for i, (a, b) in enumerate(points)
            if (a + 2 * b) % 3 == deleted_color and len(incidence[i]) < 3
        }
        mutable = set(candidates)
        for i in candidates:
            for edge in incidence[i]:
                mutable.update(edge)

        model = quiet_deterministic_model(f"boundary_{len(points)}_{deleted_color}")
        variables = {i: model.addVar(vtype="B", name=f"x_{i}") for i in mutable}

        def fixed_value(i: int) -> int:
            return int(i in base)

        for edge in edges:
            terms = [variables[i] for i in edge if i in variables]
            fixed = sum(fixed_value(i) for i in edge if i not in variables)
            if terms:
                model.addCons(quicksum(terms) + fixed <= 2)
            elif fixed > 2:
                raise AssertionError("base coloring is not independent")

        fixed_total = sum(1 for i in base if i not in mutable)
        model.setObjective(fixed_total + quicksum(variables.values()), "maximize")
        start = model.createSol()
        for i, variable in variables.items():
            model.setSolVal(start, variable, fixed_value(i))
        model.addSol(start, free=True)
        model.optimize()
        if str(model.getStatus()) != "optimal":
            raise RuntimeError(f"boundary ILP status {model.getStatus()}")

        chosen = {i for i in base if i not in mutable}
        chosen.update(i for i, variable in variables.items() if model.getVal(variable) > 0.5)
        verify_independent(len(points), edges, chosen)
        if len(chosen) > len(best):
            best = chosen
    return best


def solve_min_cover(
    points: list[Point],
    edges: list[Edge],
    independent_hint: set[int],
    seconds: float,
    log_path: Path,
) -> tuple[int, set[int], dict[str, object]]:
    """Solve the exact binary minimum vertex-cover formulation."""
    k = len(points)
    model = Model(f"corner_cover_{k}")
    model.setIntParam("parallel/maxnthreads", 1)
    model.setIntParam("randomization/randomseedshift", 0)
    model.setIntParam("display/verblevel", 4)
    model.setRealParam("limits/time", seconds)
    model.setLogfile(str(log_path))

    variables = [model.addVar(vtype="B", name=f"z_{i}") for i in range(k)]
    for edge in edges:
        model.addCons(quicksum(variables[i] for i in edge) >= 1)
    model.setObjective(quicksum(variables), "minimize")

    start = model.createSol()
    for i, variable in enumerate(variables):
        model.setSolVal(start, variable, int(i not in independent_hint))
    if not model.addSol(start, free=True):
        raise AssertionError("SCIP rejected the independently checked start solution")

    started = time.monotonic()
    model.optimize()
    elapsed = time.monotonic() - started
    status = str(model.getStatus())
    if status != "optimal":
        raise RuntimeError(
            f"k={k}: SCIP status {status} after {elapsed:.3f}s; see {log_path}"
        )

    objective = model.getObjVal()
    cover_size = round(objective)
    if abs(objective - cover_size) > 1e-6:
        raise AssertionError(f"nonintegral reported objective {objective}")
    cover = {i for i, variable in enumerate(variables) if model.getVal(variable) > 0.5}
    if len(cover) != cover_size:
        raise AssertionError("extracted cover and reported objective disagree")
    verify_cover(k, edges, cover)
    independent = set(range(k)) - cover
    verify_independent(k, edges, independent)

    stats: dict[str, object] = {
        "status": status,
        "objective": cover_size,
        "dual_bound": model.getDualbound(),
        "gap": model.getGap(),
        "nodes": model.getNNodes(),
        "lp_iterations": model.getNLPIterations(),
        "seconds": elapsed,
        "log": log_path.name,
    }
    model.freeProb()
    return cover_size, independent, stats


def encode_points(indices: set[int], points: list[Point]) -> list[list[int]]:
    return [list(points[i]) for i in sorted(indices)]


def write_point_file(path: Path, indices: set[int], points: list[Point]) -> None:
    path.write_text(
        "".join(f"{points[i][0]} {points[i][1]}\n" for i in sorted(indices)),
        encoding="ascii",
    )


def read_point_file(path: Path, points: list[Point]) -> set[int]:
    index = {point: i for i, point in enumerate(points)}
    chosen: set[int] = set()
    for line in path.read_text(encoding="ascii").splitlines():
        if not line:
            continue
        point = tuple(map(int, line.split()))
        if len(point) != 2 or point not in index:
            raise ValueError(f"invalid point in {path}: {line}")
        chosen.add(index[point])
    return chosen


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--through", type=int, default=5020)
    parser.add_argument("--seconds-per-flat", type=float, default=600.0)
    parser.add_argument("--bfile", type=Path, default=DEFAULT_BFILE)
    parser.add_argument("--out-dir", type=Path, default=HERE / "frontier_scip")
    args = parser.parse_args()
    if args.through < 5001:
        raise ValueError("--through must be at least 5001")

    increments, bfile_sha256 = read_bfile(args.bfile)
    if len(increments) != 3335 or increments[-1] != 5000:
        raise ValueError("expected the published A004059 endpoint 3335 5000")
    expected_hash = "bba41cd187052c20e638c539893f16f73d23956f9900caa882e06778256b15ea"
    if bfile_sha256 != expected_hash:
        raise ValueError(f"unexpected b-file SHA-256 {bfile_sha256}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    values, all_points = smooth_prefix(args.through)
    result_path = args.out_dir / "results.json"
    rows: list[dict[str, object]] = []
    solved: list[int] = []
    started = time.monotonic()

    previous_optimum: int | None = None
    previous_witness: set[int] = set()
    first_k = 5000
    prior_wall_seconds = 0.0
    if result_path.exists():
        prior = json.loads(result_path.read_text(encoding="ascii"))
        if prior["problem"]["oeis_bfile_sha256"] != bfile_sha256:
            raise ValueError("resume file was made from a different b-file")
        rows = prior["rows"]
        if not rows or rows[0]["k"] != 5000:
            raise ValueError("resume file does not begin at k=5000")
        if any(right["k"] != left["k"] + 1 for left, right in zip(rows, rows[1:])):
            raise ValueError("resume rows are not consecutive")
        last = rows[-1]
        last_k = int(last["k"])
        if last_k > args.through:
            raise ValueError("resume file already extends beyond --through")
        last_points = all_points[:last_k]
        last_edges = edges_for(last_points)
        previous_witness = read_point_file(args.out_dir / last["witness"], last_points)
        previous_optimum = int(last["f"])
        if len(previous_witness) != previous_optimum:
            raise ValueError("resume witness has wrong cardinality")
        verify_independent(last_k, last_edges, previous_witness)
        solved = list(map(int, prior["solved_prefixes"]))
        prior_wall_seconds = float(prior["runtime"]["wall_seconds"])
        first_k = last_k + 1
        print(f"resuming after verified k={last_k}, f={previous_optimum}", flush=True)

    def save_result() -> None:
        result = {
            "problem": {
                "definition": "maximum corner-free subset of first k 3-smooth numbers",
                "corner": "(a,b),(a+1,b),(a,b+1)",
                "oeis_bfile": str(args.bfile.resolve()),
                "oeis_bfile_sha256": bfile_sha256,
                "published_endpoint": {"k": 5000, "f": 3335},
            },
            "runtime": {
                "python": platform.python_version(),
                "pyscipopt": pyscipopt.__version__,
                "one_worker": True,
                "seconds_per_flat_limit": args.seconds_per_flat,
                "wall_seconds": prior_wall_seconds + time.monotonic() - started,
            },
            "solved_prefixes": solved,
            "rows": rows,
        }
        result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="ascii")

    for k in range(first_k, args.through + 1):
        points = all_points[:k]
        edges = edges_for(points)
        constructive = boundary_witness(points, edges)
        if previous_optimum is not None and len(constructive) < previous_optimum:
            constructive = set(previous_witness)
        verify_independent(k, edges, constructive)

        must_solve = k == 5000 or len(constructive) == previous_optimum
        solver_stats: dict[str, object] | None = None
        method: str
        if must_solve:
            log_path = args.out_dir / f"scip_k{k}.log"
            cover_size, witness, solver_stats = solve_min_cover(
                points, edges, constructive, args.seconds_per_flat, log_path
            )
            optimum = k - cover_size
            solved.append(k)
            method = "SCIP optimal minimum vertex cover"
        else:
            if previous_optimum is None or len(constructive) != previous_optimum + 1:
                raise AssertionError("constructive bound violates one-vertex Lipschitz bound")
            optimum = len(constructive)
            witness = constructive
            method = "witness plus f(k)<=f(k-1)+1"

        if previous_optimum is not None and optimum not in (
            previous_optimum, previous_optimum + 1
        ):
            raise AssertionError("exact optimum violates one-vertex Lipschitz bound")
        verify_independent(k, edges, witness)

        witness_path = args.out_dir / f"independent_k{k}.txt"
        write_point_file(witness_path, witness, points)
        row: dict[str, object] = {
            "k": k,
            "smooth_value": str(values[k - 1]),
            "exponents": list(points[-1]),
            "corners": len(edges),
            "f": optimum,
            "increment": None if previous_optimum is None else optimum - previous_optimum,
            "method": method,
            "constructive_lower_bound": len(constructive),
            "witness": witness_path.name,
            "solver": solver_stats,
        }
        rows.append(row)
        print(json.dumps(row), flush=True)
        previous_optimum = optimum
        previous_witness = witness
        save_result()

    save_result()
    print(f"wrote {result_path}")


if __name__ == "__main__":
    main()
