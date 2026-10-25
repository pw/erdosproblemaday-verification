# Positive control for Thm 4.3 (k=3) / Lemma 5.2: an explicit admissible map RP^2 -> Delta^5
# (smooth bumps on caps of angular radius rho around the 6 icosahedral axes, rho in (37.38deg, 45deg)).
import numpy as np, itertools
from scipy.optimize import fsolve
rng=np.random.default_rng(7)
phi=(1+5**0.5)/2
axes=np.array([[0,1,phi],[0,1,-phi],[1,phi,0],[1,-phi,0],[phi,0,1],[-phi,0,1]],float)
axes/=np.linalg.norm(axes,axis=1,keepdims=True)
G=np.abs(axes@axes.T); print("pairwise |cos| between axes:",np.unique(np.round(G[np.triu_indices(6,1)],6)))
rho=np.deg2rad(40.0); s0=np.sin(rho)**2
def bumps(X):            # X (N,3) unit -> (N,6) unnormalised smooth bumps in s=1-<x,a>^2
    s=1-(X@axes.T)**2
    out=np.zeros_like(s); ins=s<s0
    out[ins]=np.exp(-1.0/(s0-s[ins])); return out
def f(X):
    b=bumps(X); tot=b.sum(1,keepdims=True); assert (tot>0).all(), "caps do not cover"
    return b/tot
# admissibility: two lines in the same cap have angle <= 2*rho < 90deg -> never orthogonal
print("2*rho deg =",np.rad2deg(2*rho)," (<90 => admissible)")
# support complex by dense sampling
N=3_000_000; X=rng.normal(size=(N,3)); X/=np.linalg.norm(X,axis=1,keepdims=True)
S=bumps(X)>0
faces=set(tuple(np.nonzero(r)[0]) for r in np.unique(S,axis=0))
maxfaces=[F for F in faces if not any(set(F)<set(G2) for G2 in faces)]
print("max face sizes:",sorted(set(len(F) for F in maxfaces)),"#facets",len(maxfaces))
edges=set(e for F in faces for e in itertools.combinations(F,2))
print("#edges",len(edges),"(15 expected)")
tri=[F for F in maxfaces if len(F)==3]
cnt={e:sum(1 for t in tri if set(e)<=set(t)) for e in itertools.combinations(range(6),2)}
print("edge multiplicities:",sorted(set(cnt.values())))
comp_ok=all((tuple(sorted(set(range(6))-set(T))) in tri)!=(T in tri) for T in itertools.combinations(range(6),3))
print("exactly one of each complementary pair is a triangle:",comp_ok)
# (4.9): |f^{-1}(r~)| odd for a facet I and a generic r in the open simplex
def count_L(I,r,trials=4000):
    sols=[]
    J=[j for j in range(6) if j not in I]
    for _ in range(trials):
        x0=rng.normal(size=3); x0/=np.linalg.norm(x0)
        fx=f(x0[None])[0]
        if not all(fx[i]>0 for i in I): continue
        def eq(p):
            x=np.array([p[0],p[1],1.0]) if abs(x0[2])>0.3 else None
            return None
        # param: x = (cos a sin b, sin a sin b, cos b)
        def F2(p):
            a,b=p; x=np.array([np.cos(a)*np.sin(b),np.sin(a)*np.sin(b),np.cos(b)])
            v=f(x[None])[0]; return [v[I[0]]-r[0],v[I[1]]-r[1]]
        b0=np.arccos(np.clip(x0[2],-1,1)); a0=np.arctan2(x0[1],x0[0])
        p,info,ier,msg=fsolve(F2,[a0,b0],full_output=True)
        if ier!=1 or np.max(np.abs(info['fvec']))>1e-10: continue
        a,b=p; x=np.array([np.cos(a)*np.sin(b),np.sin(a)*np.sin(b),np.cos(b)])
        v=f(x[None])[0]
        if np.max(np.abs(v[J]))>0 or np.max(np.abs(v[list(I)]-r))>1e-9: continue
        if x[np.argmax(np.abs(x))]<0: x=-x
        if not any(np.linalg.norm(x-y)<1e-6 for y in sols): sols.append(x)
    return sols
for T in tri[:4]:
    for _ in range(2):
        r=rng.dirichlet([3,3,3])
        sols=count_L(list(T),r)
        print("facet",T,"r",np.round(r,3),"|L| =",len(sols))
