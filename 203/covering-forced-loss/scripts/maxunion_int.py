#!/usr/bin/env python3
"""Third implementation of the exact block maximum: cosets as Python big-int bitsets (one int of T*T bits per (prime,coset)),
union by `|`, count by int.bit_count(). Enumerates all configurations with c_0 = 0 (translation).  Usage: maxunion_int.py block.txt"""
import sys, itertools, time
from math import lcm
rows=[tuple(map(int,l.split())) for l in open(sys.argv[1]) if l.strip()]
T=1
for e,_,_ in rows: T=lcm(T,e)
t0=time.time()
bits=[]
for e,u,v in rows:
    cs=[0]*e
    for k in range(T):
        base=u*k
        for l in range(T):
            cs[(base+v*l)%e]|=1<<(k*T+l)
    assert all(c.bit_count()==T*T//e for c in cs)
    bits.append(cs)
best=-1; nbest=0; wit=None
for ch in itertools.product(*([range(1)]+[range(e) for e,_,_ in rows[1:]])):
    acc=0
    for i,c in enumerate(ch): acc|=bits[i][c]
    n=acc.bit_count()
    if n>best: best,nbest,wit=n,1,ch
    elif n==best: nbest+=1
s=sum(1/e for e,_,_ in rows)
print(f"bigint: n={len(rows)} T={T} MAX={best} density={best/(T*T):.6f} loss={s-best/(T*T):.6f} #opt(c0=0)={nbest} witness={wit} wall={time.time()-t0:.0f}s")
