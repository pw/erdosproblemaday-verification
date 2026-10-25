from fractions import Fraction as Fr
import field as F
from model import Toy
RAW = frozenset(); CMP = frozenset({0})
t = Toy([5,7,11],1,1,[RAW,CMP],2,Fr(1,2),Fr(9,10),1,[1,1],seed=3)
print("qv:", [F.fmt(x) for x in t.qv])
print("b:", {p: F.fmt(v) for p, v in t.b.items()})
# instrument: per-path contributions, see if sqrt2 parts appear and cancel
import itertools
tot_sqrt2 = Fr(0); n_irr = 0; n = 0
orig = t._lhs_rec
contribs = []
def rec(i, lists, hs, w, brute):
    if i == t.N:
        Efac = t._Ey(lists, hs); ph = F.e8(t.th*hs[-1])
        c = F.mul(F.mul(w, Efac), ph)
        contribs.append((tuple(lists), tuple(hs), c))
        return
    return orig(i, lists, hs, w, brute)
t._lhs_rec = rec
# monkeypatch recursion: orig calls self._lhs_rec -> rec
L = t.lhs()
irr = [c for c in contribs if c[2][1] != 0 or c[2][3] != 0]
print("paths", len(contribs), "with sqrt2 part:", len(irr))
s = [Fr(0)]*4
for _,_,c in irr:
    for k in range(4): s[k] += c[2][k] if False else c[k] if False else 0
tot = F.ZERO
for _,_,c in irr: tot = F.add(tot, c)
print("sum of irrational-part paths:", F.fmt(tot))
for lists, hs, c in irr[:6]: print(lists, hs, F.fmt(c))
