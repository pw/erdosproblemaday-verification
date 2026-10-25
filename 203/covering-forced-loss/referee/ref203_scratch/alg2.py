import numpy as np, itertools, time, sys, json
from math import gcd, lcm
from fractions import Fraction as F
from sympy import primefactors, divisors, n_order
P=[int(x) for x in sys.argv[1].split(",")]
# characters derived from scratch (generator search), not from the pool file
def char(p):
    e=lcm(n_order(2,p),n_order(3,p))
    H={1}; fr=[1]
    while fr:
        y=fr.pop()
        for g in (2,3):
            z=y*g%p
            if z not in H: H.add(z); fr.append(z)
    h=next(h for h in sorted(H) if n_order(h,p)==e)
    lg={}; t=1
    for i in range(e): lg[t]=i; t=t*h%p
    return e,lg[2],lg[3]
rows=[char(p) for p in P]
T=1
for e,_,_ in rows: T=lcm(T,e)
LCM=1
for p in P: LCM=lcm(LCM,p-1)
k,l=np.meshgrid(np.arange(T),np.arange(T),indexing="ij")
def pk(b): 
    b=b.reshape(-1); pad=(-len(b))%64
    return np.packbits(np.concatenate([b,np.zeros(pad,bool)])).view(np.uint64)
cos=[[pk((u*k+v*l)%e==c) for c in range(e)] for e,u,v in rows]
def admissible(p,e,u,v,c,d):
    for kk in range(e):
        for ll in range(e):
            if (u*kk+v*ll)%e==c:
                a=pow(2,kk,p)*pow(3,ll,p)%p; m=(-pow(a,-1,p))%p; g=gcd(d,p-1)
                return pow(m,(p-1)//g,p)==1
def free(d):
    Fs=np.zeros((T,T),bool)
    for q in primefactors(d):
        if q%2: assert T%q==0; Fs|=(k%q==0)&(l%q==0)
    if d%4==0: Fs|=(k%4==2)&(l%4==0)
    return Fs
best_all=(-1,None); t0=time.time()
for d in divisors(LCM):
    al=[[c for c in range(e) if admissible(p,e,u,v,c,d)] for p,(e,u,v) in zip(P,rows)]
    if d==1: al[0]=[0]
    Fb=pk(free(d)); best=-1
    lastI=max(range(len(P)),key=lambda i:len(al[i])); others=[i for i in range(len(P)) if i!=lastI]
    L=np.stack([cos[lastI][c] for c in al[lastI]])
    for cs in itertools.product(*[al[i] for i in others]):
        acc=Fb.copy()
        for i,c in zip(others,cs): acc|=cos[i][c]
        m=int(np.bitwise_count(acc[None,:]|L).sum(axis=1).max()); best=max(best,m)
    U=F(best,T*T)
    if U>best_all[0]: best_all=(U,d)
print("block",P,"T",T,"LCM",LCM,"max_d U_d =",best_all[0],"= %.6f at d=%d"%(float(best_all[0]),best_all[1]),"%.0fs"%(time.time()-t0))
