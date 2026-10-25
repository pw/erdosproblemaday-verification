#!/usr/bin/env python3
"""Build PG(2,q), the C-bounded blocking-set CNF (DIMACS) and/or solve with CP-SAT.
usage: model1159.py cnf  q C out.cnf [--minimal] [--lo LO --hi HI]
       model1159.py cpsat q C [--workers W --time T] [--minimal]
       model1159.py check q C "pointlist"   # independent check of a witness
Symmetry break: (0,0,1) in S, line x=0 (vector (1,0,0)) is a tangent -> its other points forced 0.
"""
import sys, itertools, argparse, time, json

def plane(q,check=None):
    pts=[(1,a,b) for a in range(q) for b in range(q)]+[(0,1,a) for a in range(q)]+[(0,0,1)]
    idx={p:i for i,p in enumerate(pts)}
    lines=[[i for i,p in enumerate(pts) if (p[0]*L[0]+p[1]*L[1]+p[2]*L[2])%q==0] for L in pts]
    # sanity: incidence axioms (full pair check only for small q unless forced)
    assert all(len(l)==q+1 for l in lines)
    for i in range(len(pts)):
        assert sum(1 for l in lines if i in l)==q+1
    if check or (check is None and q<=19):
        import numpy as np
        A=np.zeros((len(pts),len(pts)),dtype=np.int32)
        for li,l in enumerate(lines): A[li,l]=1
        AtA=A.T@A; off=AtA-np.diag(np.diag(AtA))+np.eye(len(pts),dtype=np.int32); assert (off==1).all(), "pair axiom"
    return pts,idx,lines

