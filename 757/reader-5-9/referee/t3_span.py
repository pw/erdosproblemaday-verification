from fractions import Fraction as F
import itertools
O=(0,49,75,83,98,101,117,119,121,159,269); Oi=[x for x in O if x not in (0,269)]
r=F(18,269); L=F(27169,251)
assert L==F(101*269,251) and 101+r*L==L
z=lambda x:251*x-27169
print('max|z| on O\\{0,269}:',max(abs(z(x)) for x in Oi),' z on 0,269:',z(0),z(269))
M=max(abs(z(x)) for x in Oi)
# two-level: d<=3 ?
for d in range(1,6): print('d',d,'3M r^d =',float(3*M*r**d), '>=1' if 3*M*r**d>=1 else '<1')
for g1 in range(1,6): print('g1',g1, float(r**g1*(M+2*M*r)), '>=1' if r**g1*(M+2*M*r)>=1 else '<1')
for g1 in range(1,4):
    gs=[g2 for g2 in range(1,12) if r**g2*2*M>=F(1,18**g1)]
    print('g1',g1,'admissible g2 <=',max(gs))
# pairs at one level: eps1 z1 + eps2 z2 == 0 for distinct x, eps in {±1,±2}, over all of O (covers level 0 too)
bad=[(a,b,e1,e2) for a,b in itertools.permutations(O,2) for e1 in (1,-1,2,-2) for e2 in (1,-1,2,-2) if e1*z(a)+e2*z(b)==0]
print('two-point zero groups:',bad)
# top single point: 269 | x or 269 | 2x for x in Oi?
print('single top:',[x for x in Oi if x%269==0 or (2*x)%269==0])
