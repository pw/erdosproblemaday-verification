import json, sys
from math import gcd, log10
from fractions import Fraction as F
sys.path.insert(0,'/home/exedev/MathDyad/erdos203/lines'); import linelemma as LL
D='/home/exedev/MathDyad/erdos203'
for N in (110880,166320,221760,332640,720720):
    pool=json.load(open(f'{D}/pool_{N}.json'))['pool']
    print('N',N)
    for d in [(1,1)]:
        for Mp in (60,120,180,240,360,420,720,840,1260,1680,2520,3960,5040,9240,13860,27720,None):
            E,lum,M,ev=LL.instance(pool,d,Mp)
            prod=1
            for _,i,_ in lum: prod*=i
            lumpy_mass=sum(w for *_,w in lum)
            print(f'   dir {d} Mp {Mp}: E={float(E):.4f} lumpy={len(lum)} M={M} log10 prod_i={log10(prod):.1f} max possible W=E+sum w={float(E+lumpy_mass):.3f}')
