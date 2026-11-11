import numpy as np
from sympy import primerange
for y in (61,251,401):
    lnp=np.log(np.array(list(primerange(2,y+1)),dtype=np.longdouble))
    best=[]
    for R in range(1000000,2000001):
        x=R*lnp; best.append((float((np.abs(x-np.rint(x))/x).max()),R))
    d=dict((r,e) for e,r in best); best.sort(); print(y,best[:3],'R=1e6:',d[1000000],flush=True)
