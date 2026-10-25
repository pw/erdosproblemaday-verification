import itertools
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153
bad=0
for m in range(1,10):
    for k in range(0,m+1):
        lits=list(range(1,m+1))
        enc=CardEnc.equals(lits=lits,bound=k,top_id=m+5,encoding=EncType.seqcounter)
        with Cadical153(bootstrap_with=enc.clauses) as s:
            for bits in range(1<<m):
                a=[i+1 if bits>>i&1 else -(i+1) for i in range(m)]
                if s.solve(assumptions=a)!=(bin(bits).count('1')==k): bad+=1
print("bad",bad)
