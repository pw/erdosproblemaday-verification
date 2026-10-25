#!/usr/bin/env python3
"""Cube split on top of the two-flag break — a chain of WLOG normalisations (each a projectivity preserving everything fixed before it):
 0. S is a blocking set with |S∩L| ≤ C for every line L; pass to an inclusion-MINIMAL blocking subset (still max ≤ C, smaller), so every
    point of S lies on a tangent (a line meeting S only there). Lower size bounds used below are the elementary count bounds valid for
    EVERY max-C blocking set, so they survive this step; upper bounds survive trivially.
 1. Flag: P0=(0,0,1) ∈ S and L0 = {x=0} is a tangent at P0 (PGL(3,q) is transitive on point–tangent flags).
 2. Among the q lines through P0 other than L0, let L1 = {y=0} carry the MAXIMUM number c1 ≥ 1 of further points of S
    (the flag stabilizer acts on those q lines as AGL(1,q), transitively).
 3. Q1=(1,0,0) ∈ S: the elation E_a:(x,y,z)↦(x,y,z+ax) has centre P0 and axis L0, fixes EVERY line through P0 (so L1 stays the max line)
    and moves (1,0,b)↦(1,0,b+a) along L1.
 4. M1 = {z=0} is a tangent at Q1 (minimality gives Q1 a tangent M1 ≠ L1; M1 meets L0 at R=(0,1,r); the elation (x,y,z)↦(x,y,z−ry) has
    centre P0 and axis L1, fixes every line through P0 and L0 as a set, and sends R to (0,1,0), hence M1 to {z=0}).
 5. L2 = {y=x} carries the SECOND-largest count c2 (1 ≤ c2 ≤ c1): diag(1,1/μ,1) maps y=μx to y=x and fixes P0, L0, L1, Q1, M1.
 6. If c1 ≥ 2 then (1,0,1) ∈ S: diag(1,1,1/t) sends (1,0,t)↦(1,0,1) and fixes every line through P0, L0, M1, L2, Q1.
 Every other line through P0 then has ≤ c2 further points. The cube (c1,c2) encodes exactly c1 further points on L1, exactly c2 on L2,
 ≤ c2 on each of the other q−2 lines through P0 (all counts EXCLUDING P0), plus steps 1, 3, 4, 6 as unit clauses and lo ≤ |S| ≤ hi.
 Size floor: a cube admits at most 1 + c1 + (q−1)·c2 points, so for q=13, lo=20 the cubes (1,1),(2,1),(3,1) are empty by arithmetic
 (14, 15, 16 < 20) and only (2,2),(3,2),(3,3) can hold a solution.
 usage: cubes1159.py q C lo hi [tag]  -> runs/cube_q{q}_c{C}{tag}_{c1}{c2}.cnf"""
import sys, json
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool, CNF
sys.path.insert(0,'.'); from model1159 import plane
q,C,lo,hi=map(int,sys.argv[1:5]); tag=sys.argv[5] if len(sys.argv)>5 else ''
pts,idx,lines=plane(q,check=False); x=lambda i:i+1
P0=idx[(0,0,1)]; Q1=idx[(1,0,0)]; Q2=idx[(1,0,1)]
L0=lines[idx[(1,0,0)]]; L1=lines[idx[(0,1,0)]]; M1=lines[idx[(0,0,1)]]; L2=lines[idx[(1,q-1,0)]]  # y=x : x - y = 0
assert P0 in L0 and P0 in L1 and P0 in L2 and Q1 in L1 and Q1 in M1 and P0 not in M1 and Q2 in L1
through=[L for L in lines if P0 in L]; assert len(through)==q+1
others=[L for L in through if L is not L0 and L is not L1 and L is not L2]; assert len(others)==q-2
for c1 in range(1,C):
    for c2 in range(1,c1+1):
        pool=IDPool(start_from=len(pts)+1); cnf=CNF()
        for L in lines:
            lits=[x(i) for i in L]; cnf.append(lits)
            cnf.extend(CardEnc.atmost(lits=lits,bound=C,vpool=pool,encoding=EncType.seqcounter).clauses)
        cnf.append([x(P0)])
        for i in L0:
            if i!=P0: cnf.append([-x(i)])
        cnf.append([x(Q1)])
        for i in M1:
            if i!=Q1: cnf.append([-x(i)])
        if c1>=2: cnf.append([x(Q2)])
        l1=[x(i) for i in L1 if i!=P0]; l2=[x(i) for i in L2 if i!=P0]
        cnf.extend(CardEnc.equals(lits=l1,bound=c1,vpool=pool,encoding=EncType.seqcounter).clauses)
        cnf.extend(CardEnc.equals(lits=l2,bound=c2,vpool=pool,encoding=EncType.seqcounter).clauses)
        for L in others:
            cnf.extend(CardEnc.atmost(lits=[x(i) for i in L if i!=P0],bound=c2,vpool=pool,encoding=EncType.seqcounter).clauses)
        allx=[x(i) for i in range(len(pts))]
        cnf.extend(CardEnc.atleast(lits=allx,bound=lo,vpool=pool,encoding=EncType.seqcounter).clauses)
        cnf.extend(CardEnc.atmost(lits=allx,bound=hi,vpool=pool,encoding=EncType.seqcounter).clauses)
        out=f"runs/cube_q{q}_c{C}{tag}_{c1}{c2}.cnf"; cnf.to_file(out); print(f"{out}: vars={cnf.nv} clauses={len(cnf.clauses)}")
json.dump({'q':q,'points':pts},open(f'runs/cube_q{q}_c{C}{tag}.points.json','w'))
