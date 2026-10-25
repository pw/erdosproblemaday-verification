#!/usr/bin/env python3
"""Referee: exact peak location (DTFT maximisation over the element set, no parabolic step), bias of spectrum.py's
log-parabolic refine(), and integer-relation / rank-1 tests on the peak frequencies.  usage: ref_spectrum.py elems.u32"""
import sys, numpy as np, itertools, math
fn=sys.argv[1]
el=np.fromfile(fn,dtype='<u4').astype(np.int64); N=int(el[-1]); lo=N//5
b=np.zeros(N+1,dtype=np.float64); b[el]=1; x=b[lo:]; x=x-x.mean(); L=len(x)
F=np.fft.rfft(x); P=np.abs(F)**2; P[0]=0; tot=P.sum(); del F
order=np.argsort(-P); peaks=[]
for k in order[:3000]:
    if all(abs(k-j)>3 for j in peaks): peaks.append(int(k))
    if len(peaks)>=40: break
def refine(k):
    y0,y1,y2=np.log(P[k-1]),np.log(P[k]),np.log(P[k+1]); den=(y0-2*y1+y2); d=0.5*(y0-y2)/den if den else 0; return (k+d)/L
w=el[el>=lo]-lo   # positions in window
def pw(f): # |DTFT|^2 of the (non-mean-subtracted) indicator at f (fine away from 0)
    z=np.exp(-2j*np.pi*f*w); return abs(z.sum())**2
def exact(k):
    a,c=(k-1)/L,(k+1)/L; gr=(math.sqrt(5)-1)/2
    x1=c-gr*(c-a); x2=a+gr*(c-a); f1=pw(x1); f2=pw(x2)
    for _ in range(40):
        if f1>f2: c,x2,f2=x2,x1,f1; x1=c-gr*(c-a); f1=pw(x1)
        else: a,x1,f1=x1,x2,f2; x2=a+gr*(c-a); f2=pw(x2)
    return (a+c)/2
ex=[exact(k) for k in peaks]; par=[refine(k) for k in peaks]
print(f"file={fn} L={L} bin={1/L:.3e}")
bias=[(p-e)*L for p,e in zip(par,ex)]
print("parabolic refine minus exact DTFT max, in bins: max |.| =",round(max(abs(t) for t in bias),3)," mean |.| =",round(float(np.mean(np.abs(bias))),3))
for i,(k,e,p) in enumerate(zip(peaks,ex,par)): print(f"  #{i+1:2d} bin {k} exact f={e:.10f} parabolic={p:.10f} diff={(p-e)*L:+.3f} bins  share={P[k]/tot*100:.2f}%")
np.save(fn.split('/')[-1]+'.peaks.npy',np.array(ex))
# share of variance within +-3 bins of top 14
m=np.zeros(len(P),bool)
for k in peaks[:14]: m[max(0,k-3):k+4]=True
print(f"variance within +-3 bins of the 14 largest peaks: {P[m].sum()/tot*100:.2f}%  (single-bin sum of top 14: {sum(P[k] for k in peaks[:14])/tot*100:.2f}%)")
# integer relations among the two / three largest
def rel(fs,C):
    out=[]
    for c in itertools.product(range(-C,C+1),repeat=len(fs)):
        if not any(c) or next(t for t in c if t)<0: continue
        v=sum(ci*fi for ci,fi in zip(c,fs)); d=abs((v+0.5)%1-0.5)*L; out.append((d,c))
    out.sort(); return out[:4]
print("smallest relations among top-2 (|c|<=20), distance in bins:",[(round(d,3),c) for d,c in rel(ex[:2],20)])
print("smallest relations among top-3 (|c|<=12):",[(round(d,3),c) for d,c in rel(ex[:3],12)])
# rank-1 search: candidate generators g = a*f_i + b*f_j for top-4 pairs, |a|,|b|<=12; score = #peaks within 1 bin of m*g, |m|<=150
best=(0,None)
cands=set()
for i,j in itertools.combinations(range(4),2):
    for a in range(-12,13):
        for bb in range(-12,13):
            if a==0 and bb==0: continue
            g=(a*ex[i]+bb*ex[j])%1
            if g>0.5: g=1-g
            if g>1e-4: cands.add(round(g,12))
ms=np.arange(1,151)
E=np.array(ex)
for g in cands:
    mg=(np.outer(ms,[g]).ravel())%1
    d=np.abs(((mg[None,:]-E[:,None])+0.5)%1-0.5); d=np.minimum(d,np.abs(((mg[None,:]+E[:,None])+0.5)%1-0.5))
    hit=(d.min(1)*L<=1.0).sum()
    if hit>best[0]: best=(int(hit),g)
g=best[1]; print(f"best single generator (|m|<=150, within 1 bin): g={g:.10f} explains {best[0]}/40 peaks")
# least-squares refine g from assigned multipliers
assign=[]
for f in ex:
    cand=[(abs(((m*g-s*f)+0.5)%1-0.5),m,s) for m in range(1,151) for s in (1,-1)]
    d,m,s=min(cand); assign.append((d*L,m,s,f))
good=[(m,s,f) for d,m,s,f in assign if d<=1.0]
# m*g = s*f + n  -> g = (s*f+n)/m ; weighted LS
num=0;den=0
for m,s,f in good:
    n=round(m*g-s*f); num+=m*(s*f+n); den+=m*m
g2=num/den
res=[ (abs(((m*g2-s*f)+0.5)%1-0.5)*L) for m,s,f in good]
print(f"LS-refined g={g2:.11f}; residuals on the {len(good)} assigned peaks: max {max(res):.3f} bins; multipliers used: {sorted(set(m for m,_,_ in good))}")
print("unexplained peaks (index, f, nearest |m|<=150 distance in bins):",[(i+1,round(f,8),round(d,2)) for i,(d,m,s,f) in enumerate(assign) if d>1.0])
xg=g2; cf=[]
for _ in range(10):
    a_=math.floor(xg); cf.append(a_); xg=xg-a_
    if xg<1e-12: break
    xg=1/xg
q0,q1=0,1; qs=[]
for a_ in cf[1:]:
    q0,q1=q1,a_*q1+q0; qs.append(q1)
print("continued fraction of g:",cf," denominators:",qs)
