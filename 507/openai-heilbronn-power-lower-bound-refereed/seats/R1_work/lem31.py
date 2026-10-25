# Lemma 3.1 check for d=3 (and d=1) over r in {3,5}: N has F_r coefficients, alternation, c_{pps}=0,
# every monomial = m_p(X1)m_q(X2)m_s(X3) with p,q,s distinct, decomposition identity, and (3.4).
import itertools, random, sys
from collections import defaultdict
def field(r,d):
    # find irreducible monic poly of degree d over F_r
    for coeffs in itertools.product(range(r),repeat=d):
        f=list(coeffs)+[1]  # f[0]+f[1]t+...+t^d
        # irreducible check for d<=3: no roots
        if d==1: return f
        if all(sum(f[i]*pow(x,i,r) for i in range(d+1))%r!=0 for x in range(r)):
            if d<=3: return f
    raise Exception
def fmul(a,b,r,f,d):
    prod=[0]*(2*d-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y: prod[i+j]=(prod[i+j]+x*y)%r
    for i in range(2*d-2,d-1,-1):
        c=prod[i]
        if c:
            for j in range(d+1):
                prod[i-d+j]=(prod[i-d+j]-c*f[j])%r
    return tuple(prod[:d])
def fadd(a,b,r): return tuple((x+y)%r for x,y in zip(a,b))
def fpow(a,e,r,f,d):
    res=tuple([1]+[0]*(d-1)); base=a
    while e:
        if e&1: res=fmul(res,base,r,f,d)
        base=fmul(base,base,r,f,d); e>>=1
    return res
def check(r,d):
    f=field(r,d)
    one=tuple([1]+[0]*(d-1)); zero=tuple([0]*d)
    beta=[tuple(1 if i==nu else 0 for i in range(d)) for nu in range(d)]  # polynomial basis
    # variable index: group g (0..2), row i (0..2), nu (0..d-1) -> g*3d + i*d + nu
    var=lambda g,i,nu: g*3*d+i*d+nu
    D=defaultdict(lambda: zero)
    for perm in itertools.permutations(range(3)):
        sgn=1
        for a in range(3):
            for b in range(a+1,3):
                if perm[a]>perm[b]: sgn=-sgn
        # det of matrix M[i][j]=Z(X^{(j)})_i : sum_perm sgn prod_j M[perm[j]][j]
        for nus in itertools.product(range(d),repeat=3):
            mon=tuple(sorted(var(j,perm[j],nus[j]) for j in range(3)))
            c=one
            for j in range(3): c=fmul(c,beta[nus[j]],r,f,d)
            if sgn<0: c=tuple((-x)%r for x in c)
            D[mon]=fadd(D[mon],c,r)
    def frob(P,times):
        return {m:fpow(c,r**times,r,f,d) for m,c in P.items()}
    def pmul(P,Q):
        R=defaultdict(lambda: zero)
        for m1,c1 in P.items():
            if c1==zero: continue
            for m2,c2 in Q.items():
                if c2==zero: continue
                m=tuple(sorted(m1+m2))
                R[m]=fadd(R[m],fmul(c1,c2,r,f,d),r)
        return {m:c for m,c in R.items() if c!=zero}
    Nn={m:c for m,c in D.items() if c!=zero}
    for j in range(1,d):
        Nn=pmul(Nn,frob(D,j))
    # coefficients in F_r?
    inFr=all(all(x==0 for x in c[1:]) for c in Nn.values())
    Nc={m:c[0] for m,c in Nn.items()}
    # split monomials by group
    def split(m):
        parts=[[],[],[]]
        for v in m: parts[v//(3*d)].append(v%(3*d))
        return tuple(tuple(p) for p in parts)
    homog=all(all(len(p)==d for p in split(m)) for m in Nc)
    S={}
    for m,c in Nc.items(): S[split(m)]=c
    rep=sum(1 for k3 in S if len(set(k3))<3)
    # alternation: coefficient of permuted triple = sgn * c
    alt_ok=True
    for k3,c in S.items():
        for perm in itertools.permutations(range(3)):
            sgn=1
            for a in range(3):
                for b in range(a+1,3):
                    if perm[a]>perm[b]: sgn=-sgn
            k3p=tuple(k3[perm[j]] for j in range(3))
            if S.get(k3p,0)%r != (sgn*c)%r: alt_ok=False
    # number of orbits = nonzero c_{pqs}
    orbits=set(tuple(sorted(k3)) for k3 in S)
    # decomposition identity: sum over orbits c_{pqs} det(m_p,m_q,m_s) reproduces S exactly
    Rec=defaultdict(int)
    for o in orbits:
        p,q,s=o
        c=S[(p,q,s)]
        for perm in itertools.permutations(range(3)):
            sgn=1
            for a in range(3):
                for b in range(a+1,3):
                    if perm[a]>perm[b]: sgn=-sgn
            # det(f_i(X^{(j)})): sum_perm sgn prod_i f_i(X^{(perm(i))}) with f=(c m_p, m_q, m_s)
            key=[None]*3
            for i,mono in enumerate((p,q,s)): key[perm[i]]=mono
            Rec[tuple(key)]=(Rec[tuple(key)]+sgn*c)%r
    Rec={k:v for k,v in Rec.items() if v}
    decomp_ok=(Rec=={k:v%r for k,v in S.items()})
    # (3.4): evaluate N at X(xi) and compare with Norm of Vandermonde
    def X_of(xi):
        z=[one,xi,fmul(xi,xi,r,f,d)]
        return [z[i][nu] for i in range(3) for nu in range(d)]  # coordinates in poly basis
    def evalN(xs):
        tot=0
        for m,c in Nc.items():
            v=c
            for var_ in m:
                g=var_//(3*d); loc=var_%(3*d)
                v=v*xs[g][loc]%r
            tot=(tot+v)%r
        return tot
    def norm(a):
        p=one
        for j in range(d): p=fmul(p,fpow(a,r**j,r,f,d),r,f,d)
        return p
    ok34=True; nz=0
    els=list(itertools.product(range(r),repeat=d))
    random.seed(0)
    for trial in range(40):
        xs=[random.choice(els) for _ in range(3)]
        if trial%5==0: xs[2]=xs[0]
        val=evalN([X_of(x) for x in xs])
        sub=lambda a,b: tuple((x-y)%r for x,y in zip(a,b))
        V=fmul(fmul(sub(xs[1],xs[0]),sub(xs[2],xs[0]),r,f,d),sub(xs[2],xs[1]),r,f,d)
        nv=norm(V)
        if any(nv[1:]) or nv[0]!=val: ok34=False
        if len(set(xs))==3 and val==0: ok34=False
    print(f"r={r} d={d}: #terms(N)={len(Nc)} coeffs in F_r={inFr} homog deg d per group={homog} repeated-index terms={rep} alternating={alt_ok} nonzero c_pqs={len(orbits)} decomposition exact={decomp_ok} (3.4) ok={ok34}",flush=True)
for (r,d) in [(3,1),(5,1),(3,3),(5,3)]:
    check(r,d)
