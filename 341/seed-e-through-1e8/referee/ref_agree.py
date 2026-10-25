#!/usr/bin/env python3
"""Exact agreement fraction A(q) = #{x in [lo, N-q): b[x]==b[x+q]} / (N-q-lo) for EVERY shift q <= maxshift, from exact
pair counts (FFT, rounded), vs analyze.py's record chain which ranks shifts by ac[q]/ac[0] (no overlap normalisation)."""
import sys, numpy as np
fn=sys.argv[1]; el=np.fromfile(fn,dtype='<u4').astype(np.int64); N=int(el[-1]); lo=N//5
maxshift=int(sys.argv[2]) if len(sys.argv)>2 else N//3
b=np.zeros(N+1,dtype=np.float64); b[el]=1; x=b[lo:N]   # analyze.py compares b[lo:N-q] with b[lo+q:N]
n=len(x); Lf=1
while Lf<2*n: Lf*=2
F=np.fft.rfft(x,Lf); both=np.rint(np.fft.irfft(F*np.conj(F),Lf)[:maxshift+1]); del F
cs=np.concatenate([[0],np.cumsum(x)])
q=np.arange(maxshift+1); ov=n-q
ones_first=cs[n-q]-cs[0]; ones_second=cs[n]-cs[q]
agree=(ov-ones_first-ones_second+2*both)/ov
# analyze.py's biased statistic
xm=x-x.mean(); F=np.fft.rfft(xm,Lf); ac=np.fft.irfft(F*np.conj(F),Lf)[:maxshift+1]; ac=ac/ac[0]; del F
for s in (130,253,636,766,889,1655,2544,4199,9547,10436,27875):
    a=ac; loc=a[s]>=a[max(1,s-20):s+21].max()
    print(f"shift {s}: agreement {agree[s]:.4f}  analyze.py ac={ac[s]:.4f}  local max of ac within +-20: {bool(loc)}  ac>0.8: {bool(ac[s]>0.8)}")
a=agree.copy(); a[:21]=0
top=np.argsort(-a)[:15]
print("largest exact agreement over 21<=q<=%d:"%maxshift,[(int(t),round(float(agree[t]),5)) for t in top])
for lim in (30000,100000,300000,1000000,maxshift):
    t=21+int(np.argmax(agree[21:lim+1])); print(f"  best exact agreement for q<={lim}: q={t} A={agree[t]:.5f}; analyze.py's ac at that q={ac[t]:.4f} (bias factor (n-q)/n={(n-t)/n:.4f})")
# largest q at which analyze.py's ac could exceed its own best (0.9512) even at perfect true correlation
qq=np.arange(1,maxshift+1); cap=(n-qq)/n
print("analyze.py candidate threshold ac>0.8 is unreachable (even at true correlation 1) for q >",int(qq[cap<=0.8][0]) if (cap<=0.8).any() else None)
print("analyze.py cannot record a new best above 0.9512 for q >",int(qq[cap<=0.9512][0]) if (cap<=0.9512).any() else None)
