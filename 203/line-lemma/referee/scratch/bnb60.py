# Solver-free exact check: is there a class choice with W(tau) >= 1 for all tau mod Mp?  (coarse line instance)
# Pruning bound (valid): for any cell set T, sum_{tau in T} W(tau) <= sum_T Wfix + sum_free w_p * max_c |{tau in T: tau = c mod i_p}|.
import json, sys, time
from math import gcd
from fractions import Fraction as F
import numpy as np
from sympy import n_order
D='/home/exedev/MathDyad/erdos203'
N=int(sys.argv[1]); a,b=map(int,sys.argv[2].split(',')); Mp=int(sys.argv[3]); TL=float(sys.argv[4]); sym=(sys.argv[5]=='sym') if len(sys.argv)>5 else False
import os
PF=os.environ.get('POOLFILE'); pool=json.load(open(PF if PF else f'{D}/pool_{N}.json'))['pool']
E=F(0); lum=[]
for q in pool:
    p=q['p']; o2,o3=n_order(2,p),n_order(3,p); e=o2*o3//gcd(o2,o3)
    o=n_order(pow(2,a,p)*pow(3,b,p)%p,p); i=gcd(e//o,Mp)
    if i==1: E+=F(1,e)
    else: lum.append((p,i,F(i,e)))
S=E.denominator
for *_,w in lum: S=S*w.denominator//gcd(S,w.denominator)
lum.sort(key=lambda x:(-x[2], -x[1]))
wi=[int(w*S) for *_,w in lum]; ii=[i for _,i,_ in lum]
need=S-int(E*S)          # each cell needs lumpy mass >= need
tau=np.arange(Mp)
masks=[[ (tau%i==c) for c in range(i)] for i in ii]
suffix=[0]*(len(lum)+1)
for j in range(len(lum)-1,-1,-1): suffix[j]=suffix[j+1]+wi[j]
nodes=0; t0=time.time(); timed_out=False
def bound_ok(W,j):
    # return False if provably infeasible
    order=np.argsort(W, kind='stable')
    Ws=W[order]
    if Ws[0]+suffix[j] < need: return False
    # cell sets T = k lowest cells, k = 2..Mp (check a few sizes)
    for k in (2,3,4,6,8,12,16,24,32,48,Mp):
        if k>Mp: break
        T=order[:k]
        tot=int(Ws[:k].sum())
        for jj in range(j,len(lum)):
            i=ii[jj]
            cnt=np.bincount(T%i, minlength=i).max()
            tot+=wi[jj]*int(cnt)
            if tot>=need*k: break
        if tot < need*k: return False
    return True
def dfs(j,W):
    global nodes,timed_out
    nodes+=1
    if nodes%20000==0 and time.time()-t0>TL: timed_out=True; return True
    if j==len(lum): return bool((W>=need).all())
    if not bound_ok(W,j): return False
    rng=[0] if (sym and j==0) else range(ii[j])
    for c in rng:
        W2=W.copy(); W2[masks[j][c]]+=wi[j]
        if dfs(j+1,W2): return True
        if timed_out: return True
    return False
W0=np.zeros(Mp,dtype=np.int64)
found=dfs(0,W0)
print(json.dumps({'N':N,'dir':[a,b],'Mp':Mp,'lumpy':len(lum),'sym':sym,'result':('TIMEOUT' if timed_out else ('FEASIBLE' if found else 'INFEASIBLE (no class choice reaches 1 on every cell)')),'nodes':nodes,'secs':round(time.time()-t0,1)}),flush=True)
