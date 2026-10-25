# Referee's own PG(2,q), q prime. Points/lines = normalized vectors (first nonzero coord = 1).
import itertools
def norm(v,q):
    for c in v:
        if c%q:
            inv=pow(c,q-2,q); return tuple((a*inv)%q for a in v)
    return None
def plane(q):
    pts=sorted({norm(v,q) for v in itertools.product(range(q),repeat=3) if any(v)})
    assert len(pts)==q*q+q+1
    lines={L:frozenset(p for p in pts if (L[0]*p[0]+L[1]*p[1]+L[2]*p[2])%q==0) for p in pts for L in [p]}
    for L,s in lines.items(): assert len(s)==q+1
    return pts,lines
