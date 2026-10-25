#!/usr/bin/env python3
"""Independent (numpy) brute force of the same quantity as maxunion.c: max over coset choices of |∪ C_i| on (Z/T)^2.
Different representation: boolean arrays per (prime, coset) built from a meshgrid, union via np.logical_or.reduce;
enumerates ALL choices incl. the first prime's (no translation trick) when configs <= 2e5, else fixes c_0 = 0.
Also re-checks a given witness choice literally (positive control on the C tool's witness)."""
import sys, json, itertools, numpy as np
from math import lcm
rows=[tuple(map(int,l.split())) for l in open(sys.argv[1]) if l.strip()]
T=1
for e,_,_ in rows: T=lcm(T,e)
k,l=np.meshgrid(np.arange(T),np.arange(T),indexing="ij")
chi=[(u*k+v*l)%e for e,u,v in rows]
masks=[[c_==c for c in range(e)] for c_,(e,u,v) in zip(chi,rows)]
for i,(e,u,v) in enumerate(rows):
    for c in range(e): assert masks[i][c].sum()==T*T//e
full=np.prod([e for e,_,_ in rows])
ranges=[range(e) for e,_,_ in rows]
if full>2e5: ranges[0]=range(1)
best=-1;nbest=0;wit=None
for ch in itertools.product(*ranges):
    cnt=int(np.logical_or.reduce([masks[i][c] for i,c in enumerate(ch)]).sum())
    if cnt>best: best,nbest,wit=cnt,1,ch
    elif cnt==best: nbest+=1
s=sum(1/e for e,_,_ in rows)
print(f"numpy: n={len(rows)} T={T} enumerated={'all' if full<=2e5 else 'c0=0'} MAX={best} density={best/(T*T):.6f} loss={s-best/(T*T):.6f} #opt={nbest} witness={wit}")
if len(sys.argv)>2:
    w=list(map(int,sys.argv[2].split(',')))
    cnt=int(np.logical_or.reduce([masks[i][c] for i,c in enumerate(w)]).sum()); print("witness re-check:",w,"covers",cnt)
