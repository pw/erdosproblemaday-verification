# Third instrument: the submitted spin file under Marinari-Parisi-Ritort's coupling (cond-mat/9410089 eq. 4,
# J(x,x+e_nu) = (-1)^{sum_{mu<nu} x_mu}, bit mu = (x>>mu)&1, spin '1' -> +1) reproduces the 1532-edge set,
# and its energy E = -(1/sqrt D) sum J s s / 2^D equals MPR's reported D=9 value -.494792 (-380 on their x768 scale).
from fractions import Fraction as F
import sys
n=9; N=1<<n
sp=open(sys.argv[1]).read().strip(); assert len(sp)==N and set(sp)<={'0','1'}
s=[1 if c=='1' else -1 for c in sp]
E=set(tuple(sorted(map(int,l.split()))) for l in open(sys.argv[2]) if l.strip())
P=set(); bond=0
for x in range(N):
    for nu in range(n):
        if x>>nu&1: continue
        y=x|1<<nu; J=(-1)**sum(x>>mu&1 for mu in range(nu)); v=J*s[x]*s[y]; bond+=v
        if v==1: P.add((x,y))
print('positive bonds',len(P),'equals edge file:',P==E)
e=F(-bond,3*N)   # sqrt(9)=3
print('sum J s s =',bond,' E per spin =',e,'=',float(e),' x768 =',e*768)
assert P==E and e*768==-380
