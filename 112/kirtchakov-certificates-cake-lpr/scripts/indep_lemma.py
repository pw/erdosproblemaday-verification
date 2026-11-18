#!/usr/bin/env python3
"""Our encoder for the two lemma formulas, from the definitions, compared as clause sets with his gen_cnf.py output.
(a,b,N): oriented graphs on N vertices with no independent a-set and no transitive b-tournament.
Clauses: at most one direction per pair; for each a-set, at least one arc inside; for each b-set and each order of it,
not all forward arcs.  Usage: indep_lemma.py a b N file.cnf"""
import sys, itertools
a, b, N, f = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
pairs = list(itertools.combinations(range(N), 2)); idx = {p: i for i, p in enumerate(pairs)}
arc = lambda u, v: 2 * idx[(u, v)] + 1 if u < v else 2 * idx[(v, u)] + 2
E = {frozenset((-arc(x, y), -arc(y, x))) for x, y in pairs}
E |= {frozenset(arc(u, v) for u in S for v in S if u != v) for S in itertools.combinations(range(N), a)}
E |= {frozenset(-arc(o[i], o[j]) for i in range(b) for j in range(i + 1, b)) for S in itertools.combinations(range(N), b) for o in itertools.permutations(S)}
got = [frozenset(map(int, l.split()[:-1])) for l in open(f) if l[0] not in 'cp']
hdr = [l.split() for l in open(f) if l.startswith('p')][0]
print(f, 'EQUAL' if set(got) == E and len(got) == len(set(got)) and int(hdr[3]) == len(got) else 'DIFF', len(E), len(got))
