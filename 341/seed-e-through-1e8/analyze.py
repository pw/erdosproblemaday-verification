#!/usr/bin/env python3
"""analyze.py — every structural number quoted in the entry, from ONE elems file (uint32 LE, increasing), by routes
independent of fast341's C code: Python border-array period test on gap suffixes (a second implementation of the
KMP probe), counting-function discrepancy, FFT autocorrelation hierarchy, residue-class census, factor complexity,
membership-bit SHA-256 in the July 2026 packing (bit x = [x in S], little-endian bytes).
usage: analyze.py elems.u32 [maxshift] [--fast]"""
import sys, numpy as np, hashlib, time
from collections import Counter
fn=sys.argv[1]; fast='--fast' in sys.argv
el=np.fromfile(fn,dtype='<u4').astype(np.int64); N=int(el[-1]); n=len(el)
maxshift=int([a for a in sys.argv[2:] if not a.startswith('--')][0]) if len([a for a in sys.argv[2:] if not a.startswith('--')]) else min(4_000_000,N//3)
print(f"file={fn} elements={n} last={N} density={n/N:.6f}")
g=np.diff(el); print("maxgap",int(g.max()),"gap histogram",sorted(Counter(g.tolist()).items()))
# --- exact-period test on gap-word suffixes (border array, pure Python) ---
def smallest_period(w):
    L=len(w); pi=[0]*L; k=0
    for i in range(1,L):
        while k and w[i]!=w[k]: k=pi[k-1]
        if w[i]==w[k]: k+=1
        pi[i]=k
    return L-pi[-1]
for frac in (0.5,0.75,0.9):
    s=int(len(g)*frac); w=g[s:].tolist(); t0=time.time(); p=smallest_period(w)
    print(f"gap suffix from term {s} (len {len(w)}): smallest period {p} -> {'A PERIOD OF THIS SUFFIX' if p<=len(w)//2 else 'no period <= half the suffix'} ({time.time()-t0:.0f}s)")
# --- discrepancy of the counting function ---
dens=n/N; D=np.arange(1,n+1)-dens*el
for X in [10**5,10**6,10**7,N]:
    if X<=N: m=el<=X; print(f"max|count(x)-density*x| for x<={X}: {np.abs(D[m]).max():.1f}  (sqrt X = {X**0.5:.0f})")
# --- membership SHA-256 (July packing) ---
def sha_through(limit):
    bits=np.zeros(limit+1,dtype=np.uint8); bits[el[el<=limit]]=1
    raw=np.packbits(bits,bitorder='little').tobytes()[:(limit+8)//8]
    return hashlib.sha256(raw).hexdigest()
if N>=500000: print("membership sha256 through 500000:",sha_through(500000),"(July 2026 report: 3a045efefd9edd5c74813c40d09c592abb8bea461daba7da9f4f156a94d60aa9)")
print(f"membership sha256 through {N}:",sha_through(N))
# --- residue-class census (rails?) ---
lo=N//2; w=el[el>=lo]
worst=[]
for m in range(2,401):
    c=np.bincount(w%m,minlength=m); worst.append((c.min()/c.mean(),c.max()/c.mean(),m))
worst.sort(); print("residue census m<=400 on [N/2,N]: most depleted class (min/mean, m):",[(round(a,3),m) for a,b,m in worst[:3]],"most over-full (max/mean, m):",[(round(b,3),m) for a,b,m in sorted(worst,key=lambda t:-t[1])[:3]])
# --- autocorrelation hierarchy on [N/5, N] ---
if not fast:
    b=np.zeros(N+1,dtype=np.float32); b[el]=1; lo=N//5; x=b[lo:]-b[lo:].mean()
    L=1
    while L<2*len(x): L*=2
    F=np.fft.rfft(x,L); ac=np.fft.irfft(F*np.conj(F),L)[:len(x)]; ac=ac/ac[0]; del F,x
    n_=len(b)-lo; ac[:maxshift]=ac[:maxshift]/((n_-np.arange(maxshift))/n_)   # v2: normalise by the overlap (referee item 8)
    a=ac[:maxshift]
    cand=[q for q in range(21,maxshift-21) if a[q]>0.8 and a[q]>=a[q-20:q+21].max()]
    rec=[];best=0
    for q in cand:
        if a[q]>best: best=a[q]; rec.append((q,round(float(a[q]),4)))
    print(f"autocorrelation on [{lo},{N}], shifts <= {maxshift}: record chain {rec}")
    top=sorted(cand,key=lambda q:-a[q])[:12]; print("top peaks:",[(q,round(float(a[q]),4)) for q in top])
    ex=sorted(((float((b[lo:N-q]==b[lo+q:N]).mean()),q) for q in sorted(cand,key=lambda q:-a[q])[:60]),reverse=True)
    print(f"exact (overlap-normalised) agreement at the 60 strongest candidates: best {ex[0][1]} at {ex[0][0]:.5f}; next {[(q,round(v,5)) for v,q in ex[1:6]]}")
    if top:
        q=ex[0][1]; agree=ex[0][0]; print(f"best shift {q}: agreement fraction {agree:.4f} (mismatch {1-agree:.4f})")
    print("agreement at 889, 9547, 27875:",[(q,round(float((b[lo:N-q]==b[lo+q:N]).mean()),4)) for q in (889,9547,27875) if q<N-lo])
# --- discrepancy on the post-transient window [N/5, N], density refitted there, with a random comparator (referee item 7) ---
rng=np.random.default_rng(1); wmask=el>=N//5; xs=el[wmask]; k=np.arange(1,len(xs)+1); dloc=len(xs)/(N-N//5)
D2=k-dloc*(xs-N//5); print(f"post-transient discrepancy on [{N//5},{N}] (density refitted {dloc:.6f}): max|.| = {np.abs(D2).max():.0f}")
for trial in range(3):
    r=np.sort(rng.choice(np.arange(N//5,N+1),size=len(xs),replace=False)); Dr=np.arange(1,len(r)+1)-dloc*(r-N//5); print(f"   random set, same count/window, trial {trial}: {np.abs(Dr).max():.0f}")
# --- factor complexity of the gap word: whole word AND the post-transient second half, as a fraction of available windows ---
gb=g.astype(np.uint8)
def complexity(word,k):
    W=np.lib.stride_tricks.sliding_window_view(word,k); rows=np.ascontiguousarray(W).view(np.dtype((np.void,k))).ravel(); return len(np.unique(rows))
pts=[(k,complexity(gb,k)) for k in (10,20,30,50,100)]; print("factor complexity p(k) of the whole gap word:",pts)
h=gb[len(gb)//2:]; pts2=[(k,complexity(h,k)) for k in (10,20,30,50,100)]; print(f"factor complexity on the second half ({len(h)} gaps): {[(k,p,round(p/(len(h)-k+1),3)) for k,p in pts2]}  (k, p(k), p(k)/windows) — sample-limited, no exponent is claimed")
