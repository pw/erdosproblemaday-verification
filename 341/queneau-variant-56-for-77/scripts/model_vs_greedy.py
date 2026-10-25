#!/usr/bin/env python3
"""For a rail IC (q0=1) build the seed A = D ∪ B ∪ (49+B) ∪ {rail elements}, run the REAL strict greedy on the integers
(../erdos341/greedy341, distinct=1, an independent bitset implementation of the Queneau rule) to N, and compare every
element with the rail model (gates.run, strict).  Exit 0 only on an exact match."""
import sys, subprocess, numpy as np, gates, os
P=[7,14,28]; B=[3,22,32,40,48]; D=[1,2,5,13,27,36,47]
def seed_of(ic):
    bits=[[(ic>>(i*2+q))&1==1 for q in range(2)] for i in range(3)]
    A=set(D)|set(B)|{49+b for b in B}|{49*q+P[i] for i in range(3) for q in range(2) if bits[i][q]}
    return sorted(A), bits
def model_S(bits,N):
    Q=N//49+2; Y=gates.run(3,True,bits,Q)
    S=np.zeros(N+1,bool); S[D]=True
    for b in B: S[b::49]=True
    for i in range(3):
        qs=np.flatnonzero(Y[i]); e=49*qs+P[i]; S[e[e<=N]]=True
    return S
def run_greedy(A,N,tag):
    out=subprocess.run(['nice','-n','19','../erdos341/greedy341',str(N),tag,'1']+[str(a) for a in A],capture_output=True,text=True).stdout
    el=np.fromfile(tag+'_elems.u32',dtype='<u4'); return el,out
if __name__=='__main__':
    ic=int(sys.argv[1]); N=int(sys.argv[2]) if len(sys.argv)>2 else 10**6
    A,bits=seed_of(ic); tag=f'ic{ic}_strict'
    el,out=run_greedy(A,N,tag)
    S=model_S(bits,N); G=np.zeros(N+1,bool); G[el]=True
    mism=np.flatnonzero(S!=G)
    print(f"ic={ic} seed({len(A)})={A}")
    print(out.splitlines()[0]); print(out.splitlines()[-1])
    print(f"model vs greedy on [1,{N}]: {len(mism)} mismatches; first: {mism[:10].tolist()}  (greedy count {G.sum()}, model count {S.sum()})")
    sys.exit(0 if len(mism)==0 else 1)
