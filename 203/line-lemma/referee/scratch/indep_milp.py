# Independent formulation of the coarse line instance; HiGHS via scipy; no symmetry reduction.
import json, sys, time
from math import gcd
from fractions import Fraction as F
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
from sympy import n_order
D='/home/exedev/MathDyad/erdos203'
def inst(N,a,b,Mp):
    pool=json.load(open(f'{D}/pool_{N}.json'))['pool']
    E=F(0); lum=[]
    for q in pool:
        p=q['p']; o2,o3=n_order(2,p),n_order(3,p); e=o2*o3//gcd(o2,o3)
        o=n_order(pow(2,a,p)*pow(3,b,p)%p if a>=0 and b>=0 else (pow(2,a,p)*pow(3,b,p))%p, p)
        i=gcd(e//o, Mp)
        if i==1: E+=F(1,e)
        else: lum.append((p,i,F(i,e)))
    return E,lum
def solve(N,a,b,Mp,mode,tl):
    E,lum=inst(N,a,b,Mp)
    S=E.denominator
    for *_,w in lum: S=S*w.denominator//gcd(S,w.denominator)
    off=[0]
    for _,i,_ in lum: off.append(off[-1]+i)
    nx=off[-1]; nv=nx+1; zi=nx
    rows=[];cols=[];vals=[]; lo=[];hi=[]
    r=0
    for tau in range(Mp):
        for j,(p,i,w) in enumerate(lum): rows.append(r); cols.append(off[j]+tau%i); vals.append(int(w*S))
        rows.append(r); cols.append(zi); vals.append(-1); lo.append(-int(E*S)); hi.append(np.inf); r+=1
    for j,(p,i,w) in enumerate(lum):
        for c in range(i): rows.append(r); cols.append(off[j]+c); vals.append(1)
        lo.append(1); hi.append(1); r+=1
    A=coo_matrix((vals,(rows,cols)),shape=(r,nv)).tocsr()
    lb=np.zeros(nv); ub=np.ones(nv); ub[zi]=int(E*S)+sum(int(w*S) for *_,w in lum)
    if mode=='feas': lb[zi]=S; cobj=np.zeros(nv)
    else: cobj=np.zeros(nv); cobj[zi]=-1
    t0=time.time()
    res=milp(cobj,constraints=LinearConstraint(A,lo,hi),integrality=np.ones(nv),bounds=Bounds(lb,ub),options={'time_limit':tl})
    out={'N':N,'dir':[a,b],'Mp':Mp,'lumpy':len(lum),'mode':mode,'status':int(res.status),'msg':res.message[:60],'secs':round(time.time()-t0,1)}
    if mode=='max':
        db=getattr(res,'mip_dual_bound',None)
        if db is not None: out['dual_bound_on_V']=float(-db/S); out['dual_bound_lt_1']=bool(-db < S)
        if res.x is not None:
            t=[int(np.argmax(res.x[off[j]:off[j+1]])) for j in range(len(lum))]
            W=np.full(Mp,int(E*S),dtype=np.int64); tau=np.arange(Mp)
            for (p,i,w),c in zip(lum,t): W[tau%i==c]+=int(w*S)
            out['V_witness']=str(F(int(W.min()),S)); out['V_witness_f']=float(F(int(W.min()),S))
    print(json.dumps(out),flush=True)
N=int(sys.argv[1]); a,b=map(int,sys.argv[2].split(',')); Mp=int(sys.argv[3]); mode=sys.argv[4]; tl=float(sys.argv[5])
solve(N,a,b,Mp,mode,tl)
