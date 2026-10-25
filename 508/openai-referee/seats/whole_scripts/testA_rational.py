# Test (A): the rational analogue of Theorem 2.3 / Prop 4.2 is FALSE, and the
# F(i)-specific inputs the proof uses fail over Q(i).  Exact arithmetic only.
from fractions import Fraction as Fr
from math import gcd, isqrt
import itertools, random
random.seed(1)

def factor(n):
    f=[];p=2
    while p*p<=n:
        while n%p==0: f.append(p); n//=p
        p+=1
    if n>1: f.append(n)
    return f

# (1) all rational unit vectors (a+bi)/c with c <= N: primitive triples + axes
N=3000
units=set([(Fr(1),Fr(0)),(Fr(-1),Fr(0)),(Fr(0),Fr(1)),(Fr(0),Fr(-1))])
bad_c_even=bad_parity=bad_prime=0
for m in range(2,isqrt(N)+2):
    for n in range(1,m):
        if (m-n)%2==0 or gcd(m,n)!=1: continue
        a,b,c=m*m-n*n,2*m*n,m*m+n*n
        if c>N: continue
        if c%2==0: bad_c_even+=1
        if (a+b)%2==0: bad_parity+=1
        if any(p%4!=1 for p in factor(c)): bad_prime+=1
        for x,y in ((a,b),(b,a)):
            for sx in (1,-1):
                for sy in (1,-1):
                    units.add((Fr(sx*x,c),Fr(sy*y,c)))
for (x,y) in units: assert x*x+y*y==1
print("rational units with denominator <=",N,":",len(units))
print("  even denominators:",bad_c_even,"| a+b even:",bad_parity,"| denominator with a prime !=1 mod 4:",bad_prime)

def odd_den(q): return q.denominator%2==1
def par(z):                      # parity map pi on Z_(2)[i]:  (x+y) mod 2
    x,y=z; s=x+y; assert odd_den(s); return s.numerator%2
assert all(par(u)==1 for u in units)     # chi(u) = (-1)^pi(u) = -1 for EVERY rational unit
print("  pi(u)=1 (chi(u)=-1) for all", len(units), "units: OK")

def mul(z,w): return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])
def add(z,w): return (z[0]+w[0], z[1]+w[1])
def rnd():
    d=random.choice([1,3,5,7,9,15,21,25,27,35,45,63,99,125])
    return (Fr(random.randint(-500,500),d),Fr(random.randint(-500,500),d))
U=list(units)
ok_add=ok_rot=0
for _ in range(20000):
    z,w=rnd(),rnd(); u=random.choice(U)
    ok_add += par(add(z,w))==(par(z)+par(w))%2
    ok_rot += par(mul(u,z))==par(z)
print("  homomorphism pi(z+w)=pi(z)+pi(w):",ok_add,"/20000 ; rotation invariance pi(uz)=pi(z):",ok_rot,"/20000")

# (1b) independent sanity check: every integer relation sum n_u u = 0 among a few small
# rational units has EVEN coefficient sum (forced if chi exists)
small=sorted(U,key=lambda z:(max(z[0].denominator,z[1].denominator),z))[:7]
rels=odd=0
for coeffs in itertools.product(range(-2,3),repeat=len(small)):
    if not any(coeffs): continue
    s=(Fr(0),Fr(0))
    for n,u in zip(coeffs,small): s=(s[0]+n*u[0],s[1]+n*u[1])
    if s==(0,0):
        rels+=1; odd += sum(coeffs)%2
print("  relations among 7 smallest units, coeffs in [-2,2]:",rels,"found; with ODD coefficient sum:",odd)

# CONTROL that must FAIL: the same assignment on algebraic units.  Q(sqrt-3) elements as
# a+b*w with w^2=-1-w.  1+w+w^2 = 0 with three unit vectors and coefficient sum 3 (odd):
def emul(p,q):  # (a+bw)(c+dw), w^2 = -1 - w
    a,b=p;c,d=q; return (a*c-b*d, a*d+b*c-b*d)
one=(1,0); w=(0,1); w2=emul(w,w)
tot=(one[0]+w[0]+w2[0], one[1]+w[1]+w2[1])
norm=lambda p: p[0]*p[0]-p[0]*p[1]+p[1]*p[1]          # |a+bw|^2
print("CONTROL (algebraic K): 1+w+w^2 =",tot,"; norms",norm(one),norm(w),norm(w2),
      "; coefficient sum 3 is odd -> a character d with d(u)=-1 on all of K would give d(0)=(-1)^3=-1, but d(0)=1: the set S is EMPTY over F(i)")
assert tot==(0,0) and norm(w)==1 and norm(w2)==1

# (2) Z-span of K: over Q(i) every denominator is a product of primes = 1 mod 4, so 1/3 is
# NOT in span_Z(K_Q) (span is a proper K_Q-invariant subgroup -> Haar on its annihilator is a
# wild, K_Q-invariant, non-Haar law).  Over F(i): u=(1+2*sqrt2 i)/3 is in K and 1/3 = 1-(u+conj u).
print("(2) over F(i): |(1+2sqrt2 i)/3|^2 =", Fr(1,9)+Fr(8,9), "; 1-(u+conj u) =", 1-Fr(2,3))

# (3) Lemma 2.7's k_j step / Sec 3.5's t+i*sqrt(1-t^2): x in Q is a sum of two rational
# units iff 1-x^2/4 is a rational square.
def is_sq(q):
    if q<0: return False
    a,b=q.numerator,q.denominator; return isqrt(a)**2==a and isqrt(b)**2==b
cand=sorted({Fr(p,q) for q in range(1,61) for p in range(1,2*q)})
rep=[x for x in cand if is_sq(1-x*x/4)]
print("(3) x=p/q in (0,2), q<=60:",len(cand),"values; sums of two rational units:",len(rep),
      "e.g.",[str(x) for x in rep[:6]])
trip=[t for t in {Fr(p,q) for q in range(1,401) for p in range(1,q)}
      if all(is_sq(1-(j*t)**2/4) for j in (1,2,3))]
print("    positive control: 6/5 = 2Re((3+4i)/5) detected:", Fr(6,5) in rep, "| negative control 1 (needs sqrt3/2):", Fr(1) in rep)
print("    t=p/q in (0,1), q<=400 with t,2t,3t ALL sums of two rational units:",len(trip))
print("    over F (real algebraic): every |x|<2 qualifies (sqrt(1-x^2/4) in F)")

# (4) square map not onto K_Q: (3+4i)/5 = ((2+i)/sqrt5)^2, and no enumerated rational unit squares to it
target=(Fr(3,5),Fr(4,5))
print("(4) rational units u (den<=%d) with u^2=(3+4i)/5:"%N, sum(mul(u,u)==target for u in U),
      "| CONTROL: u with u^2 = (-7+24i)/25:", sum(mul(u,u)==(Fr(-7,25),Fr(24,25)) for u in U))
# (5) Lemma 3.3's L=sqrt(AB): A=1,B=2 -> sqrt2 not rational
print("(5) is 1*2 a rational square?", is_sq(Fr(2)))
