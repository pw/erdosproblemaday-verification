import numpy as np, itertools
rng = np.random.default_rng(5)
def tv(a,b): return 0.5*np.abs(a-b).sum()
def exact_agree(p,q):
    d=tv(p,q); return ((1-d)+np.sum(np.maximum(p-q,0)*q)+np.sum(np.maximum(q-p,0)*p))/(1+d)
def sim_pair(p,q,N):
    m=len(p); ag=0
    # vectorised: simulate trials in blocks
    yp=-np.ones(N,int); yq=-np.ones(N,int)
    while (yp<0).any() or (yq<0).any():
        z=rng.integers(m,size=N); u=rng.random(N)
        ap=(yp<0)&(u<=p[z]); aq=(yq<0)&(u<=q[z])
        yp[ap]=z[ap]; yq[aq]=z[aq]
    return np.mean(yp!=yq), [np.bincount(yp,minlength=m)/N, np.bincount(yq,minlength=m)/N]
mx=0
for t in range(60):
    m=int(rng.integers(2,7)); p,q=rng.dirichlet(np.ones(m)*rng.uniform(0.2,3),size=2)
    N=400000
    dis,(ep,eq)=sim_pair(p,q,N); ex=1-exact_agree(p,q); d=tv(p,q)
    z=(dis-ex)/np.sqrt(ex*(1-ex)/N)
    mx=max(mx,abs(z))
    assert ex<=2*d/(1+d)+1e-15
    if abs(z)>3: print('z',z,p,q)
print('max |z| over 60 pairs, N=4e5:',mx)
