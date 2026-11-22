"""Independent brute-force checker (seat O): oriented? transitive triangles? independent k-sets? degrees."""
import itertools
def check(n, arcs, k):
    A = set(arcs)
    loops = sum(1 for (i, j) in A if i == j)
    two = sum(1 for (i, j) in A if (j, i) in A and i < j)
    bad_vertex = [x for e in A for x in e if not (0 <= x < n)]
    adj = [[False]*n for _ in range(n)]
    for i, j in A:
        adj[i][j] = adj[j][i] = True
    tt = 0
    for x, y, z in itertools.permutations(range(n), 3):
        if (x, y) in A and (y, z) in A and (x, z) in A:
            tt += 1
    indep = 0
    first = None
    for S in itertools.combinations(range(n), k):
        if not any(adj[i][j] for i, j in itertools.combinations(S, 2)):
            indep += 1
            if first is None: first = S
    outd = [sum(1 for (i, j) in A if i == v) for v in range(n)]
    ind = [sum(1 for (i, j) in A if j == v) for v in range(n)]
    return dict(n=n, arcs=len(A), loops=loops, two_cycles=two, bad_vertex=len(bad_vertex), tt=tt,
                indep=indep, first_indep=first, outdeg=sorted(set(outd)), indeg=sorted(set(ind)),
                deg=sorted(set(o+i for o, i in zip(outd, ind))))
