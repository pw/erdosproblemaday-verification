#!/usr/bin/env python3
"""From-scratch check of an l6 SAT model (03:00Z seat, independent of config188/l6_stats): rebuild unit pairs and
unit-step 6-runs from the POINT COORDINATES alone (not from the instance's pair/run lists), then test the colouring."""
import sys, json, math, itertools, collections
import numpy as np
base=sys.argv[1]; k=int(sys.argv[2]) if len(sys.argv)>2 else 6
meta=json.load(open(base+".json")); P=np.array(meta["points"],dtype=float); n=len(P)
vals={}
for line in open(base+".sol"):
    if line.startswith("v "):
        for t in line.split()[1:]:
            v=int(t)
            if v: vals[abs(v)]=v>0
assert set(vals)>=set(range(1,n+1)), "model does not cover all point variables"
red=np.array([vals[i+1] for i in range(n)])
# unit pairs by geometry (tolerance 1e-7), via sorted-by-x sweep
EPS=1e-7
order=np.argsort(P[:,0]); Ps=P[order]
pairs=[]
xs=Ps[:,0]
for ii in range(n):
    jj=ii+1
    while jj<n and xs[jj]-xs[ii]<=1+EPS:
        d=math.hypot(Ps[jj,0]-Ps[ii,0],Ps[jj,1]-Ps[ii,1])
        if abs(d-1)<EPS: pairs.append((order[ii],order[jj]))
        jj+=1
print("points",n,"unit pairs (geometry)",len(pairs),"instance says",meta["n_unit_pairs"])
bad_pairs=sum(1 for a,b in pairs if red[a] and red[b])
# 6-runs: for every unit pair (a,b) as a step u=P[b]-P[a], walk forward while points exist
key=lambda p:(round(p[0]*1e6),round(p[1]*1e6))
idx={}
for i,p in enumerate(P): idx.setdefault(key(p),[]).append(i)
def find(p):
    L=idx.get(key(p))
    if L: return L[0]
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            L=idx.get((key(p)[0]+dx,key(p)[1]+dy))
            if L and math.hypot(P[L[0],0]-p[0],P[L[0],1]-p[1])<EPS: return L[0]
    return None
runs=set()
for a,b in pairs:
    for s,t in ((a,b),(b,a)):
        u=P[t]-P[s]; seq=[s,t]; cur=P[t]
        while len(seq)<k:
            cur=cur+u; j=find(cur)
            if j is None: break
            seq.append(j)
        if len(seq)==k: runs.add(tuple(seq))
# a run found from (a,b) and from (b,a) reversed are different tuples only if direction differs; canonicalise by min endpoint
canon=set(tuple(r) if r[0]<r[-1] else tuple(reversed(r)) for r in runs)
print("unit-step %d-runs (geometry)"%k,len(canon),"instance says",meta["n_runs"])
bad_runs=sum(1 for r in canon if not any(red[i] for i in r))
# WLOG points: origin red, the named blue point
o=find(np.array([0.0,0.0])); bl=meta.get("blue")
print("origin index",o,"red?",bool(red[o]) if o is not None else None,"| blue tag",bl)
if bl:
    bx,by=[float(v) for v in bl.split(",")]; bi=find(np.array([bx,by])); print("blue point index",bi,"blue?",(not red[bi]) if bi is not None else None)
print("red density",red.mean().round(4))
print("VIOLATIONS: red unit pairs",bad_pairs,"| all-blue %d-runs"%k,bad_runs)
print("VERDICT:","VALID l%d-free colouring"%k if bad_pairs==0 and bad_runs==0 else "INVALID")
