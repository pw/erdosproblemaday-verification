import numpy as np, itertools, time
from math import lcm
from fractions import Fraction as F
D="/home/exedev/MathDyad/erdos203/"
rows=[tuple(map(int,l.split())) for l in open(D+"S6.txt") if l.strip()]
T=1
for e,_,_ in rows: T=lcm(T,e)
k,l=np.meshgrid(np.arange(T),np.arange(T),indexing="ij")
tup=np.stack([((u*k+v*l)%e).reshape(-1) for e,u,v in rows],axis=1)
img=np.unique(tup,axis=0); n=len(img); print("quotient size",n)
masks=[np.packbits(np.stack([img[:,i]==c for c in range(e)]),axis=1) for i,(e,_,_) in enumerate(rows)]
pc=np.array([bin(i).count("1") for i in range(256)],dtype=np.int32)
t0=time.time(); best=-1; nb=0
last=masks[-1]
for cs in itertools.product(range(1),*[range(e) for e,_,_ in rows[1:-1]]):
    acc=masks[0][cs[0]].copy()
    for i in range(1,len(cs)): acc|=masks[i][cs[i]]
    tot=pc[acc[None,:]|last].sum(axis=1); m=tot.max()
    if m>best: best=m; nb=int((tot==m).sum())
    elif m==best: nb+=int((tot==m).sum())
print("S6 on quotient: max",best,"of",n,"=",F(int(best),n),"vs README 294900/518400 =",F(294900,518400),"#opt",nb,"%.1fs"%(time.time()-t0))
