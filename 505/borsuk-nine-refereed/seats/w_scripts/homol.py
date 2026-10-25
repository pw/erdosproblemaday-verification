import numpy as np, sys, itertools
from fractions import Fraction
C=np.load(sys.argv[1]); K=len(C)
T=set()
for Q in itertools.combinations(range(K),4):
    for sg in itertools.product([1,-1],repeat=3):
        sgn=np.array((1,)+sg,float); M=sgn[:,None]*C[list(Q)]
        try: y=np.linalg.solve(M,np.ones(4))
        except np.linalg.LinAlgError: continue
        s=1/np.linalg.norm(y); v=y*s
        if np.delete(np.abs(C@v),list(Q)).max()<s-1e-9: T.add(Q)
T=sorted(T); F=sorted(set(f for t in T for f in itertools.combinations(t,3)))
E=sorted(set(e for t in T for e in itertools.combinations(t,2))); V=sorted(set(i for t in T for i in t))
# each triangle in exactly two tetrahedra?
from collections import Counter
cnt=Counter(f for t in T for f in itertools.combinations(t,3)); print("triangle degrees",Counter(cnt.values()))
def bd(hi,lo):
    idx={s:i for i,s in enumerate(lo)}; B=np.zeros((len(lo),len(hi)),dtype=np.int64)
    for j,s in enumerate(hi):
        for k in range(len(s)):
            B[idx[s[:k]+s[k+1:]],j]=(-1)**k
    return B
def rank_mod(B,p):
    A=B.copy()%p if p else B.astype(object)
    A=[[Fraction(int(x)) for x in row] for row in B] if p==0 else [[int(x)%p for x in row] for row in B]
    m=len(A); n=len(A[0]) if m else 0; r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if A[i][c]!=0),None)
        if piv is None: continue
        A[r],A[piv]=A[piv],A[r]
        inv=(1/A[r][c]) if p==0 else pow(A[r][c],-1,p)
        A[r]=[x*inv if p==0 else (x*inv)%p for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]!=0:
                f=A[i][c]; A[i]=[a-f*b if p==0 else (a-f*b)%p for a,b in zip(A[i],A[r])]
        r+=1
    return r
B1=bd([tuple(e) for e in E],[(v,) for v in V]); B2=bd(F,[tuple(e) for e in E]); B3=bd(T,F)
for p in (0,2):
    r1,r2,r3=rank_mod(B1,p),rank_mod(B2,p),rank_mod(B3,p)
    b0=len(V)-r1; b1=len(E)-r1-r2; b2=len(F)-r2-r3; b3=len(T)-r3
    print("field", "Q" if p==0 else "F2", "Betti",(b0,b1,b2,b3))
