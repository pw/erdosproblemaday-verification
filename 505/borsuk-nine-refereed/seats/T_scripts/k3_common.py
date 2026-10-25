import numpy as np, itertools
phi=(1+5**0.5)/2
axes=np.array([[0,1,phi],[0,1,-phi],[1,phi,0],[1,-phi,0],[phi,0,1],[-phi,0,1]],float)
axes/=np.linalg.norm(axes,axis=1,keepdims=True)
rho=np.deg2rad(40.0); s0=np.sin(rho)**2
def bumps(X):
    s=1-(X@axes.T)**2
    out=np.zeros_like(s); ins=s<s0
    out[ins]=np.exp(-1.0/(s0-s[ins])); return out
def f(X):
    b=bumps(X); return b/b.sum(1,keepdims=True)
tris=[(0,1,4),(0,1,5),(0,2,3),(0,2,4),(0,3,5),(1,2,3),(1,2,5),(1,3,4),(2,4,5),(3,4,5)]
