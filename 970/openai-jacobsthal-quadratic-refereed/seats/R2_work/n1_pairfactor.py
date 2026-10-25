# N1: brute-force check of the pair factor (9.pair-factor) in Lemma 9.1, with a control.
import itertools, math
from fractions import Fraction as Fr
def primes(n):
    return [p for p in range(2,n+1) if all(p%q for q in range(2,int(p**.5)+1))]
def brute(ps, h):
    # independent uniform forbidden class at each prime; positions 0 and h
    # P(both survive) factorises over primes
    P=Fr(1)
    for t in ps:
        good=0
        for c in range(t):
            if 0%t!=c and h%t!=c: good+=1
        P*=Fr(good,t)
    return P
def formula(ps,h, variant=0):
    V0=Fr(1)
    for t in ps: V0*=Fr(t-1,t)
    f = Fr(2 if h%2==0 else 0)
    for t in ps:
        if t==2: continue
        f*= 1-Fr(1,(t-1)**2)
        if h%t==0:
            f*= 1+ (Fr(1,t-2) if variant==0 else Fr(1,t-1))
    return f*V0*V0
ps=primes(13)
ok=all(brute(ps,h)==formula(ps,h) for h in range(1,200))
bad=sum(brute(ps,h)!=formula(ps,h,1) for h in range(1,200))
print("formula exact for h<200, w=13:",ok,"| control (1/(t-1) instead of 1/(t-2)) mismatches:",bad,"of 199")
# exact check of the truncated identity prod_{2<t<=w}(1-1/(t-1)^2) * sum_{l|P(w) odd} lambda_l/l = 1
for w in [13,50,200]:
    ps=[t for t in primes(w) if t>2]
    lhs=Fr(1)
    for t in ps: lhs*= (1-Fr(1,(t-1)**2))*(1+Fr(1,t*(t-2)))
    lhs_ctrl=Fr(1)
    for t in ps: lhs_ctrl*= (1-Fr(1,(t-1)**2))*(1+Fr(1,t*(t-1)))
    print("w=%d identity value:"%w, lhs, "| control value:", float(lhs_ctrl))
