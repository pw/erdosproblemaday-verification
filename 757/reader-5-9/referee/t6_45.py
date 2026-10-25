# Literal (4,5) test: every 4-subset has >=5 distinct positive differences. Integer coords. Own code.
import sys, itertools, time; sys.path.insert(0,'/tmp/ref757')
from core import *
def bad(P):
    n=len(P); cnt=0; ex=None
    # fast: for each 4-set count distinct diffs
    for B in itertools.combinations(P,4):
        a,b,c,d=B
        D={b-a,c-a,d-a,c-b,d-b,d-c}
        if len(D)<5:
            cnt+=1; ex=ex or B
    return cnt,ex
# controls
assert bad([0,1,2,3])[0]==1 and bad([0,1,2,4])[0]==1 and bad([0,1,2,5])[0]==0 and bad([1,2,3,6])[0]==0 and bad([1,2,3,5])[0]==1
for K in range(int(sys.argv[1])+1):
    t=time.time(); sc=269**K; P=[int(x*sc) for x in SK(K)]
    print(K,len(P),'bad 4-sets:',bad(P),f'{time.time()-t:.0f}s',flush=True)
