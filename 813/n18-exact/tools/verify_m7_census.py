#!/usr/bin/env python3
"""Independent exhaustive verification of the 71 canonical M graphs."""

from __future__ import annotations

import argparse
from itertools import combinations, permutations


PAIRS = [(u, v) for v in range(1, 7) for u in range(v)]
PAIR_INDEX = {pair: i for i, pair in enumerate(PAIRS)}
TRIPLE_MASKS = [sum(1 << PAIR_INDEX[tuple(sorted(p))] for p in combinations(s, 2))
                for s in combinations(range(7), 3)]
K5_MASKS = [sum(1 << PAIR_INDEX[tuple(sorted(p))] for p in combinations(s, 2))
            for s in combinations(range(7), 5)]


def decode(line: bytes) -> int:
    line = line.strip()
    assert line and line[0] == 70
    bits = []
    for char in line[1:]:
        value = char - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    return sum(bit << i for i, bit in enumerate(bits[:21]))


def valid(mask: int) -> bool:
    if any(mask & pattern == 0 for pattern in TRIPLE_MASKS):
        return False
    if any(mask & pattern == pattern for pattern in K5_MASKS):
        return False
    return True


def permute(mask: int, p: tuple[int, ...]) -> int:
    output = 0
    for i, (u, v) in enumerate(PAIRS):
        a, b = sorted((p[u], p[v]))
        j = PAIR_INDEX[(a, b)]
        output |= ((mask >> i) & 1) << j
    return output


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("census")
    args = ap.parse_args()
    census = [decode(line) for line in open(args.census, "rb") if line.strip()]
    assert len(census) == 71 and len(set(census)) == 71 and all(map(valid, census))
    representatives = set(census)
    seen = set()
    perms = list(permutations(range(7)))
    orbit_sizes = []
    for representative in census:
        orbit = {permute(representative, p) for p in perms}
        assert not orbit & seen
        seen |= orbit
        orbit_sizes.append(len(orbit))
    direct_valid = {mask for mask in range(1 << 21) if valid(mask)}
    assert seen == direct_valid
    print(f"VERIFIED representatives={len(representatives)} disjoint_orbits=YES")
    print(f"orbit_union={len(seen)} direct_valid_masks={len(direct_valid)} exact_equal=YES")
    print(f"total_masks={1<<21} min_orbit={min(orbit_sizes)} max_orbit={max(orbit_sizes)}")


if __name__ == "__main__":
    main()
