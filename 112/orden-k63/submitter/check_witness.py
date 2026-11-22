#!/usr/bin/env python3
"""check_witness.py: check that an oriented graph has no transitive triangle and no independent set of 6 vertices.

Input: one line per vertex, "v: w1 w2 ..." listing the out-neighbours of v (an arc v -> w for each w).
A transitive triangle is x -> y, y -> z, x -> z. An independent set has no arc in either direction between any two members.
Usage: python3 check_witness.py witness_k63_29_vertices.txt
"""
import sys

def main(path, m=6):
    out = {}
    for line in open(path):
        if ":" in line and not line.startswith("#"):
            v, rest = line.split(":")
            out[int(v)] = set(int(t) for t in rest.split())
    V = sorted(out)
    arcs = {(v, w) for v in V for w in out[v]}
    assert all(v != w for v, w in arcs), "a loop"
    assert not any((w, v) in arcs for v, w in arcs), "an arc in both directions"
    adj = {v: {w for w in V if (v, w) in arcs or (w, v) in arcs} for v in V}
    tt = sum(1 for x in V for y in out[x] for z in out[y] if z in out[x])
    found = []
    def extend(chosen, cand):
        if found: return
        if len(chosen) == m:
            found.append(list(chosen)); return
        for i, v in enumerate(cand):
            extend(chosen + [v], [w for w in cand[i + 1:] if w not in adj[v]])
    extend([], V)
    print("%d vertices, %d arcs, %d transitive triangles, independent %d-set: %s" % (len(V), len(arcs), tt, m, found[0] if found else "none"))
    return tt == 0 and not found

if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1]) else 1)
