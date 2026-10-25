#!/usr/bin/env python3
"""Brute-force second instrument for the three labels in Itabe's v0.2.1 manuscript (Erdős #160, N^(1/3+o(1))).

 (i)  cubic factor nu_p on [0,p^3): colour n = r + p w + p^2 u by (tau_p(r), tau_p(w), Norm(r,w,u)) with the
      F_{p^3}/F_p norm in SOME basis (basis-independence is part of what is being tested: we use a random
      irreducible cubic).  Claim (Lemma 7.1 + §7.2): no nontrivial 4-AP a,a+d,a+2d,a+3d < p^3 has the
      proper ABBA equalities c(a)=c(a+3d) and c(a+d)=c(a+2d).  Also tested on the cyclic group Z/p^3Z: this colouring is
      Shi–Dong's k=4 colouring (arXiv 2607.20752, Thm 1.1) restricted to the subgroup pZ/p^4Z (the slice x0=0), so their
      theorem predicts the same there.
 (ii) shared mod-24 label lambda_{P,L} on [0,P^(L+1)), P = 24B+1: claim = no three equal colours on any
      nontrivial 4-AP (patterns AAAB, AABA, ABAA, BAAA, AAAA) and no ABAB.
 (iii) dyadic label mu_{B,L} on [0,B^(L+1)): claim = no AABB (incl. AAAA).
Controls: for (i) drop the norm / use an isotropic cubic; for (ii) drop the mod-24 digit labels (keep the
square norm) -> carries break the argument and ABAB/AAAB should appear; for (iii) drop the buckets.
Exit 0 = all claims hold on the tested horizons and every control fired; 1 = violation; 2 = cannot see.
"""
import sys, itertools, random

def irreducible_cubics(p):
    out=[]
    for c2 in range(p):
        for c1 in range(p):
            for c0 in range(p):
                if all((t**3 + c2*t*t + c1*t + c0) % p for t in range(p)): out.append((c0,c1,c2))
    return out

def mul(a,b,p,f):
    c0,c1,c2=f; r=[0]*5
    for i in range(3):
        for j in range(3): r[i+j]=(r[i+j]+a[i]*b[j])%p
    for deg in (4,3):
        k=r[deg]
        if k:
            r[deg]=0; s=deg-3
            r[s+2]=(r[s+2]-k*c2)%p; r[s+1]=(r[s+1]-k*c1)%p; r[s]=(r[s]-k*c0)%p
    return (r[0],r[1],r[2])

def powr(a,e,p,f):
    res=(1,0,0)
    while e:
        if e&1: res=mul(res,a,p,f)
        a=mul(a,a,p,f); e>>=1
    return res

def norm_table(p,f):
    tab={}
    for z in itertools.product(range(p),repeat=3):
        zp=powr(z,p,p,f); zpp=powr(zp,p,p,f); n=mul(mul(z,zp,p,f),zpp,p,f)
        assert n[1]==0 and n[2]==0; tab[z]=n[0]
    return tab

