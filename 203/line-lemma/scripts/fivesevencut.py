#!/usr/bin/env python3
"""Theorem D (the 5–7 cut on lines) — solver-free exclusion, recomputed independently of the referee.
Direction (1,1): lines τ = k − ℓ. For every pool prime, i_p = gcd(u_p+v_p, e_p) (= [⟨2,3⟩:⟨6⟩]), w_p = i_p/e_p.
Coarsen to M = 60: i'_p = gcd(i_p, 60), w'_p = i'_p/e_p. 5: e=4, 6≡1 ⇒ i=4, w=1 (whole lines, one class mod 4).
7: e=6, ord_7(6)=2 ⇒ i=3, w=1/2 (one class mod 3). WLOG (translation) t_5 = 0; for each t_7 ∈ Z/3 let
S = {τ mod 60 : τ ≢ 0 (4), τ ≢ t_7 (3)} (|S| = 30). For τ ∈ S, W(τ) = Σ_{p≠5,7} w'_p [τ ≡ t_p (i'_p)]. Averaging over S:
  avg_S W ≤ B := Σ_{p≠5,7} w'_p · max_c |{τ∈S : τ ≡ c (i'_p)}| / |S|,
and min_τ W ≤ avg_S W ≤ B. If B < 1 for the pool, no covering system uses a subset of it. B is the same for all t_7
(the three S are translates mod 60 — asserted below)."""
import json, glob, sys
from math import gcd
from fractions import Fraction as F
def B_of(pool):
    vals=[]
    for t7 in range(3):
        S=[t for t in range(60) if t%4!=0 and t%3!=t7]
        assert len(S)==30
        B=F(0); have5=have7=False
        for q in pool:
            e,u,v=q['e'],q['u'],q['v']
            s=(u+v)%e; i=gcd(s,e) if s else e; ip=gcd(i,60); wp=F(ip,e)
            if q['p']==5: assert (i,wp)==(4,F(1)) ; have5=True; continue
            if q['p']==7: assert (i,wp)==(3,F(1,2)); have7=True; continue
            best=max(sum(1 for t in S if t%ip==c) for c in range(ip))
            B+=wp*F(best,30)
        assert have5 and have7
        vals.append(B)
    assert len(set(vals))==1, vals
    return vals[0]
if __name__=='__main__':
    rows=[]
    for f in sorted(glob.glob('pool_*.json'), key=lambda s:int(s[5:-5])):
        d=json.load(open(f)); B=B_of(d['pool'])
        rows.append((d['N'],len(d['pool']),float(d['density']),B))
        print(f"N={d['N']:7d} primes={len(d['pool']):3d} density={float(d['density']):.4f}  B={B} = {float(B):.4f}  {'EXCLUDED' if B<1 else 'NOT excluded'}")
    small=[r for r in rows if r[0]<=65520 and r[2]>=1]; big=[r for r in rows if r[0]>65520]
    print("max B over the %d periods ≤ 65520 with density ≥ 1: %.4f (N=%d)"%(len(small),max(float(r[3]) for r in small), max(small,key=lambda r:r[3])[0]))
    print("open pools:", [(r[0],str(r[3]),round(float(r[3]),4)) for r in big])
    print("ALL < 1:", all(r[3]<1 for r in rows if r[2]>=1))
