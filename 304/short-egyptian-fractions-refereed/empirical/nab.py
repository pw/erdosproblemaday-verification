#!/usr/bin/env python3
"""N(a,b) = least k with a/b = 1/n_1+...+1/n_k, 2<=n_1<...<n_k; N(b)=max_{1<=a<b} N(a,b). Exact (iterative deepening,
last two terms by divisors of q^2). Erdős #304 small-b table, 18:00Z erdos seat 2026-10-21."""
import sys
from math import gcd
from sympy import divisors
def has(p,q,j,prev):
    if j==1: return p==1 and q>prev
    if j==2:
        for d1 in divisors(q*q):
            if d1>=q: return False
            if (d1+q)%p==0 and (d1+q)//p>prev and (q*q//d1+q)%p==0: return True
        return False
    lo=max(prev+1,-(-q//p)); hi=(j*q)//p
    for n in range(lo,hi+1):
        np_,nq=p*n-q,q*n
        if np_<=0: continue
        g=gcd(np_,nq)
        if has(np_//g,nq//g,j-1,n): return True
    return False
def N(a,b):
    g=gcd(a,b); p,q=a//g,b//g
    j=1
    while not has(p,q,j,1): j+=1
    return j
B=int(sys.argv[1]) if len(sys.argv)>1 else 40
row=[]
for b in range(2,B+1):
    row.append(max(N(a,b) for a in range(1,b)))
print("N(b), b=2..%d:"%B, row)
