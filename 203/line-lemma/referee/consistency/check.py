import json, sys, math
from fractions import Fraction as F
from sympy.ntheory import n_order
from math import gcd
D='/home/exedev/MathDyad/erdos203/'
Ns=[5040,7920,10080,15120,15840,18480,20160,23760,25200,27720,30240,31680,35280,36960,39600,40320,41580,45360,46800,47520,50400,51480,55440,60480,63360,65520,110880,166320,221760,332640,720720]
def lcm(a,b): return a*b//gcd(a,b)
res={}
for N in Ns:
    d=json.load(open(D+f'pool_{N}.json'))
    pool=d['pool']
    ps=[int(x['p']) if isinstance(x,dict) else int(x) for x in pool]
    dens=F(0); B=F(0)
    S=[t for t in range(60) if t%4!=0 and t%3!=0]
    assert len(S)==30
    for p in ps:
        e=lcm(n_order(2,p),n_order(3,p)); assert N%e==0
        dens+=F(1,e)
        if p in (5,7):
            if p==5: assert e==4 and n_order(6,5)==1
            if p==7: assert e==6 and n_order(6,7)==2
            continue
        i=e//n_order(6,p); ip=gcd(i,60)
        mx=max(sum(1 for t in S if t%ip==c) for c in range(ip))
        B+=F(ip,e)*F(mx,30)
    res[N]=(len(ps),dens,B)
    print(N,len(ps),float(dens),B,round(float(B),4))
print('max B <=65520:',max((v[2],k) for k,v in res.items() if k<=65520))
print('second max:',sorted(((float(v[2]),k) for k,v in res.items() if k<=65520))[-2])
