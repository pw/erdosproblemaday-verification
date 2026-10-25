# Toy check of the digit construction (3.5)-(3.8) and Lemma 3.3 with arbitrary residues rho_{ia}(j)
import random, itertools
from sympy import nextprime
def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
random.seed(7)
# (3.7) exhaustive for small T
for T in range(1,40):
    k=T*T+1
    I=[a for a in range(T)]; J=[T*a for a in range(T)]; Lp=[T*T-(T+1)*a for a in range(T)]
    assert all(0<=x<k for x in I+J+Lp) and len(set(I))==T and len(set(J))==T and len(set(Lp))==T
    for a,b,c in itertools.product(range(T),repeat=3):
        assert (I[a]+J[b]+Lp[c]==k-1)==(a==b==c)
print("(3.6)-(3.7) verified exhaustively for T<40")
fails=0; tests=0; minmargin=None
for (T,r,Lexp) in [(1,3,2),(1,5,2),(2,3,2),(3,3,1),(3,5,1),(4,3,1),(2,7,2)]:
    L=r**Lexp; k=T*T+1
    B=nextprime(100*k*k*L**3)
    h=B**k; tau=B**(k-1)//2
    pos={1:{a:a for a in range(T)},2:{T*a:a for a in range(T)},3:{T*T-(T+1)*a:a for a in range(T)}}
    for trial in range(300):
        # residues rho[i][a][j]
        rho=[[[random.randrange(r) for j in range(3)] for a in range(T)] for i in range(3)]
        if trial%3==0:  # repeated label pattern: column 2 equals column 0
            for i in range(3):
                for a in range(T): rho[i][a][2]=rho[i][a][0]
        target=sum(det3([[rho[i][a][j] for j in range(3)] for i in range(3)]) for a in range(T))%r
        dig=[[[0]*k for j in range(3)] for i in range(3)]
        for i in range(3):
            for j in range(3):
                for v in range(k):
                    a=pos[i+1].get(v)
                    res=rho[i][a][j] if a is not None else 0
                    choices=[x for x in range(1,L+1) if x%r==res]
                    assert len(choices)==L//r
                    dig[i][j][v]=random.choice(choices)
        C=[[sum(dig[i][j][v]*B**v for v in range(k))%h for j in range(3)] for i in range(3)]
        # gamma_u via polynomial det
        def polymul(p,q):
            out=[0]*(len(p)+len(q)-1)
            for x,a in enumerate(p):
                for y,b in enumerate(q): out[x+y]+=a*b
            return out
        def polyadd(p,q,s=1):
            n=max(len(p),len(q)); p=p+[0]*(n-len(p)); q=q+[0]*(n-len(q))
            return [a+s*b for a,b in zip(p,q)]
        P=[[dig[i][j] for j in range(3)] for i in range(3)]
        gam=[0]
        for perm in itertools.permutations(range(3)):
            sgn=1
            for x in range(3):
                for y in range(x+1,3):
                    if perm[x]>perm[y]: sgn=-sgn
            t=polymul(polymul(P[0][perm[0]],P[1][perm[1]]),P[2][perm[2]])
            gam=polyadd(gam,t,sgn)
        A0=6*k*k*L**3
        assert all(abs(g)<=A0 for g in gam), "coef bound"
        assert gam[k-1]%r==target, "gamma_{k-1} mismatch"
        SC=sum(gam[u]*B**u for u in range(k))
        dC=det3(C)%h
        assert (SC-dC)%h==0 and abs(SC)<h/2
        cent=dC if dC<=h//2 else dC-h
        tests+=1
        if target!=0:
            if abs(cent)<=tau: fails+=1
            m=abs(cent)/tau
            minmargin=m if minmargin is None else min(minmargin,m)
print(f"Lemma 3.3 toy: {tests} digit matrices, failures (|centered det|<=tau with nonzero target) = {fails}, min |rep|/tau over nonzero-target cases = {minmargin:.4f}")
