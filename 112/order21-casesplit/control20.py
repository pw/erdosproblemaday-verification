#!/usr/bin/env python3
"""Targeted positive control for the order-21 case split: take a KNOWN 20-vertex (I_3,L_4)-free witness
(cyclic, connection set from the August report), verify it from the definition, find its root profile and
the isomorphism types of N^+(0), N^-(0), N^0(0) by canonical matching against types.json, build exactly that
case with the SAME generator at ORDER=20, and require cadical to return SAT with a model that validates."""
import os, sys, json, itertools, subprocess
os.environ["ORDER"] = "20"
sys.path.insert(0, "/home/exedev/MathDyad/erdos112")
N = 20
C = [1, 2, 4, 14, 15, 17]                       # i -> i+c (mod 20)
arcs = set((i, (i + c) % N) for i in range(N) for c in C)
assert all((v, u) not in arcs for u, v in arcs), "not an oriented graph"
def arc(u, v): return (u, v) in arcs
def free_check(V):
    for a, b, c in itertools.combinations(V, 3):
        if not (arc(a,b) or arc(b,a) or arc(a,c) or arc(c,a) or arc(b,c) or arc(c,b)): return "I3 " + str((a,b,c))
    for S in itertools.combinations(V, 4):
        for o in itertools.permutations(S):
            if all(arc(o[i], o[j]) for i in range(4) for j in range(i+1, 4)): return "L4 " + str(o)
    return None
assert free_check(range(N)) is None, free_check(range(N))
print("witness C=", C, "is (I3,L4)-free on 20 vertices: OK")
out = sorted(v for v in range(N) if arc(0, v)); inn = sorted(v for v in range(N) if arc(v, 0)); non = sorted(v for v in range(1, N) if not arc(0, v) and not arc(v, 0))
print("root profile of vertex 0:", (len(out), len(inn), len(non)))
T = json.load(open("types.json"))
def canon_of(verts, tournament):
    k = len(verts); best = None
    for p in itertools.permutations(range(k)):
        key = tuple(sorted((p[i], p[j]) for i in range(k) for j in range(k) if i != j and arc(verts[i], verts[j])))
        if best is None or key < best: best = key
    return best
def type_index(verts, kind):
    k = len(verts); key = canon_of(verts, kind == "T")
    for idx, typ in enumerate(T[kind][str(k)]):
        # canonical form of the stored representative under the same convention
        a = set(tuple(x) for x in typ["arcs"]); best = None
        for p in itertools.permutations(range(k)):
            kk = tuple(sorted((p[i], p[j]) for i, j in a))
            if best is None or kk < best: best = kk
        if best == key: return idx
    raise SystemExit(f"type not found for {kind} {k} -- types.json incomplete?!")
ti, tj, tk = type_index(out, "N"), type_index(inn, "N"), type_index(non, "T")
print("types: N+ idx", ti, "N- idx", tj, "N0 idx", tk)
import cases_any
prof = (len(out), len(inn), len(non))
if prof[0] < prof[1]:  # generator assumes out >= in; reverse all arcs instead
    arcs = set((v, u) for u, v in arcs); out, inn = inn, out; prof = (prof[1], prof[0], prof[2]); ti, tj = tj, ti
cnf, var = cases_any.build(prof, ti, tj, tk)
cnf.to_file("control20_case.cnf"); print("case CNF written: vars", var.pool.top, "clauses", len(cnf.clauses))
r = subprocess.run(["cadical", "-q", "control20_case.cnf"], capture_output=True, text=True)
open("control20_case.out", "w").write(r.stdout)
print("cadical exit", r.returncode, "(10=SAT)")
if r.returncode == 10:
    v = subprocess.run([sys.executable, "check_any.py", "control20_case.out"], capture_output=True, text=True, env={**os.environ, "ORDER": "20"})
    print(v.stdout.strip())
