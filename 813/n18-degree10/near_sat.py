#!/usr/bin/env python3
"""Search for an h(18)=4 witness within a bounded edge distance of a seed.

The base clauses are regenerated from the graph definition.  A satisfying
model is checked again by direct subset enumeration before being printed.
"""

from __future__ import annotations

import argparse
from itertools import combinations
from time import perf_counter

from neighbourhood_census_sat import build, decode_model
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver


def load_masks(path: str) -> list[int]:
    with open(path) as stream:
        return [int(line.split("#", 1)[0].strip(), 16)
                for line in stream if line.split("#", 1)[0].strip()]


def direct_check(adj: list[int]) -> tuple[int, int]:
    vertices = range(18)
    k5 = sum(
        all(adj[u] >> v & 1 for u, v in combinations(subset, 2))
        for subset in combinations(vertices, 5)
    )
    tf7 = 0
    for subset in combinations(vertices, 7):
        if not any(
            (adj[u] >> v & 1)
            and (adj[u] & adj[v] & sum(1 << w for w in subset))
            for u, v in combinations(subset, 2)
        ):
            tf7 += 1
    return k5, tf7


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("seed")
    parser.add_argument("distance", type=int)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--conflicts", type=int, default=0,
                        help="conflict budget; zero means unlimited")
    parser.add_argument("--out")
    args = parser.parse_args()

    seed = load_masks(args.seed)
    assert len(seed) == 18
    nvars, clauses, pairs = build(18, 5)

    # Literal true exactly when this model edge differs from the seed edge.
    differences = []
    for edge_var, (u, v) in enumerate(pairs, 1):
        differences.append(-edge_var if seed[u] >> v & 1 else edge_var)
    pool = IDPool(start_from=nvars + 1)
    bound = CardEnc.atmost(
        lits=differences,
        bound=args.distance,
        encoding=EncType.totalizer,
        vpool=pool,
    )
    clauses.extend(bound.clauses)

    started = perf_counter()
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        if args.conflicts:
            solver.conf_budget(args.conflicts)
            result = solver.solve_limited(expect_interrupt=True)
        else:
            result = solver.solve()
        elapsed = perf_counter() - started
        print(
            f"solver={args.solver} distance<={args.distance} "
            f"vars={pool.top} clauses={len(clauses)} result={result} "
            f"seconds={elapsed:.3f}",
            flush=True,
        )
        if result is not True:
            return
        model = solver.get_model()

    masks = decode_model(model, 18)
    actual_distance = sum(
        bool(seed[u] >> v & 1) != bool(masks[u] >> v & 1)
        for u, v in pairs
    )
    k5, tf7 = direct_check(masks)
    assert actual_distance <= args.distance
    assert (k5, tf7) == (0, 0)
    print(f"WITNESS distance={actual_distance}")
    print("MASKS " + " ".join(f"{row:05x}" for row in masks))
    if args.out:
        with open(args.out, "w") as stream:
            for row in masks:
                stream.write(f"{row:05x}\n")


if __name__ == "__main__":
    main()
