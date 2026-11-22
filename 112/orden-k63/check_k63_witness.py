#!/usr/bin/env python3
"""Own check of Orden's 29-vertex witness (format 'v: w1 w2 ...' = arcs v->w). Reuses check_orden.py's search."""
import sys
exec(open('check_orden.py').read().split('allok=True')[0])
arcs=set(); N=0
for l in open(sys.argv[1]):
    l=l.split('#')[0].strip()
    if not l: continue
    v,rest=l.split(':'); v=int(v); N=max(N,v+1)
    for w in rest.split(): arcs.add((v,int(w))); N=max(N,int(w)+1)
outdeg=[0]*N; indeg=[0]*N
for a,b in arcs: outdeg[a]+=1; indeg[b]+=1
print(f"N={N} arcs={len(arcs)} outdeg set={sorted(set(outdeg))} indeg set={sorted(set(indeg))}")
ok=check("Orden 29-vertex witness, k(6,3)>=30",N,arcs,6,3)
ok&=check("neg: same graph asked for no independent 5-set",N,arcs,5,3,expect_pass=False)
a0=next(iter(arcs)); ok&=check("neg: one arc reversed in addition (2-cycle)",N,arcs|{(a0[1],a0[0])},6,3,expect_pass=False)
print("ALL AS EXPECTED" if ok else "SOMETHING UNEXPECTED"); sys.exit(0 if ok else 1)
