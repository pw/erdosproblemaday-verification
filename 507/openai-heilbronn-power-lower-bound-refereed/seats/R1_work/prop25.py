# Prop 2.5 check: #{3x3 A : rows in Lambda, |row|<=X, det A = t} vs (log 2X)^2 X^6/I^2, for anisotropic sublattices
import numpy as np, math, itertools
def ball(R):
    m=int(math.floor(R))
    a=np.arange(-m,m+1)
    g=np.stack(np.meshgrid(a,a,a,indexing='ij'),-1).reshape(-1,3)
    return g[(g**2).sum(1)<=R*R]
def count(rows,tmax):
    cr=np.cross(rows[:,None,:],rows[None,:,:]).reshape(-1,3)
    cr=cr[np.any(cr!=0,axis=1)]
    hist=np.zeros(2*tmax+1,dtype=np.int64)
    ch=max(1,int(2e7//len(rows)))
    for s in range(0,len(cr),ch):
        d=(rows@cr[s:s+ch].T).ravel()
        d=d[np.abs(d)<=tmax]
        hist+=np.bincount(d+tmax,minlength=2*tmax+1)
    return hist
cases=[]
# Lambda given by congruence conditions: v . w_i == 0 mod m_i
cases.append(("v3=0 mod 8",8,lambda P:(P[:,2]%8==0),8))
cases.append(("Z x 4Z x 16Z",16,lambda P:(P[:,1]%4==0)&(P[:,2]%16==0),64))
cases.append(("v1+2v2+3v3=0 mod 9, v2=0 mod 3",9,lambda P:((P[:,0]+2*P[:,1]+3*P[:,2])%9==0)&(P[:,1]%3==0),27))
cases.append(("Z^3",6,lambda P:np.ones(len(P),bool),1))
cases.append(("v1=v2 mod 5, v3=0 mod 5",10,lambda P:((P[:,0]-P[:,1])%5==0)&(P[:,2]%5==0),25))
for name,X,cond,I in cases:
    P=ball(X); rows=P[cond(P)]
    tmax=3*I if I>1 else 30
    h=count(rows,tmax)
    bound=(math.log(2*X))**2*X**6/I**2
    nz=[(h[t+tmax],t) for t in range(1,tmax+1) if h[t+tmax]>0]
    mx=max(nz)
    print(f"{name}: I={I} X={X} #rows={len(rows)} max_t count={mx[0]} at t={mx[1]}  X^6/I^2={X**6/I**2:.0f} ratio count/(X^6/I^2)={mx[0]/(X**6/I**2):.2f} ratio to full bound={mx[0]/bound:.3f}",flush=True)
