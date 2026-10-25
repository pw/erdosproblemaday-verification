"""Referee: the closed-form Klein set at q=11 (Seceleanu 2014 coordinates, c=4, cbar=-1-c=6), printed and re-checked."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpg
p = 11; c = 4; cb = (-1 - c) % p
assert (c * c + c + 2) % p == 0 and (cb * cb + cb + 2) % p == 0
base = [(1, 0, 0)] + [(1, s, 0) for s in (1, p - 1)] + [(1, s, (t * cb) % p) for s in (1, p - 1) for t in (1, p - 1)]
K = sorted({rpg.norm(pm, p) for v in base for pm in itertools.permutations(v)})
pts, idx, lines, inc = rpg.plane(p)
print(f"c={c}, cbar={cb}; |K|={len(K)}; spectrum {rpg.spectrum([idx[P] for P in K], inc)}")
print("K =", K)
