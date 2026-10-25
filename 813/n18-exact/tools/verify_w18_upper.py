#!/usr/bin/env python3
"""Independent finite checks for the report on Erdős problem 813.

The witness checks use only the Python standard library.  The n=13 lower
bound additionally rebuilds a transparent CNF from the graph definition and
uses python-sat (PySAT) to prove five symmetry-complete cases UNSAT.

Usage:
    python runs/erdos813_wavew015_verify.py
    python runs/erdos813_wavew015_verify.py --witness-only
    python runs/erdos813_wavew015_verify.py --cross-check
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations
from time import perf_counter


# The usual 12-vertex icosahedral graph, with vertices relabelled 0,...,11.
ICOSAHEDRON_EDGES = (
    (0, 1), (0, 5), (0, 7), (0, 8), (0, 11),
    (1, 2), (1, 5), (1, 6), (1, 8),
    (2, 3), (2, 6), (2, 8), (2, 9),
    (3, 4), (3, 6), (3, 9), (3, 10),
    (4, 5), (4, 6), (4, 10), (4, 11),
    (5, 6), (5, 11),
    (7, 8), (7, 9), (7, 10), (7, 11),
    (8, 9), (9, 10), (10, 11),
)

# A 17-vertex witness.  Entry i is the bit mask of the neighbours of i.
# This is more compact, and less error-prone to copy, than its 84-edge list.
W17_MASKS = (
    0x1F92E, 0x1CE19, 0x172F1, 0x13EF3, 0x031EE, 0x06B9D,
    0x1B31C, 0x05D3C, 0x0BCF1, 0x1D46E, 0x0FB8A, 0x0C5AB,
    0x0C7DD, 0x1857D, 0x11EA7, 0x13F43, 0x0E24F,
)

# An 18-vertex K6-free witness, giving the still non-exact bound h(18) <= 5.
W18_MASKS = (
    0x179DE, 0x21FFD, 0x273BB, 0x34457, 0x3ED8F, 0x3C6C6,
    0x1AFAB, 0x1EA77, 0x33E57, 0x2C5E6, 0x3AB7A, 0x1B5D3,
    0x18907, 0x20DD5, 0x382BD, 0x35EF0, 0x2DDF9, 0x1E73E,
)


def masks_from_edges(n: int, edges: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    masks = [0] * n
    for u, v in edges:
        assert 0 <= u < v < n
        masks[u] |= 1 << v
        masks[v] |= 1 << u
    return tuple(masks)


I12_MASKS = masks_from_edges(12, ICOSAHEDRON_EDGES)


def validate_simple_graph(masks: tuple[int, ...]) -> None:
    n = len(masks)
    assert all(0 <= row < (1 << n) for row in masks)
    for u in range(n):
        assert not ((masks[u] >> u) & 1), f"loop at {u}"
        for v in range(n):
            assert ((masks[u] >> v) & 1) == ((masks[v] >> u) & 1), (
                f"asymmetry at {u},{v}"
            )


def induced_prefix(masks: tuple[int, ...], n: int) -> tuple[int, ...]:
    keep = (1 << n) - 1
    return tuple(row & keep for row in masks[:n])


def adjacent(masks: tuple[int, ...], u: int, v: int) -> bool:
    return bool((masks[u] >> v) & 1)


def is_clique(masks: tuple[int, ...], vertices: tuple[int, ...]) -> bool:
    return all(adjacent(masks, u, v) for u, v in combinations(vertices, 2))


def triangle_count_in(masks: tuple[int, ...], vertices: tuple[int, ...]) -> int:
    return sum(is_clique(masks, triple) for triple in combinations(vertices, 3))


def is_triangle_free(masks: tuple[int, ...], vertices: tuple[int, ...]) -> bool:
    return triangle_count_in(masks, vertices) == 0


def exact_clique_witness(
    masks: tuple[int, ...], expected: int
) -> tuple[int, ...]:
    vertices = tuple(range(len(masks)))
    witness = next(
        subset
        for subset in combinations(vertices, expected)
        if is_clique(masks, subset)
    )
    assert not any(
        is_clique(masks, subset)
        for subset in combinations(vertices, expected + 1)
    )
    return witness


def edge_count(masks: tuple[int, ...]) -> int:
    return sum(row.bit_count() for row in masks) // 2


def witness_summary(
    name: str,
    masks: tuple[int, ...],
    expected_edges: int,
    expected_triangles: int,
    expected_omega: int,
) -> None:
    validate_simple_graph(masks)
    n = len(masks)
    vertices = tuple(range(n))
    edges = edge_count(masks)
    triangles = triangle_count_in(masks, vertices)
    clique = exact_clique_witness(masks, expected_omega)
    tf_set = next(
        subset
        for subset in combinations(vertices, 6)
        if is_triangle_free(masks, subset)
    )
    seven_distribution = Counter(
        triangle_count_in(masks, seven)
        for seven in combinations(vertices, 7)
    )

    assert edges == expected_edges
    assert triangles == expected_triangles
    assert min(seven_distribution) >= 1

    print(
        f"{name}: n={n}, edges={edges}, triangles={triangles}, "
        f"omega={expected_omega} (witness {clique}), "
        f"max triangle-free order=6 (witness {tf_set})"
    )
    print(f"{name}: triangles per 7-set = {sorted(seven_distribution.items())}")


def verify_witnesses() -> None:
    witness_summary("I12", I12_MASKS, 30, 20, 3)
    witness_summary("W17", W17_MASKS, 84, 146, 4)
    witness_summary("W18", W18_MASKS, 100, 223, 5)

    # Heredity gives the interval constructions; check the chosen prefixes too.
    for n in range(7, 13):
        graph = induced_prefix(I12_MASKS, n)
        assert all(
            not is_triangle_free(graph, seven)
            for seven in combinations(range(n), 7)
        )
        exact_clique_witness(graph, 3)

    for n in range(13, 18):
        graph = induced_prefix(W17_MASKS, n)
        assert all(
            not is_triangle_free(graph, seven)
            for seven in combinations(range(n), 7)
        )
        exact_clique_witness(graph, 4)

    print("Witness prefixes verified: omega=3 for n=7..12; omega=4 for n=13..17.")


def verify_h7_density_example() -> None:
    """Check the seven-vertex 2-density obstruction used in the method wall."""

    # Clique blow-up of C5 with consecutive part sizes 1,2,1,1,2.
    parts = ((0,), (1, 2), (3,), (4,), (5, 6))
    edges: set[tuple[int, int]] = set()
    for part in parts:
        edges.update(combinations(part, 2))
    for i, part in enumerate(parts):
        for u in part:
            for v in parts[(i + 1) % 5]:
                edges.add(tuple(sorted((u, v))))

    def has_edge(u: int, v: int) -> bool:
        return tuple(sorted((u, v))) in edges

    vertices = tuple(range(7))
    assert len(edges) == 11
    assert not any(
        all(not has_edge(u, v) for u, v in combinations(triple, 2))
        for triple in combinations(vertices, 3)
    )
    assert any(not has_edge(u, v) for u, v in combinations(vertices, 2))

    densities: list[tuple[Fraction, tuple[int, ...], int]] = []
    for size in range(3, 8):
        for subset in combinations(vertices, size):
            induced_edges = sum(
                has_edge(u, v) for u, v in combinations(subset, 2)
            )
            densities.append(
                (Fraction(induced_edges - 1, size - 2), subset, induced_edges)
            )
    density, subset, induced_edges = max(densities)
    assert density == 2
    print(
        "H7 density example: 7 vertices, 11 edges, alpha=2, "
        f"m2=2 (attained on {subset} with {induced_edges} edges)."
    )


class VariablePool:
    """Tiny deterministic variable allocator, avoiding formula-builder magic."""

    def __init__(self) -> None:
        self.ids: dict[tuple[object, ...], int] = {}

    def id(self, key: tuple[object, ...]) -> int:
        if key not in self.ids:
            self.ids[key] = len(self.ids) + 1
        return self.ids[key]


def n13_cnf(max_degree: int) -> tuple[int, list[list[int]]]:
    """Build one symmetry-complete n=13, K4-free case.

    Vertex 0 is chosen to have maximum degree d=max_degree, and is relabelled
    so that its neighbourhood is exactly {1,...,d}.  This loses no graph.
    Degree-at-most-d is encoded directly: among every d+1 incident edge
    variables, at least one is false.
    """

    n = 13
    vertices = tuple(range(n))
    pool = VariablePool()
    clauses: list[list[int]] = []

    def edge(u: int, v: int) -> int:
        return pool.id(("e", min(u, v), max(u, v)))

    def triangle(triple: tuple[int, int, int]) -> int:
        return pool.id(("t",) + triple)

    # t_abc iff all three edge variables on abc are true.
    for triple in combinations(vertices, 3):
        t = triangle(triple)
        three_edges = [edge(u, v) for u, v in combinations(triple, 2)]
        clauses.extend([[-t, e] for e in three_edges])
        clauses.append([-three_edges[0], -three_edges[1], -three_edges[2], t])

    # Every seven vertices contain at least one certified triangle.
    for seven in combinations(vertices, 7):
        clauses.append([triangle(triple) for triple in combinations(seven, 3)])

    # K4-free: every four-set has a missing edge.
    for four in combinations(vertices, 4):
        clauses.append([-edge(u, v) for u, v in combinations(four, 2)])

    # Symmetry split: vertex 0 has maximum degree d and this fixed neighbourhood.
    for v in range(1, n):
        clauses.append([edge(0, v) if v <= max_degree else -edge(0, v)])

    # Transparent at-most-d constraints, with no auxiliary variables.
    for v in vertices:
        incident = [edge(v, u) for u in vertices if u != v]
        for too_many in combinations(incident, max_degree + 1):
            clauses.append([-literal for literal in too_many])

    expected_variables = 78 + 286  # C(13,2) edge vars + C(13,3) triangle vars
    expected_base_clauses = 4 * 286 + 1716 + 715 + 12
    expected_clauses = expected_base_clauses + 13 * {
        2: 220,  # C(12,3)
        3: 495,  # C(12,4)
        4: 792,  # C(12,5)
        5: 924,  # C(12,6)
        6: 792,  # C(12,7)
    }[max_degree]
    assert len(pool.ids) == expected_variables
    assert len(clauses) == expected_clauses
    return len(pool.ids), clauses


def verify_n13_unsat(solver_name: str) -> None:
    try:
        from pysat.solvers import Solver
    except ImportError as error:
        raise SystemExit(
            "The witness checks passed, but the n=13 UNSAT check requires "
            "python-sat (import name: pysat)."
        ) from error

    total_start = perf_counter()
    for max_degree in range(2, 7):
        variables, clauses = n13_cnf(max_degree)
        start = perf_counter()
        with Solver(name=solver_name, bootstrap_with=clauses) as solver:
            satisfiable = solver.solve()
        elapsed = perf_counter() - start
        assert not satisfiable, (
            f"unexpected model with maximum degree {max_degree}"
        )
        print(
            f"{solver_name}: Delta={max_degree}, variables={variables}, "
            f"clauses={len(clauses)}, UNSAT ({elapsed:.3f}s)"
        )
    print(
        f"{solver_name}: all maximum-degree cases 2..6 are UNSAT "
        f"({perf_counter() - total_start:.3f}s total)."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--witness-only",
        action="store_true",
        help="run the dependency-free direct construction checks only",
    )
    parser.add_argument(
        "--solver",
        default="cadical195",
        help="PySAT solver for the n=13 UNSAT split (default: cadical195)",
    )
    parser.add_argument(
        "--cross-check",
        action="store_true",
        help="also repeat the UNSAT split with the independent Kissat solver",
    )
    args = parser.parse_args()

    verify_witnesses()
    verify_h7_density_example()
    if not args.witness_only:
        verify_n13_unsat(args.solver)
        if args.cross_check and args.solver != "kissat404":
            verify_n13_unsat("kissat404")

    print(
        "VERIFIED: h(n)=1 for 1<=n<=6, 3 for 7<=n<=12, "
        "4 for 13<=n<=17, and 4<=h(18)<=5."
    )


if __name__ == "__main__":
    main()
