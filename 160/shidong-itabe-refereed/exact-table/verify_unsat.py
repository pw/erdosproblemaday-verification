#!/usr/bin/env python3
"""Decorrelated second instrument for the exact h(N) table: a DIFFERENT encoding on a DIFFERENT solver.
Encoding: per 4-AP, equality indicators e_ij <-> OR_c (x_ic AND x_jc) for the 6 position pairs; '>= 3 distinct colours'
<=> none of the 7 at-most-two-colour equality patterns: AABB-type (e01&e23, e02&e13, e03&e12) and three-equal
(e01&e12, e12&e23, e01&e13, e02&e23).  Solver: pysat Glucose4 (cadical produced the table).
Usage: verify_unsat.py N k  -> prints SAT (with independently verified witness) or UNSAT.  Exit 0 either way; 2 on error.
"""
import sys, itertools
from pysat.solvers import Glucose4

def run(N,k):
    V={}; 
    def var(key):
        if key not in V: V[key]=len(V)+1
        return V[key]
    cls=[]
    for n in range(1,N+1):
        cls.append([var(('x',n,c)) for c in range(k)])
        for c1,c2 in itertools.combinations(range(k),2): cls.append([-var(('x',n,c1)),-var(('x',n,c2))])
    # equality indicator e(n,m) for every pair n<m that co-occur in some 4-AP: e <-> OR_c (x_nc & x_mc)
    def eq(n,m):
        key=('e',n,m)
        if key in V: return V[key]
        e=var(key); ands=[]
        for c in range(k):
            a=var(('a',n,m,c)); ands.append(a)
            cls.append([-a,var(('x',n,c))]); cls.append([-a,var(('x',m,c))]); cls.append([a,-var(('x',n,c)),-var(('x',m,c))])
            cls.append([-a,e])
        cls.append([-e]+ands)
        return e
    for a in range(1,N+1):
        d=1
        while a+3*d<=N:
            p=(a,a+d,a+2*d,a+3*d); E={}
            for i,j in itertools.combinations(range(4),2): E[(i,j)]=eq(p[i],p[j])
            for (u,v) in [((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)),((0,1),(1,2)),((1,2),(2,3)),((0,1),(1,3)),((0,2),(2,3))]:
                cls.append([-E[u],-E[v]])
            d+=1
    cls.append([var(('x',1,0))])
    s=Glucose4(bootstrap_with=cls)
    ok=s.solve()
    if ok:
        m=set(l for l in s.get_model() if l>0)
        col=[None]*(N+1)
        for n in range(1,N+1):
            for c in range(k):
                if var(('x',n,c)) in m: col[n]=c
        good=all(len({col[a],col[a+d],col[a+2*d],col[a+3*d]})>=3 for a in range(1,N+1) for d in range(1,(N-a)//3+1))
        print(f"N={N} k={k}: SAT  witness verified={good}  {''.join(str(c) for c in col[1:])}")
        return 0 if good else 2
    print(f"N={N} k={k}: UNSAT  (vars={len(V)} clauses={len(cls)})"); return 0
if __name__=='__main__':
    sys.exit(run(int(sys.argv[1]),int(sys.argv[2])))
