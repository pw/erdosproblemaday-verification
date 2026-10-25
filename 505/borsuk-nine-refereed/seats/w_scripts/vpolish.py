# Voronoi-vertex minimax polish for K lines in RP^3: holes are points equidistant (in |<p,c>|) from 4 lines.
# Minimise t s.t. every near-active vertex has angle <= t, via SLSQP with fixed vertex combinatorics; iterate.
import numpy as np, sys
from scipy.optimize import minimize
K=int(sys.argv[1]); files=sys.argv[2].split(',')
rng=np.random.default_rng(7)
def sphere(n):
    X=rng.normal(size=(n,4)); return X/np.linalg.norm(X,axis=1,keepdims=True)
S=sphere(200000)
def refine_hole(C,p,steps=400):
    lr=0.02
    for _ in range(steps):
        s=C@p; j=np.argmax(np.abs(s)); g=-np.sign(s[j])*C[j]
        q=p+lr*(g-(g@p)*p); q/=np.linalg.norm(q)
        if np.abs(C@q).max()<np.abs(C@p).max(): p=q
        else: lr*=0.7
        if lr<1e-10: break
    return p
def vertex(C,Q,sg):
    M=(sg[:,None]*C[list(Q)]); y=np.linalg.solve(M,np.ones(4)); return 1/np.linalg.norm(y), y/np.linalg.norm(y)
def find_vertices(C,n=400,tol_deg=2.0):
    c=np.abs(S@C.T).max(axis=1); idx=np.argsort(c)[:n]
    V={}
    for i in idx:
        p=refine_hole(C,S[i].copy()); a=np.abs(C@p); Q=tuple(sorted(np.argsort(-a)[:4]))
        sg=np.sign(C[list(Q)]@p)
        try: s,v=vertex(C,Q,sg)
        except np.linalg.LinAlgError: continue
        if np.sign(sg[0])<0: sg=-sg
        key=(Q,tuple(sg))
        # validity: no other line closer than s at v
        if np.abs(C@v).max()<=s+1e-9: V[key]=s
    if not V: return [],0
    smin=min(V.values()); tmax=np.degrees(np.arccos(smin))
    act=[k for k,s in V.items() if np.degrees(np.arccos(s))>=tmax-tol_deg]
    return act,tmax
def covrad(C):
    c=np.abs(S@C.T).max(axis=1); idx=np.argsort(c)[:300]
    return max(np.degrees(np.arccos(np.abs(C@refine_hole(C,S[i].copy())).max())) for i in idx)
for f in files:
    C=np.load(f); best=covrad(C)
    print(f"{f}: start covering radius {best:.4f}",flush=True)
    for outer in range(8):
        act,tmax=find_vertices(C)
        if not act: break
        x0=np.r_[C.ravel(),np.cos(np.radians(tmax))]
        def obj(x): return -x[-1]
        cons=[]
        for (Q,sg) in act:
            Q=list(Q); sg=np.array(sg,float)
            def g(x,Q=Q,sg=sg):
                Cx=x[:-1].reshape(K,4); M=sg[:,None]*Cx[Q]
                try: y=np.linalg.solve(M,np.ones(4))
                except np.linalg.LinAlgError: return -1.0
                return 1/np.linalg.norm(y)-x[-1]
            cons.append({'type':'ineq','fun':g})
        for i in range(K):
            cons.append({'type':'eq','fun':lambda x,i=i: np.sum(x[4*i:4*i+4]**2)-1})
        bnds=[(v-0.03,v+0.03) for v in x0[:-1]]+[(0,1)]
        r=minimize(obj,x0,method='SLSQP',constraints=cons,bounds=bnds,options={'maxiter':200,'ftol':1e-12})
        Cn=r.x[:-1].reshape(K,4); Cn/=np.linalg.norm(Cn,axis=1,keepdims=True)
        cr=covrad(Cn)
        if cr<best-1e-6: C=Cn; best=cr
        print(f"  outer {outer}: active {len(act)} tmax {tmax:.4f} -> covering radius {cr:.4f} (best {best:.4f})",flush=True)
        if cr>=best-1e-6 and outer>5 and abs(cr-best)<1e-4: pass
    np.save(f.replace('.npy','_vp.npy'),C)
    print(f"VPOLISHED {f}: {best:.5f} deg",flush=True)
