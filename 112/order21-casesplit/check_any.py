#!/usr/bin/env python3
"""Definition-level check of a claimed order-N (I_3,L_4)-free oriented graph given as a cadical
model (v-lines) for one of our case CNFs. Independent of pysat: decodes the fixed variable
numbering (first 3*C(N,2) vars are f(u,v), r(u,v)=f(v,u), n(u,v) in pair order), rebuilds the
graph, and checks: antisymmetry, no independent triple, no transitive 4-tournament."""
import sys, itertools
N = int(__import__("os").environ.get("ORDER", "21"))
P = list(itertools.combinations(range(N), 2))
idx = {}
k = 1
for u, v in P:
    idx[("f", u, v)] = k; idx[("r", u, v)] = k + 1; idx[("n", u, v)] = k + 2; k += 3
true = set()
for line in open(sys.argv[1]):
    if line.startswith("v"):
        for t in line.split()[1:]:
            x = int(t)
            if x > 0: true.add(x)
arc = set(); none = set()
for u, v in P:
    f, r, n = idx[("f", u, v)] in true, idx[("r", u, v)] in true, idx[("n", u, v)] in true
    assert f + r + n == 1, (u, v, f, r, n)
    if f: arc.add((u, v))
    elif r: arc.add((v, u))
    else: none.add((u, v))
bad_i3 = [t for t in itertools.combinations(range(N), 3) if all(tuple(sorted(e)) in none for e in itertools.combinations(t, 2))]
bad_tt4 = [S for S in itertools.combinations(range(N), 4) if any(all((o[i], o[j]) in arc for i in range(4) for j in range(i+1, 4)) for o in itertools.permutations(S))]
print(f"arcs={len(arc)} nonedges={len(none)} independent_triples={len(bad_i3)} transitive_4={len(bad_tt4)}")
print("WITNESS VALID" if not bad_i3 and not bad_tt4 else "WITNESS INVALID")
sys.exit(0 if not bad_i3 and not bad_tt4 else 1)
