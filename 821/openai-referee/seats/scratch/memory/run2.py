import sys, time
from fractions import Fraction as Fr
import field as F
from model import Toy
RAW = frozenset(); CMP = frozenset({0})
def show(tag, toy):
    t = time.time()
    L = toy.lhs(); n = toy._npaths
    R = toy.rhs_full()
    print(f"{tag}: paths={n} memo={len(toy.memo)}\n   LHS={F.fmt(L)}\n   RHS={F.fmt(R)}\n   equal={L==R}  LHS~{F.approx(L):.6g} RHS~{F.approx(R):.6g}  ({time.time()-t:.1f}s)", flush=True)
    return L, R
show("raw+cmp N=2 P={5,7,11} q=1/2 rho=9/10 th=1/8 k=(1,1)", Toy([5,7,11],1,1,[RAW,CMP],2,Fr(1,2),Fr(9,10),1,[1,1],seed=3))
show("raw+cmp N=2 P={5,7,11} q=1/4 rho=3/4 th=3/8 k=(2,3)", Toy([5,7,11],1,1,[RAW,CMP],2,Fr(1,4),Fr(3,4),3,[2,3],seed=4))
show("raw N=4 P={5,7,11} q=1/2 rho=9/10 th=1/8 k=(1,1,1,1)", Toy([5,7,11],1,1,[RAW],4,Fr(1,2),Fr(9,10),1,[1,1,1,1],seed=5))
show("raw+cmp N=4 P={5,7,11} q=1/2 rho=9/10 th=1/8 k=(1,2,3,1)", Toy([5,7,11],1,1,[RAW,CMP],4,Fr(1,2),Fr(9,10),1,[1,2,3,1],seed=6))
