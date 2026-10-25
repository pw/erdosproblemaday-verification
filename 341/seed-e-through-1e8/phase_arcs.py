#!/usr/bin/env python3
"""Arc structure of a greedy set under the rotation by g: on a SHORT window [X, X+w) (so that an error in g smears the phases by
less than one bin) histogram {x g} for x in S with B bins, extract the arcs (maximal runs of bins holding at least half the flat
density), report their total measure vs the density of S, the fraction of S inside the arcs, the fraction of non-elements inside the arcs,
and test the greedy's continuous shadow: W + W (mod 1) should be the complement of W.   usage: phase_arcs.py elems.u32 g X w [B=1000]"""
import sys, numpy as np
el=np.fromfile(sys.argv[1],dtype='<u4').astype(np.int64); g=float(sys.argv[2]); X=int(sys.argv[3]); w=int(sys.argv[4]); B=int(sys.argv[5]) if len(sys.argv)>5 else 1000
xs=el[(el>=X)&(el<X+w)]; dens=len(xs)/w; ph=(xs*g)%1.0; h=np.bincount((ph*B).astype(int),minlength=B)/len(xs)*B   # density per unit phase (1 = uniform)
flat=np.median(h[h>0.5*h.max()]) if (h>0.5*h.max()).any() else h.max()
inarc=h>=0.5*flat
# arcs as maximal circular runs
runs=[]; i=0
while i<B:
    if inarc[i] and not inarc[i-1]:
        j=i
        while inarc[(j+1)%B] and j<i+B: j+=1
        runs.append((i,j%B)); i=j+1
    else: i+=1
if inarc.all(): runs=[(0,B-1)]
arcs=[((a)/B,(b+1)/B) for a,b in runs]
meas=sum(((b-a)%1.0) or 1.0 for a,b in arcs)
print(f"window [{X},{X+w}) elements {len(xs)} density {dens:.5f}; g={g}; bins {B}; flat level {flat:.2f}; arcs ({len(arcs)}): {[(round(a,4),round(b,4)) for a,b in arcs]}; total measure {meas:.4f}")
inS=sum(h[a:b+1].sum() for a,b in runs if a<=b)/B + sum((h[a:].sum()+h[:b+1].sum()) for a,b in runs if a>b)/B
print(f"fraction of S with phase inside the arcs: {inS*100:.2f}%")
b=np.zeros(X+w,bool); b[xs]=True; non=np.arange(X,X+w)[~b[X:X+w]]; phn=(non*g)%1.0; bn=(phn*B).astype(int)
nin=sum(((bn>=a)&(bn<=b_)).sum() if a<=b_ else ((bn>=a)|(bn<=b_)).sum() for a,b_ in runs)/len(non)
print(f"fraction of NON-elements with phase inside the arcs: {nin*100:.2f}%  (if S were exactly the coding this would be 0; the arcs hold {meas*100:.1f}% of the circle)")
# edges: how wide are the transition zones? count bins with 0.1*flat < h < 0.9*flat
print(f"edge bins (between 10% and 90% of the flat level): {int(((h>0.1*flat)&(h<0.9*flat)).sum())} of {B} = {((h>0.1*flat)&(h<0.9*flat)).sum()/B*100:.2f}% of the circle")
# W + W vs complement of W, on the bin grid
Wb=inarc.astype(np.int64); ss=np.fft.irfft(np.fft.rfft(Wb,2*B)**2,2*B)[:2*B]; ss=np.rint(ss)>0; sumset=np.zeros(B,bool)
for k in range(2*B):
    if ss[k]: sumset[k%B]=True
comp=~inarc
print(f"W+W (bin grid) vs complement of W: |W+W| = {sumset.sum()/B:.4f}, |complement| = {comp.sum()/B:.4f}, symmetric difference {np.logical_xor(sumset,comp).sum()/B:.4f} of the circle; W∩(W+W) = {(inarc&sumset).sum()/B:.4f}; uncovered = {(~inarc&~sumset).sum()/B:.4f}")
