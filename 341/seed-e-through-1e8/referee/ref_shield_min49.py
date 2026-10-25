#!/usr/bin/env python3
"""Minimise |D| + 2|B| over Li-Lemma-3.1 shields at M=49 for both 3-cycles (seed = D u B u (49+B) u R, |R|>=3, Li uses 4)."""
import sys; sys.path.insert(0,'.')
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
import ref_shield_union as U
def build(M,P):
    # reuse U.solve's clause construction by monkeypatching the solver call
    import pysat.solvers as S
    captured={}
    class Fake:
        def __init__(self,bootstrap_with): captured['cl']=bootstrap_with
        def __enter__(self): return self
        def __exit__(self,*a): pass
        def solve(self): return False
    old=U.Cadical195; U.Cadical195=Fake
    vids={}
    def extra(b,d,R):
        for r in R: vids[r]=(b(r),d(r))
        return []
    U.solve(M,P,extra=extra); U.Cadical195=old
    return captured['cl'],vids
for P in ([7,14,28],[21,42,35]):
    cl,v=build(49,P); w=WCNF()
    for c in cl: w.append(c)
    for r,(bb,dd) in v.items(): w.append([-bb],weight=2); w.append([-dd],weight=1)
    with RC2(w) as rc:
        m=rc.compute(); m=set(l for l in m if l>0)
        B=sorted(r for r,(bb,dd) in v.items() if bb in m); D=sorted(r for r,(bb,dd) in v.items() if dd in m)
        print(f"P={P}: min |D|+2|B| = {rc.cost}  B={B} D={D}  -> seed size >= {rc.cost}+|R| (Li: 7+10=17, +4 = 21)")
