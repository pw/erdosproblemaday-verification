# Probe the distinct-rule extension of the July lemma: does any x in [2N+q-1, 2N+2q-2] need u=v?
import sys, numpy as np
elems, qgap = sys.argv[1], int(sys.argv[2]); seed=[int(x) for x in sys.argv[3:]]
el=np.fromfile(elems,dtype='<u4').astype(np.int64); M=max(seed)
shifts=el[qgap:]-el[:-qgap]; Q=int(shifts[-1]); bad=np.nonzero(shifts!=Q)[0]; K=int(bad[-1])+1 if len(bad) else 0
N=int(el[K]); P=[int(x) for x in el if x<N]; R=sorted({int(x)%Q for x in el[K:K+qgap]})
Pm={p%Q for p in P}; Rs=set(R)
# residues s not in R that have NO non-diagonal witness (e in P mod q) or (e,r in R, e!=r)
only_diag=[]
for s in range(Q):
    if s in Rs: continue
    ok=any(((s-r)%Q) in Pm for r in R) or any((((s-r)%Q) in Rs and (s-r)%Q!=r) for r in R)
    if not ok: only_diag.append(s)
print(f"N={N} q={Q} |R|={len(R)} residues outside R with only a diagonal (u=v) witness: {len(only_diag)} {only_diag[:10]}")
# brute-force: proposed T, distinct recurrence through 2N+2q-2 (one extra period beyond the certify.py range)
L=2*N+2*Q-2
T=np.zeros(L+1,dtype=bool); T[P]=True; xs=np.arange(N,L+1); T[xs[np.isin(xs%Q,R)]]=True
Lp=1
while Lp<2*(L+1): Lp*=2
F=np.fft.rfft(T.astype(np.float64),Lp); cnt=np.rint(np.fft.irfft(F*F,Lp)[:L+1]).astype(np.int64)
ev=np.arange(0,L+1,2); cnt[ev]-=T[ev//2].astype(np.int64)
x=np.arange(M+1,L+1); viol=x[T[x]==(cnt[x]>0)]
print(f"distinct recurrence on ({M},{L}] (= through 2N+2q-2): violations={len(viol)} first={viol[:5].tolist()}")
# and the actual greedy data agrees with the proposal far beyond
G=np.zeros(int(el.max())+1,dtype=bool); G[el]=True
Lmax=int(el.max()); T2=np.zeros(Lmax+1,dtype=bool); T2[P]=True; xs=np.arange(N,Lmax+1); T2[xs[np.isin(xs%Q,R)]]=True
print(f"proposal vs greedy run on [1,{Lmax}]: mismatches={int((T2!=G).sum())}")
