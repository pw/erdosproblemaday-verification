import json, sys
from math import gcd
from fractions import Fraction as F
import numpy as np
from sympy import n_order
D='/home/exedev/MathDyad/erdos203'
N=int(sys.argv[1]); a,b=1,1; Mp=60
pool=json.load(open(f'{D}/pool_{N}.json'))['pool']
E=F(0); lum=[]
for q in pool:
    p=q['p']; o2,o3=n_order(2,p),n_order(3,p); e=o2*o3//gcd(o2,o3)
    o=n_order(pow(2,a,p)*pow(3,b,p)%p,p); i=gcd(e//o,Mp)
    if i==1: E+=F(1,e)
    else: lum.append((p,i,F(i,e),e))
lum.sort(key=lambda x:(-x[2],-x[1]))
print('N',N,'E =',E,float(E),' need lumpy mass >= 1-E =',float(1-E))
print('lumpy primes (p, i=gcd(e/ord(6),60), w=i/e):',[(p,i,str(w)) for p,i,w,e in lum[:8]],'...',len(lum),'total')
from collections import defaultdict
byi=defaultdict(F)
for p,i,w,e in lum: byi[i]+=w
print('lumpy weight by i:',{i:float(v) for i,v in sorted(byi.items())})
tau=np.arange(Mp)
def explain(fixed):
    # fixed: list of (j, c); compute W over lumpy, then the best k-lowest bound
    W=np.zeros(Mp,dtype=object)
    for j,c in fixed: W[tau%lum[j][1]==c]+=lum[j][2]
    order=sorted(range(Mp),key=lambda t:(W[t],t))
    best=None
    for k in range(1,Mp+1):
        T=order[:k]
        tot=sum(W[t] for t in T)
        for jj in range(len(fixed),len(lum)):
            i=lum[jj][1]; cnt=max(sum(1 for t in T if t%i==c) for c in range(i)); tot+=lum[jj][2]*cnt
        slack=F(tot,k)-(1-E)
        if best is None or slack<best[0]: best=(slack,k,sorted(T)[:12])
    return best
# depth-1 / depth-2 tree
j0=lum[0]
print('root bound:',explain([])[:2])
for c0 in range(j0[1]):
    r=explain([(0,c0)])
    print(f' prime {j0[0]} (i={j0[1]}) class {c0}: best avg-bound slack {float(r[0]):+.4f} with k={r[1]} lowest cells {r[2]}')
    if r[0]>=0:
        j1=lum[1]
        for c1 in range(j1[1]):
            r1=explain([(0,c0),(1,c1)])
            print(f'    prime {j1[0]} (i={j1[1]}) class {c1}: slack {float(r1[0]):+.4f} k={r1[1]} cells {r1[2]}')
