# Direct check of (4.24) tensorization: F symmetric under independent permutations inside each of
# G groups (M slots each, alphabet {0,1} with law p), probes = first m slots of each group,
# last l slots averaged.  Compare ||F_full||^2/||F||^2 with prod_g max_j frac(j) .
import itertools, random
from math import comb
random.seed(7)
def run(G,M,m,l,p,trials=5):
    n=G*M
    X=list(itertools.product((0,1),repeat=n))
    def P(x):
        r=1.0
        for a in x: r*= p if a else 1-p
        return r
    def E_i(Gf,i):
        out={}
        for x in X:
            y0=list(x); y0[i]=0; y1=list(x); y1[i]=1
            out[x]=(1-p)*Gf[tuple(y0)]+p*Gf[tuple(y1)]
        return out
    fr=max((comb(M-m-l,j-m)/comb(M,j) if 0<=j-m<=M-m-l else 0) for j in range(M+1))
    worst=0
    for t in range(trials):
        tab={}
        def f(x):
            key=tuple(sum(x[g*M:(g+1)*M]) for g in range(G))
            if key not in tab: tab[key]=complex(random.gauss(0,1),random.gauss(0,1))
            return tab[key]
        F={x:f(x) for x in X}
        nF=sum(P(x)*abs(F[x])**2 for x in X)
        Ff=F
        for g in range(G):
            for i in range(M-l,M): Ff=E_i(Ff,g*M+i)          # average last l
        for g in range(G):
            for i in range(m):                                 # (1-E_i) on probes
                e=E_i(Ff,g*M+i); Ff={x:Ff[x]-e[x] for x in X}
        nFf=sum(P(x)*abs(Ff[x])**2 for x in X)
        worst=max(worst,nFf/nF)
    print("G=%d M=%d m=%d l=%d p=%.2f : max ||F_full||^2/||F||^2 = %.5f   bound prod max frac = %.5f   theta_m^G=%.4f"%(
        G,M,m,l,p,worst,fr**G,(2*l**l*m**(-l))**G))
run(1,5,2,1,0.3)
run(2,4,1,1,0.4)
run(2,5,2,1,0.3)
