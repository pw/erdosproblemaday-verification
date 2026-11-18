#!/usr/bin/env python3
"""Our own encoder for one cube of the k(3,4) chain, written from the definitions, compared clause-set
by clause-set with Kirtchakov's CNF.  Semantics (read from his docstring, re-derived here): for a<b the
literal 2i+1 means arc a->b and 2i+2 means arc b->a (i = index of (a,b) in combinations(range(N),2)).
Expected clauses: (1) at most one direction per pair; (2) no independent triple; (3) no transitive
4-tournament (one clause per 4-set and per linear order); (4) two units per fixed pair: vertex 0 to
everyone (out 1..p, in p+1..p+q, non-adjacent rest) and every pair inside a block (arc from the block
file, else non-adjacent).  Usage: indep_encode.py name N p q s pf qf sf cnf  -> prints EQUAL / DIFF."""
import sys, json, itertools
name, N, p, q, s, pf, qf, sf, cnf = sys.argv[1], *map(int, sys.argv[2:6]), *sys.argv[6:10]
pairs = list(itertools.combinations(range(N), 2)); idx = {pr: i for i, pr in enumerate(pairs)}
def arc(u, v):  # literal "u -> v"
    return 2 * idx[(u, v)] + 1 if u < v else 2 * idx[(v, u)] + 2
exp = set()
for (a, b) in pairs:
    exp.add(frozenset((-arc(a, b), -arc(b, a))))
for t in itertools.combinations(range(N), 3):
    exp.add(frozenset(arc(u, v) for u in t for v in t if u != v))
for f in itertools.combinations(range(N), 4):
    for o in itertools.permutations(f):
        exp.add(frozenset(-arc(o[i], o[j]) for i in range(4) for j in range(i + 1, 4)))
def fix(u, v, state):  # state: 'uv', 'vu', 'none'
    if state == 'uv': exp.update({frozenset((arc(u, v),)), frozenset((-arc(v, u),))})
    elif state == 'vu': exp.update({frozenset((arc(v, u),)), frozenset((-arc(u, v),))})
    else: exp.update({frozenset((-arc(u, v),)), frozenset((-arc(v, u),))})
for x in range(1, N):
    fix(0, x, 'uv' if x <= p else ('vu' if x <= p + q else 'none'))
def block(fn, off, k):
    d = json.load(open(fn)); assert d['N'] == k, (fn, d['N'], k)
    A = set(map(tuple, d['arcs']))
    for u, v in itertools.combinations(range(k), 2):
        fix(u + off, v + off, 'uv' if (u, v) in A else ('vu' if (v, u) in A else 'none'))
block(pf, 1, p); block(qf, 1 + p, q)
if s: block(sf, 1 + p + q, s)
got = []; hdr = None
for line in open(cnf):
    if line.startswith('c'): continue
    if line.startswith('p'): hdr = line.split(); continue
    lits = list(map(int, line.split())); assert lits[-1] == 0; got.append(frozenset(lits[:-1]))
gs = set(got)
ok = (gs == exp and len(got) == len(gs) and int(hdr[3]) == len(got) and int(hdr[2]) == 2 * len(pairs))
print(name, 'EQUAL' if ok else 'DIFF', len(exp), len(gs), len(got), len(exp - gs), len(gs - exp))
