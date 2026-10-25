# Itabe sec.7 factor: n=r+p(w+pu), colour (tau(r),tau(w),N(r,w,u)); check on CYCLIC Z/p^3Z.
import sys, numpy as np
sys.path.insert(0,'/tmp/erdos160/seats/B_work/scripts')
from check_k4_cyclic import irreducible_cubic, power, count_violations
for p in [int(x) for x in sys.argv[1:]]:
    a,b=irreducible_cubic(p); M=p**3; C=np.zeros(M,dtype=np.int64)
    for n in range(M):
        r=n%p; w=(n//p)%p; u=n//p**2
        Nv=power((r,w,u),1+p+p*p,p,a,b)[0]
        C[n]=(((3*r)//p)*3+(3*w)//p)*p+Nv
    bad,ex=count_violations(M,C)
    print(f"Itabe-cyclic p={p} M={M} colours={len(set(C.tolist()))} (9p={9*p}) violations={bad} ex={ex}",flush=True)
