#!/usr/bin/env python3
"""Definition-level audit for the N=21 search artifacts for Erdős #112."""

from __future__ import annotations

import hashlib
from itertools import combinations


ORDER = 21

# Lexicographic unordered-pair states from one local-search near witness.
# '+' means u->v, '-' means v->u, and '0' means no edge for u<v.
NEAR_STATES = (
    "+00++-0-000-0+-+++--+0+++-0-+-++000-00--0+0-++-+-+000--0++00---+"
    "-0++-+0+-00+-++-+0+-++00-0-+0-+++0000+-0+00+00-0--+--++---+0--+"
    "0000+0--0+--+0-++---+000+00--0-0-0+00-+-+0000-00+0-+---++000+0--"
    "0++0-+---+-+++++--0"
)

CYCLIC_CONNECTION_SETS = (
    (1, 2, 4, 14, 15, 17),
    (1, 2, 6, 12, 13, 15),
    (2, 3, 5, 6, 11, 12),
    (2, 4, 5, 7, 11, 14),
    (3, 5, 6, 16, 18, 19),
    (5, 7, 8, 14, 18, 19),
    (6, 9, 13, 15, 16, 18),
    (8, 9, 14, 15, 17, 18),
)


def decode_states(states: str) -> list[list[int]]:
    assert len(states) == ORDER * (ORDER - 1) // 2 == 210
    matrix = [[0] * ORDER for _ in range(ORDER)]
    at = 0
    for u in range(ORDER):
        for v in range(u + 1, ORDER):
            state = states[at]
            at += 1
            assert state in "+-0"
            if state == "+":
                matrix[u][v], matrix[v][u] = 1, -1
            elif state == "-":
                matrix[u][v], matrix[v][u] = -1, 1
    return matrix


def independent(vertices: tuple[int, ...], matrix: list[list[int]]) -> bool:
    return all(matrix[u][v] == 0 for u, v in combinations(vertices, 2))


def transitive_tournament(vertices: tuple[int, ...], matrix: list[list[int]]) -> bool:
    if any(matrix[u][v] == 0 for u, v in combinations(vertices, 2)):
        return False
    outdegrees = [sum(matrix[u][v] == 1 for v in vertices if v != u) for u in vertices]
    return sorted(outdegrees) == list(range(len(vertices)))


def bad_sets(matrix: list[list[int]]) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    independent_triples = [
        vertices
        for vertices in combinations(range(ORDER), 3)
        if independent(vertices, matrix)
    ]
    transitive_fours = [
        vertices
        for vertices in combinations(range(ORDER), 4)
        if transitive_tournament(vertices, matrix)
    ]
    return independent_triples, transitive_fours


def root_profile(matrix: list[list[int]], vertex: int) -> tuple[int, int, int]:
    outdegree = sum(matrix[vertex][u] == 1 for u in range(ORDER))
    indegree = sum(matrix[vertex][u] == -1 for u in range(ORDER))
    return outdegree, indegree, ORDER - 1 - outdegree - indegree


def verify_near_witness() -> None:
    matrix = decode_states(NEAR_STATES)
    assert all(matrix[u][v] == -matrix[v][u] for u in range(ORDER) for v in range(ORDER))
    arcs = sum(matrix[u][v] != 0 for u, v in combinations(range(ORDER), 2))
    nonedges = ORDER * (ORDER - 1) // 2 - arcs
    assert (arcs, nonedges) == (137, 73)
    independent_triples, transitive_fours = bad_sets(matrix)
    assert independent_triples == [(5, 13, 16)]
    assert not transitive_fours
    profiles = [root_profile(matrix, v) for v in range(ORDER)]
    assert profiles[0] == (7, 6, 7)
    assert max(p[0] for p in profiles) == 7
    assert max(p[1] for p in profiles) == 7
    assert max(p[2] for p in profiles) == 8
    assert {v for v, p in enumerate(profiles) if p[2] == 8} == {5, 13, 16}
    digest = hashlib.sha256(NEAR_STATES.encode("ascii")).hexdigest()
    print(
        f"NEAR N=21: arcs={arcs} nonedges={nonedges} root_profile=(7,6,7) "
        "independent_triples=[(5,13,16)] transitive_fours=0 "
        f"sha256={digest}"
    )


