# Test (A): run the arithmetic steps of Sec 2-3 with E=Q(i), K_Q={u in Q(i): |u|=1}.
from fractions import Fraction as Fr
from math import isqrt, gcd
from itertools import product
def is_sq(q):
    q=Fr(q)
    if q<0: return False
    n,d=q.numerator,q.denominator; return isqrt(n)**2==n and isqrt(d)**2==d
def prime_factors(n):
    f=set(); p=2
    while p*p<=n:
        while n%p==0: f.add(p); n//=p
        p+=1
    if n>1: f.add(n)
    return f
# (1) p.13 step: "Each |x_j|<1 is a sum of two elements of K."  For real x != 0, k+k'=x with |k|=|k'|=1 forces
#     Re k = x/2 and (Im k)^2 = 1-x^2/4  (from |x-k|^2=1 => 2Re(x k-bar)=x^2).  Over Q this needs 1-x^2/4 to be a rational square.
def sum_of_two_rational_units(x):
    x=Fr(x); return x==0 or is_sq(1-x*x/4)
tests=[Fr(1,2),Fr(1,3),Fr(1,5),Fr(2,3),Fr(3,4),Fr(1,7),Fr(6,5),Fr(8,5),Fr(24,25)]
print('(1) x in Q, is x = k+k\' with k,k\' in K_Q ?', {str(x):sum_of_two_rational_units(x) for x in tests})
H=60; cnt=tot=0
for d in range(1,H+1):
    for n in range(1,d):
        if gcd(n,d)==1:
            tot+=1; cnt+=sum_of_two_rational_units(Fr(n,d))
print('    among the %d reduced rationals in (0,1) with denominator <= %d, only %d are sums of two rational unit vectors'%(tot,H,cnt))
# the proof needs x_j = j t for j=1..M ALL decomposable, t chosen by an invariant mean (no arithmetic control).
best=0
for d in range(1,400):
    for n in range(1,d):
        if gcd(n,d)!=1: continue
        t=Fr(n,d); M=0
        while abs((M+1)*t)<1 and sum_of_two_rational_units((M+1)*t): M+=1
        best=max(best,M)
print('    largest M with jt decomposable for all j=1..M (t=n/d, d<400, |Mt|<1):',best,' (the proof needs M >= 2 with 0.9M/L > 10m^2, i.e. M huge)')
# (2) Stronger: Z[K_Q] avoids 1/3 and 1/2: every rational unit vector (a/c,b/c) (primitive triple) has c with prime factors = 1 mod 4.
bad=0; seen=0
for m in range(1,90):
    for n in range(1,m):
        if (m-n)%2==1 and gcd(m,n)==1:
            a,b,c=m*m-n*n,2*m*n,m*m+n*n; seen+=1
            if any(p%4!=1 for p in prime_factors(c)): bad+=1
print('(2) %d primitive Pythagorean triples: hypotenuses with a prime factor not = 1 mod 4: %d'%(seen,bad))
print('    => K_Q subset Z[i][1/p : p=1 mod 4]; so EVERY integer combination of elements of K_Q has no 2 or 3 in its denominator;')
print('       x=1/3 or 1/2 is not a Z-combination of rational unit vectors of ANY length.')
# control: the algebraic field passes: x=1/3 = k+k' with k = 1/6 + i sqrt(35)/6 (in K, algebraic) -- see check_lemma33.py
# (3) 3-adic counterexample to the rational Theorem 2.3 / Lemma 2.7: K_Q acts ISOMETRICALLY on Q_3(i) (3 inert).
def v_p(q,p):
    q=Fr(q)
    if q==0: return 99
    n,d=q.numerator,q.denominator; v=0
    while n%p==0: n//=p; v+=1
    while d%p==0: d//=p; v-=1
    return v
units=[]
for m in range(1,40):
    for n in range(-39,40):
        if n!=0 and gcd(m,abs(n))==1 and (m-n)%2==1:
            c=m*m+n*n; units.append((Fr(m*m-n*n,c),Fr(2*m*n,c)))
print('(3) sample |K_Q| =',len(units),'; min 3-adic valuation of coordinates:',min(min(v_p(x,3),v_p(y,3)) for x,y in units),
      '; min 2-adic:',min(min(v_p(x,2),v_p(y,2)) for x,y in units))
# image of K_Q in (Z/3^n)[i]^x grows with n => orbit closure G_3 in Z_3[i]^x is infinite => Haar(G_3) nonatomic.
for n in range(1,6):
    mod=3**n; img=set()
    for x,y in units:
        inv=pow(x.denominator,-1,mod)  # denominators prime to 3
        img.add(((x.numerator*inv)%mod,(y.numerator*pow(y.denominator,-1,mod))%mod))
    print('    |image of sample of K_Q in (Z/3^%d)[i]| = %d'%(n,len(img)))
print('    => nu_3 := Haar on G_3 = closure of K_Q.1 in Z_3[i]^x (embedded in D_Q as characters trivial on Z_(3)[i]) is K_Q-invariant,')
print('       ergodic (minimal isometric rotation), gives C measure 0 (C meets that compact subgroup only in 0, and 0 is not in G_3),')
print('       and has Fourier coefficient f(1)=1 (1 in Z_(3)[i]); it is NOT Haar on D_Q.  Rational Theorem 2.3 is FALSE.')
# (4) Payne's 2-colouring lives on the 2-adic isometric place: colour Z_(2)^2 by (x+y) mod 2; a rational unit step flips it.
flips=all(((x+y).numerator%2==1 and (x+y).denominator%2==1) for x,y in units)
print('(4) every sampled rational unit vector (x,y) has x+y a 2-adic UNIT (odd/odd):',flips,' => colour(x,y)=(x+y mod 2) flips on every rational unit step')
ctrl=(Fr(3,5),Fr(1,5)); print('    control: non-unit step (3/5,1/5): x+y = 4/5 odd/odd?',(ctrl[0]+ctrl[1]).numerator%2==1,'(expected False -> the test can fail)')
# (5) the other two real-closedness uses, rational analogues
print('(5) Lemma 3.3 needs L=sqrt(AB) in the base field: A=1,B=2 -> AB square in Q?',is_sq(Fr(2)),
      '; p.21 "every t in [-1,1] is Re of an element of K": t=1/2 -> 1-t^2 square in Q?',is_sq(Fr(3,4)))
print('    p.18 "radii lie in F_{>=0}": |1+i| = sqrt2 rational?',is_sq(Fr(2)))
