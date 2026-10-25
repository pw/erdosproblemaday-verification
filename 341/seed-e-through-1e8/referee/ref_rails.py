#!/usr/bin/env python3
"""Referee check of census2.c's model: (1) independent set-based rail dynamics; (2) the REAL greedy (fast341) from a
Lemma-5 seed D u B u (M+B) u R must have exactly that rail content and the shield residues; (3) census2's own verdict."""
import subprocess, numpy as np, itertools, os
def rails(M,x,L,ic,Q):  # ic: dict residue -> set of q<=q0 ; returns dict residue -> sorted list of q<Q
    res=sorted({(x<<i)%M for i in range(L)}); pred={j:[i for i in res if (2*i)%M==j][0] for j in res}
    carry={i:int(2*i>=M) for i in res}; q0=max(max(v) for v in ic.values() if v) if any(ic.values()) else 0
    q0=max(q for v in ic.values() for q in v) if any(ic.values()) else 0
    Y={r:set(ic[r]) for r in res}; q0=max(1,q0)
    for q in range(q0+1,Q):
        for j in res:
            i=pred[j]; qq=q-carry[i]
            # qq in Y_i+Y_i ?  (Y_i already contains q if i<j and carry 0)
            rep=any((qq-u) in Y[i] for u in Y[i] if u<=qq)
            if not rep: Y[j].add(q)
    return {r:sorted(v) for r,v in Y.items()}
def greedy_rails(M,B,D,R,res,Q):
    seed=sorted(set(D)|set(B)|{M+b for b in B}|set(R)); N=M*Q
    subprocess.run(['../fast341',str(N),'/tmp/refrails','0']+[str(s) for s in seed],capture_output=True,check=True)
    el=np.fromfile('/tmp/refrails_elems.u32',dtype='<u4').astype(np.int64); os.remove('/tmp/refrails_elems.u32')
    tail=el[el>2*M-1]; out={r:sorted(int(v)//M for v in el if v%M==r) for r in res}
    bad=[int(v) for v in tail if v%M not in set(res)|set(B)]
    Bfull=all(((q*M+b) in set(el.tolist())) for b in B for q in range(2,Q))
    return seed,out,bad,Bfull
for (M,x,L,B,D,R) in [(6,2,2,[3],[],[2,4,10]),(6,2,2,[3],[],[2,8,4]),(6,2,2,[3],[],[2,8,4,10]),
                      (49,7,3,[3,22,32,40,48],[1,2,5,13,27,36,47],[7,28,63,77]),(49,7,3,[3,22,32,40,48],[1,2,5,13,27,36,47],[7,56,14,28])]:
    Q=1500
    res=sorted({(x<<i)%M for i in range(L)})
    ic={r:{v//M for v in R if v%M==r} for r in res}
    sim=rails(M,x,L,ic,Q)
    seed,gr,bad,Bfull=greedy_rails(M,B,D,R,res,Q)
    same=all(sim[r]==[q for q in gr[r] if q<Q] for r in res)
    # periodicity of the simulated rail word on [Q/2,Q)
    W=[tuple(int(q in set(sim[r])) for r in res) for q in range(Q)]
    per=next((p for p in range(1,Q//4) if all(W[q]==W[q+p] for q in range(Q//2,Q-p))),None)
    print(f"M={M} rails {res} seed={seed}: greedy rail content == simulated dynamics: {same}; non-shield residues after 2M-1: {len(bad)}; B rails full: {Bfull}; simulated suffix period on [Q/2,Q): {per}")
