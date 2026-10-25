#!/usr/bin/env python3
"""Referee's from-scratch greedy (sets, no bitsets), straight from the problem statement:
a_{n+1} = least integer > a_n not of the form a_i + a_j, i,j <= n (equal: i=j allowed; distinct: i != j)."""
import sys, numpy as np, subprocess, os
def greedy(seed,N,distinct):
    S=sorted(seed); sums=set()
    for i,u in enumerate(S):
        for j,v in enumerate(S):
            if distinct and i==j: continue
            sums.add(u+v)
    t=S[-1]
    while True:
        t+=1
        if t>N: break
        if t in sums: continue
        for u in S:
            if u+t<=N: sums.add(u+t)
        if not distinct and 2*t<=N: sums.add(2*t)
        S.append(t)
    return S
seeds=[[1,4,8,10,11,12],[1,2],[1,2,7,8,10,11,12],[3,5,8,10,13],[1,4,9,16,25],[2,3,5,9,13],[1],[5,6,7],[1,2,3,5,7,13,22,27,28,32,36,40,47,48,52,63,71,77,81,89,97]]
N=int(sys.argv[1]) if len(sys.argv)>1 else 6000
bad=0
for s in seeds:
    for dist in (0,1):
        py=greedy(s,N,dist)
        tag=f"/tmp/refg_{os.getpid()}"
        for prog in ("../fast341","../greedy341"):
            subprocess.run([prog,str(N),tag,str(dist)]+[str(v) for v in s],capture_output=True,check=True)
            c=np.fromfile(tag+"_elems.u32",dtype='<u4').tolist(); os.remove(tag+"_elems.u32")
            ok=(c==py); bad+= (not ok)
            print(f"{prog.split('/')[-1]:10s} seed={s if len(s)<8 else 'Li'} rule={'distinct' if dist else 'equal'} N={N}: {'MATCH' if ok else 'MISMATCH'} ({len(py)} elems)")
print("mismatches:",bad)
