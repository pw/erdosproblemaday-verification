# Referee's own DIMACS reader: decompose a cube CNF into (units, pure point clauses, aux-connected components),
# identify every component's point set geometrically, and determine each component's semantics by SAT tests
# (exhaustive over all 2^n input assignments for n<=14; sampled for the 183-point blocks).
import sys,json,random,itertools,time
from pysat.solvers import Minisat22
from pg import plane
q=13; NP=q*q+q+1
cnf_path,pts_path=sys.argv[1],sys.argv[2]; exhaustive=len(sys.argv)>3 and sys.argv[3]=='exh'
P=[tuple(p) for p in json.load(open(pts_path))['points']]
mypts,lines=plane(q); assert sorted(P)==sorted(mypts) and len(P)==NP and len(set(P))==NP
v2p={i+1:P[i] for i in range(NP)}; p2v={p:v for v,p in v2p.items()}
cls=[];nv=nc=None
for ln in open(cnf_path):
    if ln.startswith('c'): continue
    if ln.startswith('p'): _,_,nv,nc=ln.split(); nv,nc=int(nv),int(nc); continue
    cls.append([int(t) for t in ln.split()][:-1])
assert len(cls)==nc, (len(cls),nc)
def name(S):
    S=frozenset(S)
    if len(S)==NP: return 'ALL183'
    for L,s in lines.items():
        if S==s: return f'line{L}'
        if len(S)==q and S<=s: return f'line{L}-minus{tuple(sorted(s-S)[0])}'
    return f'??{len(S)}pts'
units=[c[0] for c in cls if len(c)==1]
pos=sorted(v2p[u] for u in units if u>0 and u<=NP); neg=sorted(v2p[-u] for u in units if u<0 and -u<=NP)
auxunits=[u for u in units if abs(u)>NP]
print('vars',nv,'clauses',nc,'| pos units:',pos,'| #neg units:',len(neg),'| aux units:',len(auxunits))
negset=set(neg)
for L in [(1,0,0),(0,0,1)]:
    print(f'  neg units == {name(lines[L])} minus pos?', negset==set(lines[L])-set(pos) and True, '| neg units on', L, ':', len(set(lines[L])&negset))
print('  neg units exactly = (x=0 \\ P0) U (z=0 \\ Q1):', negset==(set(lines[(1,0,0)])-{(0,0,1)})|(set(lines[(0,0,1)])-{(1,0,0)}))
pure=[c for c in cls if len(c)>1 and all(abs(l)<=NP for l in c)]
purelines=sorted(name({v2p[l] for l in c}) for c in pure if all(l>0 for l in c))
print('pure point clauses:',len(pure),'all positive & each a full line:',len(purelines)==len(pure) and all(n.startswith('line') and 'minus' not in n for n in purelines),'distinct lines:',len(set(purelines)))
# union-find over aux vars
par={}
def f(a):
    while par.setdefault(a,a)!=a: par[a]=par[par[a]]; a=par[a]
    return a
for c in cls:
    ax=[abs(l) for l in c if abs(l)>NP]
    for a in ax[1:]: par[f(a)]=f(ax[0])
    if ax: f(ax[0])
comp={}
for c in cls:
    ax=[abs(l) for l in c if abs(l)>NP]
    if ax: comp.setdefault(f(ax[0]),[]).append(c)
print('aux components:',len(comp))
def canon(cc):
    m={}; out=[]
    for c in cc:
        out.append(tuple((1 if l>0 else -1)*m.setdefault(abs(l),len(m)+1) for l in c))
    return tuple(out)
seen_canon={}
rows=[]; t0=time.time()
for r,cc in comp.items():
    inp=sorted({abs(l) for c in cc for l in c if abs(l)<=NP}); n=len(inp)
    s=Minisat22(bootstrap_with=cc); sat=set()
    def test(on):
        return s.solve(assumptions=[v if v in on else -v for v in inp])
    cf=canon(cc) if n==14 else None
    if cf is not None and cf in seen_canon:
        sat=seen_canon[cf]
    elif n<=14 and exhaustive:
        res={}
        for mask in range(1<<n):
            on={inp[i] for i in range(n) if mask>>i&1}; k=len(on); b=test(on)
            res.setdefault(k,set()).add(b)
        assert all(len(v)==1 for v in res.values()), 'count-dependent? NO: semantics not symmetric'
        sat={k for k,v in res.items() if True in v}
    else:
        R=random.Random(1)
        for k in range(n+1):
            reps=40 if (n==NP and (k in range(15,25) or k in range(33,42))) else 3
            outs={test(set(R.sample(inp,k))) for _ in range(reps)}
            assert len(outs)==1,(k,outs)
            if True in outs: sat.add(k)
    s.delete()
    if cf is not None and cf not in seen_canon: seen_canon[cf]=sat
    lo,hi=min(sat),max(sat); assert sat==set(range(lo,hi+1))
    sem=('>=%d'%lo if hi==n else '')+(' & ' if lo>0 and hi<n else '')+('<=%d'%hi if hi<n else '')
    if lo==0 and hi==n: sem='TRIVIAL'
    rows.append((name({v2p[v] for v in inp}),n,sem,len(cc)))
from collections import Counter
cnt=Counter((('line(any)' if (nm.startswith('line') and 'minus' not in nm) else nm),n,sem) for nm,n,sem,_ in rows)
for k,v in sorted(cnt.items(),key=lambda z:(-z[1],z[0])): print(f'  {v:4d} x  {k[0]:28s} n={k[1]:3d}  {k[2]}')
print('distinct canonical forms among 14-point components:',len(seen_canon))
print('component-test time',round(time.time()-t0,1),'s; exhaustive' if exhaustive else '; sampled')
