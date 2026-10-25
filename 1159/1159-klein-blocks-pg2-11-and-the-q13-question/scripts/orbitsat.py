#!/usr/bin/env python3
"""Orbit-union search: H = <generators> <= PGL(3,q) (q prime here); variables = H-orbits on points;
CP-SAT: for every line L, 1 <= sum_O |L∩O| y_O <= C. Any solution is re-checked pointwise by model1159.check.
usage: orbitsat.py q C preset [--time T] [--workers W] [--all]
presets: singer:d   (subgroup of order d of a Singer cycle, d | q^2+q+1)
         hessian    (q ≡ 1 mod 3, needs sqrt(-3): order-216 Hessian group)
         conic:d    (cyclic subgroup of order d of PGL(2,q) acting on the conic via Sym^2; d | q±1 or d=q)
         diag       (torus diag(1,a,b), order (q-1)^2)
         perm       (S_3 coordinate permutations)
"""
import sys, json, argparse, itertools, time, collections
sys.path.insert(0,'.')
from model1159 import plane, check
ap=argparse.ArgumentParser(); ap.add_argument('q',type=int); ap.add_argument('C',type=int); ap.add_argument('preset')
ap.add_argument('--time',type=float,default=120); ap.add_argument('--workers',type=int,default=4); ap.add_argument('--lo',type=int); ap.add_argument('--hi',type=int)
a=ap.parse_args(); q,C=a.q,a.C
pts,idx,lines=plane(q,check=False); v=len(pts)
def norm(vec):
    vec=[x%q for x in vec]
    for x in vec:
        if x: inv=pow(x,-1,q); return tuple((y*inv)%q for y in vec)
def apply(M,p): return norm([sum(M[i][j]*p[j] for j in range(3)) for i in range(3)])
def matmul(A,B): return [[sum(A[i][k]*B[k][j] for k in range(3))%q for j in range(3)] for i in range(3)]
def matpow(A,e):
    R=[[1,0,0],[0,1,0],[0,0,1]]
    while e:
        if e&1: R=matmul(R,A)
        A=matmul(A,A); e>>=1
    return R
def primitive_cubic():
    # find monic irreducible x^3 - c2 x^2 - c1 x - c0 whose companion matrix has projective order q^2+q+1
    n=q*q+q+1
    for c0 in range(1,q):
        for c1 in range(q):
            for c2 in range(q):
                M=[[0,0,c0],[1,0,c1],[0,1,c2]]
                # projective order: smallest e with M^e scalar
                P=M; e=1
                while True:
                    if P[0][1]==0 and P[0][2]==0 and P[1][0]==0 and P[1][2]==0 and P[2][0]==0 and P[2][1]==0 and P[0][0]==P[1][1]==P[2][2] and P[0][0]!=0:
                        break
                    P=matmul(P,M); e+=1
                    if e>n: break
                if e==n: return M
    raise SystemExit("no Singer cycle found")
gens=[]
pre=a.preset
if pre.startswith('singer:'):
    d=int(pre.split(':')[1]); n=q*q+q+1; assert n%d==0
    S=primitive_cubic(); gens=[matpow(S,n//d)]
elif pre=='hessian':
    assert q%3==1
    w=next(x for x in range(2,q) if pow(x,3,q)==1 and x!=1)
    r=next(x for x in range(1,q) if (x*x)%q==(-3)%q)  # sqrt(-3)
    ri=pow(r,-1,q)
    T=[[0,1,0],[0,0,1],[1,0,0]]; D=[[1,0,0],[0,w,0],[0,0,w*w%q]]
    F=[[ri%q,ri%q,ri%q],[ri%q,ri*w%q,ri*w*w%q],[ri%q,ri*w*w%q,ri*w%q]]
    gens=[T,D,F]
elif pre.startswith('conic:'):
    d=int(pre.split(':')[1])
    # find a 2x2 matrix of projective order d in PGL(2,q), embed via Sym^2 acting on (x^2,xy,y^2) coords
    def sym2(m):
        a_,b_,c_,d_=m
        return [[a_*a_%q,2*a_*b_%q,b_*b_%q],[a_*c_%q,(a_*d_+b_*c_)%q,b_*d_%q],[c_*c_%q,2*c_*d_%q,d_*d_%q]]
    def pord(m):
        a_,b_,c_,d_=m; P=(1,0,0,1); e=0
        while True:
            P=((P[0]*a_+P[1]*c_)%q,(P[0]*b_+P[1]*d_)%q,(P[2]*a_+P[3]*c_)%q,(P[2]*b_+P[3]*d_)%q); e+=1
            if P[1]==0 and P[2]==0 and P[0]==P[3]!=0: return e
            if e>q*q+q+2: return None
    found=None
    for m in itertools.product(range(q),repeat=4):
        if (m[0]*m[3]-m[1]*m[2])%q==0: continue
        if pord(m)==d: found=m; break
    assert found, "no element of that order in PGL(2,q)"
    gens=[sym2(found)]
elif pre=='diag':
    g=next(x for x in range(2,q) if all(pow(x,(q-1)//p,q)!=1 for p in range(2,q) if (q-1)%p==0 and all(p%k for k in range(2,int(p**0.5)+1))))
    gens=[[[1,0,0],[0,g,0],[0,0,1]],[[1,0,0],[0,1,0],[0,0,g]]]
elif pre=='perm':
    gens=[[[0,1,0],[0,0,1],[1,0,0]],[[0,1,0],[1,0,0],[0,0,1]]]
else: raise SystemExit("unknown preset")
# orbits = components under generators
parent=list(range(v))
def find(i):
    while parent[i]!=i: parent[i]=parent[parent[i]]; i=parent[i]
    return i
for M in gens:
    for i,p in enumerate(pts):
        j=idx[apply(M,p)]; ri,rj=find(i),find(j)
        if ri!=rj: parent[ri]=rj
orb=collections.defaultdict(list)
for i in range(v): orb[find(i)].append(i)
orbits=list(orb.values()); sizes=collections.Counter(len(o) for o in orbits)
print(f"q={q} C={C} preset={pre}: {len(orbits)} orbits, sizes {dict(sorted(sizes.items()))}")
from ortools.sat.python import cp_model
m=cp_model.CpModel(); y=[m.NewBoolVar(f"y{k}") for k in range(len(orbits))]
oid=[0]*v
for k,o in enumerate(orbits):
    for i in o: oid[i]=k
for L in lines:
    w=collections.Counter(oid[i] for i in L)
    expr=sum(c*y[k] for k,c in w.items())
    m.Add(expr>=1); m.Add(expr<=C)
tot=sum(len(o)*y[k] for k,o in enumerate(orbits))
if a.lo: m.Add(tot>=a.lo)
if a.hi: m.Add(tot<=a.hi)
s=cp_model.CpSolver(); s.parameters.num_search_workers=a.workers; s.parameters.max_time_in_seconds=a.time
t0=time.time(); r=s.Solve(m); dt=time.time()-t0; st=s.StatusName(r)
print(f"  CP-SAT -> {st} in {dt:.1f}s")
if st in ('OPTIMAL','FEASIBLE'):
    S=[list(pts[i]) for k,o in enumerate(orbits) if s.Value(y[k]) for i in o]
    ok,hist,n=check(q,C,S); print(f"  WITNESS |S|={n} check={ok} spectrum={hist}")
    out=f"runs/witness_q{q}_c{C}_orbit_{pre.replace(':','')}.json"; json.dump(S,open(out,'w')); print("  wrote",out)
