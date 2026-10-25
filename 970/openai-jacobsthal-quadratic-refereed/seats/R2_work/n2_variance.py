# N2: Lemma 9.1 -- exact relative variance E(S-JV0)^2/(JV0)^2 in the independent forbidden-class model,
# computed from the exact pair factor (9.12) (verified by N1). Shows decay for J = w^delta, and a control:
# fixed J (outside the hypothesis J >= w^delta) where it does NOT tend to 0.
import math, sys
def primes(n):
    s=bytearray([1])*(n+1); s[0:2]=b'\x00\x00'
    for i in range(2,int(n**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]
def relvar(w,J):
    ps=primes(w); V0=1.0
    for t in ps: V0*=1-1/t
    odd=[t for t in ps if t>2]
    c=1.0
    for t in odd: c*=1-1/(t-1)**2
    # G(h) = pair prob / V0^2
    off=0.0
    for h in range(1,J):
        if h%2: G=0.0
        else:
            G=2*c
            for t in odd:
                if h%t==0: G*=1+1/(t-2)
        off+=2*(J-h)*(G-1)
    var=J*V0*(1-V0)+V0*V0*off
    return var/(J*V0)**2, J*V0
print("delta=1.5:  w, J, JV0, relvar")
for w in [11,23,47,97,199,401,797]:
    J=int(w**1.5); r,m=relvar(w,J); print(w,J,round(m,2),round(r,5))
print("delta=1.0:")
for w in [11,23,47,97,199,401,797,1601]:
    J=w; r,m=relvar(w,J); print(w,J,round(m,2),round(r,5))
print("CONTROL fixed J=12 (violates J>=w^delta uniformly):")
for w in [11,23,47,97,199,401,797]:
    r,m=relvar(w,12); print(w,12,round(m,3),round(r,4))
