import numpy as np, itertools, time
from math import lcm
from fractions import Fraction as F
D="/home/exedev/MathDyad/erdos203/"
rows=[tuple(map(int,l.split())) for l in open(D+"S7.txt") if l.strip()]
T=720
k,l=np.meshgrid(np.arange(T),np.arange(T),indexing="ij")
tup=np.stack([((u*k+v*l)%e).reshape(-1) for e,u,v in rows],axis=1)
img=np.unique(tup,axis=0); n=len(img); print("S7 quotient size",n)
masks=[np.packbits(np.stack([img[:,i]==c for c in range(e)]),axis=1) for i,(e,_,_) in enumerate(rows)]
pc=np.array([bin(i).count("1") for i in range(256)],dtype=np.int32)
t0=time.time()
LB=25278  # witness value (303336/518400 * 43200)
assert F(303336,518400)*n==LB
m31=masks[6]; m19=masks[5]
best=-1; nb=0; checked=0
for cs in itertools.product(range(1),*[range(e) for e,_,_ in rows[1:5]]):
    acc=masks[0][cs[0]].copy()
    for i in range(1,5): acc|=masks[i][cs[i]]
    u6=acc[None,:]|m19                      # 18 options for c19
    s6=pc[u6].sum(axis=1)
    for j in np.nonzero(s6 + n//30 >= LB)[0]:   # prune: adding 31 adds at most n/30
        checked+=1
        tot=pc[u6[j][None,:]|m31].sum(axis=1); m=tot.max()
        if m>best: best=m; nb=int((tot==m).sum())
        elif m==best: nb+=int((tot==m).sum())
print("S7 exact max on quotient (pruned B&B):",best,"of",n,"=",F(int(best),n),"README:",F(303336,518400),"#opt(c5=0)",nb,"S6-configs expanded",checked,"%.1fs"%(time.time()-t0))
