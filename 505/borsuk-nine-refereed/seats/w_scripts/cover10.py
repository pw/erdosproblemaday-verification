# Numerical falsification probe: minimise the covering radius of K lines in R^4 (RP^3, angle metric).
# Theorem 1.1 implies: for K=10 the covering radius is >= 45 deg. If this finds K=10 < 45 deg (certified
# by a dense check), the theorem would be false. For K=11/12 it reports the best found (context only).
import numpy as np, sys, time
K=int(sys.argv[1]); restarts=int(sys.argv[2]); seed=int(sys.argv[3]) if len(sys.argv)>3 else 0
rng=np.random.default_rng(seed)
def sphere(n):
    X=rng.normal(size=(n,4)); return X/np.linalg.norm(X,axis=1,keepdims=True)
S=sphere(60000)
def covrad(C,P):
    # angle from each sample line to nearest centre line; return max (deg) and argmax point
    c=np.abs(P@C.T).max(axis=1); i=np.argmin(c); return np.degrees(np.arccos(min(1,c[i]))), P[i]
def refine_hole(C,p,steps=200):
    # local ascent on f(p)=min_i angle(p,C_i)  (maximise distance to nearest line)
    p=p/np.linalg.norm(p); lr=0.02
    for _ in range(steps):
        s=C@p; j=np.argmax(np.abs(s)); g=-np.sign(s[j])*C[j]  # decrease |<p,c_j>|
        q=p+lr*(g-(g@p)*p); q/=np.linalg.norm(q)
        if np.abs(C@q).max()<np.abs(C@p).max(): p=q
        else: lr*=0.7
        if lr<1e-7: break
    return np.degrees(np.arccos(min(1,np.abs(C@p).max()))), p
best=(99,None)
t0=time.time()
for r in range(restarts):
    C=sphere(K); T=40.0; lr=0.05
    for it in range(1500):
        P=S[rng.choice(len(S),8000,replace=False)]
        A=np.abs(P@C.T)                      # cos of angles
        # soft-max over centres (nearest), then soft-min over samples (worst covered)
        w=np.exp(T*(A-A.max(axis=1,keepdims=True))); w/=w.sum(axis=1,keepdims=True)
        m=(w*A).sum(axis=1)                  # ~ max_i |<p,c_i>|
        v=np.exp(-T*(m-m.min())); v/=v.sum() # weight worst-covered samples
        sg=np.sign(P@C.T)
        G=((v[:,None]*w*sg).T)@P             # gradient to increase coverage of worst points
        C=C+lr*G; C/=np.linalg.norm(C,axis=1,keepdims=True)
        if it%300==299: T*=1.6; lr*=0.7
    cr,p=covrad(C,S)
    # refine the deepest few holes
    c=np.abs(S@C.T).max(axis=1); idx=np.argsort(c)[:40]
    cr=max(refine_hole(C,S[i])[0] for i in idx)
    if cr<best[0]:
        best=(cr,C.copy()); np.save(f"/tmp/oaimath/156/seats/w_scripts/best_K{K}_s{seed}.npy",best[1])
    print(f"K={K} restart {r}: covering radius ~ {cr:.3f} deg (best {best[0]:.3f})",flush=True)
np.save(f"/tmp/oaimath/156/seats/w_scripts/best_K{K}_s{seed}.npy",best[1])
# final dense check of best
C=best[1]; P=sphere(400000); c=np.abs(P@C.T).max(axis=1); idx=np.argsort(c)[:200]
cr=max(refine_hole(C,P[i],400)[0] for i in idx)
print(f"FINAL K={K}: best covering radius (dense+refined) ~ {cr:.4f} deg; elapsed {time.time()-t0:.0f}s")
