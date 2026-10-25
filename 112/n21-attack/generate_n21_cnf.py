#!/usr/bin/env python3
"""Generate SAT instances for 21-vertex (I_3,L_4)-free oriented graphs.

Each unordered pair has exactly one of three states: forward arc, reverse
arc, or no edge.  Vertex 0 is split canonically into its out-, in-, and
non-neighbourhoods.  Elementary local bounds leave only six profiles up to
global arc reversal.
"""

from __future__ import annotations

import argparse
from itertools import combinations, permutations
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool


ORDER = 21
PROFILES = ((8, 8, 4), (8, 7, 5), (8, 6, 6), (7, 7, 6), (8, 5, 7), (7, 6, 7))


class Variables:
    def __init__(self, pool: IDPool) -> None:
        self.pool = pool

    def fwd(self, u: int, v: int) -> int:
        """Literal variable for the arc u -> v."""
        assert u != v
        if u < v:
            return self.pool.id(("f", u, v))
        return self.pool.id(("r", v, u))

    def none(self, u: int, v: int) -> int:
        assert u != v
        a, b = sorted((u, v))
        return self.pool.id(("n", a, b))

    def pair(self, u: int, v: int) -> tuple[int, int, int]:
        assert u < v
        return self.fwd(u, v), self.fwd(v, u), self.none(u, v)


def add_exactly_one(cnf: CNF, values: tuple[int, int, int]) -> None:
    cnf.append(list(values))
    for a, b in combinations(values, 2):
        cnf.append([-a, -b])


def build(
    profile: tuple[int, int, int] | None,
    degree_bounds: bool = True,
) -> tuple[CNF, IDPool, Variables]:
    if profile is not None:
        out_size, in_size, none_size = profile
        assert out_size + in_size + none_size == ORDER - 1
        assert profile in PROFILES

    pool = IDPool()
    var = Variables(pool)
    cnf = CNF()

    # Definition-level ternary edge states.
    for u, v in combinations(range(ORDER), 2):
        add_exactly_one(cnf, var.pair(u, v))

    # No independent triple.
    for a, b, c in combinations(range(ORDER), 3):
        cnf.append([-var.none(a, b), -var.none(a, c), -var.none(b, c)])

    # No transitive tournament of order four.  Every transitive orientation
    # has a unique topological order, so the 24 clauses per four-set are exact.
    for vertices in combinations(range(ORDER), 4):
        for linear_order in permutations(vertices):
            cnf.append([
                -var.fwd(linear_order[i], linear_order[j])
                for i in range(4)
                for j in range(i + 1, 4)
            ])

    # Canonical root profile.  Reversal lets us require out_size >= in_size;
    # arbitrary relabelling makes each class a consecutive interval.
    if profile is not None:
        out = range(1, 1 + out_size)
        inn = range(1 + out_size, 1 + out_size + in_size)
        non = range(1 + out_size + in_size, ORDER)
        for v in out:
            cnf.append([var.fwd(0, v)])
        for v in inn:
            cnf.append([var.fwd(v, 0)])
        for v in non:
            cnf.append([var.none(0, v)])

    if degree_bounds:
        # These redundant but valid bounds follow from k(3,3)=9 and the
        # elementary tournament bound k(2,4)<=8.  For every vertex:
        # outdegree <=8, indegree <=8, nondegree <=7.
        for u in range(ORDER):
            outgoing = [var.fwd(u, v) for v in range(ORDER) if v != u]
            incoming = [var.fwd(v, u) for v in range(ORDER) if v != u]
            missing = [var.none(u, v) for v in range(ORDER) if v != u]
            for literals, bound, tag in (
                (outgoing, 8, "out"),
                (incoming, 8, "in"),
                (missing, 7, "none"),
            ):
                card = CardEnc.atmost(
                    lits=literals,
                    bound=bound,
                    vpool=pool,
                    encoding=EncType.seqcounter,
                )
                cnf.extend(card.clauses)

    return cnf, pool, var


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", choices=["-".join(map(str, p)) for p in PROFILES])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--no-degree-bounds", action="store_true")
    args = parser.parse_args()
    profile = tuple(map(int, args.profile.split("-")))
    cnf, pool, _ = build(profile, degree_bounds=not args.no_degree_bounds)
    cnf.to_file(args.output)
    print(
        f"profile={profile} variables={pool.top} clauses={len(cnf.clauses)} "
        f"output={args.output}"
    )


if __name__ == "__main__":
    main()
