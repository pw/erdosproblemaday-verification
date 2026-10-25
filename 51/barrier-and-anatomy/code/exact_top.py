import numpy as np
from fractions import Fraction
from bnb import ell
R=np.load('R23.npy')
pts=[(int(x),int(y)) for x,y in zip(*np.nonzero(~np.isnan(R))) if y>=1 and R[x,y]>1.99]
worst=None
for x,y in sorted(pts):
    a=2**x*3**y
    n,cov=ell(a,{2:x,3:y} if x else {3:y})
    r=Fraction(n,a)
    if worst is None or r>worst[0]: worst=(r,x,y,cov)
    print(x,y,float(r-2),cov)
r,x,y,cov=worst
print('MAX exact R-2 over these:',float(r-2),'at',(x,y),cov)
