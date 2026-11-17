# Run the proof's own chain on the periodic+sparse model and check each claimed step:
#  i* exists, d(X_i*) >= i* delta, Kneser equality |Y| = |P|+|S|-1 at the minimal period g of X_{i*+1},
#  |P| >= i* delta g, |S| >= delta g, s >= delta g, s>=2 (g>=2), Lemma-1 count t_bound, and
#  true order <= i*+1+t_actual <= i*+1+t_bound <= floor(2/delta)-1.
# Model: B = the full classes D only (sparse members are not good centres here; that is the worst case for |S|).
import sys
from fractions import Fraction as F
from math import floor, ceil
def ss(X,Y,g): return frozenset((x+y)%g for x in X for y in Y)
def model_order(M,D,T):
    dist=[-1]*M; dist[0]=0; q=[0]
    for u in q:
        for k in T:
            v=(u+k)%M
            if dist[v]<0: dist[v]=dist[u]+1; q.append(v)
    return max(min(1+dist[(r-d)%M] for d in D) for r in range(M))
MMAX=int(sys.argv[1]) if len(sys.argv)>1 else 11
stats=dict(sets=0,bad=0,slack0=0); worst_slack=None
for M in range(2,MMAX+1):
    full=frozenset(range(M))
    for Dbits in range(1,1<<M):
        D=frozenset(c for c in range(M) if Dbits>>c&1)
        if 2*len(D)>M: continue
        rest=[c for c in range(M) if c not in D]
        for Eb in range(1<<len(rest)):
            E=frozenset(rest[j] for j in range(len(rest)) if Eb>>j&1)
            T=D|E
            # (H): T generates Z/M
            Gs=frozenset([0]);
            while True:
                n2=Gs|ss(Gs,T,M)
                if n2==Gs: break
                Gs=n2
            if Gs!=full: continue
            stats['sets']+=1
            delta=F(len(D),M)
            S0=D|frozenset([0])                       # classes met by B0
            I={1:D}                                   # cofinite classes of X_i
            Met={1:S0}
            i=1
            while True:
                I[i+1]=ss(D, Met[i], M)               # cofinite classes of X_{i+1}: need >=1 full-class summand
                Met[i+1]=ss(Met[i],S0,M)
                if F(len(I[i+1]),M) < F(len(I[i]),M)+delta: break
                i+=1
                assert i<=M+2
            istar=i
            ok = F(len(I[istar]),M) >= istar*delta and istar<=floor(1/delta)
            U=I[istar+1]
            g=min(p for p in range(1,M+1) if M%p==0 and all(((u+p)%M) in U for u in U))
            Y=frozenset(u%g for u in U); P=frozenset(x%g for x in Met[istar]); S=frozenset(x%g for x in S0)
            Sp=frozenset(x%g for x in T)|frozenset([0]); s=len(Sp)
            ok = ok and len(Y)==len(P)+len(S)-1 and len(P)>=istar*delta*g and len(S)>=delta*g and s>=delta*g and (g==1 or s>=2)
            Z=Y; t=0
            while len(Z)<g: Z=ss(Z,Sp,g); t+=1; assert t<=g+1
            a=g-len(Y); tb=0 if a==0 else -(-a//(-(-s//2)))
            h_act=istar+1+t; h_b=istar+1+tb
            true=model_order(M,D,T)
            fb=floor(2/delta)-1 if delta<=F(1,2) else None
            ok = ok and true<=h_act<=h_b<=fb
            if not ok:
                stats['bad']+=1
                if stats['bad']<=5: print("BAD",M,sorted(D),sorted(E),istar,g,sorted(Y),sorted(P),sorted(S),s,t,tb,true,h_act,h_b,fb)
            if h_b==fb: stats['slack0']+=1
            sl=(fb-true, M, sorted(D), sorted(E))
print(stats)
