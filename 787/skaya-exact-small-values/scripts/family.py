import sys; sys.path.insert(0,'/tmp/e1125/787work')
from mis import *
A43=[-42,-26,-24,-22,-20,-18,-16,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,18,20,22,24,26,42]
F=A43
for d in range(7):
    k=d+6
    al,B=alpha_cpsat(F)
    s1,_=has_indep(F,k); s2,_=has_indep(F,k+1)
    full_interval=all(x in set(F) for x in range(-(2*k+2),2*k+3))
    print(f"d={d} k={k} |F|={len(F)} k^2+3k-11={k*k+3*k-11} k^2+k+1={k*k+k+1} alpha_cpsat={al} sat(>=k)={s1} sat(>=k+1)={s2} contains[-(2k+2),2k+2]={full_interval} symmetric={sorted(F)==sorted(-x for x in F)}", flush=True)
    kn=k+1
    odds=[s*(2*j+1) for j in range(kn+1) for s in (1,-1)]
    F=sorted(set(odds+[2*x for x in F]))
    assert len(F)==len(odds)+ (len(F)-len(odds))
# negative control: perturb A43 by adding one element, alpha should rise or stay; remove clique cover element
import random
random.seed(5)
for t in range(5):
    A=list(A43); x=random.choice([y for y in range(-60,61) if y not in A]); A.append(x)
    print("A43+{%d}"%x, alpha_cpsat(A)[0])
