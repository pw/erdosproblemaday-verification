#!/usr/bin/env python3
"""Independent hostile audit of the frozen Erdős #112 order-21 bundle.

This deliberately does not import the producer's checker.  It uses a
permutation definition of a transitive tournament and a generic finite-domain
CSP search (dynamic variable choice plus complete-constraint checking) for
the eight extension instances.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product


NEAR = (
    "+00++-0-000-0+-+++--+0+++-0-+-++000-00--0+0-++-+-+000--0++00---+"
    "-0++-+0+-00+-++-+0+-++00-0-+0-+++0000+-0+00+00-0--+--++---+0--+"
    "0000+0--0+--+0-++---+000+00--0-0-0+00-+-+0000-00+0-+---++000+0--"
    "0++0-+---+-+++++--0"
)

CONNECTION_SETS = (
    (1, 2, 4, 14, 15, 17),
    (1, 2, 6, 12, 13, 15),
    (2, 3, 5, 6, 11, 12),
    (2, 4, 5, 7, 11, 14),
    (3, 5, 6, 16, 18, 19),
    (5, 7, 8, 14, 18, 19),
    (6, 9, 13, 15, 16, 18),
    (8, 9, 14, 15, 17, 18),
)

VALUES = (0, 1, -1)  # no edge, old vertex -> new vertex, new -> old


def decode_near() -> list[list[int]]:
    """Decode lexicographic pair states without using producer code."""
    n = 21
    assert len(NEAR) == n * (n - 1) // 2
    edge = [[0] * n for _ in range(n)]
    pos = 0
    for u, v in combinations(range(n), 2):
        symbol = NEAR[pos]
        pos += 1
        assert symbol in "+-0"
        if symbol != "0":
            edge[u][v] = 1 if symbol == "+" else -1
            edge[v][u] = -edge[u][v]
    return edge


def is_transitive_by_orders(vertices: tuple[int, ...], edge: list[list[int]]) -> bool:
    """Use the definition: some linear order directs every pair forward."""
    if any(edge[u][v] == 0 for u, v in combinations(vertices, 2)):
        return False
    return any(
        all(edge[order[i]][order[j]] == 1
            for i in range(len(order)) for j in range(i + 1, len(order)))
        for order in permutations(vertices)
    )


def audit_near() -> None:
    edge = decode_near()
    n = len(edge)
    assert all(edge[u][v] == -edge[v][u] for u in range(n) for v in range(n))
    independent = [
        xyz for xyz in combinations(range(n), 3)
        if all(edge[u][v] == 0 for u, v in combinations(xyz, 2))
    ]
    transitive = [
        quad for quad in combinations(range(n), 4)
        if is_transitive_by_orders(quad, edge)
    ]
    profiles = []
    for u in range(n):
        out = sum(edge[u][v] == 1 for v in range(n))
        inn = sum(edge[u][v] == -1 for v in range(n))
        profiles.append((out, inn, n - 1 - out - inn))
    arcs = sum(edge[u][v] != 0 for u, v in combinations(range(n), 2))
    nonedges = n * (n - 1) // 2 - arcs
    assert (arcs, nonedges) == (137, 73)
    assert independent == [(5, 13, 16)]
    assert transitive == []
    assert profiles[0] == (7, 6, 7)
    assert {u for u, p in enumerate(profiles) if p[2] == 8} == {5, 13, 16}
    assert max(p[0] for p in profiles) == 7
    assert max(p[1] for p in profiles) == 7
    digest = sha256(NEAR.encode("ascii")).hexdigest()
    assert digest == "6be5046ca0dc52cbea5a6127f6f7ea8879831b7b5e325fe03b9a7955838cfa6f"
    print(
        "NEAR",
        f"arcs={arcs}",
        f"nonedges={nonedges}",
        f"independent={independent}",
        f"transitive4={len(transitive)}",
        f"profile_histogram={dict(sorted(Counter(profiles).items()))}",
        f"sha256={digest}",
    )


def audit_profiles() -> None:
    """Audit the integer split once the three local upper bounds are granted."""
    got = {
        (out, inn, non)
        for out in range(9)
        for inn in range(9)
        for non in range(8)
        if out + inn + non == 20 and out >= inn
    }
    expected = {
        (8, 8, 4), (8, 7, 5), (8, 6, 6),
        (7, 7, 6), (8, 5, 7), (7, 6, 7),
    }
    assert got == expected
    print("PROFILES", sorted(got))


def cyclic_graph(connection_set: tuple[int, ...]) -> list[list[int]]:
    n = 20
    selected = set(connection_set)
    assert len(selected) == 6
    assert 0 not in selected and 10 not in selected
    assert selected.isdisjoint({(-d) % n for d in selected})
    edge = [[0] * n for _ in range(n)]
    for u, v in combinations(range(n), 2):
        delta = (v - u) % n
        if delta in selected:
            edge[u][v], edge[v][u] = 1, -1
        elif (-delta) % n in selected:
            edge[u][v], edge[v][u] = -1, 1
    return edge


def anchored_transitive(
    old_vertices: tuple[int, int, int],
    relations: tuple[int, int, int],
    old: list[list[int]],
) -> bool:
    """Definition-level check on three old vertices plus a new vertex."""
    edge = [[0] * 4 for _ in range(4)]
    for i, j in combinations(range(3), 2):
        edge[i][j] = old[old_vertices[i]][old_vertices[j]]
        edge[j][i] = -edge[i][j]
    for i, relation in enumerate(relations):
        edge[i][3] = relation
        edge[3][i] = -relation
    return is_transitive_by_orders((0, 1, 2, 3), edge)


def build_forbidden_constraints(old: list[list[int]]):
    """Return exact local obstructions in the 20 ternary new-edge states."""
    constraints: list[tuple[tuple[int, ...], frozenset[tuple[int, ...]]]] = []

    # A nonedge old pair plus two new nonedges is an independent triple.
    for u, v in combinations(range(20), 2):
        if old[u][v] == 0:
            constraints.append(((u, v), frozenset({(0, 0)})))

    # Enumerate all 27 relation patterns for each old triple directly.
    transitive_old_triples = 0
    for triple in combinations(range(20), 3):
        forbidden = frozenset(
            rel for rel in product(VALUES, repeat=3)
            if anchored_transitive(triple, rel, old)
        )
        if forbidden:
            # An induced triple of a transitive four must itself be transitive;
            # the new vertex then has exactly four possible insertion ranks.
            assert is_transitive_by_orders(triple, old)
            assert len(forbidden) == 4
            transitive_old_triples += 1
            constraints.append((triple, forbidden))
    return constraints, transitive_old_triples


def exact_extension_search(old: list[list[int]]):
    """Generic exhaustive CSP search, unrelated to producer's fixed-order DFS.

    A branch is pruned only when all variables of one explicit obstruction
    constraint are assigned.  Dynamic variable ordering changes speed, not the
    represented 3^20 assignment space.
    """
    constraints, transitive_old_triples = build_forbidden_constraints(old)
    by_vertex: list[list[int]] = [[] for _ in range(20)]
    for ci, (vertices, _) in enumerate(constraints):
        for v in vertices:
            by_vertex[v].append(ci)

    assignment: list[int | None] = [None] * 20
    nodes = 0
    rejected_values = 0

    def allowed(v: int) -> tuple[int, ...]:
        nonlocal rejected_values
        answer = []
        for value in VALUES:
            assignment[v] = value
            bad = False
            for ci in by_vertex[v]:
                variables, forbidden = constraints[ci]
                if all(assignment[u] is not None for u in variables):
                    state = tuple(int(assignment[u]) for u in variables)
                    if state in forbidden:
                        bad = True
                        break
            assignment[v] = None
            if bad:
                rejected_values += 1
            else:
                answer.append(value)
        return tuple(answer)

    def recurse(remaining: int) -> bool:
        nonlocal nodes
        nodes += 1
        if remaining == 0:
            return True

        choices = []
        for v in range(20):
            if assignment[v] is None:
                domain = allowed(v)
                if not domain:
                    return False
                # Tie-break toward variables whose constraints are already
                # closest to completion, then toward the larger label.  This
                # differs deliberately from the producer's 0..19 order.
                pressure = sum(
                    sum(assignment[u] is not None for u in constraints[ci][0])
                    for ci in by_vertex[v]
                )
                choices.append((len(domain), -pressure, -v, v, domain))
        _, _, _, v, domain = min(choices)
        for value in domain:
            assignment[v] = value
            if recurse(remaining - 1):
                return True
        assignment[v] = None
        return False

    sat = recurse(20)
    return sat, nodes, rejected_values, len(constraints), transitive_old_triples


def audit_extensions() -> None:
    for connection_set in CONNECTION_SETS:
        old = cyclic_graph(connection_set)
        independent3 = sum(
            all(old[u][v] == 0 for u, v in combinations(triple, 2))
            for triple in combinations(range(20), 3)
        )
        transitive4 = sum(
            is_transitive_by_orders(quad, old)
            for quad in combinations(range(20), 4)
        )
        arcs = sum(old[u][v] != 0 for u, v in combinations(range(20), 2))
        degree_profiles = {
            (
                sum(old[u][v] == 1 for v in range(20)),
                sum(old[u][v] == -1 for v in range(20)),
                sum(old[u][v] == 0 for v in range(20) if v != u),
            )
            for u in range(20)
        }
        assert arcs == 120
        assert degree_profiles == {(6, 6, 7)}
        assert independent3 == 0
        assert transitive4 == 0

        sat, nodes, rejected, nconstraints, transitive3 = exact_extension_search(old)
        assert not sat
        print(
            "NONEXTENDABLE",
            f"C={connection_set}",
            "base=(arcs=120,I3=0,L4=0,profile=6/6/7)",
            f"constraints={nconstraints}",
            f"transitive_old_triples={transitive3}",
            f"csp_nodes={nodes}",
            f"rejected_values={rejected}",
        )


def main() -> None:
    audit_profiles()
    audit_near()
    audit_extensions()
    print("HOSTILE AUDIT PASSED")


if __name__ == "__main__":
    main()
