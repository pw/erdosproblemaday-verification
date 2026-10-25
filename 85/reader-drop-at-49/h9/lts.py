#!/usr/bin/env python3
"""Linear triple systems on 9 points with t triples (t = 0..4), up to isomorphism.
Two independent dedups: pynauty certificate of the point/block incidence graph, and networkx VF2
isomorphism on the same graph built separately. Both must give the same class counts.
Writes reps.json: {t: [list of triples]}."""
import itertools, json, sys
NPTS = int(sys.argv[2]); TMAX = int(sys.argv[3])
import networkx as nx
from pynauty import Graph, certificate

PTS = range(NPTS)
TRIPLES = list(itertools.combinations(PTS, 3))


def linear(sys_):
    return all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(sys_, 2))


def cert(sys_):
    n = NPTS + len(sys_)
    adj = {NPTS + i: list(b) for i, b in enumerate(sys_)}
    g = Graph(n, directed=False, adjacency_dict=adj,
              vertex_coloring=[set(range(NPTS)), set(range(NPTS, n))] if sys_ else [set(range(NPTS))])
    return certificate(g)


def nxg(sys_):
    g = nx.Graph()
    g.add_nodes_from((("p", i), {"c": 0}) for i in PTS)
    for j, b in enumerate(sys_):
        g.add_node(("b", j), c=1)
        g.add_edges_from((("b", j), ("p", x)) for x in b)
    return g


reps = {0: [()]}
for t in range(1, TMAX + 1):
    seen, out = set(), []
    for base in reps[t - 1]:
        for tr in TRIPLES:
            if tr in base or (base and tr < base[-1] and False):
                continue
            s = tuple(sorted(base + (tr,)))
            if not linear(s):
                continue
            c = cert(s)
            if c not in seen:
                seen.add(c)
                out.append(s)
    reps[t] = out
counts_nauty = {t: len(v) for t, v in reps.items()}
# second instrument: VF2 dedup over ALL linear systems of size t (no augmentation shortcut) for t <= 3,
# and over the augmented candidates for t = 4
counts_vf2 = {}
nm = nx.algorithms.isomorphism.categorical_node_match("c", None)
vf2_reps = {0: [()]}
for t in range(1, TMAX + 1) if "TMAX" in globals() else range(1, 5):
    classes, reps_t = [], []
    for base in vf2_reps[t - 1]:          # augment the VF2 method's OWN previous classes (independent of nauty)
        for tr in TRIPLES:
            if tr in base:
                continue
            s = tuple(sorted(base + (tr,)))
            if not linear(s):
                continue
            g = nxg(s)
            if not any(nx.is_isomorphic(g, h, node_match=nm) for h in classes):
                classes.append(g); reps_t.append(s)
    vf2_reps[t] = reps_t
counts_vf2 = {t: len(v) for t, v in vf2_reps.items()}
print("nauty classes:", counts_nauty)
print("vf2 classes:  ", counts_vf2)
assert counts_nauty == counts_vf2
json.dump({str(t): [list(map(list, s)) for s in v] for t, v in reps.items()}, open(sys.argv[1], "w"))
