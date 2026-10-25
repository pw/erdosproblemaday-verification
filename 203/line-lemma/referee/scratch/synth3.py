import json, sys
from math import gcd
from fractions import Fraction as F
sys.path.insert(0,'/home/exedev/MathDyad/erdos203/lines'); import linelemma as LL
T=24
part=[(6,3,1,0),(6,3,1,2),(6,3,1,4),(4,1,3,1),(12,1,7,3),(12,1,7,7),(12,1,7,11)]
for k in range(T):
    for l in range(T):
        n=sum((u*k+v*l)%e==c for e,u,v,c in part); assert n==1,(k,l,n)
print('exact partition verified on (Z/24)^2; density',sum(F(1,e) for e,*_ in part))
pool=[{'p':'s%d'%j,'e':e,'u':u,'v':v} for j,(e,u,v,c) in enumerate(part)]
dirs=[(1,0),(0,1),(1,1),(1,-1),(2,1),(1,2),(2,-1),(1,-2),(3,1),(1,3),(3,-1),(1,-3),(3,2),(2,3),(3,-2),(2,-3),(5,-7)]
bad=0
for d in dirs:
    E,lum,M,ev=LL.instance(pool,d,None)
    name,V,bd,t,wt=LL.cpsat(E,lum,M,30,2); br=LL.brute(E,lum,M)
    ok=(V==1 and bd==1 and br[0]==1); bad+=not ok
    print('  dir',d,'i',[i for _,i,_ in lum],'E',E,'V',V,'bound',bd,'brute',br[0],'' if ok else '<-- WRONG')
print('EXACT PARTITION: wrong directions',bad,'(prediction: V=1 exactly everywhere)')
# M2: halve B: {k+3l ≡ 1 mod 4} -> {k+3l ≡ 1 mod 8}
pool2=[dict(q) for q in pool]; pool2[3]={'p':'s3h','e':8,'u':1,'v':3}
bad2=0; mx=F(0)
for d in dirs:
    E,lum,M,ev=LL.instance(pool2,d,None)
    name,V,bd,t,wt=LL.cpsat(E,lum,M,30,2); br=LL.brute(E,lum,M)
    ok=(V<1 and V<=F(7,8) and br[0]==V and name=='OPTIMAL'); bad2+=not ok; mx=max(mx,V)
    print('  M2 dir',d,'V',V,'brute',br[0],'' if ok else '<-- PREDICTION FAILED')
print('M2: prediction failures',bad2,'max V',mx)
# M1: classical cover, 23(24) weight halved
pos=[{"p":"c%d"%i, "e":i, "u":1, "v":0} for i in (2,3,4,8,12)]+[{"p":"c24h","e":48,"u":1,"v":24}]
E,lum,M,ev=LL.instance(pos,(0,1),None)
name,V,bd,t,wt=LL.cpsat(E,lum,M,30,2); br=LL.brute(E,lum,M)
print('M1: weights',[str(w) for *_,w in lum],'V',V,'brute',br[0],'prediction 1/2 ->','PASS' if V==F(1,2)==br[0] else 'FAIL')
# M3: real pool 5040, dir (1,1): halve an everywhere prime by doubling e (s kept odd, coprime to 2e)
D='/home/exedev/MathDyad/erdos203'
P=json.load(open(f'{D}/pool_5040.json'))['pool']
E,lum,M,ev=LL.instance(P,(1,1),None)
name,V,bd,t,wt=LL.cpsat(E,lum,M,60,2)
# pick the everywhere prime with the largest weight (smallest e)
pe=min((q for q in P if (q['p'],F(1,q['e'])) in ev), key=lambda q:q['e'])
e=pe['e']; u,v=pe['u'],pe['v']
if (u+v)%2==0: u=u+e
assert gcd(u+v,2*e)==1
P3=[dict(q) for q in P]; P3[P.index(pe)]={'p':pe['p'],'e':2*e,'u':u,'v':v}
E3,lum3,M3,ev3=LL.instance(P3,(1,1),None)
name3,V3,bd3,t3,wt3=LL.cpsat(E3,lum3,M3,60,2)
print(f"M3: 5040 dir (1,1): prime {pe['p']} e {e} -> 2e; V {V} -> {V3}; predicted {V-F(1,2*e)} ->", 'PASS' if V3==V-F(1,2*e) and name3=='OPTIMAL' else 'FAIL')
