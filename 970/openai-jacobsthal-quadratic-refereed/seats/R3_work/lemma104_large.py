# Lemma 10.4 for E = all primes < P (the case where 2 in E forces 2|d0): trend of S(P)=sum_{d0<=P^.95} W_E(d0)/d0
import numpy as np, math
G=0.5772156649015329
for P in [10**4,10**5,10**6,10**7,10**8]:
    X=int(P**.95)
    # g(n)=prod_{t|n, t>=3}(t-1)/(t-2) multiplicative on rad; compute log g via sieve over primes t<=X (all < P)
    lg=np.zeros(X+1)
    isp=np.ones(X+1,dtype=bool); isp[:2]=False
    for i in range(2,int(X**.5)+1):
        if isp[i]: isp[i*i::i]=False
    ps=np.nonzero(isp)[0]
    for t in ps:
        if t>=3: lg[t::t]+=math.log((t-1)/(t-2))
    # base = prod_{3<=t<P}(1-1/(t-1)); primes up to P needed
    if P<=X: allp=ps
    else:
        isp2=np.ones(P,dtype=bool); isp2[:2]=False
        for i in range(2,int(P**.5)+1):
            if isp2[i]: isp2[i*i::i]=False
        allp=np.nonzero(isp2)[0]
    lb=np.sum(np.log1p(-1.0/(allp[allp>=3]-1)))
    n=np.arange(2,X+1,2)   # must be even (2 in E has zero mass at V_2=0)
    S=np.exp(lb)*np.sum(np.exp(lg[n])/n)
    print(f"P=1e{int(round(math.log10(P)))}: S={S:.5f}   e^-g*.94={math.exp(-G)*.94:.5f}  e^-g*.95 (limit)={math.exp(-G)*.95:.5f}")
