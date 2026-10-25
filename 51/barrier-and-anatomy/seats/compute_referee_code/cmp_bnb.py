import sys, numpy as np, random
sys.path.insert(0, sys.argv[1])
from bnb import ell
k=np.fromfile('/tmp/refc51/c4e7/knap_ell.bin',dtype=np.uint32)
random.seed(7)
As=list(range(2,20001,2))+random.sample(range(20002,40000001,2),300)
mis=0
for a in As:
    n,_=ell(a); kn=int(k[a>>1]) or None
    if n!=kn: mis+=1
    if mis and mis<=3 and n!=kn: print('  mismatch a=%d bnb=%s knap=%s'%(a,n,kn))
# odd a and a=1
for a in [1,3,5,7,99]:
    n,_=ell(a)
    if n!=(1 if a==1 else None): mis+=1; print('  odd mismatch',a,n)
print(sys.argv[1].split('/')[-1] or 'baseline','| per-a vs knap on',len(As)+5,'values: mismatches',mis,'->','CAUGHT' if mis else 'passes')
