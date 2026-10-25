#!/usr/bin/env python3
"""Hostile definition-level arithmetic audit of frozen #1206 witnesses."""

from __future__ import annotations

import ast
import hashlib
import itertools
import re
from collections import defaultdict
from pathlib import Path


FROZEN = Path("/tmp/erdos1206_exact_132_191")


def load_rows_from_cpp():
    text = (FROZEN / "verify_exact.cpp").read_text()
    block = text.split("static const vector<Range> RANGES{", 1)[1].split("};", 1)[0]
    rows = []
    for lo, hi, tau, raw_cover in re.findall(
        r"\{(\d+),\s*(\d+),\s*(\d+),\s*\{([^}]*)\}\}", block
    ):
        cover = tuple(ast.literal_eval(x.strip()) for x in raw_cover.split(","))
        rows.append((int(lo), int(hi), int(tau), cover))
    assert len(rows) == 12
    return tuple(rows)


def groups_and_edges(n: int):
    # Deliberately traverse larger root descending and store sums in a hash
    # table, a different order/container from the frozen C++.
    buckets: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for b in range(n, 0, -1):
        for a in range(b, 0, -1):
            buckets[a**3 + b**3].append((a, b))
    edge_to_sources: dict[tuple[int, ...], set[tuple[tuple[int, int], tuple[int, int]]]] = defaultdict(set)
    for representations in buckets.values():
        for one, two in itertools.combinations(representations, 2):
            edge = tuple(sorted(set(one + two)))
            edge_to_sources[edge].add(tuple(sorted((one, two))))
    return buckets, edge_to_sources


def direct_pair_check(n: int, cover: tuple[int, ...]):
    removed = set(cover)
    kept = tuple(x for x in range(1, n + 1) if x not in removed)
    sums: dict[int, tuple[int, int]] = {}
    for a, b in itertools.combinations_with_replacement(kept, 2):
        value = pow(a, 3) + pow(b, 3)
        assert value not in sums, (n, value, sums[value], (a, b))
        sums[value] = (a, b)
    assert len(sums) == len(kept) * (len(kept) + 1) // 2
    return kept, sums


def main():
    rows = load_rows_from_cpp()
    assert rows[0][0] == 132 and rows[-1][1] == 191
    assert all(left[1] + 1 == right[0] for left, right in zip(rows, rows[1:]))

    _, full_sources = groups_and_edges(191)
    full_edges = set(full_sources)
    prior: set[tuple[int, ...]] = set()
    endpoint_rows = {endpoint for lo, hi, *_ in rows for endpoint in (lo, hi)}
    for n in range(1, 192):
        groups, edge_sources = groups_and_edges(n)
        edges = set(edge_sources)
        assert prior <= edges
        # This exact restriction identity is the premise used for endpoint
        # interpolation: no collision edge appears/disappears unexpectedly.
        assert edges == {edge for edge in full_edges if max(edge) <= n}
        prior = edges

        # Definition edge cases: every unordered pair occurs once; diagonal
        # representations are retained; every hyperedge is exactly the union
        # of two distinct equal-sum pairs; no equal pairs are compared.
        assert sum(map(len, groups.values())) == n * (n + 1) // 2
        assert sum(a == b for reps in groups.values() for a, b in reps) == n
        rebuilt = defaultdict(set)
        for value, reps in groups.items():
            assert len(reps) == len(set(reps))
            for one, two in itertools.combinations(reps, 2):
                assert one != two and one[0] <= one[1] and two[0] <= two[1]
                assert one[0] ** 3 + one[1] ** 3 == value
                assert two[0] ** 3 + two[1] ** 3 == value
                rebuilt[tuple(sorted(set(one + two)))].add(tuple(sorted((one, two))))
        assert dict(rebuilt) == dict(edge_sources)
        if n in endpoint_rows:
            print(f"N={n}: pairs={n*(n+1)//2} sums={len(groups)} edges={len(edges)}")

    # Explicit abstract representation lists exercise union shapes absent from
    # N<=191 arithmetic.  Think of each pair-of-pairs as already assigned to a
    # synthetic common bucket; these examples are about set-union mechanics,
    # not additional equalities of actual cubes.
    synthetic = (
        ((3, 3), (1, 4)),       # a diagonal representation; 3-vertex edge
        ((1, 4), (1, 5)),       # overlapping representations; 3-vertex edge
        ((2, 7), (3, 6)),       # disjoint representations; 4-vertex edge
    )
    assert [len(set(a + b)) for a, b in synthetic] == [3, 3, 4]
    assert tuple(sorted(set((3, 3) + (1, 4)))) == (1, 3, 4)

    for lo, hi, tau, cover in rows:
        assert len(cover) == tau and len(set(cover)) == tau
        assert tuple(sorted(cover)) == cover and 1 <= cover[0] <= cover[-1] <= hi
        _, edge_sources = groups_and_edges(hi)
        chosen = set(cover)
        assert all(chosen.intersection(edge) for edge in edge_sources)
        kept, sums = direct_pair_check(hi, cover)
        assert len(kept) == hi - tau
        print(
            f"range {lo}..{hi}: tau={tau}; upper witness/direct sums PASS; "
            f"retained={len(kept)} sums={len(sums)}"
        )

    buckets, source_map = groups_and_edges(191)
    edges = tuple(sorted(source_map))
    collision_buckets = [reps for reps in buckets.values() if len(reps) > 1]
    payload = "\n".join(",".join(map(str, edge)) for edge in edges).encode()
    digest = hashlib.sha256(payload).hexdigest()
    assert len(buckets) == 18_212 and len(collision_buckets) == 124
    assert max(map(len, collision_buckets)) == 2 and len(edges) == 124
    assert {len(edge) for edge in edges} == {4}
    assert len(set().union(*(set(edge) for edge in edges))) == 164
    assert digest == "644dadc2aa52bddd902f03811acff745e129add6406fac5a09be5099852fb081"
    print(f"N=191 canonical edge SHA256={digest}")
    print("HOSTILE ARITHMETIC/WITNESS/INTERVAL AUDIT PASS")


if __name__ == "__main__":
    main()
