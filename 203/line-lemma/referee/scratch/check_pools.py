import json, sys, glob, os
from math import gcd, lcm
from sympy import isprime, n_order
from sympy import gcdex as _g
def igcdex(a,b):
    x,y,g=_g(a,b); return int(x),int(y),int(g)
D='/home/exedev/MathDyad/erdos203'
def ext3(u,v,e):
    # find alpha,beta,gamma with alpha*u+beta*v+gamma*e = 1
    x1,y1,g1 = igcdex(u,v)      # x1*u+y1*v = g1
    x2,y2,g2 = igcdex(g1,e)     # x2*g1+y2*e = g2
    assert g2==1, (u,v,e)
    return x1*x2, y1*x2
bad=0
Ns=[int(os.path.basename(f)[5:-5]) for f in glob.glob(D+'/pool_*.json')]
for N in sorted(Ns):
    d=json.load(open(f'{D}/pool_{N}.json')); pool=d['pool']
    nb=0
    for q in pool:
        p,e,u,v=q['p'],q['e'],q['u'],q['v']
        o2,o3=n_order(2,p),n_order(3,p)
        ok = isprime(p) and p>=5 and o2==q['ord2'] and o3==q['ord3'] and lcm(o2,o3)==e and N%e==0 and 0<=u<e and 0<=v<e
        if ok:
            a,b=ext3(u,v,e)
            h=(pow(2,a,p)*pow(3,b,p))%p
            ok = pow(h,u,p)==2%p and pow(h,v,p)==3%p and n_order(h,p)==e
        if not ok: nb+=1; print('BAD',N,q)
    # completeness
    import time; t=time.time()
    G=gcd(2**N-1,3**N-1); R=G
    for q in pool:
        while R%q['p']==0: R//=q['p']
    dens=sum(__import__('fractions').Fraction(1,q['e']) for q in pool)
    print(f"N={N}: {len(pool)} primes, char/order errors {nb}, residual after dividing pool out of G_N: {R} ({'COMPLETE' if R==1 else 'INCOMPLETE'}), density {float(dens):.6f} (json {d['density']:.6f}) [{time.time()-t:.1f}s]", flush=True)
    bad+=nb+(R!=1)
print('TOTAL BAD',bad)
