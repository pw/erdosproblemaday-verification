#!/usr/bin/env python3
"""Independent, definition-level audit of a root degree-branch DIMACS file.

This checker deliberately does not import PySAT or either CNF generator.  It
reconstructs the natural graph clauses, checks the root units, and verifies
the existential meaning of the auxiliary degree clauses by an exhaustive
2^17-input Horn projection.  Thus the only unverified part of an UNSAT claim
is the separately replayed proof, not the cardinality encoder's semantics.
"""

from __future__ import annotations

import argparse
from collections import deque
from itertools import combinations


N = 18
NATURAL_VARS = 153 + 816


def read_dimacs(path: str) -> tuple[int, list[list[int]]]:
    variables = -1
    declared_clauses = -1
    clauses: list[list[int]] = []
    with open(path) as stream:
        for line in stream:
            line = line.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p "):
                fields = line.split()
                assert fields[:2] == ["p", "cnf"] and len(fields) == 4
                variables, declared_clauses = map(int, fields[2:])
                continue
            fields = list(map(int, line.split()))
            assert fields and fields[-1] == 0 and 0 not in fields[:-1]
            clauses.append(fields[:-1])
    assert variables >= NATURAL_VARS
    assert declared_clauses == len(clauses)
    assert max(abs(lit) for clause in clauses for lit in clause) == variables
    return variables, clauses


def natural_clauses() -> tuple[list[list[int]], dict[tuple[int, int], int]]:
    pairs = list(combinations(range(N), 2))
    triples = list(combinations(range(N), 3))
    edge = {pair: i for i, pair in enumerate(pairs, 1)}
    triangle = {triple: len(pairs) + i for i, triple in enumerate(triples, 1)}
    clauses: list[list[int]] = []
    for triple in triples:
        t = triangle[triple]
        es = [edge[pair] for pair in combinations(triple, 2)]
        clauses.extend([[-t, e] for e in es])
        clauses.append([-es[0], -es[1], -es[2], t])
    for vertices in combinations(range(N), 5):
        clauses.append([-edge[pair] for pair in combinations(vertices, 2)])
    for vertices in combinations(range(N), 7):
        clauses.append([triangle[t] for t in combinations(vertices, 3)])
    assert len(clauses) == 43656
    return clauses, edge


def normalized_block(
    block: list[list[int]], incident: list[int]
) -> tuple[tuple[int, ...], ...]:
    """Rename incident inputs to 1..17 and private auxiliaries above 17."""
    input_map = {var: i for i, var in enumerate(incident, 1)}
    aux = sorted({abs(lit) for clause in block for lit in clause
                  if abs(lit) > NATURAL_VARS})
    aux_map = {var: 17 + i for i, var in enumerate(aux, 1)}
    renamed = input_map | aux_map
    assert all(abs(lit) in renamed for clause in block for lit in clause)
    return tuple(tuple((1 if lit > 0 else -1) * renamed[abs(lit)]
                       for lit in clause) for clause in block)


def horn_projection_table(block: tuple[tuple[int, ...], ...], aux_count: int) -> int:
    """Return the 2^17-bit truth table after existentially projecting aux vars.

    Degree encoder clauses are Horn in their auxiliary variables.  All input
    literals must be negative.  A negative input literal makes its clause
    irrelevant when that input is false; otherwise the remaining clause is a
    Horn implication.  Forward chaining computes Horn satisfiability exactly.
    """
    seeds: list[tuple[int, int | None]] = []
    by_body: list[list[tuple[int, int | None]]] = [[] for _ in range(aux_count)]
    for clause in block:
        edge_mask = 0
        body: list[int] = []
        heads: list[int] = []
        for lit in clause:
            var = abs(lit)
            if var <= 17:
                assert lit < 0, "degree clause contains a positive input literal"
                edge_mask |= 1 << (var - 1)
            elif lit < 0:
                body.append(var - 18)
            else:
                heads.append(var - 18)
        assert len(heads) <= 1, "auxiliary formula is not Horn"
        assert len(body) <= 1, "checker expects the unary sequential Horn form"
        head = heads[0] if heads else None
        assert head is None or 0 <= head < aux_count
        if body:
            assert 0 <= body[0] < aux_count
            by_body[body[0]].append((edge_mask, head))
        else:
            seeds.append((edge_mask, head))

    table = 0
    for assignment in range(1 << 17):
        true_aux = 0
        queue: deque[int] = deque()
        satisfiable = True

        def fire(head: int | None) -> None:
            nonlocal true_aux, satisfiable
            if head is None:
                satisfiable = False
            elif not (true_aux >> head) & 1:
                true_aux |= 1 << head
                queue.append(head)

        for required, head in seeds:
            if required & ~assignment == 0:
                fire(head)
                if not satisfiable:
                    break
        while satisfiable and queue:
            body_var = queue.popleft()
            for required, head in by_body[body_var]:
                if required & ~assignment == 0:
                    fire(head)
                    if not satisfiable:
                        break
        if satisfiable:
            table |= 1 << assignment
    return table


