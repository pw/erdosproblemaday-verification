# Independent exhaustive max over line classes of min over tau, for the line instance.
# i_p computed as e_p / ord_p(2^a 3^b) from the actual prime (not from u,v); weights 1/ord.
import json, sys, itertools, time
from math import gcd
from fractions import Fraction as F
import numpy as np
from sympy import n_order
D='/home/exedev/MathDyad/erdos203'
N=int(sys.argv[1]); a,b=map(int,sys.argv[2].split(',')); sym=len(sys.argv)>3 and sys.argv[3]=='sym'
pool=json.load(open(f'{D}/pool_{N}.json'))['pool']
lum=[]; E=F(0)
for q in pool:
    p=q['p']; e=n_order(2,p)*n_order(3,p)//gcd(n_order(2,p),n_order(3,p))
    g=pow(2,a,p)*pow(3,b,p)%p; o=n_order(g,p); i=e//o
    if i==1: E+=F(1,o)
    else: lum.append((p,i,F(1,o)))
M=1
for _,i,_ in lum: M=M*i//gcd(M,i)
S=E.denominator
for *_,w in lum: S=S*w.denominator//gcd(S,w.denominator)
lum.sort(key=lambda x:-x[1])
tau=np.arange(M)
def table(group, fix_first):
    # all class choices for this group: matrix (n, M) of contributions
    W=np.zeros((1,M),dtype=np.int64)
    for j,(p,i,w) in enumerate(group):
        rng=[0] if (fix_first and j==0) else range(i)
        vecs=np.stack([np.where(tau%i==r, int(w*S), 0) for r in rng])
        W=(W[:,None,:]+vecs[None,:,:]).reshape(-1,M)
    return W
prod=1
for _,i,_ in lum: prod*=i
# split so that both tables are moderate
cut=1; pa=1
while cut<len(lum) and pa*lum[cut-1][1] <= int(prod**0.5)+1: pa*=lum[cut-1][1]; cut+=1
A=lum[:cut-1] if cut>1 else lum[:1]; B=lum[len(A):]
t0=time.time()
WA=table(A, sym); WB=table(B, False); WB+=int(E*S)
best=-1
chunk=max(1, int(2.5e7 // (WB.shape[0]*M)))
for s in range(0, WA.shape[0], chunk):
    blk=WA[s:s+chunk]
    m=(blk[:,None,:]+WB[None,:,:]).min(axis=2).max()
    if m>best: best=int(m)
V=F(best,S)
print(json.dumps({'N':N,'dir':[a,b],'M':M,'lumpy':len(lum),'prod_i':prod,'sym':sym,'configs':WA.shape[0]*WB.shape[0],'V':str(V),'V_f':float(V),'secs':round(time.time()-t0,1)}))
