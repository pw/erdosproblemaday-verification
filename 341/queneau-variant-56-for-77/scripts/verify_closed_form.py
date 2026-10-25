#!/usr/bin/env python3
"""Closed-form verification for the seed A = {1,2,3,5,7,13,22,27,28,32,36,40,47,48,52,56,63,71,81,89,97} (Li's seed with
77 → 56) under BOTH rules.  Everything here is computed from the CLOSED FORMS below, by FFT sumsets — independent of
gates.py / census.c (sequential dynamics) and of greedy341.c (the real greedy on the integers).

Strict (Queneau, i<j) controller:  Y0 = {0,1} ∪ ⋃_{k≥0}[8^k+1, 2·8^k]   Y1 = {1} ∪ ⋃_{k≥0}[4·8^k, 8·8^k]   Y2 = {0} ∪ ⋃_{k≥0}[2·8^k, 4·8^k]
Equal  (Dickson, i≤j) controller:  Y0 = {0,1} ∪ ⋃_{k≥0}[2·8^k, 4·8^k−1]  Y1 = {1} ∪ ⋃_{k≥1}[8^k−1, 2·8^k−1]   Y2 = {0} ∪ ⋃_{k≥0}[4·8^k−1, 8·8^k−1]
Gates (for q ≥ 2):  Y1 = cpl(Y0 ⊕ Y0),  Y2 = cpl(Y1 ⊕ Y1),  Y0 = 1 + cpl(Y2 ⊕ Y2)   (⊕ = sumset, distinct summands if strict)
Controls: each identity must FAIL under the other rule (same sets), and must FAIL when a block endpoint is shifted by one.
Also: Li's shield mod 49 recomputed from scratch incl. the strict-rule distinctness of every cover pair; S∩[1,97] = A."""
import numpy as np, sys
P=[7,14,28]; B=[3,22,32,40,48]; D=[1,2,5,13,27,36,47]; Qset=set(P)|set(B)
A=[1,2,3,5,7,13,22,27,28,32,36,40,47,48,52,56,63,71,81,89,97]
def blocks(Q, lo, hi, k0=0):   # ⋃_{k≥k0} [lo(k), hi(k)] on [0,Q)
    Y=np.zeros(Q,bool); k=k0
    while lo(k)<Q: Y[lo(k):min(hi(k)+1,Q)]=True; k+=1
    return Y
def closed(rule,Q):
    if rule=='strict':
        Y0=blocks(Q,lambda k:8**k+1,lambda k:2*8**k); Y0[[0,1]]=True
        Y1=blocks(Q,lambda k:4*8**k,lambda k:8*8**k); Y1[1]=True
        Y2=blocks(Q,lambda k:2*8**k,lambda k:4*8**k); Y2[0]=True
    else:
        Y0=blocks(Q,lambda k:2*8**k,lambda k:4*8**k-1); Y0[[0,1]]=True
        Y1=blocks(Q,lambda k:8**k-1,lambda k:2*8**k-1,1); Y1[1]=True
        Y2=blocks(Q,lambda k:4*8**k-1,lambda k:8*8**k-1); Y2[0]=True
    return [Y0,Y1,Y2]
