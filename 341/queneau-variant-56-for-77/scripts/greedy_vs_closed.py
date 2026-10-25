#!/usr/bin/env python3
"""Real greedy on the integers (greedy341.c, an independent bitset implementation written for the 10-13 referee) vs the
closed-form S for seed A, under a given rule.  usage: greedy_vs_closed.py strict|equal N"""
import sys, subprocess, numpy as np
from verify_closed_form import closed, S_from, A
rule=sys.argv[1]; N=int(sys.argv[2]); st=(rule=='strict'); tag=f'A_{rule}_{N}'
out=subprocess.run(['nice','-n','19','../erdos341/greedy341',str(N),tag,'1' if st else '0']+[str(a) for a in A],capture_output=True,text=True).stdout
el=np.fromfile(tag+'_elems.u32',dtype='<u4'); G=np.zeros(N+1,bool); G[el]=True
S=S_from(closed(rule,N//49+2),N); mism=np.flatnonzero(S!=G)
print(out.splitlines()[0]); print([l for l in out.splitlines() if l.startswith('suffix')][0] if any(l.startswith('suffix') for l in out.splitlines()) else '')
print(f"[{rule}] greedy341 vs closed form on [1,{N}]: {len(mism)} mismatches (first {mism[:5].tolist()}); greedy {int(G.sum())} elements, closed form {int(S.sum())}")
sys.exit(0 if len(mism)==0 else 1)
