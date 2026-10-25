#!/usr/bin/env python3
"""Gap-6 check (ours, 2026-10-21): does Robb's explanation reproduce the module headers' source_cnf_sha256?
Claim: pysat IDPool numbered edge vars by FIRST USE (the 315 leading unit clauses = 21 high-high + 294 low-high,
then the C4 loop), while the Lean CNF uses lexicographic orderFortyNineEdgeIndex (vars 1..1176). Same clauses,
same order. Test: rename vars in our Lean-rendered DIMACS by first use over the whole file (edge vars only,
aux vars > 1176 untouched — tried both ways), re-hash, compare to the header."""
import sys, hashlib, re
NE = 1176
def render(clauses, header):
    out = [header]
    for c in clauses: out.append(" ".join(map(str, c)) + " 0")
    return ("\n".join(out) + "\n").encode()
def load(p):
    L = open(p).read().split("\n")
    hdr = L[0]; cl = []
    for ln in L[1:]:
        if not ln.strip(): continue
        t = list(map(int, ln.split())); assert t[-1] == 0; cl.append(t[:-1])
    return hdr, cl
def firstuse(cl, scope):
    m = {}; nxt = 1
    for c in cl:
        for l in c:
            v = abs(l)
            if v <= scope and v not in m: m[v] = nxt; nxt += 1
    for v in range(1, scope + 1):
        if v not in m: m[v] = nxt; nxt += 1
    return m
def apply(cl, m):
    return [[(1 if l > 0 else -1) * m.get(abs(l), abs(l)) for l in c] for c in cl]
p, want = sys.argv[1], sys.argv[2]
hdr, cl = load(p)
orig = hashlib.sha256(render(cl, hdr)).hexdigest()
m = firstuse(cl, NE)
moved = sum(1 for v in range(1, NE + 1) if m[v] != v)
h = hashlib.sha256(render(apply(cl, m), hdr)).hexdigest()
print(f"{p}\trender_roundtrip={'same' if orig==hashlib.sha256(open(p,'rb').read()).hexdigest() else 'DIFF'}\tmoved={moved}\tfirstuse_sha={h[:16]}\tmatch={h==want}")
