#!/usr/bin/env python3
"""CNF for the C-bounded blocking set in PG(2,q), q a prime power (galois). Flag break (0,0,1) in S, line (1,0,0) tangent.
usage: cnf_gf.py q C out.cnf lo hi"""
import sys, json
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool, CNF
from plane_gf import plane_gf
q,C=int(sys.argv[1]),int(sys.argv[2]); out=sys.argv[3]; lo,hi=int(sys.argv[4]),int(sys.argv[5]); break2=(len(sys.argv)>6 and sys.argv[6]=='--break2')
pts,lines=plane_gf(q); idx={p:i for i,p in enumerate(pts)}
pool=IDPool(start_from=len(pts)+1); cnf=CNF(); x=lambda i:i+1
for L in lines:
    lits=[x(i) for i in L]; cnf.append(lits)
    cnf.extend(CardEnc.atmost(lits=lits,bound=C,vpool=pool,encoding=EncType.seqcounter).clauses)
P0=idx[(0,0,1)]; L0=lines[idx[(1,0,0)]]; assert P0 in L0
cnf.append([x(P0)])
for i in L0:
    if i!=P0: cnf.append([-x(i)])
if break2:
    Q1=idx[(1,0,0)]; cnf.append([x(Q1)])
    M1=lines[idx[(0,0,1)]]; assert Q1 in M1 and P0 not in M1
    for i in M1:
        if i!=Q1: cnf.append([-x(i)])
allx=[x(i) for i in range(len(pts))]
cnf.extend(CardEnc.atleast(lits=allx,bound=lo,vpool=pool,encoding=EncType.seqcounter).clauses)
cnf.extend(CardEnc.atmost(lits=allx,bound=hi,vpool=pool,encoding=EncType.seqcounter).clauses)
cnf.to_file(out); json.dump({'q':q,'points':pts},open(out+'.points.json','w'))
print(f"q={q} C={C} vars={cnf.nv} clauses={len(cnf.clauses)} -> {out}")
