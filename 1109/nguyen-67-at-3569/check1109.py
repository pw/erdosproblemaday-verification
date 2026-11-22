#!/usr/bin/env python3
"""Own checker for submission 2wvfme: every sum a+b (a<=b, incl. 2a) of the set squarefree; set inside [1,N].
Squarefreeness by full factorisation (sympy) AND by a p^2 sieve, as two routes."""
import sys
from sympy import factorint
L=open(sys.argv[1]).read().split(); k,N=int(L[0]),int(L[1]); A=list(map(int,L[2:]))
def sqf_fact(n): return all(e==1 for e in factorint(n).values())
M=2*N+1; sq=bytearray(M)       # sieve: sq[n]=1 if p^2|n for some p
p=2
while p*p<M:
    for m in range(p*p,M,p*p): sq[m]=1
    p+=1
def check(A,N):
    sums=[a+b for i,a in enumerate(A) for b in A[i:]]
    f1=[s for s in sums if not sqf_fact(s)]; f2=[s for s in sums if sq[s]]
    return len(A), len(set(A))==len(A), min(A)>=1 and max(A)<=N, len(sums), f1, f2
n,distinct,inrange,ns,f1,f2=check(A,N)
print(f"header k={k} N={N}; parsed {n} elements, distinct={distinct}, in [1,{N}]={inrange}, max={max(A)}; sums checked={ns}; non-squarefree by factorisation={len(f1)}, by sieve={len(f2)}")
ok = n==k==67 and distinct and inrange and ns==67*68//2 and not f1 and not f2
# negative controls: add 1 to one element / add one more element
B=A[:]; B[10]+=1; _,_,_,_,g1,g2=check(B,N); print(f"neg control (element 11 +1): non-squarefree sums {len(g1)}/{len(g2)}"); ok &= bool(g1) and bool(g2)
best=None
for x in range(1,N+1):
    if x in A: continue
    _,_,_,_,g1,_=check(A+[x],N)
    if not g1: best=x; break
print(f"neg control: some x in [1,{N}] extends the set to 68? {'YES x='+str(best) if best else 'no'} (not a claim either way; reported)")
print("PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
