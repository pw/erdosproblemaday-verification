# Check t in S <=> t not in S+S for all 97 < t <= N, S = Li's explicit set (from the Lean defs), via exact-enough FFT.
# Also: positive/negative controls (perturbed S must FAIL).
import numpy as np, sys
LOG2=int(sys.argv[1]) if len(sys.argv)>1 else 24
N=(1<<LOG2)-1
n=np.arange(N+1,dtype=np.int64); r=n%49; q=n//49
def ex(lo,hi,q,plus1):
    out=np.zeros(q.shape,dtype=bool); a=1
    while lo*a<= q.max()+1:
        lhs=(q+1) if plus1 else q
        out|=(lo*a<=lhs)&(q<hi*a); a*=8
    return out
Y0=(q==0)|ex(4,8,q,False)
Y1=((1<=q)&(q<=3))|ex(16,32,q,True)
Y2=(q<=1)|((7<=q)&(q<=15))|ex(64,128,q,True)
D=np.isin(n,[1,2,5,13,27,36,47]); B=np.isin(r,[3,22,32,40,48])
S=D|B|((r==7)&Y0)|((r==14)&Y1)|((r==28)&Y2)
assert not S[0]
assert np.nonzero(S[:98])[0].tolist()==[1,2,3,5,7,13,22,27,28,32,36,40,47,48,52,63,71,77,81,89,97]
def check(S,label):
    L=1<<(LOG2+1)
    f=np.fft.rfft(S.astype(np.float64),L); f*=f
    c=np.fft.irfft(f,L)[:N+1]; del f
    err=np.abs(c-np.rint(c)).max()
    rep=np.rint(c)>0.5
    bad=np.nonzero((S!=~rep)[98:])[0]+98
    print(f"{label}: N={N} |S|={int(S.sum())} max FFT rounding err={err:.2e} violations of (t in S <=> t not in S+S) for t>97: {len(bad)} first={bad[:8].tolist()}",flush=True)
    return len(bad)
v=check(S,"Li S")
# controls: (a) delete one far rail element on residue 7 inside a Y0 block; (b) add one element on residue 28 outside Y2
kk=max(k for k in range(12) if 49*(4*8**k)+7<=N)
S2=S.copy(); t=49*(4*8**kk)+7; assert S2[t]; S2[t]=False
v2=check(S2,f"control: drop 49*4*8^{kk}+7")
S3=S.copy()
qn=next(x for x in range(16,10**6) if not Y2[49*x])
t3=49*qn+28; assert not S3[t3]; S3[t3]=True
v3=check(S3,f"control: add 49*{qn}+28")
print("VERDICT:", "PASS" if v==0 and v2>0 and v3>0 else "FAIL")
