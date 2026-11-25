"""Exactly re-certify every cached Farkas core from their k=6 run (learned_cores_m22.txt),
using MY certificate routine (cegar_pos.lp_cert/rationalize/check_cert), not theirs."""
import sys; sys.path.insert(0,'/tmp/e1125/787work')
from cegar_pos import lp_cert, rationalize, check_cert
m=int(sys.argv[2]); path=sys.argv[1]
trip=[(i,j,l) for i in range(m) for j in range(i+1,m) for l in range(j+1,m)]
idmap={1+3*t:tr for t,tr in enumerate(trip)}
n=bad=0; sizes={}
for line in open(path):
    lits=[int(x) for x in line.split()]
    if not lits: continue
    n+=1
    assert all(x<0 for x in lits)
    E=[idmap[-x] for x in lits]
    yf=lp_cert(m,E)
    ok=False
    if yf is not None:
        y=rationalize(yf); ok=check_cert(m,E,y)
    if not ok:
        bad+=1; print("NOT CERTIFIED:",E, flush=True)
    sizes[len(E)]=sizes.get(len(E),0)+1
print(f"cores audited={n} not_certified={bad} size_hist={sorted(sizes.items())}")
