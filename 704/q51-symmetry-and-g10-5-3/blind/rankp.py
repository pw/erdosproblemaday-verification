import sys, itertools, random, numpy as np, time
sys.path.insert(0,'/home/exedev/MathDyad/erdos704/q51')
from wstruct import random_copy
N=13
V=[frozenset(c) for c in itertools.combinations(range(N),5)]
idx={s:i for i,s in enumerate(V)}
random.seed(int(sys.argv[2]) if len(sys.argv)>2 else 7)
R=1450
A0=np.zeros((R,len(V)),dtype=np.int64)
for r in range(R):
    for s in random_copy(random): A0[r,idx[s]]=1
def rank_mod(A,p):
    A=A.copy()%p; rows,cols=A.shape; r=0
    for c in range(cols):
        if r==rows: break
        nz=np.nonzero(A[r:,c])[0]
        if len(nz)==0: continue
        piv=r+nz[0]
        if piv!=r: A[[r,piv],c:]=A[[piv,r],c:]
        inv=pow(int(A[r,c]),p-2,p); A[r,c:]=(A[r,c:]*inv)%p
        below=np.nonzero(A[r+1:,c])[0]+r+1
        if len(below): A[np.ix_(below,np.arange(c,cols))]=(A[np.ix_(below,np.arange(c,cols))]-np.outer(A[below,c],A[r,c:]))%p
        r+=1
    return r
for p in [int(x) for x in sys.argv[1].split(',')]:
    t=time.time(); print(p, rank_mod(A0,p), 'of', len(V), f'{time.time()-t:.0f}s', flush=True)
