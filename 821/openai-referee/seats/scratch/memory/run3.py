import sys, time
from fractions import Fraction as Fr
import field as F
from model import Toy
RAW = frozenset(); CMP = frozenset({0})
def show(tag, toy):
    t = time.time()
    L = toy.lhs(); n = toy._npaths
    R = toy.rhs_full()
    irr = (L[1] != 0 or L[3] != 0)
    print(f"{tag}: paths={n} memo={len(toy.memo)} equal={L==R} sqrt2-part-present={irr} LHS~{F.approx(L):.6g} ({time.time()-t:.1f}s)\n   LHS={F.fmt(L)}\n   RHS={F.fmt(R)}", flush=True)
    return L, R
show("raw+cmp N=4 P={5,7,11} q=1/2 th=0 k=(1,2,3,1)", Toy([5,7,11],1,1,[RAW,CMP],4,Fr(1,2),Fr(9,10),0,[1,2,3,1],seed=6))
show("raw+cmp N=4 P={5,7,11} q=1/2 th=1/8 k=(1,1,1,1)", Toy([5,7,11],1,1,[RAW,CMP],4,Fr(1,2),Fr(9,10),1,[1,1,1,1],seed=7))
show("raw+cmp N=2 P={5,7,11,13} q=1/2 th=1/8 k=(1,1)", Toy([5,7,11,13],1,1,[RAW,CMP],2,Fr(1,2),Fr(9,10),1,[1,1],seed=8))
show("raw N=4 P={5,7,11,13} q=1/2 th=1/8 k=(1,1,1,1)", Toy([5,7,11,13],1,1,[RAW],4,Fr(1,2),Fr(9,10),1,[1,1,1,1],seed=9))
