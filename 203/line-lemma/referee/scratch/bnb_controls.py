import json, sys, time
from math import gcd
from fractions import Fraction as F
import numpy as np
sys.path.insert(0,'/home/exedev/MathDyad/erdos203/lines'); import linelemma as LL
core=open('/tmp/ref203lines/bnb_core.py').read()
def run(E,lum,Mp,TL=120,sym=False,label=''):
    g={'E':E,'lum':[(p,i,w) for p,i,w in lum],'Mp':Mp,'TL':TL,'sym':sym,'np':np,'json':json,'time':time,'gcd':gcd,'F':F,'N':label,'a':0,'b':0}
    exec(core,g)
# control A: exact 2-D partition, every direction feasible
part=[(6,3,1),(6,3,1),(6,3,1),(4,1,3),(12,1,7),(12,1,7),(12,1,7)]
pool=[{'p':'s%d'%j,'e':e,'u':u,'v':v} for j,(e,u,v) in enumerate(part)]
for d in [(1,1),(1,-1),(3,1),(1,-3),(5,-7)]:
    E,lum,M,ev=LL.instance(pool,d,None); run(E,lum,M,label='partition'+str(d))
# control B: same partition with B halved (no cover) -> infeasible
pool2=[dict(q) for q in pool]; pool2[3]={'p':'h','e':8,'u':1,'v':3}
for d in [(1,1),(1,-3)]:
    E,lum,M,ev=LL.instance(pool2,d,None); run(E,lum,M,label='halved'+str(d))
# control C: real pool 110880 direction (0,1): CP-SAT found V=23347/22176>=1 (witness recounted) -> must be FEASIBLE
P=json.load(open('/home/exedev/MathDyad/erdos203/pool_110880.json'))['pool']
E,lum,M,ev=LL.instance(P,(0,1),None); run(E,lum,M,TL=240,sym=True,label='110880(0,1)exact')
# and the 5040 pool dir (0,1) (V=529/630 <1) -> must be INFEASIBLE
P=json.load(open('/home/exedev/MathDyad/erdos203/pool_5040.json'))['pool']
E,lum,M,ev=LL.instance(P,(0,1),None); run(E,lum,M,label='5040(0,1)')