def cyclic_matrix(connection_set: tuple[int, ...]) -> list[list[int]]:
    matrix = [[0] * 20 for _ in range(20)]
    selected = set(connection_set)
    for u in range(20):
        for v in range(u + 1, 20):
            difference = (v - u) % 20
            if difference in selected:
                matrix[u][v], matrix[v][u] = 1, -1
            elif (-difference) % 20 in selected:
                matrix[u][v], matrix[v][u] = -1, 1
    return matrix


def relation_safe_with_new_vertex(
    old: list[list[int]],
    relations: tuple[int, ...],
) -> bool:
    """Independent direct check for adjoining vertex 20.

    relations[u]=+1 means u->20, -1 means 20->u, and 0 means nonadjacent.
    Since the order-20 graph is already free, every new obstruction contains
    vertex 20. We check only those anchored subsets directly.
    """
    for u, v in combinations(range(20), 2):
        if relations[u] == relations[v] == 0 and old[u][v] == 0:
            return False
    for a, b, c in combinations(range(20), 3):
        vertices = (a, b, c)
        if any(old[u][v] == 0 for u, v in combinations(vertices, 2)):
            continue
        matrix = [[0] * 4 for _ in range(4)]
        for i in range(3):
            for j in range(i + 1, 3):
                matrix[i][j] = old[vertices[i]][vertices[j]]
                matrix[j][i] = -matrix[i][j]
            matrix[i][3] = relations[vertices[i]]
            matrix[3][i] = -relations[vertices[i]]
        if transitive_tournament((0, 1, 2, 3), matrix):
            return False
    return True


def verify_extension_instances() -> None:
    # Exact backtracking over ternary relations to the new vertex, with early
    # rejection of anchored independent triples and transitive fours.
    for connection_set in CYCLIC_CONNECTION_SETS:
        old = cyclic_matrix(connection_set)
        # Establish that the fixed 20-vertex base is itself free before using
        # the fact that every new obstruction must contain vertex 20.
        assert not any(
            independent(vertices, old)
            for vertices in combinations(range(20), 3)
        )
        assert not any(
            transitive_tournament(vertices, old)
            for vertices in combinations(range(20), 4)
        )
        assert sum(
            old[u][v] != 0 for u, v in combinations(range(20), 2)
        ) == 120
        relations = [0] * 20
        nodes = 0

        def rec(at: int) -> bool:
            nonlocal nodes
            nodes += 1
            if at == 20:
                return relation_safe_with_new_vertex(old, tuple(relations))
            for state in (0, 1, -1):
                relations[at] = state
                # Check newly complete independent triples through vertex 20.
                if state == 0 and any(
                    relations[u] == 0 and old[u][at] == 0
                    for u in range(at)
                ):
                    continue
                # Check newly complete transitive fours through vertex 20.
                failed = False
                for a, b in combinations(range(at), 2):
                    if old[a][b] == 0 or relations[a] == 0 or relations[b] == 0:
                        continue
                    vs = (a, b, at)
                    matrix = [[0] * 4 for _ in range(4)]
                    for i in range(3):
                        for j in range(i + 1, 3):
                            matrix[i][j] = old[vs[i]][vs[j]]
                            matrix[j][i] = -matrix[i][j]
                        matrix[i][3] = relations[vs[i]]
                        matrix[3][i] = -relations[vs[i]]
                    if transitive_tournament((0, 1, 2, 3), matrix):
                        failed = True
                        break
                if not failed and rec(at + 1):
                    return True
            return False

        assert not rec(0), connection_set
        print(f"NONEXTENDABLE C={connection_set} backtracking_nodes={nodes}")


def verify_profiles() -> None:
    # In a free order-21 graph, N+(v) and N-(v) are (I_3,L_3)-free, hence
    # have size <=8 because k(3,3)=9. I(v) is (I_2,L_4)-free, hence has size
    # <=7 because every tournament on 8 vertices contains a transitive four.
    # Reversal permits out >= in. Enumerate all integer profiles.
    profiles = {
        (out, inn, non)
        for out in range(9)
        for inn in range(9)
        for non in range(8)
        if out + inn + non == 20 and out >= inn
    }
    expected = {(8, 8, 4), (8, 7, 5), (8, 6, 6), (7, 7, 6), (8, 5, 7), (7, 6, 7)}
    assert profiles == expected
    print(f"ROOT PROFILES: {sorted(profiles)}")


def main() -> None:
    verify_profiles()
    verify_near_witness()
    verify_extension_instances()
    print("ALL DEFINITION-LEVEL AUDITS PASSED")


if __name__ == "__main__":
    main()
