#!/usr/bin/env python3
"""Batch form of indep_encode.py (same expected clause set; the base encoding is cached per N).
Also checks the block inventories: every I3L3 file is an oriented graph with no independent triple and no
transitive triple; every TT4F file is a tournament with no transitive 4-subtournament; files of one size are
pairwise non-isomorphic (brute force).  Our October enumeration (enum_types.py, independent SAT + canonical
form) found 25/31/7/1 and 3/3/1/1 classes; equal counts + validity + non-isomorphism = a complete system."""
import sys, os, json, itertools
sys.path.insert(0, os.getcwd())
from verify_chain import I3L3, TT4F
def arcs_of(fn):
    d = json.load(open(fn)); return d['N'], set(map(tuple, d['arcs']))
def oriented(k, A): return all(not ((u, v) in A and (v, u) in A) for u, v in A) and all(u != v and 0 <= u < k and 0 <= v < k for u, v in A)
def adj(A, u, v): return (u, v) in A or (v, u) in A
def no_I(k, A, r): return all(any(adj(A, u, v) for u, v in itertools.combinations(t, 2)) for t in itertools.combinations(range(k), r))
def no_TT(k, A, r): return not any(all((o[i], o[j]) in A for i in range(r) for j in range(i + 1, r)) for t in itertools.combinations(range(k), r) for o in itertools.permutations(t))
def iso(k, A, B): return len(A) == len(B) and any(all((pm[u], pm[v]) in B for u, v in A) for pm in itertools.permutations(range(k)))
ok = True
for fam, kind in ((I3L3, 'I3L3'), (TT4F, 'TT4F')):
    for k, files in sorted(fam.items()):
        G = [arcs_of(f) for f in files]
        assert all(m == k for m, _ in G)
        if kind == 'I3L3': valid = all(oriented(k, A) and no_I(k, A, 3) and no_TT(k, A, 3) for _, A in G)
        else: valid = all(oriented(k, A) and no_I(k, A, 2) and no_TT(k, A, 4) for _, A in G)
        noniso = all(not iso(k, G[i][1], G[j][1]) for i in range(len(G)) for j in range(i + 1, len(G)))
        print(kind, k, 'classes', len(G), 'valid', valid, 'pairwise-non-isomorphic', noniso, flush=True); ok &= valid and noniso
base = {}
def arcf(N):
    pairs = list(itertools.combinations(range(N), 2)); idx = {pr: i for i, pr in enumerate(pairs)}
    return pairs, (lambda u, v: 2 * idx[(u, v)] + 1 if u < v else 2 * idx[(v, u)] + 2)
def base_set(N):
    if N in base: return base[N]
    pairs, arc = arcf(N); E = set()
    for a, b in pairs: E.add(frozenset((-arc(a, b), -arc(b, a))))
    for t in itertools.combinations(range(N), 3): E.add(frozenset(arc(u, v) for u in t for v in t if u != v))
    for f in itertools.combinations(range(N), 4):
        for o in itertools.permutations(f): E.add(frozenset(-arc(o[i], o[j]) for i in range(4) for j in range(i + 1, 4)))
    base[N] = (E, pairs, arc); return base[N]
cnfdir = sys.argv[1]; res = {'EQUAL': 0, 'DIFF': 0}
for line in open('cubes.txt'):
    name, N, p, q, s, pf, qf, sf = line.split(); N, p, q, s = map(int, (N, p, q, s))
    E, pairs, arc = base_set(N); U = set()
    def fix(u, v, st):
        if st == 'uv': U.update({frozenset((arc(u, v),)), frozenset((-arc(v, u),))})
        elif st == 'vu': U.update({frozenset((arc(v, u),)), frozenset((-arc(u, v),))})
        else: U.update({frozenset((-arc(u, v),)), frozenset((-arc(v, u),))})
    for x in range(1, N): fix(0, x, 'uv' if x <= p else ('vu' if x <= p + q else 'none'))
    for fn, off, k in ((pf, 1, p), (qf, 1 + p, q), (sf, 1 + p + q, s)):
        if k == 0: continue
        m, A = arcs_of(fn); assert m == k
        for u, v in itertools.combinations(range(k), 2): fix(u + off, v + off, 'uv' if (u, v) in A else ('vu' if (v, u) in A else 'none'))
    got = []; hdr = None
    for l in open(os.path.join(cnfdir, name + '.cnf')):
        if l[0] == 'c': continue
        if l[0] == 'p': hdr = l.split(); continue
        z = l.split(); assert z[-1] == '0'; got.append(frozenset(map(int, z[:-1])))
    gs = set(got); exp_all = E | U
    eq = gs == exp_all and len(got) == len(gs) and int(hdr[3]) == len(got) and int(hdr[2]) == 2 * len(pairs)
    res['EQUAL' if eq else 'DIFF'] += 1
    print(name, 'EQUAL' if eq else 'DIFF', len(exp_all), len(got), flush=True)
print('SUMMARY', res, 'inventories_ok', ok)
