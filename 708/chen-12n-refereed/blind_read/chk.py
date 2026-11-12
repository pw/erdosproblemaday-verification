import json,sys
from math import prod, isqrt
def isprime(n):
    if n<2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%p==0: return n==p
    d=n-1;s=0
    while d%2==0: d//=2;s+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True
d=json.load(open(sys.argv[1]))
for c in d:
    t=c['t'];w=c['w'];qu=c['q_u'];qv=c['q_v'];m=c['m']
    primes=w+[qu,qv]
    assert all(isprime(p) for p in primes) and primes==sorted(primes) and len(set(primes))==len(primes)
    # consecutive? check whether w are consecutive primes
    consec = all(not any(isprime(z) for z in range(w[i]+1,w[i+1])) for i in range(t-1))
    assert m==w[-1]*qv
    P1 = m < 2*w[0]*w[1]; P2 = qu*qu >= m+qu
    u=int(c['u']); x=int(c['x']); Pi=prod(primes)
    assert u%Pi==0 and int(c['k'])*Pi==u
    I=range(x+1,x+m+1)
    assert u in I and u-x-1==m//2
    A=sorted(w[i]*q for i in range(t) for q in (qu,qv)); assert A==sorted(c['A']) and max(A)==m and len(set(A))==2*t
    two=[b for b in I if sum(1 for p in primes if b%p==0)>=2]
    sq=[b for b in I if b%(qu*qu)==0 or b%(qv*qv)==0]
    vu=all((u//p)%p!=0 for p in primes)
    W=[int(z) for z in c['witness']]; Wp=[int(z) for z in c['witness_plus']]
    ok1 = len(set(W))==len(W)==c['min_B'] and all(b in I for b in W) and prod(W)%prod(A)==0
    Ap=sorted(A+[qu]); assert Ap==sorted(c['A_plus'])
    ok2 = len(set(Wp))==len(Wp)==c['min_B_plus'] and all(b in I for b in Wp) and prod(Wp)%prod(Ap)==0
    print(t, w[0],w[-1], len(w), qu,qv, m, 'consec_w',consec, 'P1',P1,'P2',P2, 'two',two==[u], 'sq',sq==[], 'v1',vu, 'x>=0',x>=0, 'min',c['min_B'],c['min_B_plus'], 'exp',3*t-1,3*t, 'wit',ok1,ok2, 'digits',len(str(x+1)))
