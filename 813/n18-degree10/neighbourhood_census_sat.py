#!/usr/bin/env python3
"""Test one shard of a complete neighbourhood census in the n=18 formula."""

from __future__ import annotations

import argparse
from itertools import combinations
from time import perf_counter

import networkx as nx
from pysat.solvers import Solver


def build(n: int, forbidden_clique: int) -> tuple[int, list[list[int]], list[tuple[int, int]]]:
    """Natural definition-level encoding, with deterministic variable IDs."""
    pairs = list(combinations(range(n), 2))
    triples = list(combinations(range(n), 3))
    edge = {pair: index for index, pair in enumerate(pairs, 1)}
    triangle = {
        triple: len(pairs) + index
        for index, triple in enumerate(triples, 1)
    }
    clauses: list[list[int]] = []
    for triple in triples:
        t = triangle[triple]
        three_edges = [edge[pair] for pair in combinations(triple, 2)]
        clauses.extend([[-t, e] for e in three_edges])
        clauses.append([-three_edges[0], -three_edges[1], -three_edges[2], t])
    for subset in combinations(range(n), forbidden_clique):
        clauses.append([-edge[pair] for pair in combinations(subset, 2)])
    for subset in combinations(range(n), 7):
        clauses.append([triangle[triple] for triple in combinations(subset, 3)])
    return len(pairs) + len(triples), clauses, pairs


def decode_model(model: list[int], n: int) -> list[int]:
    true = {literal for literal in model if literal > 0}
    masks = [0] * n
    for variable, (u, v) in enumerate(combinations(range(n), 2), 1):
        if variable in true:
            masks[u] |= 1 << v
            masks[v] |= 1 << u
    return masks


def direct_check(adj: list[int]) -> tuple[int, int]:
    k5 = sum(
        all(adj[u] >> v & 1 for u, v in combinations(S, 2))
        for S in combinations(range(18), 5)
    )
    tf7 = sum(
        not any(
            all(adj[u] >> v & 1 for u, v in combinations(T, 2))
            for T in combinations(S, 3)
        )
        for S in combinations(range(18), 7)
    )
    return k5, tf7


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("degree", type=int)
    parser.add_argument("census")
    parser.add_argument("shard", type=int)
    parser.add_argument("shards", type=int)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--conflicts", type=int, default=0)
    parser.add_argument("--case", type=int, action="append",
                        help="test only this absolute census index (repeatable)")
    parser.add_argument("--witness")
    args = parser.parse_args()
    assert 0 <= args.shard < args.shards

    with open(args.census, "rb") as stream:
        census = list(nx.read_graph6(stream))
    assert all(len(graph) == args.degree for graph in census)

    _, base, pairs = build(18, 5)
    edge = {pair: index for index, pair in enumerate(pairs, 1)}

    def e(u: int, v: int) -> int:
        return edge[tuple(sorted((u, v)))]

    selected = (args.case if args.case is not None
                else list(range(args.shard, len(census), args.shards)))
    assert all(0 <= case < len(census) for case in selected)
    total_conflicts = 0
    unsat = 0
    unknown = 0
    started_all = perf_counter()
    for sequence, case in enumerate(selected, 1):
        neighbourhood = census[case]
        clauses = list(base)
        for v in range(1, 18):
            clauses.append([e(0, v) if v <= args.degree else -e(0, v)])
        for u, v in combinations(range(args.degree), 2):
            literal = e(u + 1, v + 1)
            clauses.append([literal if neighbourhood.has_edge(u, v) else -literal])

        started = perf_counter()
        with Solver(name=args.solver, bootstrap_with=clauses) as solver:
            if args.conflicts:
                solver.conf_budget(args.conflicts)
                result = solver.solve_limited(expect_interrupt=True)
            else:
                result = solver.solve()
            try:
                stats = solver.accum_stats()
            except NotImplementedError:
                stats = {}
            model = solver.get_model() if result is True else None
        elapsed = perf_counter() - started
        conflicts = stats.get("conflicts", -1)
        total_conflicts += max(conflicts, 0)
        if result is False:
            unsat += 1
        elif result is None:
            unknown += 1
        print(
            f"shard={args.shard}/{args.shards} sequence={sequence}/{len(selected)} "
            f"case={case}/{len(census)} edges={neighbourhood.number_of_edges()} "
            f"result={result} conflicts={conflicts} seconds={elapsed:.3f}",
            flush=True,
        )
        if result is True:
            masks = decode_model(model, 18)
            assert direct_check(masks) == (0, 0)
            print("WITNESS " + " ".join(f"{row:05x}" for row in masks))
            if args.witness:
                with open(args.witness, "w") as out:
                    for row in masks:
                        out.write(f"{row:05x}\n")
            return

    print(
        f"SHARD_DONE shard={args.shard}/{args.shards} degree={args.degree} "
        f"cases={len(selected)} unsat={unsat} unknown={unknown} "
        f"conflicts={total_conflicts} seconds={perf_counter()-started_all:.3f}",
        flush=True,
    )


if __name__ == "__main__":
    main()
