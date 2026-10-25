import numpy as np, random, sys
from bnb import ell
from fractions import Fraction
random.seed(51)
def check(fn, P, npts, maxlog=60):
    R = np.load(fn); bad=0; done=0
    pts=[idx for idx in zip(*np.nonzero(~np.isnan(R)))]
    pts=[p for p in pts if sum(int(e)*np.log10(q) for e,q in zip(p,P))<=maxlog]
    sample=random.sample(pts, min(npts,len(pts)))
    for idx in sample:
        a=1
        for q,e in zip(P,idx): a*=q**int(e)
        n,cov=ell(a, {q:int(e) for q,e in zip(P,idx) if e>0})
        r=n/a
        if abs(r-R[idx])>1e-9*r: bad+=1; print('MISMATCH',idx,r,R[idx],cov)
        done+=1
    # also every non-totient in DP must have no preimage
    nontot=[idx for idx in zip(*np.nonzero(np.isnan(R)))]
    nt_ok=0
    for idx in random.sample(nontot,min(40,len(nontot))):
        a=1
        for q,e in zip(P,idx): a*=q**int(e)
        n,cov=ell(a,{q:int(e) for q,e in zip(P,idx) if e>0} if a>1 else None)
        if n is not None: bad+=1; print('NONTOT MISMATCH',idx,n)
        else: nt_ok+=1
    print(fn, 'checked', done, 'totient points +', nt_ok, 'non-totient points; mismatches', bad)
check('R23.npy',[2,3],300,maxlog=45)
check('R235.npy',[2,3,5],300,maxlog=30)
