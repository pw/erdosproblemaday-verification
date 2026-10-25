# Exact small-case experiment for Lemma 4.2 (randomly signed product avoids a thin rectangle).
# For every sign vector sigma in {+,-}^r, decide exactly whether the rectangle
#   Q = { x in Z^2 : |x.e| <= R1p , |x cross e| <= W1p }   (true half-lengths R1p/|e|, W1p/|e|)
# contains a nonzero multiple of beta_sigma = prod pi_i^{sigma_i}, and if so record the witness line.
# Since area(Q) = 4 R1 W1 < 2 P = 2 covol(beta Z[i]), all lattice points of beta Z[i] in Q are collinear,
# so the shortest vector (after exact Lagrange reduction in the metric adapted to Q) decides badness.
import math, random, itertools, sys
from math import gcd, isqrt
random.seed(2026)

def isprime(n):
    if n<2: return False
    for q in range(2,isqrt(n)+1):
        if n%q==0: return False
    return True
def two_squares(p):
    for a in range(1,isqrt(p)+1):
        b2=p-a*a; b=isqrt(b2)
        if b*b==b2: return (a,b)
def gmul(x,y): return (x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0])
def gconj(x): return (x[0],-x[1])

def lagrange(b1,b2,Qf):
    # exact Lagrange/Gauss reduction for positive definite integer quadratic form Qf on Z^2
    def ip(u,v): return (Qf(tuple(a+b for a,b in zip(u,v)))-Qf(u)-Qf(v))  # = 2 B(u,v)
    if Qf(b1)>Qf(b2): b1,b2=b2,b1
    while True:
        n1=Qf(b1)
        # mu = round(B(b1,b2)/Q(b1)) = round(ip/(2 n1))
        num=ip(b1,b2); mu=(2*num+2*n1)//(4*n1) if n1 else 0  # round(num/(2n1))
        mu=round(num/(2*n1)) if abs(num)<2**52 else (num + n1)//(2*n1)
        b2=(b2[0]-mu*b1[0], b2[1]-mu*b1[1])
        if Qf(b2)<Qf(b1): b1,b2=b2,b1
        else: return b1,b2

def run(primes, factors, e, R1p, W1p, label):
    r=len(primes); P=math.prod(primes)
    e2=e[0]**2+e[1]**2
    R1=R1p/math.sqrt(e2); W1=W1p/math.sqrt(e2)
    bad={}; lines={}
    for mask in range(1<<r):
        beta=(1,0)
        for i in range(r):
            f=factors[i] if (mask>>i)&1 else gconj(factors[i])
            beta=gmul(beta,f)
        # u -> x = beta*u ; x.e = u.w1 ; x cross e = u.w2
        w1=gmul(gconj(beta),e)  # (A,B)
        A,B=w1
        def L1(u): return u[0]*A+u[1]*B
        def L2(u): return u[0]*B-u[1]*A
        Qf=lambda u: W1p*W1p*L1(u)**2 + R1p*R1p*L2(u)**2
        b1,b2=lagrange((1,0),(0,1),Qf)
        if abs(L1(b1))<=R1p and abs(L2(b1))<=W1p and b1!=(0,0):
            x=gmul(beta,b1)
            # sanity: check x really is in Q via direct dot/cross with e
            assert abs(x[0]*e[0]+x[1]*e[1])<=R1p and abs(x[0]*e[1]-x[1]*e[0])<=W1p
            g=gcd(x[0],x[1]); d=(x[0]//g,x[1]//g)
            if d[0]<0 or (d[0]==0 and d[1]<0): d=(-d[0],-d[1])
            bad[mask]=d; lines.setdefault(d,[]).append(mask)
            # also confirm b2-direction is outside (collinearity): any point with nonzero b2-coefficient
            # would need Q(...) >= det-based lower bound; checked implicitly by area argument
    nb=len(bad)
    # min Hamming distance between distinct line classes
    keys=list(lines)
    mind=None
    for i in range(len(keys)):
        for j in range(i+1,len(keys)):
            for a in lines[keys[i]]:
                for b in lines[keys[j]]:
                    h=bin(a^b).count('1')
                    mind=h if mind is None else min(mind,h)
    return nb, len(lines), mind, R1, W1

T=220
primes=[p for p in range(T,2*T+1) if isprime(p) and p%4==1][:16]
r=len(primes); P=math.prod(primes)
factors=[two_squares(p) for p in primes]
d=0.249
print(f"T={T}, r={r}, primes={primes}")
print(f"log P={math.log(P):.2f}; d={d}; d*r/4={d*r/4:.3f}; collinearity margin d*r*(logT-0.25log2T)-log2 = {d*r*(math.log(T)-0.25*math.log(2*T))-math.log(2):.2f} (>0 required)")
lim=P**(1-d)
# (a) random orientations, W1 = 1 and moderate widths
for trial in range(6):
    e=(random.randint(1,50),random.randint(-50,50))
    en=math.sqrt(e[0]**2+e[1]**2)
    W1=[1,3,30,1000,1,1][trial]
    R1=lim/W1
    nb,nl,mind,R1r,W1r=run(primes,factors,e,int(R1*en),int(W1*en),"rand")
    print(f"random dir e={e}: R1={R1r:.3e} (sqrt P={math.sqrt(P):.3e}), W1={W1r:.2f}: bad sign vectors {nb}/{1<<r}, lines {nl}, min inter-class Hamming {mind}")
# (b) dangerous directions: e = product of '+' factors over the first m primes; R1 chosen as large as allowed
for m in [6,7,8,9,10]:
    e=(1,0)
    for i in range(m): e=gmul(e,factors[i])
    g=gcd(e[0],e[1]); e=(e[0]//g,e[1]//g)
    en=math.sqrt(e[0]**2+e[1]**2)
    R1=lim; W1=1.0
    nb,nl,mind,R1r,W1r=run(primes,factors,e,int(R1*en),int(W1*en),"danger")
    print(f"dangerous dir (m={m}): bad {nb}/{1<<r} = 2^{math.log2(nb/(1<<r)) if nb else float('-inf'):.2f}, lines {nl}, min inter-class Hamming {mind};  2dr*log(2T)/logT={2*d*r*math.log(2*T)/math.log(T):.2f}")
