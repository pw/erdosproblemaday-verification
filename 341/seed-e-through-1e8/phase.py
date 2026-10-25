#!/usr/bin/env python3
"""Phase histogram: is S (on [N/5,N]) concentrated on an arc of the circle under x -> {x*g}?  If S were a coding of the rotation by g
with an interval window W, every element would satisfy {x g} in W; the fraction of S inside the best arc of length = density
measures how much of S the rotation explains (referee item 2: 'a dominant rotation plus a residual').
usage: phase.py elems.u32 g [bins=200]"""
import sys, numpy as np
el=np.fromfile(sys.argv[1],dtype='<u4').astype(np.int64); g=float(sys.argv[2]); B=int(sys.argv[3]) if len(sys.argv)>3 else 200
N=int(el[-1]); lo=N//5; xs=el[el>=lo]; dens=len(xs)/(N-lo)
ph=(xs*g)%1.0; h=np.bincount((ph*B).astype(int),minlength=B)/len(xs)
# best arc of length dens (in bins) and of length 2*dens
for arc in (dens,1.5*dens,2*dens):
    w=max(1,int(round(arc*B))); cs=np.concatenate([h,h]); win=np.array([cs[i:i+w].sum() for i in range(B)]); i=int(win.argmax())
    print(f"best arc of length {arc:.4f} ({w} bins): starts at {i/B:.3f}, holds {win[i]*100:.1f}% of S  (a uniform set would hold {arc*100:.1f}%)")
print("histogram (200 bins, % of S):"); print(" ".join(f"{v*100:.2f}" for v in h))
# complement: are NON-elements excluded from the arc? sample 2e6 non-elements
b=np.zeros(N+1,bool); b[el]=True; cand=np.arange(lo,N+1); non=cand[~b[lo:]]; rng=np.random.default_rng(0); non=rng.choice(non,size=min(2_000_000,len(non)),replace=False)
phn=(non*g)%1.0; hn=np.bincount((phn*B).astype(int),minlength=B)/len(non)
w=max(1,int(round(dens*B))); cs=np.concatenate([h,h]); win=np.array([cs[i:i+w].sum() for i in range(B)]); i=int(win.argmax())
inarc=sum(hn[(i+j)%B] for j in range(w)); print(f"non-elements with phase inside S's best arc: {inarc*100:.1f}%  (uniform: {w/B*100:.1f}%)")
