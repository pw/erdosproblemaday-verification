import numpy as np, itertools, time, sys
from math import gcd, lcm
from fractions import Fraction as F
from sympy import primefactors, divisors
D="/home/exedev/MathDyad/erdos203/"
P=[5,7,11,13,17,19]
rows=[tuple(map(int,l.split())) for l in open(D+"S6.txt") if l.strip()]
T=720
k,l=np.meshgrid(np.arange(T),np.arange(T),indexing="ij")
def pk(b): return np.packbits(b.reshape(-1)).view(np.uint64)
cos=[]; adm_by_rep={}
for p,(e,u,v) in zip(P,rows):
    chi=(u*k+v*l)%e
    cos.append([pk(chi==c) for c in range(e)])
def admissible(p,e,u,v,c,d):
    # decorrelated: pick a representative (k,l) of coset c, a = 2^k 3^l mod p is -m^{-1}; m = -a^{-1}
    for kk in range(e):
        for ll in range(e):
            if (u*kk+v*ll)%e==c:
                a=pow(2,kk,p)*pow(3,ll,p)%p; m=(-pow(a,-1,p))%p; g=gcd(d,p-1)
                return pow(m,(p-1)//g,p)==1
def free(d):
    Fs=np.zeros((T,T),bool)
    for q in primefactors(d):
        if q%2: Fs|=(k%q==0)&(l%q==0)
    if d%4==0: Fs|=(k%4==2)&(l%4==0)
    return Fs
def Ud(d):
    al=[[c for c in range(e) if admissible(p,e,u,v,c,d)] for p,(e,u,v) in zip(P,rows)]
    Fb=pk(free(d)); best=-1
    lastI=max(range(6),key=lambda i:len(al[i])); others=[i for i in range(6) if i!=lastI]
    L=np.stack([cos[lastI][c] for c in al[lastI]])
    for cs in itertools.product(*[al[i] for i in others]):
        acc=Fb.copy()
        for i,c in zip(others,cs): acc|=cos[i][c]
        tot=np.bitwise_count(acc[None,:]|L).sum(axis=1); m=int(tot.max())
        best=max(best,m)
    return [len(a) for a in al], F(best,T*T), float(F(int(free(d).sum()),T*T))
t0=time.time()
for d in [int(x) for x in sys.argv[1].split(",")]:
    a,U,fr=Ud(d); print("d",d,"allowed",a,"F %.4f"%fr,"U_d",U,"= %.6f"%float(U),"%.0fs"%(time.time()-t0),flush=True)
