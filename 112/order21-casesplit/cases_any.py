#!/usr/bin/env python3
"""Lossless case split for a hypothetical 21-vertex (I_3,L_4)-free oriented graph.

Root vertex 0 has out-/in-/non-neighbourhoods of sizes (p,q,r), p+q+r=20, p<=8, q<=8, r<=7
(k(3,3)=9 and every 8-tournament contains TT_4); up to reversing all arcs, p>=q.
N^+(0) and N^-(0) are (I_3,L_3)-free oriented graphs; N^0(0) is an L_4-free tournament.
types.json lists EVERY isomorphism type of each (enum_types.py, with controls). Fixing each
part to one labelled representative of each type is lossless (relabel within the part).
For every (profile, type triple) this writes one DIMACS CNF whose only free decisions are the
cross-part pair states. SAT => explicit witness => k(3,4) >= 22. All UNSAT (with DRAT proofs)
=> no order-21 witness => k(3,4) = 21.
"""
import json, itertools, os, sys
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool

ORDER = int(__import__("os").environ.get("ORDER", "21"))
PROFILES = [(p,q,ORDER-1-p-q) for p in range(8,2,-1) for q in range(p,2,-1) if 1 <= ORDER-1-p-q <= 7]
T = json.load(open(os.path.join(os.path.dirname(__file__), "types.json")))

class V:
    def __init__(s): s.pool = IDPool()
    def fwd(s, u, v):
        assert u != v
        return s.pool.id(("f", u, v)) if u < v else s.pool.id(("r", v, u))
    def none(s, u, v): a, b = sorted((u, v)); return s.pool.id(("n", a, b))

def base(cnf, var):
    for u, v in itertools.combinations(range(ORDER), 2):
        f, r, z = var.fwd(u, v), var.fwd(v, u), var.none(u, v)
        cnf.append([f, r, z]); cnf.append([-f, -r]); cnf.append([-f, -z]); cnf.append([-r, -z])
    for a, b, c in itertools.combinations(range(ORDER), 3):
        cnf.append([-var.none(a, b), -var.none(a, c), -var.none(b, c)])
    for S in itertools.combinations(range(ORDER), 4):
        for o in itertools.permutations(S):
            cnf.append([-var.fwd(o[i], o[j]) for i in range(4) for j in range(i+1, 4)])
    for u in range(ORDER):  # valid redundant bounds: out<=8, in<=8, non<=7
        others = [v for v in range(ORDER) if v != u]
        for lits, bound in (([var.fwd(u, v) for v in others], 8), ([var.fwd(v, u) for v in others], 8), ([var.none(u, v) for v in others], 7)):
            cnf.extend(CardEnc.atmost(lits=lits, bound=bound, vpool=var.pool, encoding=EncType.seqcounter).clauses)

def fix_part(cnf, var, verts, typ):
    """typ = {'n':k,'arcs':[[i,j],...]} on labels 0..k-1 -> impose on verts (ordered list)."""
    k = typ["n"]; assert len(verts) == k
    arcs = set((a, b) for a, b in typ["arcs"])
    for i, j in itertools.combinations(range(k), 2):
        u, v = verts[i], verts[j]
        if (i, j) in arcs: cnf.append([var.fwd(u, v)])
        elif (j, i) in arcs: cnf.append([var.fwd(v, u)])
        else: cnf.append([var.none(u, v)])

def build(profile, ti, tj, tk):
    p, q, r = profile
    out = list(range(1, 1 + p)); inn = list(range(1 + p, 1 + p + q)); non = list(range(1 + p + q, ORDER))
    cnf = CNF(); var = V()
    base(cnf, var)
    for v in out: cnf.append([var.fwd(0, v)])
    for v in inn: cnf.append([var.fwd(v, 0)])
    for v in non: cnf.append([var.none(0, v)])
    fix_part(cnf, var, out, T["N"][str(p)][ti])
    fix_part(cnf, var, inn, T["N"][str(q)][tj])
    fix_part(cnf, var, non, T["T"][str(r)][tk])
    return cnf, var

def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "cases"
    os.makedirs(outdir, exist_ok=True)
    manifest = []
    for prof in PROFILES:
        p, q, r = prof
        for ti in range(len(T["N"][str(p)])):
            for tj in range(len(T["N"][str(q)])):
                for tk in range(len(T["T"][str(r)])):
                    name = f"p{p}{q}{r}_o{ti}_i{tj}_n{tk}"
                    cnf, var = build(prof, ti, tj, tk)
                    cnf.to_file(os.path.join(outdir, name + ".cnf"))
                    manifest.append({"name": name, "profile": prof, "types": [ti, tj, tk], "vars": var.pool.top, "clauses": len(cnf.clauses)})
    json.dump(manifest, open(os.path.join(outdir, "manifest.json"), "w"), indent=0)
    print(f"{len(manifest)} cases written to {outdir}/; vars~{manifest[0]['vars']} clauses~{manifest[0]['clauses']}")

if __name__ == "__main__":
    main()