def expected_atmost_table(degree: int) -> int:
    table = 0
    for assignment in range(1 << 17):
        if assignment.bit_count() <= degree:
            table |= 1 << assignment
    return table


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("degree", type=int)
    parser.add_argument("cnf")
    parser.add_argument(
        "--local-lemma",
        choices=("root", "global"),
        help="independently check and strip appended alpha(N(v))<=3 clauses",
    )
    args = parser.parse_args()
    d = args.degree
    assert 0 <= d <= 17

    variables, clauses = read_dimacs(args.cnf)
    expected_natural, edge = natural_clauses()

    lemma_count = 0
    if args.local_lemma:
        def e(u: int, v: int) -> int:
            return edge[tuple(sorted((u, v)))]

        expected_lemma: list[list[int]] = []
        vertices = [0] if args.local_lemma == "root" else range(N)
        for v in vertices:
            others = (list(range(1, d + 1)) if args.local_lemma == "root"
                      else [u for u in range(N) if u != v])
            for four in combinations(others, 4):
                clause = [-e(v, u) for u in four]
                clause.extend(e(x, y) for x, y in combinations(four, 2))
                expected_lemma.append(clause)
        assert clauses[-len(expected_lemma):] == expected_lemma
        lemma_count = len(expected_lemma)
        clauses = clauses[:-lemma_count]
    assert clauses[:len(expected_natural)] == expected_natural

    expected_root = [[edge[(0, v)]] if v <= d else [-edge[(0, v)]]
                     for v in range(1, N)]
    assert clauses[-17:] == expected_root

    middle = clauses[len(expected_natural):-17]
    assert len(middle) % N == 0
    block_size = len(middle) // N
    blocks = [middle[i * block_size:(i + 1) * block_size] for i in range(N)]

    normalized: list[tuple[tuple[int, ...], ...]] = []
    aux_sets: list[set[int]] = []
    for v, block in enumerate(blocks):
        incident = [edge[tuple(sorted((u, v)))] for u in range(N) if u != v]
        natural_seen = {abs(lit) for clause in block for lit in clause
                        if abs(lit) <= NATURAL_VARS}
        assert natural_seen <= set(incident)
        assert all(var <= 153 for var in natural_seen)
        aux = {abs(lit) for clause in block for lit in clause
               if abs(lit) > NATURAL_VARS}
        assert aux
        aux_sets.append(aux)
        normalized.append(normalized_block(block, incident))

    assert all(normalized[i] == normalized[0] for i in range(1, N))
    assert all(aux_sets[i].isdisjoint(aux_sets[j])
               for i in range(N) for j in range(i))
    all_aux = set().union(*aux_sets)
    assert all_aux == set(range(NATURAL_VARS + 1, variables + 1))

    aux_count = len(aux_sets[0])
    actual = horn_projection_table(normalized[0], aux_count)
    expected = expected_atmost_table(d)
    assert actual == expected

    print(f"VERIFIED cnf={args.cnf}")
    print(f"degree={d} variables={variables} clauses={len(clauses)}")
    print(f"natural_clauses={len(expected_natural)} root_units=17")
    print(f"degree_blocks={N} block_clauses={block_size} private_aux_per_block={aux_count}")
    print("degree_projection=EXACT exhaustive_assignments=131072 method=independent_Horn_closure")
    if args.local_lemma:
        print(f"local_lemma={args.local_lemma} lemma_clauses={lemma_count} exact_clause_match=YES")


if __name__ == "__main__":
    main()
