# Brute-force check of Lemma 2.4: #{(u1,u2,u3): |u_j|<=R_j, det(u1,u2,u3)=t} vs (R1R2R3)^2 (log 2R1)^2
import numpy as np, itertools, math, sys
def ball(R):
    m=int(math.floor(R))
    pts=[(a,b,c) for a in range(-m,m+1) for b in range(-m,m+1) for c in range(-m,m+1) if a*a+b*b+c*c<=R*R]
    return np.array(pts,dtype=np.int64)
def counts(R1,R2,R3,tmax):
    B1,B2,B3=ball(R1),ball(R2),ball(R3)
    # all pairs (u2,u3) -> cross products
    cr=np.cross(B2[:,None,:],B3[None,:,:]).reshape(-1,3)
    cr=cr[np.any(cr!=0,axis=1)]
    hist=np.zeros(2*tmax+1,dtype=np.int64)
    ch=max(1,int(2e7//len(B1)))
    for s in range(0,len(cr),ch):
        d=B1@cr[s:s+ch].T   # det(u1,u2,u3)=u1.(u2 x u3)
        d=d.ravel()
        d=d[np.abs(d)<=tmax]
        hist+=np.bincount(d+tmax,minlength=2*tmax+1)
    return hist
if __name__=="__main__":
    out=[]
    for (R1,R2,R3) in [(3,3,3),(5,3,2),(6,4,1),(8,2,1),(5,5,5),(7,4,2),(9,3,1.5),(10,6,1),(6,6,4)]:
        tmax=60
        hist=counts(R1,R2,R3,tmax)
        bound=(R1*R2*R3)**2*math.log(2*R1)**2
        best=[]
        for t in range(1,tmax+1):
            c=hist[t+tmax]
            best.append((c/bound,t,c))
        best.sort(reverse=True)
        print(f"R=({R1},{R2},{R3}) maxratio={best[0][0]:.4f} at t={best[0][1]} count={best[0][2]} ; t=1 ratio={hist[1+tmax]/bound:.4f}; (R1R2R3)^2 ratio max={best[0][2]/(R1*R2*R3)**2:.3f}",flush=True)
    