def abba_violations(col, N, cyclic=False, stop=False):
    bad=0; first=None
    if cyclic:
        for a in range(N):
            for d in range(1,N):
                if col[a]==col[(a+3*d)%N] and col[(a+d)%N]==col[(a+2*d)%N]:
                    bad+=1; first=first or (a,d)
                    if stop: return bad,first
    else:
        for a in range(N):
            for d in range(1,(N-1-a)//3+1):
                if col[a]==col[a+3*d] and col[a+d]==col[a+2*d]:
                    bad+=1; first=first or (a,d)
                    if stop: return bad,first
    return bad,first

def three_equal_or_abab(col, N, stop=False):
    """count nontrivial 4-APs in [0,N) with some three positions equal, or ABAB."""
    bad3=0; babab=0; f3=None; fab=None
    for a in range(N):
        for d in range(1,(N-1-a)//3+1):
            c=(col[a],col[a+d],col[a+2*d],col[a+3*d])
            if (c[0]==c[1]==c[2]) or (c[1]==c[2]==c[3]) or (c[0]==c[1]==c[3]) or (c[0]==c[2]==c[3]):
                bad3+=1; f3=f3 or (a,d)
            if c[0]==c[2] and c[1]==c[3]:
                babab+=1; fab=fab or (a,d)
            if stop and bad3 and babab: return bad3,babab,f3,fab
    return bad3,babab,f3,fab

def aabb_violations(col,N,stop=False):
    bad=0; first=None
    for a in range(N):
        for d in range(1,(N-1-a)//3+1):
            if col[a]==col[a+d] and col[a+2*d]==col[a+3*d]:
                bad+=1; first=first or (a,d)
                if stop: return bad,first
    return bad,first

def digits(n,base,L):
    xs=[]
    for _ in range(L): xs.append(n%base); n//=base
    return xs

def main():
    rc=0
    random.seed(160)
    # ---------- (i) cubic factor ----------
    for p in [5,7,11]:
        f=random.choice(irreducible_cubics(p)); nt=norm_table(p,f)
        N=p**3
        col=[]; colNoNorm=[]; colIso=[]
        for n in range(N):
            r,w,u=digits(n,p,3)
            t=(3*r//p, 3*w//p)
            col.append(t+(nt[(r,w,u)],)); colNoNorm.append(t); colIso.append(t+(pow(r,3,p),))
        pal=len(set(col))
        b,first=abba_violations(col,N)
        bc,firstc=abba_violations(col,N,cyclic=True)
        k1,_=abba_violations(colNoNorm,N,stop=True); k2,_=abba_violations(colIso,N,stop=True)
        print(f"(i) p={p} f={f}: horizon [0,{N})  palette {pal} (<=9p={9*p}: {pal<=9*p})  proper-ABBA 4-APs: interval {b}  cyclic Z/p^3Z {bc}   controls no-norm {k1} / isotropic {k2} (each >0)")
        if b or bc: rc=1
        if not (k1 and k2): rc=max(rc,2)
    # ---------- (ii) shared mod-24 label ----------
    for (B,L) in [(1,1),(1,2),(2,1)]:
        P=24*B+1; N=P**(L+1)
        if N>200000: continue
        col=[]; colNoMod=[]
        for n in range(N):
            x=digits(n,P,L+1)
            col.append(tuple(xj%24 for xj in x[:L])+(sum(v*v for v in x),))
            colNoMod.append((sum(v*v for v in x),))
        bad3,babab,f3,fab=three_equal_or_abab(col,N)
        k3,kab,_,_=three_equal_or_abab(colNoMod,N,stop=True)
        print(f"(ii) P={P} L={L}: horizon [0,{N})  palette {len(set(col))} (codomain 24^L((L+1)P^2+1)={24**L*((L+1)*P*P+1)})  three-equal {bad3}  ABAB {babab}   control (no mod-24 digits): three-equal {k3} ABAB {kab} (each >0)")
        if bad3 or babab: rc=1
        if not (k3 and kab): rc=max(rc,2)
    # ---------- (iii) dyadic label ----------
    import math
    for (B,L) in [(4,2),(8,2),(16,2),(8,3)]:
        N=B**(L+1)
        if N>200000: continue
        col=[]; colNoBucket=[]
        for n in range(N):
            x=digits(n,B,L+1)
            col.append(tuple(int(math.floor(math.log2(xj+1))) for xj in x[:L])+(sum(v*v for v in x),))
            colNoBucket.append((sum(v*v for v in x),))
        b,first=aabb_violations(col,N); k,_=aabb_violations(colNoBucket,N,stop=True)
        print(f"(iii) B={B} L={L}: horizon [0,{N})  palette {len(set(col))}  AABB {b}   control (no buckets) {k} (>0)")
        if b: rc=1
        if not k: rc=max(rc,2)
    print("RC",rc); sys.exit(rc)
main()
