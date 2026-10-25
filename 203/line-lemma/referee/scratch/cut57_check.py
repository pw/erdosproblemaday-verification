import json, sys
from fractions import Fraction as F
sys.path.insert(0,'/home/exedev/MathDyad/erdos203/lines'); import linelemma as LL
D='/home/exedev/MathDyad/erdos203'
T=[t for t in range(60) if t%4!=0 and t%3!=0]
def B_from_LL(pool):
    E,lum,M,ev=LL.instance(pool,(1,1),60)
    # sanity: 5 and 7 lumps
    d={p:(i,w) for p,i,w in lum}; assert d[5]==(4,F(1)) and d[7]==(3,F(1,2))
    B=E
    for p,i,w in lum:
        if p in (5,7): continue
        B+=w*F(max(sum(1 for t in T if t%i==c) for c in range(i)),30)
    return B,E,lum,M
for N in (5040,25200,55440,65520,110880,720720):
    pool=json.load(open(f'{D}/pool_{N}.json'))['pool']
    B,E,lum,M=B_from_LL(pool)
    # exact coarse optimum at Mp=60 (CP-SAT) must be <= B
    name,V,bd,t,wt=LL.cpsat(E,lum,M,120,2)
    # direct check of the cut on the optimal witness: shift so c5=c7=0 and evaluate avg over T
    print(f'N={N}: B via (u,v) instance = {float(B):.6f} [{B}]  exact V(Mp=60) = {float(V):.6f} ({name})  V<=B: {V<=B}')
