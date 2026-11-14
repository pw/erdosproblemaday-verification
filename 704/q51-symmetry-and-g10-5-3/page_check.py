"""Read the three families of digit strings straight out of the page HTML, apply the 7 shifts, check it is a proper 21-colouring
of G(10,5,3). (The page text itself must be a certificate.)"""
import re, sys
from itertools import combinations
html = open(sys.argv[1]).read()
fams = re.findall(r'<li>((?:\d{5}, )+\d{5});</li>|<li>((?:\d{5}, )+\d{5})\.</li>', html)
fams = [(a or b).split(', ') for a, b in fams]
assert len(fams) == 3 and all(len(f) == 12 for f in fams), (len(fams), [len(f) for f in fams])
classes = []
for f in fams:
    sets = [frozenset(int(ch) for ch in w) for w in f]
    assert all(len(s) == 5 for s in sets)
    for t in range(7):
        classes.append([frozenset((x + t) % 7 if x < 7 else x for x in s) for s in sets])
allsets = [s for c in classes for s in c]
ok = (len(classes) == 21 and len(set(allsets)) == 252 and set(allsets) == {frozenset(c) for c in combinations(range(10), 5)}
      and all(len(a & b) != 3 for c in classes for a, b in combinations(c, 2)))
print('page families parsed:', [len(f) for f in fams], '| 21 classes, 252 distinct sets, proper:', ok)
