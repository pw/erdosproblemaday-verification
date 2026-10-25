#!/usr/bin/env python3
"""Line-lemma census. For a pool (primes p with e_p and character (u,v): L_p = {uk+vl ≡ 0 mod e_p},
2 ↦ u, 3 ↦ v in Z/e_p ≅ H_p) and a primitive direction d=(a,b): the element g = 2^a 3^b ↦ a*u+b*v,
ord(g) = e/gcd(a*u+b*v, e) =: ord_p(g); a coset of L_p meets exactly one class of lines mod i_p := gcd(a*u+b*v, e)
(transverse index), and on each such line it is one residue class mod ord_p(g): intensity w_p = i_p/e_p = 1/ord_p(g).
E = sum of w_p over i_p = 1 ('everywhere' primes); Lambda = sum of 1/e_p over lumpy primes; M = lcm of lumpy i_p."""
import json, sys, glob
from math import gcd
from fractions import Fraction as F
from functools import reduce
def lcm(a,b): return a*b//gcd(a,b)
def census(pool, d):
    a,b = d
    ev=[]; lum=[]
    for q in pool:
        e,u,v = q['e'],q['u'],q['v']
        i = gcd((a*u+b*v)%e, e) if (a*u+b*v)%e else e
        w = F(i,e)
        (ev if i==1 else lum).append((q['p'],e,i,w))
    E = sum(w for _,_,_,w in ev)
    Lam = sum(F(1,e) for _,e,_,_ in lum)
    M = reduce(lcm,[i for _,_,i,_ in lum],1)
    return E,Lam,ev,lum,M
if __name__=='__main__':
    dirs=[(1,0),(0,1),(1,1),(1,-1),(2,1),(1,2),(2,-1),(1,-2),(3,1),(1,3),(3,-1),(1,-3),(3,2),(2,3),(3,-2),(2,-3)]
    for f in sorted(glob.glob('pool_*.json'), key=lambda s:int(s[5:-5])):
        d=json.load(open(f)); N=d['N']; pool=d['pool']
        print(f"N={N} primes={len(pool)} density={float(d['density']):.6f}")
        for dd in dirs:
            E,Lam,ev,lum,M = census(pool,dd)
            print(f"  dir={dd}: E={float(E):.4f} Lam={float(Lam):.4f} E+Lam={float(E+Lam):.4f} lumpy={len(lum)} M={M} maxi={max([i for _,_,i,_ in lum],default=1)} maxw={float(max([w for *_,w in lum],default=0)):.4f}")
