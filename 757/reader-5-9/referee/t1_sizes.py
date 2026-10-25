import sys; sys.path.insert(0,'/tmp/ref757')
from core import *
for K in list(range(0,15))+[30,60]:
    cs=copies(K); S=set().union(*cs)
    ok=len(S)==11+9*K
    # copy intersections
    bad=[]
    for i in range(K+1):
        for j in range(i+1,K+1):
            I=cs[i]&cs[j]
            if j==i+1:
                exp={phi(F(x)) if False else None for x in ()}
                # expected: phi^i(101), phi^i(119)
                p=F(101); q=F(119)
                for _ in range(i): p=phi(p); q=phi(q)
                if I!={p,q}: bad.append((i,j,len(I)))
            elif I: bad.append((i,j,len(I)))
    print(K,len(S),11+9*K,ok,'intersection anomalies:',bad[:3])
