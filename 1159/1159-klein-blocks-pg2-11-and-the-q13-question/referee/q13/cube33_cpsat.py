# Referee's third model: cube (c1,c2) of the author's chain, built from scratch, CP-SAT native linear constraints.
import sys,time,json
from ortools.sat.python import cp_model
from pg import plane
import os
q=int(os.environ.get("Q","13")); C=int(os.environ.get("C","4")); LO=int(os.environ.get("LO","20")); HI=int(os.environ.get("HI","37")); FIX=os.environ.get("FIX")
c1,c2=int(sys.argv[1]),int(sys.argv[2]); tl=float(sys.argv[3])
pts,lines=plane(q)
m=cp_model.CpModel(); X={p:m.NewBoolVar(str(p)) for p in pts}
for L,s in lines.items(): m.Add(sum(X[p] for p in s)>=1); m.Add(sum(X[p] for p in s)<=C)
P0=(0,0,1);Q1=(1,0,0);Q2=(1,0,1)
xeq0=lines[(1,0,0)]; yeq0=lines[(0,1,0)]; zeq0=lines[(0,0,1)]; yeqx=lines[(1,q-1,0)]
assert all(p[0]==0 for p in xeq0) and all(p[1]==0 for p in yeq0) and all(p[2]==0 for p in zeq0) and all(p[0]==p[1] for p in yeqx)
m.Add(X[P0]==1); [m.Add(X[p]==0) for p in xeq0 if p!=P0]
m.Add(X[Q1]==1); [m.Add(X[p]==0) for p in zeq0 if p!=Q1]
if c1>=2: m.Add(X[Q2]==1)
m.Add(sum(X[p] for p in yeq0 if p!=P0)==c1); m.Add(sum(X[p] for p in yeqx if p!=P0)==c2)
thr=[L for L,s in lines.items() if P0 in s]; assert len(thr)==q+1
oth=[L for L in thr if L not in [(1,0,0),(0,1,0),(1,q-1,0)]]; assert len(oth)==q-2
for L in oth: m.Add(sum(X[p] for p in lines[L] if p!=P0)<=c2)
m.Add(sum(X.values())>=LO); m.Add(sum(X.values())<=HI)
if FIX:
    F={tuple(p) for p in json.loads(open(FIX).read())}; [m.Add(X[p]==(1 if p in F else 0)) for p in pts]
s=cp_model.CpSolver(); s.parameters.num_workers=1; s.parameters.max_time_in_seconds=tl; s.parameters.log_search_progress=True
t=time.time(); r=s.Solve(m); print('STATUS',s.StatusName(r),'wall',round(time.time()-t,1),flush=True)
if r in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    S=[p for p in pts if s.Value(X[p])]; json.dump(S,open(os.environ.get('WOUT',f'SAT_q{q}_C{C}_cube{c1}{c2}_witness.json'),'w')); print('WITNESS',len(S),S)
