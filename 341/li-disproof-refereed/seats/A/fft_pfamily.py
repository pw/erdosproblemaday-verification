import numpy as np, sys
p=int(sys.argv[1]); LOG2=int(sys.argv[2]); N=(1<<LOG2)-1; M=7*p
n=np.arange(N+1,dtype=np.int64); r=n%M; q=n//M
def ex(lo,hi,q,plus1):
    out=np.zeros(q.shape,dtype=bool); a=1
    while lo*a<=q.max()+1:
        lhs=(q+1) if plus1 else q
        out|=(lo*a<=lhs)&(q<hi*a); a*=8
    return out
Y0=(q==0)|ex(4,8,q,False); Y1=((1<=q)&(q<=3))|ex(16,32,q,True); Y2=(q<=1)|((7<=q)&(q<=15))|ex(64,128,q,True)
Pset=[p,2*p,4*p]; Bset=[M-3,M-1,6*p+3]; Q=set(Pset)|set(Bset)
F=Q|{(x-b)%M for x in Q for b in Bset}|{(x-a)%M for x in Q for a in Pset}
Dl=[d for d in range(1,M) if d not in F]
S=np.isin(n,Dl)|np.isin(r,Bset)|((r==p)&Y0)|((r==2*p)&Y1)|((r==4*p)&Y2)
A=sorted(set(Dl)|set(Bset)|{M+b for b in Bset}|{p,4*p,M+2*p,M+4*p})
assert np.nonzero(S[:2*M])[0].tolist()==A, "seed prefix mismatch"
L=1<<(LOG2+1)
f=np.fft.rfft(S.astype(np.float64),L); f*=f; c=np.fft.irfft(f,L)[:N+1]
rep=np.rint(c)>0.5; err=np.abs(c-np.rint(c)).max()
bad=np.nonzero((S!=~rep)[2*M:])[0]+2*M
print(f"p={p} M={M} N={N} |A_p|={len(A)} (7p-20={7*p-20}) |S|={int(S.sum())} fft_err={err:.1e} recurrence violations t>2M-1: {len(bad)} first={bad[:6].tolist()}")
# also: rail-p indicator equals Y0 (rail encodes the aperiodic controller)
qs=np.arange((N-p)//M+1); print("rail p == Y0 on q<=%d:"%qs[-1], bool(np.array_equal(S[M*qs+p], Y0[M*qs])))