def count_bounds(q,C):
    """elementary: t_0=0, i in 1..C -> feasible |S| range from the three count identities (necessary only)."""
    v=q*q+q+1; ok=[]
    for k in range(1,v+1):
        # exists nonneg integer t_1..t_C with sum t_i=v, sum i t_i=k(q+1), sum C(i,2)t_i=C(k,2)? LP relaxation check via brute force on small C
        # brute force over t_C..t_3 would be large; use LP feasibility via fractions (scipy-free): check the 3 equations have a nonneg real solution
        import fractions
        # Variables t_1..t_C; 3 equations -> for C<=4 a 1-parameter family (C=4) or unique (C=3)
        A=[[1]*C,[i for i in range(1,C+1)],[i*(i-1)//2 for i in range(1,C+1)]]
        b=[v,k*(q+1),k*(k-1)//2]
        if C==4:
            # t4=a free: t3 = K-3a, t2 = 3a + 12k... derive generally via solving with a as parameter using fractions
            feas=False
            for a in range(0,v+1):
                # solve 3x3 for t1,t2,t3 given t4=a
                import numpy as np
                M=np.array([[1,1,1],[1,2,3],[0,1,3]],dtype=float); rhs=np.array([v-a,k*(q+1)-4*a,k*(k-1)//2-6*a],dtype=float)
                t=np.linalg.solve(M,rhs)
                if all(x>=-1e-9 for x in t): feas=True;break
            if feas: ok.append(k)
        else:
            raise SystemExit("count_bounds only coded for C=4")
    return min(ok),max(ok)

def build_cnf(q,C,minimal=False,lo=None,hi=None,break2=False):
    from pysat.card import CardEnc, EncType
    from pysat.formula import IDPool, CNF
    pts,idx,lines=plane(q)
    pool=IDPool(start_from=len(pts)+1)
    cnf=CNF()
    x=lambda i:i+1
    for L in lines:
        lits=[x(i) for i in L]
        cnf.append(lits)  # >=1
        at=CardEnc.atmost(lits=lits,bound=C,vpool=pool,encoding=EncType.seqcounter)
        cnf.extend(at.clauses)
    P0=idx[(0,0,1)]; L0=lines[idx[(1,0,0)]]
    assert P0 in L0
    cnf.append([x(P0)])
    for i in L0:
        if i!=P0: cnf.append([-x(i)])
    if break2:
        # WLOG (minimal S, flag-stabilizer action): Q1=(1,0,0) in S on the line y=0 through P0, and Q1's tangent is z=0
        Q1=idx[(1,0,0)]; cnf.append([x(Q1)])
        M1=lines[idx[(0,0,1)]]; assert Q1 in M1 and P0 not in M1
        for i in M1:
            if i!=Q1: cnf.append([-x(i)])
    if lo is not None:
        cnf.extend(CardEnc.atleast(lits=[x(i) for i in range(len(pts))],bound=lo,vpool=pool,encoding=EncType.seqcounter).clauses)
    if hi is not None:
        cnf.extend(CardEnc.atmost(lits=[x(i) for i in range(len(pts))],bound=hi,vpool=pool,encoding=EncType.seqcounter).clauses)
    if minimal:
        # every chosen point lies on a tangent: t_{P,L} <-> AND_{Q in L, Q!=P} not x_Q ; x_P -> OR_L t_{P,L}
        for P in range(len(pts)):
            ts=[]
            for li,L in enumerate(lines):
                if P not in L: continue
                t=pool.id(('t',P,li)); ts.append(t)
                others=[x(Qi) for Qi in L if Qi!=P]
                for o in others: cnf.append([-t,-o])
                cnf.append([t]+others)
            cnf.append([-x(P)]+ts)
    return cnf,pts,lines,pool

def check(q,C,S):
    pts,idx,lines=plane(q)
    Sset=set(idx[tuple(p)] for p in S)
    assert len(Sset)==len(S),"duplicate points"
    hist={}
    for L in lines:
        m=len(Sset.intersection(L)); hist[m]=hist.get(m,0)+1
    ok=all(1<=m<=C for m in hist)
    return ok,dict(sorted(hist.items())),len(Sset)

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('mode'); ap.add_argument('q',type=int); ap.add_argument('C',type=int)
    ap.add_argument('rest',nargs='*'); ap.add_argument('--minimal',action='store_true'); ap.add_argument('--break2',action='store_true'); ap.add_argument('--lo',type=int); ap.add_argument('--hi',type=int)
    ap.add_argument('--workers',type=int,default=8); ap.add_argument('--time',type=float,default=600)
    a=ap.parse_args()
    if a.mode=='bounds':
        print(count_bounds(a.q,a.C))
    elif a.mode=='cnf':
        cnf,pts,lines,pool=build_cnf(a.q,a.C,a.minimal,a.lo,a.hi,a.break2)
        cnf.to_file(a.rest[0]); print(f"vars={cnf.nv} clauses={len(cnf.clauses)} -> {a.rest[0]}")
        json.dump({'points':pts},open(a.rest[0]+'.points.json','w'))
    elif a.mode=='cpsat':
        from ortools.sat.python import cp_model
        pts,idx,lines=plane(a.q); m=cp_model.CpModel()
        x=[m.NewBoolVar(f"x{i}") for i in range(len(pts))]
        for L in lines:
            m.Add(sum(x[i] for i in L)>=1); m.Add(sum(x[i] for i in L)<=a.C)
        P0=idx[(0,0,1)]; m.Add(x[P0]==1)
        for i in lines[idx[(1,0,0)]]:
            if i!=P0: m.Add(x[i]==0)
        if a.break2:
            Q1=idx[(1,0,0)]; m.Add(x[Q1]==1)
            for i in lines[idx[(0,0,1)]]:
                if i!=Q1: m.Add(x[i]==0)
        if a.lo: m.Add(sum(x)>=a.lo)
        if a.hi: m.Add(sum(x)<=a.hi)
        if a.minimal:
            for P in range(len(pts)):
                ts=[]
                for li,L in enumerate(lines):
                    if P not in L: continue
                    t=m.NewBoolVar(f"t{P}_{li}"); ts.append(t)
                    others=[x[Q] for Q in L if Q!=P]
                    m.Add(sum(others)==0).OnlyEnforceIf(t); m.Add(sum(others)>=1).OnlyEnforceIf(t.Not())
                m.AddBoolOr(ts+[x[P].Not()])
        s=cp_model.CpSolver(); s.parameters.num_search_workers=a.workers; s.parameters.max_time_in_seconds=a.time
        s.parameters.log_search_progress=False
        t0=time.time(); r=s.Solve(m); dt=time.time()-t0
        name=s.StatusName(r); print(f"CP-SAT q={a.q} C={a.C} workers={a.workers} time={a.time} -> {name} in {dt:.1f}s; branches={s.NumBranches()} conflicts={s.NumConflicts()}")
        if name in('OPTIMAL','FEASIBLE'):
            S=[pts[i] for i in range(len(pts)) if s.Value(x[i])]
            print("WITNESS",json.dumps(S)); print("check:",check(a.q,a.C,S))
    elif a.mode=='check':
        S=json.loads(a.rest[0]); print(check(a.q,a.C,S))
