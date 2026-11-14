"""Independent checker for a claimed proper colouring of J(n,5,3) given as a list of classes (lists of 5-sets).
No code shared with the search. Checks: every class independent (no two sets share exactly 3), classes pairwise disjoint,
union = all C(n,5) sets; prints class count and sizes. Usage: verify_colouring.py file.json n [key]"""
import sys, json
from itertools import combinations
from math import comb
d = json.load(open(sys.argv[1])); n = int(sys.argv[2])
classes = d['classes'] if isinstance(d, dict) else d
seen = set(); ok = True
for c in classes:
    sets = [tuple(sorted(s)) for s in c]
    for s in sets:
        if len(set(s)) != 5 or min(s) < 0 or max(s) >= n or s in seen: ok = False
        seen.add(s)
    for a, b in combinations(sets, 2):
        if len(set(a) & set(b)) == 3: ok = False
print('classes', len(classes), 'sizes', sorted(set(len(c) for c in classes)), 'sets covered', len(seen), 'of', comb(n, 5), '| PROPER COLOURING:', ok and len(seen) == comb(n, 5))
