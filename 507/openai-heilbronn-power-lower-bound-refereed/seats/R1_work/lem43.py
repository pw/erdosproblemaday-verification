# Exact check of Lemma 4.3 tail bound P(b>=j) <= (r/L)^{4j} and E[D] <= 1/(1-theta)
import numpy as np, itertools, random
def entry_values(res, B, k, r, L):
    # res: list of k residues mod r (position u -> residue); returns all values sum d_u B^u, d_u in [1,L], d_u = res[u] mod r
    choices=[[a for a in range(1,L+1) if a%r==res[u]%r] for u in range(k)]
    vals=[]
    for ds in itertools.product(*choices):
        vals.append(sum(d*B**u for u,d in enumerate(ds)))
    return np.array(vals,dtype=np.int64)
def run(B,k,r,L,presc):
    h=B**k
    # presc[i][j] = list of k residues for entry (i,j)
    V=[[entry_values(presc[i][j],B,k,r,L) for j in range(3)] for i in range(3)]
    n=len(V[0][0])
    # enumerate via meshgrid in chunks over the first column (3 entries)
    tot=0; cnt=np.zeros(k+1,dtype=np.float64)  # cnt[j] = #configs with b>=j
    ED=0.0
    for a11 in V[0][0]:
      for a21 in V[1][0]:
        for a31 in V[2][0]:
            g=np.meshgrid(V[0][1],V[0][2],V[1][1],V[1][2],V[2][1],V[2][2],indexing='ij')
            a12,a13,a22,a23,a32,a33=[x.ravel() for x in g]
            mins=[a11*a22-a21*a12, a11*a23-a21*a13, a12*a23-a22*a13,
                  a11*a32-a31*a12, a11*a33-a31*a13, a12*a33-a32*a13,
                  a21*a32-a31*a22, a21*a33-a31*a23, a22*a33-a32*a23]
            # b = min valuation of minors mod h, capped at k
            bval=np.full(a12.shape,k,dtype=np.int64)
            for m in mins:
                m=m%h
                v=np.zeros(m.shape,dtype=np.int64); mm=m.copy()
                zero=(mm==0)
                v[zero]=k
                nz=~zero
                vv=np.zeros(nz.sum(),dtype=np.int64); x=mm[nz]
                for _ in range(k):
                    d=(x%B==0); vv+=d; x=np.where(d,x//B,x)
                v[nz]=vv
                bval=np.minimum(bval,v)
            tot+=len(bval)
            for j in range(k+1): cnt[j]+=(bval>=j).sum()
            ED+=(float(B)**bval).sum()
    P=cnt/tot
    theta=B*(r/L)**4
    ok=all(P[j]<= (r/L)**(4*j)+1e-15 for j in range(1,k+1))
    return P, ED/tot, theta, ok
random.seed(1)
for (B,k,r,L,NT) in [(5,2,2,4,12),(11,2,2,4,12),(7,1,3,6,12),(13,1,2,6,12),(7,2,2,6,2),(5,3,2,4,2)]:
    worst=None
    trials=[]
    # structured: all three columns same residues (repeated label), zero residues, random
    for t in range(NT):
        if t==0: base=[[[0]*k for j in range(3)] for i in range(3)]
        elif t==1:
            col=[[random.randrange(r) for u in range(k)] for i in range(3)]
            base=[[col[i] for j in range(3)] for i in range(3)]
        else:
            base=[[[random.randrange(r) for u in range(k)] for j in range(3)] for i in range(3)]
        P,ED,theta,ok=run(B,k,r,L,base)
        trials.append((P,ED,ok))
        bound=[(r/L)**(4*j) for j in range(1,k+1)]
        print(f"B={B} k={k} r={r} L={L} presc#{t}: P(b>=j)={[f'{x:.3e}' for x in P[1:]]} bound={[f'{x:.3e}' for x in bound]} ok={ok} E[D]={ED:.4f} 1/(1-theta)={(1/(1-theta) if theta<1 else float('inf')):.4f}",flush=True)
