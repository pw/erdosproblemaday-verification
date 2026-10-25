#!/usr/bin/env python3
"""mu-subcells of one M-cell: per block X, the multiset of missed targets of its 2e(X) matched vertices is row X of M;
enumerate labelled assignments to local slots 0..2e-1 (edges (0,1),(2,3)) up to the block's internal group
G_X = <(0 1), (2 3), (0 2)(1 3)> (e = 2) or <(0 1)> (e = 1); a cell's solutions are covered because G_X fixes the
case's internal edges and the block, hence M. Output: one spec per line (comma-separated per block), for h1mcell --mu."""
import itertools, sys
from menum import PAIRS, case_E
j, flat = int(sys.argv[1]), list(map(int, sys.argv[2].split(",")))
E = case_E(j)
M = [[0]*8 for _ in range(8)]
for (X, Y), v in zip(PAIRS, flat):
    M[X][Y] = M[Y][X] = v
per = []
for X in range(8):
    T = [Y for Y in range(8) for _ in range(M[X][Y])]
    assert len(T) == 2 * E[X]
    G = [(0, 1, 2, 3), (1, 0, 2, 3), (0, 1, 3, 2), (1, 0, 3, 2), (2, 3, 0, 1), (3, 2, 0, 1), (2, 3, 1, 0), (3, 2, 1, 0)] \
        if E[X] == 2 else [(0, 1), (1, 0)]
    reps = set()
    for a in set(itertools.permutations(T)):
        reps.add(min(tuple(a[g[i]] for i in range(len(a))) for g in G))
    per.append(sorted("".join(map(str, r)) for r in reps))
for combo in itertools.product(*per):
    print(",".join(combo))
