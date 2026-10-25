# For x in L (k=3 control map), count |G_x^{-1}(g)| for g in the open negative orthant of Sigma_a (a=3).
# G_x(B) = -E_{x^perp}(-B), B<0 on x^perp, tr|B|=1.  Expect an odd count (Prop 4.1 / Hatcher 2B.6 in dim k-1=2).
import numpy as np
from scipy.optimize import fsolve
exec(open('/tmp/oaimath/156/seats/T_scripts/k3_common.py').read())
rng=np.random.default_rng(5)
NPHI=4000; ph=np.linspace(0,2*np.pi,NPHI,endpoint=False)
def Gx(x,J,theta,b):
    e1=np.cross(x,[0.31,0.52,0.79]); e1/=np.linalg.norm(e1); e2=np.cross(x,e1)
    e=np.cos(theta)*e1+np.sin(theta)*e2; ep=-np.sin(theta)*e1+np.cos(theta)*e2
    V=np.sqrt(b)*np.cos(ph)[:,None]*e+np.sqrt(1-b)*np.sin(ph)[:,None]*ep
    n2=np.sum(V**2,1); U=V/np.sqrt(n2)[:,None]
    fv=f(U)
    assert np.abs(fv[:,[i for i in range(6) if i not in J]]).max()==0, "x^perp uses a label of I"
    E=2*np.mean(n2[:,None]*fv,0)   # factor dim x^perp = 2
    return -E[J]
def find_L_point(I,r):
    import itertools
    for sg in itertools.product([1,-1],repeat=2):
        c=axes[I[0]]+sg[0]*axes[I[1]]+sg[1]*axes[I[2]]; c/=np.linalg.norm(c)
        if all(f(c[None])[0][i]>0 for i in I): break
    e1=np.cross(c,[0.3,0.5,0.7]); e1/=np.linalg.norm(e1); e2=np.cross(c,e1)
    X=lambda p:(lambda y:y/np.linalg.norm(y))(c+p[0]*e1+p[1]*e2)
    for t in range(2000):
        p0=rng.uniform(-0.08,0.08,2)
        if not all(f(X(p0)[None])[0][i]>0 for i in I): continue
        p,info,ier,msg=fsolve(lambda p:(lambda v:[v[I[0]]-r[0],v[I[1]]-r[1]])(f(X(p)[None])[0]),p0,full_output=True,xtol=1e-13)
        if ier==1: return X(p)
for I in [(0,1,4),(2,4,5),(1,3,4)]:
    I=list(I); J=[j for j in range(6) if j not in I]
    x=find_L_point(I,rng.dirichlet([2,2,2]))
    for _ in range(2):
        g=-rng.dirichlet([2,2,2])
        sols=[]
        # coarse grid seeds over theta in [0,pi), b in (0,1)
        for th0 in np.linspace(0,np.pi,24,endpoint=False):
            for b0 in np.linspace(0.04,0.96,12):
                def eq(p):
                    th,b=p; b=min(max(b,1e-6),1-1e-6); v=Gx(x,J,th,b); return [v[0]-g[0],v[1]-g[1]]
                p,info,ier,msg=fsolve(eq,[th0,b0],full_output=True,xtol=1e-12)
                th,b=p
                if ier!=1 or not (0<b<1) or np.max(np.abs(Gx(x,J,th,b)-g))>1e-8: continue
                # canonical representative of B: eigenvalue b on direction th (mod pi); identify (th,b)~(th+pi/2,1-b)
                if b<0.5: th,b=th+np.pi/2,1-b
                th=th%np.pi
                if not any(abs(b-bb)<1e-6 and min(abs(th-tt),np.pi-abs(th-tt))<1e-6 for tt,bb in sols): sols.append((th,b))
        print("facet",I,"g",np.round(g,3),"|G_x^{-1}(g)| =",len(sols))
