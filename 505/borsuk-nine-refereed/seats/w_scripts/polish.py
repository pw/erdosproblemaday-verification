# Minimax polish ("covering Lloyd"): holes = local maxima of distance-to-nearest-line; each centre moves
# to the minimax (smallest enclosing cap) centre of the holes it currently covers. Reports covering radius.
import numpy as np, sys
K=int(sys.argv[1]); seeds=[int(s) for s in sys.argv[2].split(',')]
rng=np.random.default_rng(1234)
def sphere(n):
    X=rng.normal(size=(n,4)); return X/np.linalg.norm(X,axis=1,keepdims=True)
S=sphere(150000)
def refine_hole(C,p,steps=300):
    lr=0.02
    for _ in range(steps):
        s=C@p; j=np.argmax(np.abs(s)); g=-np.sign(s[j])*C[j]
        q=p+lr*(g-(g@p)*p); q/=np.linalg.norm(q)
        if np.abs(C@q).max()<np.abs(C@p).max(): p=q
        else: lr*=0.7
        if lr<1e-8: break
    return p
def holes(C,n=300):
    c=np.abs(S@C.T).max(axis=1); idx=np.argsort(c)[:n]
    H=np.array([refine_hole(C,S[i].copy()) for i in idx]); return H
def cr(C,H): return np.degrees(np.arccos(np.abs(H@C.T).max(axis=1).min()))
def enclose(P):
    # minimax direction: maximise min_j <c,P_j> over unit c (P already sign-aligned)
    c=P.mean(axis=0); c/=np.linalg.norm(c); lr=0.05
    for _ in range(400):
        d=P@c; j=np.argmin(d); g=P[j]-(P[j]@c)*c
        q=c+lr*g; q/=np.linalg.norm(q)
        if (P@q).min()>d.min(): c=q
        else: lr*=0.7
        if lr<1e-9: break
    return c
for sd in seeds:
    C=np.load(f"best_K{K}_s{sd}.npy")
    for it in range(60):
        H=holes(C); A=H@C.T; a=np.argmax(np.abs(A),axis=1)
        r0=cr(C,H)
        worst=np.abs(A).max(axis=1); thr=np.sort(worst)[:min(len(worst),120)].max()
        Cn=C.copy()
        for i in range(K):
            m=(a==i)&(worst<=thr+1e-12)
            if m.sum()>=2:
                P=H[m]*np.sign(A[m,i])[:,None]
                Cn[i]=0.5*C[i]+0.5*enclose(P); Cn[i]/=np.linalg.norm(Cn[i])
        Hn=holes(Cn); r1=cr(Cn,Hn)
        if r1<r0: C=Cn
        if it%10==9: print(f"K={K} seed {sd} iter {it}: covering radius {min(r0,r1):.4f}",flush=True)
    np.save(f"polished_K{K}_s{sd}.npy",C)
    print(f"POLISHED K={K} seed {sd}: {cr(C,holes(C,600)):.4f} deg",flush=True)
