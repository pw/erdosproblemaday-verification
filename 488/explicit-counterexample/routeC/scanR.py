import numpy as np, sys
from sympy import primerange
ps=list(primerange(2,2040))
lnp=np.log(np.array(ps,dtype=np.longdouble))
best=[]
for R in range(1000000,1300001):
    x=R*lnp; e=np.abs(x-np.rint(x))/x
    best.append((float(e.max()),R))
best.sort()
print(best[:8])
# naive R=1e6
x=1e6*lnp; print(float((np.abs(x-np.rint(x))/x).max()))
