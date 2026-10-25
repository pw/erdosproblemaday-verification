# Toy check of the small-mark extraction identity (5.12) and the unit claim in Sec 5.4.
import itertools, math, random
from fractions import Fraction
random.seed(1)
G_small = [11,13,17,19,23]       # one small group P_gs (toy)
G_big   = [101,103,107]          # one big group (toy), carries the mark function b
V = {'s': Fraction(1,3), 'b': Fraction(2,5)}   # harmonic masses (any positive constants)
q = Fraction(1,2)
def factor(n):
    f={}; d=2
    while d*d<=n:
        while n%d==0: f[d]=f.get(d,0)+1; n//=d
        d+=1
    if n>1: f[n]=f.get(n,0)+1
    return f
bvals = {p: random.choice([1,-1,2]) for p in G_big}
def b(big_list):     # mark function depending only on big labels
    return math.prod(bvals[p] for p in big_list) if big_list else 1
def W(n, ts, tb):
    f = factor(n)
    sm = [p for p in G_small if p in f]; bg=[p for p in G_big if p in f]
    om = len(sm)+len(bg)
    tot = Fraction(0)
    for Ls in itertools.permutations(sm, ts):
        for Lb in itertools.permutations(bg, tb):
            tot += b(Lb)
    return q**(om-ts-tb) * V['s']**(-ts) * V['b']**(-tb) * tot
bad=0; checked=0; sqfail=0
for n in range(1, 400000, 7):
    f=factor(n)
    ts, tb = 2, 1
    lhs = W(n, ts, tb)
    rhs = sum(Fraction(1,1)/V['s'] * W(n//p, ts-1, tb) for p in G_small if n%p==0)
    sq = any(f.get(p,0)>=2 for p in G_small)
    if lhs!=rhs:
        if sq: sqfail+=1
        else: bad+=1
    checked+=1
print("checked",checked,"mismatch on p_s^2-free n:",bad,"mismatch on square multiples:",sqfail)
# unit claim: gcd(r/d0, r0/d0)=1 with d0=gcd(r,r0)
viol=0
for r in range(1,3000):
    for r0 in range(1,300):
        d0=math.gcd(r,r0)
        if math.gcd(r//d0, r0//d0)!=1: viol+=1
print("gcd(r/d0,r0/d0)!=1 violations:",viol)
# delta_k recursion: B_{k-2} = N^{-eps0/4}, B_j^2 <= H0^{-1}+B_{j+1}, H0=N^{eps0/(2k)}
eps0=Fraction(1,10)
for k in range(3,12):
    e = eps0/4
    for _ in range(k-2):
        e = min(eps0/(2*k), e)/2
    print(k, e, eps0/(k*2**(k-1)), e==eps0/(k*2**(k-1)))
