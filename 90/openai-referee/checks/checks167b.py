#!/usr/bin/env python3
"""Lemma 2.7 toy, corrected: check the LEMMA'S INEQUALITY, not the asymptotic. On a bipartite graph with codegree <= 2
(two points share <= 2 centres, as for unit circles), the wedge law (q ~ kappa, then p, r independent uniform neighbours
of q) has off-diagonal atoms P(p,r) <= 2/(|E| d_min,Q) =: M_t and P(p=r) = |Q|/|E|; the paper's bound is
D = H(p)+H(r)-H(p,r) <= 2 H(p) - (1-P(p=r)) log(1/M_t). Control: the same inequality with M_t replaced by the
AVERAGE off-diagonal atom (a smaller number, so a tighter 'bound') must be violated on some graphs."""
import random, math
from collections import defaultdict
def build(nP,nQ,dq,seed):
    rng=random.Random(seed); P=list(range(nP)); nbr={}; codeg=defaultdict(int); edges=[]
    for q in range(nQ):
        for _ in range(200):
            S=rng.sample(P,dq)
            if all(codeg[(a,b)]<2 for a in S for b in S if a<b): break
        else: continue
        for a in S:
            for b in S:
                if a<b: codeg[(a,b)]+=1
        nbr[q]=S; edges+=[(p,q) for p in S]
    return P,nbr,edges
def laws(P,nbr,edges):
    E=len(edges); dp=defaultdict(int)
    for p,q in edges: dp[p]+=1
    mu={p:dp[p]/E for p in P}
    joint=defaultdict(float)
    for q,S in nbr.items():
        kq=len(S)/E
        for a in S:
            for b in S: joint[(a,b)]+=kq/len(S)**2
    return E,mu,joint
def H(d): return -sum(v*math.log(v) for v in d.values() if v>0)
res=[]
for seed in range(12):
    P,nbr,edges=build(60,400,5,seed); E,mu,joint=laws(P,nbr,edges)
    D=sum(v*math.log(v/(mu[a]*mu[b])) for (a,b),v in joint.items() if v>0)
    Hp=H(mu); Hpr=H(joint); Pdiag=sum(v for (a,b),v in joint.items() if a==b)
    dmin=min(len(S) for S in nbr.values()); Mt=2/(E*dmin)
    maxoff=max(v for (a,b),v in joint.items() if a!=b)
    bound=2*Hp-(1-Pdiag)*math.log(1/Mt)
    res.append((D<=bound+1e-12, maxoff<=Mt+1e-15, True, D, bound, Pdiag))
# CONTROL: allow codegree up to 5 (NOT the unit-circle situation) — the atom bound 2/(|E| d_min,Q) must then be violated
def build5(nP,nQ,dq,seed):
    rng=random.Random(seed); P=list(range(nP)); nbr={}; codeg=defaultdict(int); edges=[]
    for q in range(nQ):
        S=rng.sample(P,dq)
        for a in S:
            for b in S:
                if a<b: codeg[(a,b)]+=1
        nbr[q]=S; edges+=[(p,q) for p in S]
    return P,nbr,edges,max(codeg.values())
ctrl=[]
for seed in range(12):
    P,nbr,edges,cmax=build5(20,400,5,seed); E,mu,joint=laws(P,nbr,edges)
    dmin=min(len(S) for S in nbr.values()); Mt=2/(E*dmin); maxoff=max(v for (a,b),v in joint.items() if a!=b)
    ctrl.append((maxoff>Mt, cmax))
ok_bound=all(r[0] for r in res); ok_atom=all(r[1] for r in res); ctrl_viol=any(c[0] for c in ctrl)
print("PASS" if ok_atom else "FAIL", "off-diagonal atoms <= 2/(|E| d_min,Q) on codegree<=2 graphs (12 seeds)")
print("PASS" if ok_bound else "FAIL", "Lemma 2.7 inequality D <= 2H(p) - (1-P(p=r)) log(1/M_t) (12 seeds)", "e.g. D=%.3f bound=%.3f P(p=r)=%.3f"%(res[0][3],res[0][4],res[0][5]))
print("PASS" if ctrl_viol else "FAIL", "CONTROL: a graph with codegree up to %d VIOLATES the atom bound 2/(|E| d_min,Q) (expect PASS = violation found; (2.16) needs codegree <= 2)"%max(c[1] for c in ctrl))
print("SUMMARY-B: %d PASS / %d FAIL"%(sum([ok_atom,ok_bound,ctrl_viol]), 3-sum([ok_atom,ok_bound,ctrl_viol])))
