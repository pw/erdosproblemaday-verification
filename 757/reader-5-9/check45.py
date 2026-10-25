# Literal (4,5)-check: every 4-subset B has |B-B| >= 11 (i.e. >= 5 distinct positive differences).
import sys, itertools
from build import S
def bad4(s):
    bad=[]
    n=len(s)
    for B in itertools.combinations(s,4):
        D={x-y for x in B for y in B}
        if len(D)<11: bad.append(B)
    return bad
if __name__=='__main__':
    Kmax=int(sys.argv[1])
    # negative control: a 4-term AP has |B-B| = 7 and must be flagged
    assert bad4([0,1,2,3])==[(0,1,2,3)]
    assert bad4([0,1,3,7])==[]   # Sidon 4-set: |B-B|=13
    assert bad4([0,1,2,5])==[]   # one coincidence (0,1,2 AP): |B-B|=11, allowed
    assert bad4([0,1,2,4])!=[]   # 0,1,2 AP and 0,2,4 AP: two coincidences -> flagged
    for K in range(Kmax+1):
        s=S(K); b=bad4(s); print(K,len(s),'bad4=',len(b), b[:3], flush=True)
