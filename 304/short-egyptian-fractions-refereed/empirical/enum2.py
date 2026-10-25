#!/usr/bin/env python3
"""Route B (independent of enum1.py): k-term distinct expansions of 1 by plain recursion over Fractions, every term in a loop
(no divisor trick, no gcd bookkeeping), k<=6. Erdős #148/#293 cross-check, 18:00Z erdos seat 2026-10-21."""
from fractions import Fraction as Fr
import sys
K=int(sys.argv[1]) if len(sys.argv)>1 else 6
def gen(r,j,prev):
    if j==0:
        if r==0: yield ()
        return
    if r<=0: return
    if j==1:
        if r.numerator==1 and r.denominator>prev: yield (r.denominator,)
        return
    n=max(prev+1, int(1/r) if 1/r==int(1/r) else int(1/r)+1)
    while Fr(j,n)>=r:   # j/n >= r needed (terms strictly decreasing, so actually > unless j=1)
        for t in gen(r-Fr(1,n),j-1,n): yield (n,)+t
        n+=1
for k in range(1,K+1):
    E=list(gen(Fr(1),k,0))
    D={n for e in E for n in e if n>=2}; v=2
    while v in D: v+=1
    print(f"k={k} F={len(E)} v={v} |D|={len(D)}",flush=True)
