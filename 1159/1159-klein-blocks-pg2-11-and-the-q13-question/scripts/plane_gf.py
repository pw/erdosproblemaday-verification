#!/usr/bin/env python3
"""PG(2,q) for prime powers via the galois library; elements encoded as ints 0..q-1 (galois' integer repr)."""
import galois, itertools
def plane_gf(q):
    GF=galois.GF(q)
    els=[int(x) for x in GF.elements]
    pts=[(1,a,b) for a in els for b in els]+[(0,1,a) for a in els]+[(0,0,1)]
    P=GF(pts)  # shape (v,3)
    # incidence: dot product zero
    M=(P @ P.T)  # v x v, lines indexed like points
    inc=(M==0)
    lines=[[j for j in range(len(pts)) if inc[i,j]] for i in range(len(pts))]
    v=q*q+q+1
    assert len(pts)==v and all(len(l)==q+1 for l in lines)
    import numpy as np
    A=np.array(inc,dtype=int); assert (A.sum(axis=0)==q+1).all()
    # every two points on exactly one line: A^T A has 1 off-diagonal
    AtA=A.T@A; assert ((AtA-np.diag(np.diag(AtA)))==1).sum()==v*(v-1)
    return pts,lines
if __name__=='__main__':
    import sys; q=int(sys.argv[1]); pts,lines=plane_gf(q); print(q,len(pts),len(lines),"axioms ok")
