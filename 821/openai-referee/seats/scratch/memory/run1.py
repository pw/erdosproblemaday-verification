import sys, time
from fractions import Fraction as Fr
import field as F
from model import Toy
RAW = frozenset(); CMP = frozenset({0})
def show(tag, toy, brute=False):
    t = time.time()
    L = toy.lhs(brute=brute); n = toy._npaths
    R = toy.rhs_full()
    print(f"{tag}: paths={n}  LHS={F.fmt(L)}\n   RHS={F.fmt(R)}\n   equal={L==R}  LHS~{F.approx(L):.6g} RHS~{F.approx(R):.6g}  ({time.time()-t:.1f}s)", flush=True)
    return L, R
toy = Toy([5,7,11], 1, 1, [RAW], 2, Fr(1,4), Fr(3,4), 1, [1,1])
Lb = toy.lhs(brute=True); Ls = toy.lhs(brute=False)
print("brute-force residue average == per-prime shortcut:", Lb == Ls, F.approx(Lb))
show("raw N=2 P={5,7,11} q=1/4 rho=3/4 th=1/8 k=1", toy)
