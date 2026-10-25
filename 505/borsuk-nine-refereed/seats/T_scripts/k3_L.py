# (4.9) check on the k=3 control map: |f^{-1}(r~)| is odd for facets I and generic r.
import numpy as np, itertools
from scipy.optimize import fsolve
exec(open('/tmp/oaimath/156/seats/T_scripts/k3_common.py').read())
rng=np.random.default_rng(11)
for T in tris:
    I=list(T)
    # center of U_I: normalised sum of the three axes with signs chosen so all pairwise dots positive
    best=None
    for sg in itertools.product([1,-1],repeat=2):
        c=axes[I[0]]+sg[0]*axes[I[1]]+sg[1]*axes[I[2]]; c/=np.linalg.norm(c)
        fc=f(c[None])[0]
        if all(fc[i]>0 for i in I): best=c
    assert best is not None
    e1=np.cross(best,[0.3,0.5,0.7]); e1/=np.linalg.norm(e1); e2=np.cross(best,e1)
    def X(p): x=best+p[0]*e1+p[1]*e2; return x/np.linalg.norm(x)
    for _ in range(2):
        r=rng.dirichlet([2,2,2])
        sols=[]
        for t in range(3000):
            p0=rng.uniform(-0.12,0.12,size=2)
            if not all(f(X(p0)[None])[0][i]>0 for i in I): continue
            F2=lambda p: (lambda v:[v[I[0]]-r[0],v[I[1]]-r[1]])(f(X(p)[None])[0])
            p,info,ier,msg=fsolve(F2,p0,full_output=True,xtol=1e-13)
            v=f(X(p)[None])[0]
            if ier!=1 or np.max(np.abs(v[I]-r))>1e-9: continue
            if not any(np.linalg.norm(p-q)<1e-6 for q in sols): sols.append(p)
        # region U_I lies in the chart around 'best' (checked: U_I within ~0.12 rad), so this counts all of L
        print("facet",T,"r",np.round(r,3),"|L| =",len(sols))
