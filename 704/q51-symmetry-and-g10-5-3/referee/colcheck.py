# Referee checker for proper colourings of J(n,5,3), written from the definition only.
import json, sys
from itertools import combinations
fn, n = sys.argv[1], int(sys.argv[2])
d = json.load(open(fn)); cl = d['classes']
print(fn, 'classes in file:', len(cl), 'sizes:', sorted({len(c) for c in cl}))
allsets = [tuple(c) for c in combinations(range(n), 5)]
seen = {}
bad = 0
for k, c in enumerate(cl):
    S = [frozenset(x) for x in c]
    assert all(len(s) == 5 and all(isinstance(e, int) and 0 <= e < n for e in s) for s in S), 'malformed set'
    assert len(set(S)) == len(S), 'duplicate in class'
    for s in S:
        assert s not in seen, ('set in two classes', sorted(s)); seen[s] = k
    for x, y in combinations(S, 2):
        if len(x & y) == 3: bad += 1
cover = len(seen) == len(allsets) and all(frozenset(t) in seen for t in allsets)
print('#classes', len(cl), '| union = all %d five-sets:' % len(allsets), cover, '| monochromatic edges:', bad,
      '| VALID' if cover and bad == 0 else '| INVALID')
