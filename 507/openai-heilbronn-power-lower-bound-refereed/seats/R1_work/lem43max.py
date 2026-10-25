# exhaustive over ALL residue prescriptions (k=1): max P(b>=1) vs (r/L)^4
import numpy as np, itertools
def run(B,r,L):
    best=0; bestp=None
    # all configs index -> digit tuple for each residue pattern
    for presc in itertools.product(range(r),repeat=9):
        ch=[np.array([a for a in range(1,L+1) if a%r==presc[e]]) for e in range(9)]
        g=np.meshgrid(*ch,indexing='ij'); a=[x.ravel()%B for x in g]
        a11,a12,a13,a21,a22,a23,a31,a32,a33=a
        mins=[a11*a22-a12*a21,a11*a23-a13*a21,a12*a23-a13*a22,a11*a32-a12*a31,a11*a33-a13*a31,a12*a33-a13*a32,a21*a32-a22*a31,a21*a33-a23*a31,a22*a33-a23*a32]
        ok=np.ones(len(a11),bool)
        for m in mins: ok&=(m%B==0)
        p=ok.mean()
        if p>best: best=p; bestp=presc
    return best,bestp
for (B,r,L) in [(5,2,4),(7,2,6),(7,3,6),(11,2,4),(11,2,10),(13,3,12)]:
    if (L//r)**9*r**9>3e8: continue
    best,bp=run(B,r,L)
    print(f"B={B} r={r} L={L}: max over all prescriptions P(b>=1)={best:.4e}  bound (r/L)^4={(r/L)**4:.4e} ok={best<=(r/L)**4+1e-15} worst presc={bp}",flush=True)
