import random, sympy as sp
import toy_invariant as T
random.seed(9)
A=[(0,0),(1,0),(2,0)]; lam=[1,-1,0]
q=sp.simplify(sum(l*sum(x*x for x in a) for l,a in zip(lam,A)))
fails=0
for _ in range(20):
    phi,w=T.path_phi(A,lam)
    if sp.simplify(phi-w*q)!=0: fails+=1
print("control lam=(1,-1,0) (not an affine dependency): identity FAILED on",fails,"/20")
