"""Our own construction of J(n,5,3) and the pair reduction (erdos704 independent route)."""
from itertools import combinations

def build(n, k=5, t=3):
    V = [frozenset(c) for c in combinations(range(n), k)]
    idx = {s: i for i, s in enumerate(V)}
    N = len(V)
    # adjacency in J as python-int bitsets
    adjJ = [0] * N
    for i in range(N):
        a = V[i]
        m = 0
        for j in range(N):
            if j != i and len(a & V[j]) == t:
                m |= 1 << j
        adjJ[i] = m
    return V, idx, adjJ

def perm_on_sets(V, idx, p):
    """p: list, permutation of range(n). Returns induced permutation of vertex indices."""
    return [idx[frozenset(p[x] for x in s)] for s in V]
