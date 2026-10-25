#!/usr/bin/env python3
"""Power spectrum of the indicator of a greedy set on [N/5, N]; sharp peaks; the integer Z-module they span.
v2 (2026-10-15, after the hostile referee): peaks are located EXACTLY by golden-section maximisation of the DTFT over the element
set (no parabolic step); window sidelobes (within 8 bins of a larger peak) are excluded; generators are tested for INTEGER RELATIONS
(|c| <= RELMAX) before being called independent, so the reported rank is a Z-rank, not a coefficient-bounded one; tolerances are stated.
usage: spectrum.py elems.u32 [C=6] [RELMAX=50]"""
import sys, numpy as np, itertools
fn=sys.argv[1]; C=int(sys.argv[2]) if len(sys.argv)>2 else 6; RELMAX=int(sys.argv[3]) if len(sys.argv)>3 else 50
el=np.fromfile(fn,dtype='<u4').astype(np.int64); N=int(el[-1]); lo=N//5
ew=el[el>=lo].astype(np.float64)
b=np.zeros(N+1,dtype=np.float64); b[el]=1; x=b[lo:]; x=x-x.mean(); L=len(x)
F=np.fft.rfft(x); P=np.abs(F)**2; P[0]=0; tot=P.sum(); bw=1/L
def dtft2(f): # |sum_{x in S, x>=lo} e^{2 pi i f x}|^2 (the centred term is negligible at f far from 0)
    z=np.exp(2j*np.pi*f*ew); return abs(z.sum())**2
def exact(k): # golden-section maximisation on [(k-1)/L,(k+1)/L]
    a,c=(k-1)/L,(k+1)/L; r=(5**0.5-1)/2; b1=c-r*(c-a); b2=a+r*(c-a); f1,f2=dtft2(b1),dtft2(b2)
    for _ in range(40):
        if f1<f2: a,b1,f1=b1,b2,f2; b2=a+r*(c-a); f2=dtft2(b2)
        else: c,b2,f2=b2,b1,f1; b1=c-r*(c-a); f1=dtft2(b1)
    return (a+c)/2
order=np.argsort(-P); peaks=[]
for k in order[:5000]:
    if all(abs(k-j)>8 for j,_ in peaks): peaks.append((int(k),float(P[k])))
    if len(peaks)>=40: break
fs=[exact(k) for k,_ in peaks]
print(f"file={fn} window=[{lo},{N}] L={L} bin width={bw:.2e}  (peaks: 40 largest local maxima, sidelobes within 8 bins excluded, located exactly)")
for (k,p),f in zip(peaks[:40],fs): print(f"  f={f:.11f}  1/f={1/f:.4f}  {p/tot*100:6.2f}%")
mask=np.zeros(len(P),bool)
for k,_ in peaks: mask[max(0,k-3):k+4]=True
print(f"variance in the 40 peaks (±3 bins): {P[mask].sum()/tot*100:.2f}%  (random set of this density: ~{40*7/len(P)*100:.4f}%)")
def frac(v): return abs((v+0.5)%1-0.5)
# --- Z-rank (v3): add generators greedily (a candidate is new if it is not a |c|<=RELMAX integer combination of the current ones),
# then search for integer RELATIONS sum c_i g_i = 0 (mod 1) among the generators, |c_i| <= RELMAX, and reduce (referee item A1).
gens=[]
def combo_dist(f,gens):
    grids=np.meshgrid(*[np.arange(-RELMAX,RELMAX+1)]*len(gens),indexing='ij'); coefs=np.stack([g_.ravel() for g_ in grids],1)
    coefs=coefs[np.any(coefs!=0,axis=1)]; v=coefs@np.array(gens); d=frac(v-f); i=int(d.argmin()); return float(d[i]),tuple(int(c) for c in coefs[i])
for f in fs:
    if len(gens)>=3: break
    if not gens: gens.append(f); continue
    d,coef=combo_dist(f,gens)
    if d<=2*bw: print(f"  peak f={f:.11f} is on the module of the earlier generators: {coef}·gens, residual {d/bw:.3f} bin — NOT a new generator")
    else: gens.append(f); print(f"  candidate generator f={f:.11f} (nearest combination with |c|<={RELMAX}: {coef}, {d/bw:.1f} bins away)")
