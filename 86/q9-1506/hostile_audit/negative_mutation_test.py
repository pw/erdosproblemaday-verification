#!/usr/bin/env python3
"""Confirm both clean-room C4 tests reject a controlled 1506-edge mutation."""

from collections import defaultdict
from itertools import combinations
import json
from pathlib import Path


path = Path(__file__).resolve().parent / "candidate_q9_1506.json"
rows = json.loads(path.read_text(encoding="utf-8"))["edges"]
edges = {tuple(row) for row in rows}
assert len(edges) == 1506

chosen_face = None
missing_edge = None
for i, j in combinations(range(9), 2):
    mi, mj = 1 << i, 1 << j
    for base in range(512):
        if base & (mi | mj):
            continue
        a, b, c, d = base, base | mi, base | mj, base | mi | mj
        face = {(a, b), (a, c), (b, d), (c, d)}
        absent = face - edges
        if len(absent) == 1:
            chosen_face = face
            missing_edge = next(iter(absent))
            break
    if chosen_face is not None:
        break

assert chosen_face is not None and missing_edge is not None
removed_edge = next(edge for edge in sorted(edges) if edge not in chosen_face)
mutant = (edges - {removed_edge}) | {missing_edge}
assert len(mutant) == 1506
assert chosen_face <= mutant

complete_faces = 0
for i, j in combinations(range(9), 2):
    mi, mj = 1 << i, 1 << j
    for base in range(512):
        if base & (mi | mj):
            continue
        a, b, c, d = base, base | mi, base | mj, base | mi | mj
        face = {(a, b), (a, c), (b, d), (c, d)}
        complete_faces += face <= mutant
assert complete_faces >= 1

adjacency: dict[int, set[int]] = defaultdict(set)
for u, v in mutant:
    adjacency[u].add(v)
    adjacency[v].add(u)
centers: dict[tuple[int, int], int] = {}
repeat = None
for center, neighbours in adjacency.items():
    for endpoints in combinations(sorted(neighbours), 2):
        if endpoints in centers:
            repeat = (endpoints, centers[endpoints], center)
            break
        centers[endpoints] = center
    if repeat is not None:
        break
assert repeat is not None

print("NEGATIVE_MUTATION_PASS both_routes_rejected=yes")
print(f"removed_edge={removed_edge} added_edge={missing_edge}")
print(f"controlled_complete_face={sorted(chosen_face)}")
print(f"complete_faces_detected={complete_faces}")
print(f"repeated_common_neighbour_witness={repeat}")
