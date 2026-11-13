"""Question 5.2 of the submission: are all maximum independent sets of J(13,5,3) equivalent under Sym(13)?
Input: the s=32 tree (every 33-set contains a 4-pair by P1, so WLOG contains v,u; orbital branching keeps at least
one image of every 33-set in some leaf, and clq3 enumerates ALL 31-cliques of every leaf). We canonicalise every
33-set found (pynauty on the point/set incidence graph) and report the isomorphism classes with |Aut|.
Usage: ~/.venv/bin/python classify.py runs/n13_s32_lg350 enum_output.txt"""
import sys, json
from itertools import combinations
from math import factorial
import pynauty
out, enum = sys.argv[1], sys.argv[2]
import os
V = [frozenset(c) for c in combinations(range(13), 5)]
if os.path.exists(out + '/forced.json'):      # the submission's tree: forced sets already include their v1
    F = {int(k): v for k, v in json.load(open(out + '/forced.json'))['F'].items()}
    EXTRA = []; solve_leaves = sorted(F)
else:
    man = json.load(open(out + '/manifest.json'))
    F = {L['id']: L['F'] for L in man['leaves']}
    EXTRA = [man['v'], man['u']]; solve_leaves = [L['id'] for L in man['leaves'] if L['status'] == 'SOLVE']
def cert(fam):
    adj = {i: [] for i in range(13 + len(fam))}
    for j, S in enumerate(fam):
        for x in S: adj[x].append(13 + j)
    g = pynauty.Graph(13 + len(fam), adjacency_dict=adj, vertex_coloring=[set(range(13)), set(range(13, 13 + len(fam)))])
    return pynauty.certificate(g), g
classes = {}; nsol = 0; done = {}; capped = []
for line in open(enum):
    t = line.split()
    if t[1] == 'DONE':
        done[int(t[0])] = t[2:]
        if 'CAPPED' in t: capped.append(int(t[0]))
        continue
    lid = int(t[0]); g = [int(x) - 1 for x in t[2:]] + F[lid] + EXTRA
    fam = [V[x] for x in g]
    assert len(set(g)) == 33 and all(len(a & b) != 3 for a, b in combinations(fam, 2))
    nsol += 1
    c, G = cert(fam)
    if c not in classes:
        gens, s1, s2, orbits, norb = pynauty.autgrp(G)
        aut = round(s1 * 10 ** s2)
        classes[c] = dict(count=0, aut=aut, example=[sorted(x + 1 for x in S) for S in fam], first_leaf=lid)
    classes[c]['count'] += 1
missing = [i for i in solve_leaves if i not in done]
print(f'solutions {nsol}  classes {len(classes)}  leaves_done {len(done)}/{len(solve_leaves)}  missing {len(missing)}  capped {capped}')
tot = 0
for c, d in sorted(classes.items(), key=lambda kv: kv[1]['aut']):
    n_lab = factorial(13) // d['aut']; tot += n_lab
    print(f"  |Aut| = {d['aut']:>8}  labelled copies = 13!/|Aut| = {n_lab:>12,}  found {d['count']:>7} times  e.g. leaf {d['first_leaf']}")
print('total maximum independent sets (labelled) =', f'{tot:,}')
json.dump([dict(aut=d['aut'], count=d['count'], example=d['example']) for d in classes.values()], open(out + '/classes.json', 'w'), indent=1)
