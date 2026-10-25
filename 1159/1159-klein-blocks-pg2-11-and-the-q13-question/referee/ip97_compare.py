"""Referee: Illés–Pisinger's own q=11 blocking set, as POSTED by them in 1997.
Source: http://www.diku.dk/~pisinger/erdos.html ("Found solutions ... compressed file output.c.gz"),
archived at web.archive.org/web/20001003134338/http://www.diku.dk:80/~pisinger/output.c.gz
(gzip header: original name erdos.out, mtime Sat Dec 6 12:07:47 1997). The q=11 block reads:
  y[1]=84 y[3]=28 y[4]=21 |B|=21 ; difference set: 3,16,24,27,31,33,43,74,75,97,111,131
  solution: 5,13,22,26,27,33,39,40,50,74,78,80,84,89,92,94,96,99,107,112,114
Plane convention (IP97 eqs (2)-(4)): points 1..n, line i contains point j iff 1+((i+j-2) mod n) is in D.
We (a) check D is a planar difference set, (b) recompute B's spectrum, (c) test with nauty whether
(cyclic plane, B) is isomorphic to (PG(2,11), our witness S) as coloured incidence structures,
(d) compute |Aut| of (cyclic plane, B)."""
import json, os, sys, itertools
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpg, pynauty
q = 11; n = q*q + q + 1
D = [3,16,24,27,31,33,43,74,75,97,111,131]
B = [5,13,22,26,27,33,39,40,50,74,78,80,84,89,92,94,96,99,107,112,114]
diffs = Counter((a - b) % n for a in D for b in D if a != b)
print("D planar difference set mod 133:", len(D) == q + 1 and len(diffs) == n - 1 and set(diffs.values()) == {1})
cyc = [frozenset(j for j in range(1, n + 1) if 1 + ((i + j - 2) % n) in D) for i in range(1, n + 1)]
assert all(len(l) == q + 1 for l in cyc)
assert all(len(a & b) == 1 for a, b in itertools.combinations(cyc, 2))
Bs = set(B); sp = Counter(len(Bs & l) for l in cyc)
print("IP97 B: |B| =", len(Bs), " spectrum:", dict(sorted(sp.items())))
def levi(lines_, Sset):
    adj = {i: [] for i in range(2 * n)}
    for li, l in enumerate(lines_):
        for j in l: adj[j].append(n + li); adj[n + li].append(j)
    col = [set(Sset), set(range(n)) - set(Sset), set(range(n, 2 * n))]
    return pynauty.Graph(2 * n, adjacency_dict=adj, vertex_coloring=col)
g_ip = levi([frozenset(j - 1 for j in l) for l in cyc], {b - 1 for b in B})
pts, idx, lines, inc = rpg.plane(q)
W = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'runs', 'witnesses_q11_c4.json')))
for key in W:
    S = {idx[rpg.norm(P, q)] for P in W[key]}
    g_ours = levi(inc, S)
    print(f"(cyclic plane, IP97 B) isomorphic to (PG(2,11), {key} witness):", pynauty.certificate(g_ip) == pynauty.certificate(g_ours))
# negative control: perturb B by swapping one point; must NOT be isomorphic
B2 = sorted((Bs - {B[0]}) | {next(j for j in range(1, n + 1) if j not in Bs)})
print("negative control (one point swapped) isomorphic?:", pynauty.certificate(levi([frozenset(j - 1 for j in l) for l in cyc], {b - 1 for b in B2})) == pynauty.certificate(levi(inc, {idx[rpg.norm(P, q)] for P in W['cadical']})))
_, a1, a2, _, _ = pynauty.autgrp(g_ip)
print("|Aut(cyclic plane, B)| (collineations of the cyclic plane fixing B):", round(a1 * 10 ** a2))
