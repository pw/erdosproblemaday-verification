# From-scratch exact h(S_K): (a) DP over the copy chain using ACTUAL points and brute-forced edges;
# (b) max-plus matrix in abstract form + stationarity; (c) brute force over all subsets for K<=1.
import sys, itertools; sys.path.insert(0,'/tmp/ref757')
from core import *
def aps(pts):
    s=set(pts); P=sorted(pts); E=set()
    for a,c in itertools.combinations(P,2):
        if (a+c)/2 in s: E.add(frozenset((a,(a+c)/2,c)))
    return E
def h_dp(K):
    cs=copies(K); S=set().union(*cs); E=aps(S)
    # every edge must sit in one copy (else DP invalid) -- checked, not assumed
    assert all(any(e<=c for c in cs) for e in E)
    # also no 4-point relations: check sums
    from collections import Counter
    P=sorted(S); cnt=Counter(a+b for a,b in itertools.combinations(P,2))
    assert max(cnt.values())==1, 'weak Sidon fails'
    Ecopy=[[e for e in E if e<=c] for c in cs]
    # DP: state = T ∩ (cs[t] ∩ cs[t+1]) as frozenset of actual points
    def free(T,edges): return not any(e<=T for e in edges)
    prev=None  # dict interface-> best count of T ∩ (copies 0..t)
    for t in range(K+1):
        c=sorted(cs[t]); Lset=cs[t]&cs[t-1] if t>0 else frozenset(); Rset=cs[t]&cs[t+1] if t<K else frozenset()
        new={}
        for k in range(len(c)+1):
            for T in itertools.combinations(c,k):
                T=frozenset(T)
                if not free(T,Ecopy[t]): continue
                Lk=T&Lset; Rk=T&Rset
                base=0 if t==0 else prev.get(Lk,None)
                if base is None: continue
                val=base+len(T-Lset)
                if new.get(Rk,-1)<val: new[Rk]=val
        prev=new
    return max(prev.values())
for K in range(0,9):
    print('K',K,'h_dp',h_dp(K),'claim',7+5*K,flush=True)
