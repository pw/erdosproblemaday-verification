import numpy as np
from math import lcm, prod
from sympy import n_order
D="/home/exedev/MathDyad/erdos203/"
def load(f): return [tuple(map(int,l.split())) for l in open(D+f) if l.strip()]
for f,w in (("S6.txt",[0,1,1,0,0,1]),("S7.txt",[0,1,1,0,0,1,0])):
    rows=load(f); T=1
    for e,_,_ in rows: T=lcm(T,e)
    k,l=np.meshgrid(np.arange(T),np.arange(T),indexing="ij")
    U=np.zeros((T,T),bool)
    for (e,u,v),c in zip(rows,w): U|=((u*k+v*l)%e==c)
    print(f,"T",T,"witness covers",U.sum(),"of",T*T)
# index of the joint kernel (size of <2,3> mod prod S)
for S in ([5,7],[5,7,11,13],[5,7,11,13,17],[5,7,11,13,17,19],[5,7,11,13,17,19,31]):
    n=prod(S); H={1}; fr=[1]
    while fr:
        y=fr.pop()
        for g in (2,3):
            z=y*g%n
            if z not in H: H.add(z); fr.append(z)
    print(S,"e_S =",len(H))
