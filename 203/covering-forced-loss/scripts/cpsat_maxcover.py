#!/usr/bin/env python3
"""Decorrelated instrument for maxunion: CP-SAT (OR-tools) max-cover on the torus (Z/T)^2 for a block file.
Variables x[i][c] (one-hot per prime, prime 0 fixed to coset 0), y[pt]; y <= sum_i x[i][chi_i(pt)]; maximize sum y.
Prints OPTIMAL/FEASIBLE, objective, solver's upper bound, wall time. Usage: cpsat_maxcover.py block.txt [seconds] [workers]"""
import sys, time
from math import lcm
from ortools.sat.python import cp_model
rows=[tuple(map(int,l.split())) for l in open(sys.argv[1]) if l.strip()]
limit=float(sys.argv[2]) if len(sys.argv)>2 else 600; workers=int(sys.argv[3]) if len(sys.argv)>3 else 1
T=1
for e,_,_ in rows: T=lcm(T,e)
m=cp_model.CpModel()
x=[[m.NewBoolVar(f"x{i}_{c}") for c in range(e)] for i,(e,_,_) in enumerate(rows)]
for i,(e,_,_) in enumerate(rows): m.AddExactlyOne(x[i])
m.Add(x[0][0]==1)
ys=[]
for k in range(T):
    for l in range(T):
        y=m.NewBoolVar(f"y{k}_{l}"); ys.append(y)
        lits=[x[i][(u*k+v*l)%e] for i,(e,u,v) in enumerate(rows)]
        m.Add(sum(lits)>=y)
m.Maximize(sum(ys))
s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=limit; s.parameters.num_workers=workers; s.parameters.log_search_progress=False
t0=time.time(); st=s.Solve(m)
name={cp_model.OPTIMAL:"OPTIMAL",cp_model.FEASIBLE:"FEASIBLE",cp_model.INFEASIBLE:"INFEASIBLE",cp_model.UNKNOWN:"UNKNOWN"}[st]
obj=s.ObjectiveValue() if st in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None
ub=s.BestObjectiveBound()
sm=sum(1/e for e,_,_ in rows)
wit=[next(c for c in range(e) if s.Value(x[i][c])) for i,(e,_,_) in enumerate(rows)] if obj is not None else None
print(f"cpsat: n={len(rows)} T={T} status={name} objective={obj} bound={ub} density={obj/(T*T) if obj else None} loss={sm-obj/(T*T) if obj else None} loss_from_bound>={sm-ub/(T*T):.6f} witness={wit} wall={time.time()-t0:.1f}s")
