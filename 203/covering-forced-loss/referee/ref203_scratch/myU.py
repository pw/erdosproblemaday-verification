import numpy as np, itertools, json
from math import lcm, gcd
from fractions import Fraction as F
from sympy import n_order, primerange
def char(p):
    # generator h of <2,3> mod p from scratch; discrete logs of 2 and 3
    o2,o3=n_order(2,p),n_order(3,p); e=lcm(o2,o3)
    H=set(); x=1
    # build group <2,3>
    H={1}; fr=[1]
    while fr:
        y=fr.pop()
        for g in (2,3):
            z=y*g%p
            if z not in H: H.add(z); fr.append(z)
    assert len(H)==e
    for h in sorted(H):
        if n_order(h,p)==e: break
    lg={}; t=1
    for i in range(e): lg[t]=i; t=t*h%p
    return e,lg[2%p],lg[3%p],h
for p in (5,7,11,13,17,19,31):
    print(p,char(p))
# p=13 by hand: 2 has order 12 => h=2, u=1; 2^4=16=3 => v=4
assert pow(2,4,13)==3 and n_order(2,13)==12
def maxU(ps, fix_first=False):
    ch=[char(p)[:3] for p in ps]; T=1
    for e,_,_ in ch: T=lcm(T,e)
    k,l=np.meshgrid(np.arange(T),np.arange(T),indexing="ij")
    masks=[np.stack([((u*k+v*l)%e==c).reshape(-1) for c in range(e)]) for e,u,v in ch]
    masks=[np.packbits(m,axis=1) for m in masks]
    # enumerate all but last prime, vectorize over last
    best=-1; nb=0
    rngs=[range(1)] if fix_first else [range(ch[0][0])]
    rngs+= [range(e) for e,_,_ in ch[1:-1]]
    pc=np.array([bin(i).count("1") for i in range(256)],dtype=np.int64)
    last=masks[-1]
    for cs in itertools.product(*rngs):
        acc=np.zeros(masks[0].shape[1],dtype=np.uint8)
        for i,c in enumerate(cs): acc|=masks[i][c]
        tot=pc[(acc[None,:]|last)].sum(axis=1)
        m=tot.max()
        if m>best: best=m; nb=int((tot==m).sum())
        elif m==best: nb+=int((tot==m).sum())
    s=sum(F(1,e) for e,_,_ in ch)
    return T, best, F(int(best),T*T), float(s-F(int(best),T*T)), nb
print("U{5,7}",maxU([5,7]))
print("U{5,7,11,13} full enumeration (no translation trick):",maxU([5,7,11,13]))
print("U{5,7,11,13,17} c5 fixed:",maxU([5,7,11,13,17],fix_first=True))
