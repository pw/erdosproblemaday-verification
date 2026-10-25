# Control for the per-prime residue shortcut _Ey: compare with honest Haar average over prod Z/pZ on sampled paths.
import random
from fractions import Fraction as Fr
import field as F
from model import Toy
t = Toy([5,7,17,19],1,1,[frozenset()],2,Fr(1,2),Fr(9,10),1,[1,1],seed=11)
paths = []
orig = t._lhs_rec
def rec(i, lists, hs, w, brute, pats):
    if i == t.N: paths.append((list(lists), list(hs))); return
    return orig(i, lists, hs, w, brute, pats)
t._lhs_rec = rec; t.lhs()
rnd = random.Random(5)
nz = [p for p in paths if t._Ey(*p) != F.ZERO]
sample = rnd.sample(nz, 12) + rnd.sample([p for p in paths if t._Ey(*p) == F.ZERO], 4)
bad = 0
for lists, hs in sample:
    a = t._Ey(lists, hs); b = t._Ey_brute(lists, hs)
    if a != b: bad += 1; print("MISMATCH", lists, hs, F.fmt(a), F.fmt(b))
print(f"sampled {len(sample)} paths ({len(nz)} nonzero of {len(paths)}): mismatches = {bad}")
