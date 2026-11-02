"""Seat C: re-verify every dumped system with checker.py (both minimality tests), and check the
paper's structural claims in 8.1 (the 24 = images of (1) under z -> +-z+b; the five moduli sets of the 216)."""
import sys, os
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checker

def load(path):
    out = []
    for line in open(path):
        if line.startswith('SYS'):
            out.append(tuple(sorted(((int(t.split('/')[0]), int(t.split('/')[1])) for t in line.split()[1:]), key=lambda p: p[1])))
    return out

def canon(S):
    return tuple(sorted(((a % n, n) for a, n in S), key=lambda p: (p[1], p[0])))

path = sys.argv[1]
S = load(path)
print('systems loaded:', len(S), ' distinct:', len(set(canon(s) for s in S)))
bad = [s for s in S if not (checker.accept(list(s)) and checker.minimal_subfamily(list(s)))]
print('failing re-verification (accept + subfamily-minimality):', len(bad))
print('moduli sets:', dict(Counter(tuple(n for a, n in s) for s in S)))
print('class counts:', dict(Counter(len(s) for s in S)))
# orbit of (1) under z -> e*z + b
base = [(0, 2), (0, 3), (1, 4), (5, 6), (7, 12)]
orb = set()
for e in (1, -1):
    for b in range(12):
        orb.add(canon([((e * a + b), n) for a, n in base]))
sub = set(canon(s) for s in S if max(n for a, n in s) <= 12)
print('systems with moduli <= 12:', len(sub), ' orbit of (1) under z->+-z+b has', len(orb), 'elements; equal:', sub == orb)
