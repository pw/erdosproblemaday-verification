# Reader-submission (7bkzb8) construction for Erdős #757: S_K = O ∪ φ(O) ∪ … ∪ φ^K(O), φ(x)=101+18x/269, scaled to integers.
from fractions import Fraction as F
O=[0,49,75,83,98,101,117,119,121,159,269]
def phi(x): return F(101)+F(18)*x/269
def S(K):
    pts=set(F(x) for x in O); cur=[F(x) for x in O]
    for k in range(K):
        cur=[phi(x) for x in cur]; pts|=set(cur)
    sc=269**K
    out=sorted(int(x*sc) for x in pts)
    assert all((x*sc).denominator==1 for x in pts)
    return out
if __name__=='__main__':
    for K in range(0,9): s=S(K); print(K,len(s), 11+9*K)
