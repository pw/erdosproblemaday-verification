import itertools
def digits(n,b,k):
    out=[]
    for _ in range(k): out.append(n%b); n//=b
    return out
def irr(p): return [(c0,c1,c2) for c2 in range(p) for c1 in range(p) for c0 in range(p) if all((t**3+c2*t*t+c1*t+c0)%p for t in range(p))]
def mul(a,b,p,f):
    c0,c1,c2=f; r=[0]*5
    for i in range(3):
        for j in range(3): r[i+j]=(r[i+j]+a[i]*b[j])%p
    for deg in (4,3):
        k=r[deg]
        if k:
            r[deg]=0; s=deg-3
            r[s+2]=(r[s+2]-k*c2)%p; r[s+1]=(r[s+1]-k*c1)%p; r[s]=(r[s]-k*c0)%p
    return tuple(r[:3])
def norm(z,p,f):
    cols=[mul(z,e,p,f) for e in ((1,0,0),(0,1,0),(0,0,1))]
    M=[[cols[j][i] for j in range(3)] for i in range(3)]
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))%p
for p in (2,3,5):
    for f in irr(p)[:3]:
        N=p**3; t=lambda r:0 if 3*r<p else (1 if 3*r<2*p else 2)
        col=[(t(r),t(w),norm((r,w,u),p,f)) for r,w,u in (digits(n,p,3) for n in range(N))]
        bad=sum(1 for a in range(N) for d in range(1,(N-1-a)//3+1) if col[a]==col[a+3*d] and col[a+d]==col[a+2*d])
        print(f"p={p} f={f}: ABBA-equality APs on [0,{N}): {bad}")
