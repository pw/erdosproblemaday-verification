#!/usr/bin/env python3
"""Definition-level verifier for f(7)=4 and F(7)=7 in Problem 1183."""

from pathlib import Path

N = 7
U = 1 << N
COLOUR_RED_RANKS = {3, 4, 6}
EXPECTED_MAXIMA = (6, 7)
LATTICE_RED_RANKS = {0, 2, 3, 5}
EXPECTED_LATTICE_MAXIMA = (4, 4)
CORE_CNF = Path(__file__).with_name("lower_core.cnf")


def union_closed(family):
    family = frozenset(family)
    return all((a | b) in family for a in family for b in family)


def maximum_union_closed(colour):
    """Exact branch-and-bound maximum with closure propagation."""
    colour = frozenset(colour)
    members = tuple(sorted(colour))
    best = set()

    def close(seed):
        closure = set(seed)
        while True:
            old = len(closure)
            current = tuple(closure)
            for i, a in enumerate(current):
                for b in current[i:]:
                    c = a | b
                    if c not in colour:
                        return None
                    closure.add(c)
            if len(closure) == old:
                return frozenset(closure)

    def dfs(chosen, candidates, forbidden):
        nonlocal best
        chosen = close(chosen)
        if chosen is None or chosen & forbidden:
            return
        candidates = tuple(x for x in candidates if x not in chosen)
        if len(chosen) + len(candidates) <= len(best):
            return
        if not candidates:
            if len(chosen) > len(best):
                best = set(chosen)
            return
        # Prefer a candidate forcing many new unions, to prune quickly.
        x = max(candidates, key=lambda y: len({y | z for z in chosen}))
        rest = tuple(y for y in candidates if y != x)
        dfs(set(chosen) | {x}, rest, forbidden)
        dfs(chosen, rest, forbidden | {x})

    dfs(set(), members, set())
    assert union_closed(best)
    return tuple(sorted(best))


def maximum_lattice_closed(colour):
    """Exact maximum via union/intersection closure and include/exclude."""
    colour = frozenset(colour)
    members = tuple(sorted(colour))
    best = set()

    def close(seed):
        closure = set(seed)
        while True:
            old = len(closure)
            current = tuple(closure)
            for i, a in enumerate(current):
                for b in current[i:]:
                    for c in (a | b, a & b):
                        if c not in colour:
                            return None
                        closure.add(c)
            if len(closure) == old:
                return frozenset(closure)

    def dfs(chosen, candidates, forbidden):
        nonlocal best
        chosen = close(chosen)
        if chosen is None or chosen & forbidden:
            return
        candidates = tuple(x for x in candidates if x not in chosen)
        if len(chosen) + len(candidates) <= len(best):
            return
        if not candidates:
            if len(chosen) > len(best):
                best = set(chosen)
            return
        x = max(candidates, key=lambda y: len({y | z for z in chosen}) +
                                           len({y & z for z in chosen}))
        rest = tuple(y for y in candidates if y != x)
        dfs(set(chosen) | {x}, rest, forbidden)
        dfs(chosen, rest, forbidden | {x})

    dfs(set(), members, set())
    assert all((a | b) in best and (a & b) in best for a in best for b in best)
    return tuple(sorted(best))


def verify_lower_family_corpus():
    seen = set()
    red_families = blue_families = 0
    lines = [line.strip() for line in CORE_CNF.read_text().splitlines()
             if line.strip() and not line.startswith("c")]
    header = lines.pop(0).split()
    assert header[:2] == ["p", "cnf"] and int(header[2]) == U
    assert int(header[3]) == len(lines) == 42035
    assert lines[0] == "-1 0"  # WLOG: the empty set is blue.
    for line in lines[1:]:
        literals = tuple(map(int, line.split()))
        assert literals[-1] == 0
        literals = literals[:-1]
        assert len(literals) == 7
        assert all(x > 0 for x in literals) or all(x < 0 for x in literals)
        want_red = literals[0] < 0
        family = tuple(sorted(abs(x) - 1 for x in literals))
        assert len(family) == len(set(family)) == 7
        assert all(0 <= x < U for x in family)
        assert union_closed(family)
        key = (want_red, family)
        assert key not in seen
        seen.add(key)
        if want_red:
            red_families += 1
        else:
            blue_families += 1

    assert len(seen) == 42034
    print("lower core:", len(seen), "valid seven-member families;",
          red_families, "red clauses;", blue_families, "blue clauses")


def main():
    verify_lower_family_corpus()
    red = [a for a in range(U) if a.bit_count() in COLOUR_RED_RANKS]
    blue = [a for a in range(U) if a.bit_count() not in COLOUR_RED_RANKS]
    red_witness = maximum_union_closed(red)
    blue_witness = maximum_union_closed(blue)
    assert (len(red_witness), len(blue_witness)) == EXPECTED_MAXIMA
    print("upper rank colouring red ranks:", sorted(COLOUR_RED_RANKS))
    print("exact colour maxima:", len(red_witness), len(blue_witness))
    print("red witness:", red_witness)
    print("blue witness:", blue_witness)
    print("CERTIFIED F(7)=7")
    lattice_red = [a for a in range(U) if a.bit_count() in LATTICE_RED_RANKS]
    lattice_blue = [a for a in range(U) if a.bit_count() not in LATTICE_RED_RANKS]
    lr = maximum_lattice_closed(lattice_red)
    lb = maximum_lattice_closed(lattice_blue)
    assert (len(lr), len(lb)) == EXPECTED_LATTICE_MAXIMA
    print("lattice upper rank colouring red ranks:", sorted(LATTICE_RED_RANKS))
    print("exact lattice colour maxima:", len(lr), len(lb))
    print("lattice red witness:", lr)
    print("lattice blue witness:", lb)
    print("CERTIFIED f(7)=4")


if __name__ == "__main__":
    main()
