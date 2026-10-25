# One-shot bound, direction (1,1), cells tau mod 60: fix c5=c7=0 (translation: Z/12 = Z/4 x Z/3 acts transitively on (c5,c7)).
# T = {tau mod 60 : tau !≡ 0 (4), tau !≡ 0 (3)}, |T| = 30.  Some cell of T has W <= avg_T W <= B where
# B = E + sum_{p != 5,7} w'_p * max_c |T ∩ {tau ≡ c mod i'_p}| / |T|.   B < 1  =>  no covering.
import json, glob, os
from math import gcd
from fractions import Fraction as F
from sympy import n_order
D='/home/exedev/MathDyad/erdos203'
T=[t for t in range(60) if t%4!=0 and t%3!=0]; assert len(T)==30
res=[]
for f in glob.glob(D+'/pool_*.json'):
    N=int(os.path.basename(f)[5:-5]); pool=json.load(open(f))['pool']
    ps={q['p'] for q in pool}
    if not {5,7}<=ps: res.append((N,None,'no 5 or 7')); continue
    B=F(0); dens=F(0)
    for q in pool:
        p=q['p']; o2,o3=n_order(2,p),n_order(3,p); e=o2*o3//gcd(o2,o3); dens+=F(1,e)
        o=n_order(6%p,p); i=gcd(e//o,60); w=F(i,e)
        if p==5: assert (i,w)==(4,1)
        if p==7: assert (i,w)==(3,F(1,2))
        if p in (5,7): continue
        cnt=max(sum(1 for t in T if t%i==c) for c in range(i))
        B+=w*F(cnt,30)
    res.append((N,B,dens))
for N,B,d in sorted(res):
    if B is None: print(N,d); continue
    print(f'N={N:>6}  density {float(d):.4f}   B_(1,1),5-7 cut = {float(B):.4f}  {"< 1  EXCLUDED" if B<1 else ">= 1"}')
