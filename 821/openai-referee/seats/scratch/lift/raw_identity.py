# Toy check of the raw-pattern lift identity of Sec 5.2 (J=1, l=1, one small + one big group).
import cmath, math, itertools, random
random.seed(1)
G = {'s':[5,7,11], 'b':[13,17,19]}          # two "groups" of primes
allP = G['s']+G['b']
V = {g: sum(1/p for p in G[g]) for g in G}
q = 0.6; k = 2; Z = 400.0; a1 = 0.7; a2 = -1.3
J, l = 1, 1; M = J+l; s = 2
def Psi(t):  # smooth bump on (1,3)
    if t<=1 or t>=3: return 0.0
    return math.exp(-1/((t-1)*(3-t)))
def nstar(n):
    for p in allP:
        while n % p == 0: n//=p
    return n
cache={}
def H(m):  # arbitrary function of the P-free part
    if m not in cache: cache[m]=complex(random.uniform(-1,1),random.uniform(-1,1))
    return cache[m]
cacheG={}
def H2(m):
    if m not in cacheG: cacheG[m]=complex(random.uniform(-1,1),random.uniform(-1,1))
    return cacheG[m]
F0 = lambda n: H(nstar(n)); G0 = lambda n: H2(nstar(n))
def divs(n,g): return [p for p in G[g] if n%p==0]
def omega(n): return sum(len(divs(n,g)) for g in G)
def Wl(n):   # (5.1) with all t_g = l = 1
    val = q**(omega(n)-s*l)
    for g in G: val *= len(divs(n,g))/V[g]
    return val
def pw(x,a): return cmath.exp(1j*a*math.log(x))
# ---- LHS: physical pairing, raw pattern, with inserted Psi(n/(ZD))/n and D^{-i(a1+a2)}
LHS=0; LHS_noov=0
Dmax = max(G['s'])*max(G['b']); nmax = int(3*Z*Dmax)+10
for n in range(1,nmax):
    ds, db = divs(n,'s'), divs(n,'b')
    if len(ds)<2 or len(db)<2: continue
    for (x1,x2) in itertools.permutations(ds,2):
        for (y1,y2) in itertools.permutations(db,2):
            D = x1*y1; ps = Psi(n/(Z*D))
            if ps==0: continue
            n2 = n+k*D
            tgt=0
            for x2p in divs(n2,'s'):
                if x2p==x1: continue
                for y2p in divs(n2,'b'):
                    if y2p==y1: continue
                    tgt += 1
            if tgt==0: continue
            term = (V['s']**-2*V['b']**-2)*(V['s']**-1*V['b']**-1)*tgt \
                 * pw(n,a1)*F0(n).conjugate()*pw(n2,a2)*G0(n2)*pw(D,-(a1+a2)) \
                 * ps/n * q**(omega(n)-M*s) * q**(omega(n2)-M*s)
            LHS += term
            w, w2 = n//D, n2//D
            if w%x1 and w%y1 and w2%x1 and w2%y1: LHS_noov += term
# ---- RHS: (5.5)-type sum, and its no-overlap restriction with shared draws mu_g
S=0; S_noov=0
for w in range(1,int(3*Z)+5):
    w2=w+k
    if Psi(w/Z)==0: continue
    t = Psi(w/Z)/w*pw(w,a1)*pw(w2,a2)*F0(w).conjugate()*G0(w2)*Wl(w)*Wl(w2)
    S += t
    for x1 in G['s']:
        for y1 in G['b']:
            if w%x1 and w%y1 and w2%x1 and w2%y1:
                S_noov += t/(V['s']*x1)/(V['b']*y1)
print("LHS_noov =",LHS_noov); print("RHS_noov =",S_noov); print("abs diff =",abs(LHS_noov-S_noov))
print("full LHS =",LHS,"  (5.5) sum S =",S, " overlap part LHS-LHS_noov =",LHS-LHS_noov, " S-S_noov =",S-S_noov)
