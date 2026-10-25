#!/usr/bin/env python3
"""Referee's independent encoding of Li's Lemma 3.1 conditions, generalised to P = a UNION of doubling cycles.
Variables: b_r (r in B), d_r (r in D) for r not in P.  Conditions (Q = P u B):
  cover: r not in Q  =>  exists (u,v), u+v=r, with (u in B or u in P or u in D) and v in B
  avoid: r in Q      =>  no u+v=r with (u,v) in BxB, PxB, DxB, DxP
  PP:    u,v in P, u != v  =>  u+v not in Q   (u+v in P checked statically)
Written from Li's tex (Lemma lem:shield), not from shield_sat_L.py."""
import sys, itertools
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType

def cycles(M):
    seen=set(); out=[]
    for x in range(1,M):
        if x in seen: continue
        y=x; L=None
        for i in range(1,M+1):
            y=(2*y)%M
            if y==x: L=i; break
        if L is None: continue
        orb=[(x*2**i)%M for i in range(L)]; seen|=set(orb); out.append(orb)
    return out

def solve(M,P,force=None,extra=None,want_model=True):
    P=set(P); R=[r for r in range(M) if r not in P]
    # static PP: mixed sums landing on P
    for u in P:
        for v in P:
            if u!=v and (u+v)%M in P: return 'PPFAIL',None
    vid={}
    def b(r): return vid.setdefault(('b',r),len(vid)+1)
    def d(r): return vid.setdefault(('d',r),len(vid)+1)
    for r in R: b(r); d(r)
    cl=[]
    for r in R: cl.append([-b(r),-d(r)])
    for u in P:
        for v in P:
            if u!=v and (u+v)%M in R: cl.append([-b((u+v)%M)])
    # auxiliary conjunction vars
    aux={}
    def AND(lits):
        lits=tuple(sorted(lits))
        if len(lits)==1: return lits[0]
        if lits in aux: return aux[lits]
        z=len(vid)+len(aux)+1+100000; aux[lits]=z
        for l in lits: cl.append([-z,l])
        cl.append([z]+[-l for l in lits]); return z
    inQ=lambda r: None if r in P else b(r)   # literal for "r in Q" (None = always true)
    for r in range(M):
        reps=[]; bad=[]
        for u in range(M):
            v=(r-u)%M
            if v in P: 
                # u in D, v in P  -> avoid only
                if u in R: bad.append(d(u))
                continue
            # v must be in B
            if u in P: reps.append(b(v)); bad.append(b(v))
            else:
                reps.append(AND([b(u),b(v)])); bad.append(AND([b(u),b(v)]))
                reps.append(AND([d(u),b(v)])); bad.append(AND([d(u),b(v)]))
        if r in P:
            for z in bad: cl.append([-z])
        else:
            cl.append([b(r)]+reps)
            for z in bad: cl.append([-b(r),-z])
    cl.append([b(r) for r in R])
    if force:
        B,D=force
        for r in R: cl.append([b(r)] if r in B else [-b(r)]); cl.append([d(r)] if r in D else [-d(r)])
    if extra: cl+=extra(b,d,R)
    with Cadical195(bootstrap_with=cl) as s:
        if not s.solve(): return 'UNSAT',None
        m=set(l for l in s.get_model() if l>0)
        return 'SAT',(sorted(r for r in R if b(r) in m),sorted(r for r in R if d(r) in m))

if __name__=='__main__':
    # controls
    print('Li forced M=49:',solve(49,[7,14,28],force=({3,22,32,40,48},{1,2,5,13,27,36,47})))
    print('Li free M=49:',solve(49,[7,14,28]))
    print('M=49 no B:', solve(49,[7,14,28],extra=lambda b,d,R:[[-b(r)] for r in R]))
    # single cycles below 49 -> compare with shield_all_v3
    tally={}
    for M in range(2,49):
        for c in cycles(M):
            st,_=solve(M,c); tally[st]=tally.get(st,0)+1
    print('single cycles M<=48:',tally)
    # unions of >=2 cycles, at least one of length >=3
    for M in range(2,49):
        cs=cycles(M)
        for k in range(2,len(cs)+1):
            for combo in itertools.combinations(cs,k):
                if max(len(c) for c in combo)<3: continue
                P=[r for c in combo for r in c]
                st,sol=solve(M,P)
                if st=='SAT': print(f'UNION SAT M={M} cycles={combo} B,D={sol}',flush=True)
    print('done unions')