def sumset(Y,strict):
    """indicator of {u+v : u,v ∈ Y (u≠v if strict)} on [0,len(Y))  via FFT pair counts."""
    n=len(Y); f=np.fft.rfft(Y.astype(float),2*n); c=np.rint(np.fft.irfft(f*f,2*n)[:n])
    if strict:
        ev=np.arange(0,n,2); c[ev]-=Y[ev//2]          # remove the double u+u
    return c>0.5
def gates_ok(Y,strict,Q,q_from=2):
    Y0,Y1,Y2=Y; S0,S1,S2=sumset(Y0,strict),sumset(Y1,strict),sumset(Y2,strict)
    g1=(Y1==~S0)[q_from:]; g2=(Y2==~S1)[q_from:]
    g3=(Y0[q_from:]==~S2[q_from-1:Q-1])
    return [int((~g).sum()) for g in (g1,g2,g3)]
def shield():
    import itertools
    Z=range(49); BB={(x+y)%49 for x in B for y in B}; PB={(x+y)%49 for x in P for y in B}; DB={(x+y)%49 for x in D for y in B}; DP={(x+y)%49 for x in D for y in P}
    cover = (BB|PB|DB)==set(Z)-Qset
    avoid = not (Qset & (BB|PB|DB|DP))
    PP={(x+y)%49 for x in P for y in P}; pp = (PP&Qset)==set(P)
    diag = sorted((x,y) for x in P for y in P if (x+y)%49 in Qset)==[(7,7),(14,14),(28,28)]
    return cover,avoid,pp,diag
def S_from(Y,N):
    S=np.zeros(N+1,bool); S[D]=True
    for b in B: S[b::49]=True
    for i in range(3):
        q=np.flatnonzero(Y[i]); e=49*q+P[i]; S[e[e<=N]]=True
    return S
if __name__=='__main__':
    Q=8**7; ok=True
    for rule in ('strict','equal'):
        st=(rule=='strict'); Y=closed(rule,Q)
        v=gates_ok(Y,st,Q); other=gates_ok(Y,not st,Q)
        print(f"[{rule}] closed form on [0,{Q}): gate violations (q≥2) = {v}  -> {'PASS' if v==[0,0,0] else 'FAIL'};  same sets under the OTHER rule: {other} (control, must be nonzero)")
        ok&=(v==[0,0,0] and all(x>0 for x in other))
        # mutation controls: shift one endpoint of one block family by ±1
        for i in range(3):
            Ym=[y.copy() for y in Y]; k=3; 
            lo=[lambda k:8**k+1,lambda k:4*8**k,lambda k:2*8**k][i](k) if st else [lambda k:2*8**k,lambda k:8**k-1,lambda k:4*8**k-1][i](k)
            Ym[i][lo-1]=True   # extend block k=3 of rail i one step down
            m=gates_ok(Ym,st,Q); print(f"   mutation (rail {i} block 3 start −1): violations {m} (must be nonzero)"); ok&=any(x>0 for x in m)
        # dynamics cross-check (gates.py, sequential, strict/equal): closed form must equal the run from the IC
        import gates
        Qd=2**17; Yd=gates.run(3,st,[[True,True],[False,True],[True,False]],Qd)
        mism=[int((Yd[i]!=Y[i][:Qd]).sum()) for i in range(3)]
        print(f"   closed form vs sequential dynamics (gates.py) on [0,{Qd}): mismatches {mism} -> {'PASS' if mism==[0,0,0] else 'FAIL'}"); ok&=(mism==[0,0,0])
        # seed prefix
        S=S_from(Y,97); pre=np.flatnonzero(S).tolist()
        print(f"   S ∩ [1,97] = {pre}  == A: {pre==A}"); ok&=(pre==A)
        # runs of both symbols on the 7-rail grow without bound (aperiodicity witness): print block lengths
        Y0=Y[0]; r=[]; q=0
        while q<min(Q,10**6):
            if Y0[q]:
                s=q
                while q<Q and Y0[q]: q+=1
                r.append((s,q-1))
            else: q+=1
        print(f"   Y0 runs of 1s (first 8): {r[:8]}")
    c=shield(); print(f"[shield mod 49] cover={c[0]} avoid={c[1]} (P+P)∩Q=P:{c[2]} diagonal-only:{c[3]}"); ok&=all(c)
    # strict-rule cover pairs are DISTINCT elements: e_x + (49(q-u_x-c)+b) with e_x ∈ {x (x∈B∪D), 7, 63, 28}
    e={x:x for x in B+D}; e[7]=7; e[14]=63; e[28]=28; bad=0; checked=0
    for r in range(49):
        if r in Qset: continue
        for q in range(2,60):
            t=49*q+r; reps=[]
            for x,ex in e.items():
                for b in B:
                    if (x+b)%49==r:
                        y=t-ex
                        if y>0 and y%49==b and y!=ex: reps.append((ex,y))
            checked+=1
            if not reps: bad+=1
    print(f"[strict cover] every t=49q+r (r∉Q, 2≤q<60) has a cover pair of two DISTINCT positive elements of S: {'PASS' if bad==0 else 'FAIL'} ({checked} checked, {bad} without)"); ok&=(bad==0)
    print("ALL PASS" if ok else "SOMETHING FAILED"); sys.exit(0 if ok else 1)
