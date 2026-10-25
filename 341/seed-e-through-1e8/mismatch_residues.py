#!/usr/bin/env python3
"""For a shift q: the set {n : b(n) != b(n+q)} on [N/5, N-q] — its density and how it is spread over residues mod q (referee item 9).
usage: mismatch_residues.py elems.u32 q [q ...]"""
import sys, numpy as np
el=np.fromfile(sys.argv[1],dtype='<u4').astype(np.int64); N=int(el[-1]); b=np.zeros(N+1,bool); b[el]=True; lo=N//5
for q in map(int,sys.argv[2:]):
    n=np.arange(lo,N-q); mm=n[b[lo:N-q]!=b[lo+q:N]]; c=np.bincount(mm%q,minlength=q)
    print(f"shift {q}: mismatches {len(mm)} = density {len(mm)/(N-q-lo):.4f}; residues mod {q} hit {int((c>0).sum())}/{q}; per-residue counts min {c.min()} mean {c.mean():.1f} max {c.max()} (Poisson sd {c.mean()**0.5:.1f})")