# relations among the candidate generators
def relations(gens):
    grids=np.meshgrid(*[np.arange(-RELMAX,RELMAX+1)]*len(gens),indexing='ij'); coefs=np.stack([g_.ravel() for g_ in grids],1)
    coefs=coefs[np.any(coefs!=0,axis=1)]; v=coefs@np.array(gens); d=frac(v); order=np.argsort(d+1e-9*np.abs(coefs).sum(1)); out=[]
    for i in order[:5]:
        out.append((float(d[i]/bw),tuple(int(c) for c in coefs[i])))
    return out
rels=relations(gens); print(f"  smallest integer relations among the candidates (bins, coefficients): {[(round(r,3),c) for r,c in rels[:3]]}")
good=[(r,c) for r,c in rels if r<=0.1]
if len(gens)==2 and good:
    c1,c2=good[0][1]; from math import gcd
    if gcd(abs(c1),abs(c2))==1:
        # find u,v with c1*v - c2*u = 1  ->  g = u*g1 + v*g2 generates: g1 = -c2 g, g2 = c1 g (mod 1)
        u=v=None
        for uu in range(-200,201):
            for vv in range(-200,201):
                if c1*vv-c2*uu==1: u,v=uu,vv; break
            if u is not None: break
        g=frac(u*gens[0]+v*gens[1]) if True else None
        gg=(u*gens[0]+v*gens[1])%1.0
        print(f"  RELATION {c1}·g1 + {c2}·g2 ≡ 0 (mod 1) to {good[0][0]:.3f} bin  ⇒  the module is CYCLIC: g = {u}·g1 + {v}·g2 = {gg:.11f}, g1 ≡ {-c2}g, g2 ≡ {c1}g")
        gens=[gg]
elif len(gens)==3 and good:
    print(f"  RELATION {good[0][1]}·gens ≡ 0 (mod 1) to {good[0][0]:.3f} bin ⇒ rank ≤ 2; testing which pair of candidates spans all three:")
    best=None
    for i,j in ((0,1),(0,2),(1,2)):
        k=3-i-j; d,coef=combo_dist(gens[k],[gens[i],gens[j]])
        print(f"    pair ({i},{j}) reaches candidate {k} as {coef} with residual {d/bw:.3f} bin")
        if d<=2*bw and best is None: best=(i,j)
    if best: gens=[gens[best[0]],gens[best[1]]]
print(f"Z-rank (relations scanned to |c|<={RELMAX}): {len(gens)}; generators {[round(g_,11) for g_ in gens]}")
if len(gens)==1:
    g=gens[0]; cf=[]; v=g
    for _ in range(16): a=int(1/v); cf.append(a); v=1/v-a
    print(f"  continued fraction of g: {cf}"); p0,q0,p1,q1=0,1,1,0; dens=[]
    for a in cf: p0,p1=p1,a*p1+p0; q0,q1=q1,a*q1+q0; dens.append(q1)
    print(f"  convergent denominators: {dens}")
# --- membership of the 40 peaks in the module of the generators, |coef|<=C, both tolerances ---
def dist_to_module(f):
    best=(1.0,None)
    for coef in itertools.product(range(-C,C+1),repeat=len(gens)):
        if not any(coef): continue
        d=frac(sum(c*g for c,g in zip(coef,gens))-f)
        if d<best[0]: best=(d,coef)
    return best
on1=on2=0; off=[]
for f in fs:
    d,coef=dist_to_module(f)
    if d<=bw: on1+=1
    if d<=2*bw: on2+=1
    else: off.append((round(f,8),round(d/bw,2),coef))
print(f"peaks on the rank-{len(gens)} module with |coef|<={C}: {on1}/40 within 1 bin, {on2}/40 within 2 bins (chance per peak for one random frequency, 2 bins: {(2*C+1)**len(gens)*4*bw:.1e})")
if off: print("  off-module peaks (f, bins away, nearest coefficients):",off[:10])
pts=set()
for coef in itertools.product(range(-C,C+1),repeat=len(gens)):
    if not any(coef): continue
    v=frac(sum(c*g for c,g in zip(coef,gens))); pts.add(int(round(v*L)))
m2=np.zeros(len(P),bool)
for kk in pts:
    if 0<kk<len(P): m2[max(0,kk-1):kk+2]=True
print(f"variance within ±1 bin of the {len(pts)} distinct module points with |coef|<={C}: {P[m2].sum()/tot*100:.2f}%  (random: ~{m2.sum()/len(P)*100:.3f}%); off the module: {100-P[m2].sum()/tot*100:.1f}%")
print("NOTE: a finite window cannot distinguish an irrational generator from a rational p/q with q beyond ~1/bin; and any statistic here is also the statistic of a periodic set of period >= the window.")
