#!/usr/bin/env python3
"""Exact phase structure on a window: with phase t(x) = {x g}, bins of width 1/B are classed by the fraction of their integers that lie
in S — CORE (>= 0.99), DEEP COMPLEMENT (<= 0.01), EDGE (between). Reports the measure of each class, the number of exceptions on core and
deep complement, and the membership fraction per edge zone.   usage: phase_core.py elems.u32 g X w [B=1000]"""
import sys, numpy as np
el=np.fromfile(sys.argv[1],dtype='<u4').astype(np.int64); g=float(sys.argv[2]); X=int(sys.argv[3]); w=int(sys.argv[4]); B=int(sys.argv[5]) if len(sys.argv)>5 else 1000
xs=np.arange(X,X+w); b=np.zeros(X+w,bool); b[el[el<X+w]]=True; inS=b[X:X+w]; k=((xs*g)%1.0*B).astype(int)
tot=np.bincount(k,minlength=B); ins=np.bincount(k,weights=inS,minlength=B); frac=ins/np.maximum(tot,1)
core=frac>=0.99; deep=frac<=0.01; edge=~core&~deep
print(f"window [{X},{X+w}) g={g} bins={B}: core {core.sum()/B:.4f} of the circle, deep complement {deep.sum()/B:.4f}, edge {edge.sum()/B:.4f}; density of S {inS.mean():.5f}")
print(f"  integers with phase in a CORE bin: {int(tot[core].sum())}, of which NOT in S: {int(tot[core].sum()-ins[core].sum())}")
print(f"  integers with phase in a DEEP bin: {int(tot[deep].sum())}, of which IN S: {int(ins[deep].sum())}")
print(f"  integers with phase in an EDGE bin: {int(tot[edge].sum())}, of which in S: {int(ins[edge].sum())} ({ins[edge].sum()/tot[edge].sum()*100:.1f}%)")
# edge zones as runs
runs=[]; i=0
while i<B:
    if edge[i] and not edge[i-1]:
        j=i
        while edge[(j+1)%B] and j<i+B: j+=1
        runs.append((i,j%B)); i=j+1
    else: i+=1
print("  edge zones (phase interval, width, membership %):",[(f"{a/B:.3f}-{(b_+1)/B:.3f}",(b_-a)%B+1,round(float(ins[a:b_+1].sum()/tot[a:b_+1].sum()*100),1) if a<=b_ else None) for a,b_ in runs])
print("  core arcs:",[(f"{a/B:.3f}-{(b_+1)/B:.3f}") for a,b_ in [(i,j) for i,j in __import__('itertools').groupby(range(B),key=lambda t: core[t]) and []]] if False else "")
runsC=[]; i=0
while i<B:
    if core[i] and not core[i-1]:
        j=i
        while core[(j+1)%B] and j<i+B: j+=1
        runsC.append((i,j%B)); i=j+1
    else: i+=1
print("  core arcs:",[f"{a/B:.3f}-{(b_+1)/B:.3f}" for a,b_ in runsC])
