import sys
from math import gcd
from fractions import Fraction as F
from functools import reduce
sys.path.insert(0,'/home/exedev/MathDyad/erdos203/lines'); import linelemma as LL
part=[(6,3,1),(6,3,1),(6,3,1),(4,1,3),(12,1,7),(12,1,7),(12,1,7)]
pool=[{'p':'s%d'%j,'e':e,'u':u,'v':v} for j,(e,u,v) in enumerate(part)]
dirs=[(1,0),(0,1),(1,1),(1,-1),(2,1),(1,2),(2,-1),(1,-2),(3,1),(1,3),(3,-1),(1,-3),(3,2),(2,3),(3,-2),(2,-3),(5,-7)]
def make(kind):
    def inst(pool,d,Mp=None):
        a,b=d; E=F(0); lum=[]; ev=[]
        for q in pool:
            e,u,v=q['e'],q['u'],q['v']
            if kind=='swap_uv': u,v=v,u
            s=(a*u+b*v)%e
            if kind=='sign': s=(a*u-b*v)%e
            i=gcd(s,e) if s else e
            w=F(1,e) if kind=='w_1_over_e' else F(i,e)
            if i==1: E+=w; ev.append((q['p'],w))
            else: lum.append((q['p'],i,w))
        M=reduce(lambda x,y:x*y//gcd(x,y),[i for _,i,_ in lum],1)
        return E,lum,M,ev
    return inst
for kind in ('correct','swap_uv','w_1_over_e','sign'):
    inst=LL.instance if kind=='correct' else make(kind)
    wrong=[]
    for d in dirs:
        E,lum,M,ev=inst(pool,d,None); V=LL.brute(E,lum,M)[0]
        if V!=1: wrong.append((d,str(V)))
    print(f'{kind:12s}: directions with V != 1: {len(wrong)}  {wrong[:4]}')
