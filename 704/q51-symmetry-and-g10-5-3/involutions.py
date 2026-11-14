"""Involution symmetries of a 39-colouring of J(13,5,3) are impossible: fixed-set count.
For every involution t in Aut(W): cycle type on the 13 points, # five-sets of W fixed by t (phi), and the total number of
five-subsets of [13] fixed by a permutation of that cycle type. A t-fixed five-set lies in a t-invariant class, and t acts on that
class as an element of its automorphism group with the same cycle type, so  #fixed five-sets = (#invariant classes) * phi."""
import json
from itertools import combinations
from math import comb
from wstruct import WA
auts = [tuple(p) for p in json.load(open('orbits.json'))['auts']]
assert len(auts) == 48 and all({frozenset(p[x] for x in s) for s in WA} == WA for p in auts)
V = [frozenset(c) for c in combinations(range(13), 5)]
rows = {}
for p in auts:
    if p == tuple(range(13)): continue
    order2 = all(p[p[x]] == x for x in range(13))
    order3 = all(p[p[p[x]]] == x for x in range(13))
    k2 = sum(1 for x in range(13) if p[x] != x) // 2
    fixW = sum(1 for s in WA if frozenset(p[x] for x in s) == s)
    fixall = sum(1 for s in V if frozenset(p[x] for x in s) == s)
    if order2:
        formula = sum(comb(k2, j) * comb(13 - 2 * k2, 5 - 2 * j) for j in range(3) if 5 - 2 * j >= 0)
        assert formula == fixall
        rows.setdefault(('2^%d' % k2, fixW, fixall), 0); rows[('2^%d' % k2, fixW, fixall)] += 1
    elif order3:
        k3 = sum(1 for x in range(13) if p[x] != x) // 3
        rows.setdefault(('3^%d' % k3, fixW, fixall), 0); rows[('3^%d' % k3, fixW, fixall)] += 1
    else:
        rows.setdefault(('other', fixW, fixall), 0); rows[('other', fixW, fixall)] += 1
print('cycle type | #elements of Aut(W) | fixed sets inside W (phi) | fixed five-sets of [13] | divisible?')
for (ty, fw, fa), cnt in sorted(rows.items()):
    div = '-' if fw == 0 else ('YES' if fa % fw == 0 else 'no  (%d = %d*%d + %d)' % (fa, fw, fa // fw, fa % fw))
    print(f'{ty:6s} | {cnt:2d} | {fw:2d} | {fa:3d} | {div}')
