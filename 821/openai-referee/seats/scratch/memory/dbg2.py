from fractions import Fraction as Fr
import field as F
from model import Toy
RAW = frozenset()
t = Toy([5,7,11,13],1,1,[RAW],4,Fr(1,2),Fr(9,10),1,[1,1,1,1],seed=9)
orig = t._lhs_rec; contribs = []
def rec(i, lists, hs, w, brute):
    if i == t.N:
        c = F.mul(F.mul(w, t._Ey(lists, hs)), F.e8(t.th*hs[-1]))
        contribs.append((tuple(lists), tuple(hs), c)); return
    return orig(i, lists, hs, w, brute)
t._lhs_rec = rec
L = t.lhs()
nz = [c for c in contribs if c[2] != F.ZERO]
irr = [c for c in nz if c[2][1] != 0 or c[2][3] != 0]
print("paths", len(contribs), "nonzero", len(nz), "with sqrt2 part", len(irr))
tot = F.ZERO
for c in irr: tot = F.add(tot, c[2])
print("sum over sqrt2-carrying paths:", F.fmt(tot))
for c in irr[:5]: print(c[0], c[1], F.fmt(c[2]))
