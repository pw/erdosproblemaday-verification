# Arithmetic of the constants in the proof of Lemma 2.7 (pp.11-14) and a numeric check of Lemma 2.6 (p.9).
from fractions import Fraction as Fr
import random, math
ok=True
for m in range(1,50):
    m2=Fr(m*m)
    # (2.7) majorant budget: arc mass < 1/(16m^2), approx error 1/(64m^2) twice, nonconstant part < 1/(32m^2)
    budget = Fr(1,16)/m2 + Fr(1,64)/m2 + Fr(1,32)/m2 + Fr(1,64)/m2
    ok &= budget == Fr(1,8)/m2 and budget < Fr(1,4)/m2
    # final collision bounds: lower > (0.95^2-0.1)/m^2 > 1/(4m^2) ; uses |J| > 10 m^2
    ok &= (Fr(95,100)**2 - Fr(1,10))/m2 > Fr(1,4)/m2
# Markov: 2g^2/t^2 < 1e-4  =>  (2 g^2)/(0.1 t^2) = 20 g^2/t^2 < 1e-3
ok &= Fr(20,2)*Fr(1,10**4) <= Fr(1,1000)
# Chebyshev: tau = s/100, distance <= 3 tau, two encodings: 2*9 tau^2/s^2
ok &= 2*9*Fr(1,100)**2 == Fr(18,10**4) and 1-Fr(18,10**4) > Fr(95,100)
# good-fiber sets: P(W-good for 2.11) > 0.99 and P(>0.9M good indices) > 0.999 => intersection > 0.989 > 0
ok &= Fr(99,100)+Fr(999,1000)-1 > 0
print('Lemma 2.7 constant arithmetic OK' if ok else 'CONSTANT FAILURE')
# Lemma 2.6: J_lambda(s) = sum_t w_t (sqrt(1+|s-t|^2)-sqrt(1+|t|^2)); |difference| <= |s|; J_{lambda'}(s)=J(s+r)-J(r) for lambda' = law(t-r)
random.seed(26)
pts=[(random.gauss(0,3),random.gauss(0,3)) for _ in range(40)]+[(1e6,-2e6)]  # one far atom: no moment assumption
wts=[random.random() for _ in pts]; Z=sum(wts); wts=[w/Z for w in wts]
def J(s,P):
    return sum(w*(math.hypot(1,math.hypot(s[0]-t[0],s[1]-t[1]))-math.hypot(1,math.hypot(t[0],t[1]))) for w,t in zip(wts,P))
r=(0.7,-1.3); Pp=[(t[0]-r[0],t[1]-r[1]) for t in pts]
errmax=0; bndok=True
for _ in range(200):
    s=(random.uniform(-9,9),random.uniform(-9,9))
    errmax=max(errmax,abs(J(s,Pp)-(J((s[0]+r[0],s[1]+r[1]),pts)-J(r,pts))))
    for t in pts[:5]:
        bndok &= abs(math.hypot(1,math.hypot(s[0]-t[0],s[1]-t[1]))-math.hypot(1,math.hypot(t[0],t[1])))<=math.hypot(*s)+1e-9
print('Lemma 2.6 translation identity max error %.2e ; |integrand|<=|s| : %s'%(errmax,bndok))
# control (must FAIL): the identity with the wrong sign J(s-r)-J(-r)
ctrl=max(abs(J(s,Pp)-(J((s[0]-r[0],s[1]-r[1]),pts)-J((-r[0],-r[1]),pts))) for s in [(1,2),(3,-1),(-2,0.5)])
print('  control J(s-r)-J(-r): max error %.3f (expected clearly nonzero)'%ctrl)
