#!/usr/bin/env python3
"""Search the exact n=18 formula inside automorphism-invariant slices.

Candidate automorphisms are taken from the 12-element automorphism group of
the best near miss.  The seed itself is not fixed: only an edge-permutation
symmetry is imposed on the otherwise unrestricted graph formula.
"""

from __future__ import annotations

import sys
from itertools import combinations
from time import perf_counter

import networkx as nx
from pysat.solvers import Solver

sys.path.insert(0, "/home/exedev/MathDyad/erdos813")
from gen_cnf import build, decode_model


def load(path: str) -> list[int]:
    with open(path) as stream:
        return [int(line.strip(), 16) for line in stream if line.strip()]


def permutation_order(p: tuple[int, ...]) -> int:
    q = tuple(range(len(p)))
    for order in range(1, 100):
        q = tuple(p[q[i]] for i in range(len(p)))
        if q == tuple(range(len(p))):
            return order
    raise AssertionError


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
    seed = load(sys.argv[1])
    graph = nx.Graph()
    graph.add_nodes_from(range(18))
    graph.add_edges_from(
        (u, v) for u, v in combinations(range(18), 2) if seed[u] >> v & 1
    )
    automorphisms = {
        tuple(mapping[i] for i in range(18))
        for mapping in nx.algorithms.isomorphism.GraphMatcher(
            graph, graph
        ).isomorphisms_iter()
    }
    identity = tuple(range(18))
    automorphisms.remove(identity)

    nvars, base, pairs = build(18, 5)
    edge_var = {pair: index for index, pair in enumerate(pairs, 1)}

    # More restrictive/high-order slices first.
    ordered = sorted(automorphisms, key=lambda p: (-permutation_order(p), p))
    for case, p in enumerate(ordered):
        clauses = list(base)
        seen: set[tuple[int, int]] = set()
        orbit_count = 0
        for pair in pairs:
            if pair in seen:
                continue
            orbit = set()
            current = pair
            while current not in orbit:
                orbit.add(current)
                current = tuple(sorted((p[current[0]], p[current[1]])))
            seen.update(orbit)
            orbit_count += 1
            rep = edge_var[min(orbit)]
            for other_pair in orbit:
                other = edge_var[other_pair]
                if other != rep:
                    clauses.append([-rep, other])
                    clauses.append([rep, -other])

        started = perf_counter()
        with Solver(name="cadical195", bootstrap_with=clauses) as solver:
            solver.conf_budget(3_000_000)
            result = solver.solve_limited(expect_interrupt=True)
            elapsed = perf_counter() - started
            print(
                f"case={case} order={permutation_order(p)} "
                f"edge_orbits={orbit_count} clauses={len(clauses)} "
                f"result={result} seconds={elapsed:.3f}",
                flush=True,
            )
            if result is not True:
                continue
            masks = decode_model(solver.get_model(), 18)
        assert direct_check(masks) == (0, 0)
        print("WITNESS " + " ".join(f"{row:05x}" for row in masks))
        with open("/tmp/erdos813_attack/symmetric_witness.masks", "w") as out:
            for row in masks:
                out.write(f"{row:05x}\n")
        return


if __name__ == "__main__":
    main()
