#!/usr/bin/env python3
"""Exact enumeration of k-term distinct Egyptian expansions of 1 (n_1<...<n_k, n_i>=1), k<=K.
Prints F(k), v(k)=min{m>=2 not a denominator}, max n_i per (0-based) position vs the Lean-proved bound k^(2^i),
and the max n_k vs Sylvester s_k - 1. Route A: DFS on the remaining fraction, last two terms by divisors of q^2.
Erdős #304/#148/#293 cross-check, 18:00Z erdos seat 2026-10-21."""
import sys
from fractions import Fraction
from math import gcd
from sympy import divisors
K=int(sys.argv[1]) if len(sys.argv)>1 else 6
def tails2(p,q,prev):
    # 1/y+1/z = p/q, prev<y<z ; (py-q)(pz-q)=q^2, d1<q
    out=[]
    for d1 in divisors(q*q):
        if d1>=q: break
        if (d1+q)%p: continue
        y=(d1+q)//p
        if y<=prev: continue
        d2=q*q//d1
        if (d2+q)%p: continue
        out.append((y,(d2+q)//p))
    return out
def expansions(k):
    res=[]
    def rec(p,q,prev,j,pre):
        # remaining p/q with j terms, all > prev
        if j==1:
            if p==1 and q>prev: res.append(pre+(q,))
            return
        if j==2:
            for y,z in tails2(p,q,prev): res.append(pre+(y,z))
            return
        lo=max(prev+1,-(-q//p))            # n >= q/p
        hi=(j*q)//p                         # n <= j q/p (strict below when n gives equal parts; distinctness handles)
        for n in range(lo,hi+1):
            np_,nq=p*n-q,q*n
            if np_<=0:
                if np_==0 and j==1: pass
                continue
            g=gcd(np_,nq); rec(np_//g,nq//g,n,j-1,pre+(n,))
    if k==1: return [(1,)]
    rec(1,1,0,k,())
    return res
syl=[2]
for _ in range(12): syl.append(syl[-1]*(syl[-1]-1)+1)
for k in range(1,K+1):
    E=expansions(k)
    for e in E: assert sum(Fraction(1,n) for n in e)==1 and all(e[i]<e[i+1] for i in range(len(e)-1))
    D=set(n for e in E for n in e if n>=2)
    v=2
    while v in D: v+=1
    mx=[max((e[i] for e in E),default=0) for i in range(k)]
    lean_ok=all(mx[i]<=k**(2**i) for i in range(k))
    print(f"k={k} F={len(E)} v={v} |D|={len(D)} max_n_by_pos={mx} lean_bound_ok={lean_ok} F<=k^(2^k-1):{len(E)<=k**(2**k-1)} "
          f"v<=1+k^(2^(k-1)):{v<=1+k**(2**(k-1))} max_nk={mx[-1]} sylvester_s_k-1={syl[k-1]-1} ok={mx[-1]<=syl[k-1]-1}",flush=True)
