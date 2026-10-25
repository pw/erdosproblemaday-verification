# Numeric sweep of the leading terms in the deduction Thm 1.2 => Thm 1.1 (paper §11.2, eqs (11.6)-(11.10)).
# R(k) = k*(1+X/log X) / (Y*V0/B^2)  with z = A0*k*log k/(log log k)^e, L=log z, Y=z^2/L^2, w=L/(log L)^2,
# B=L/log w, V0=prod_{p<=w}(1-1/p), X=Y/z.  Paper: R -> e^gamma/A0 (for e=1).  Inequality needed: rho*R < 1,
# where rho = C1/c is (deletion constant)/(survivor constant) in units of Y V0/B^2.
import math, sys
G = 0.5772156649015329
# exact V0 for w up to WMAX via sieve, Mertens beyond
WMAX = 2_000_000
sieve = bytearray([1])*(WMAX+1); sieve[0]=sieve[1]=0
for i in range(2,int(WMAX**.5)+1):
    if sieve[i]: sieve[i*i::i]=bytearray(len(sieve[i*i::i]))
primes=[i for i in range(WMAX+1) if sieve[i]]
logprefix=[]; s=0.0
for p in primes:
    s+=math.log1p(-1/p); logprefix.append(s)
import bisect
def logV0(w):
    if w < 2: return 0.0
    if w <= WMAX:
        j=bisect.bisect_right(primes,int(w))
        return logprefix[j-1] if j>0 else 0.0
    return -G - math.log(math.log(w))   # Mertens, rel. error O(exp(-c sqrt log w))

def parts(ell, A0, e=1.0):
    # cancellation-free: L = ell + delta, delta = log A0 + log ell - e*log M  (z = A0 k ell / M^e)
    M = math.log(ell)
    delta = math.log(A0) + math.log(ell) - e*math.log(M)
    L = ell + delta
    logL = math.log(L)
    w = L/logL**2
    if w < 2: return None
    logw = math.log(w)
    logX = L - 2*logL
    return M, delta, L, logL, w, logw, logX
def ratio(ell, A0, e=1.0):
    P = parts(ell, A0, e)
    if P is None: return None
    M, delta, L, logL, w, logw, logX = P
    X = math.exp(min(logX, 700))
    # log R = -delta - log(log X) + log1p(logX/X) + 2 log B - log V0 ,  B = L/log w
    logR = -delta - math.log(logX) + math.log1p(logX/X) + 2*(logL - math.log(logw)) - logV0(w)
    return math.exp(logR)
def ratio_paperform(ell, A0, e=1.0):
    P = parts(ell, A0, e)
    if P is None: return None
    M, delta, L, logL, w, logw, logX = P
    return math.exp(-delta - math.log(logX) + 2*logL - math.log(logw))
def Yratio(ell, A0, e=1.0):   # Y / (A0^2 k^2 / M^2)
    P = parts(ell, A0, e); M, delta, L, logL = P[0], P[1], P[2], P[3]
    return math.exp(2*math.log(ell/L) + 2*(1-e)*math.log(M))
print("== R(k)*A0/e^gamma (should -> 1) and paper-form ratio*A0 (should -> 1), A0=10 ==")
print(f"{'log10 k':>10} {'loglog k':>9} {'R*A0/e^g':>9} {'(11.10)*A0':>10} {'Y*M^2/(A0^2 k^2)':>16} {'logw/M':>7}")
for j in [2,3,4,5,6,8,10,15,20,30,50,100,200,300]:
    ell = j*math.log(10); A0=10.0
    r=ratio(ell,A0); rp=ratio_paperform(ell,A0)
    P=parts(ell,A0)
    if P is None: print(f"{j:>10}  (w<2: parameters undefined)"); continue
    M=P[0]; w=P[4]; Yrat=Yratio(ell,A0)
    print(f"{j:>10} {M:9.3f} {r*A0/math.exp(G) if r else float('nan'):9.4f} {rp*A0 if rp else float('nan'):10.4f} {Yrat:16.4f} {math.log(w)/M:7.4f}")
# where does ell=log k have to be for e^gamma-normalized convergence? use ell = 10^j as well (k = e^(10^j))
print("\n== astronomically large k: ell = log k = 10^j ==")
for j in [3,5,10,20,50,100,200,300]:
    ell=10.0**j; A0=10.0
    r=ratio(ell,A0); rp=ratio_paperform(ell,A0); M=math.log(ell)
    print(f"log k=1e{j:<4} loglogk={M:8.2f}  R*A0/e^g={r*A0/math.exp(G):.4f}  (11.10)*A0={rp*A0:.4f}")
# thresholds: rho*R<1 with A0 = t*e^gamma*rho  (t = safety factor; paper takes A0 > 2C1/c0, i.e. t~2)
print("\n== threshold on log k for rho*R(k) < 1, A0 = t*e^gamma*rho ==")
for rho in [1.0, 10.0, 1e3]:
  for t in [1.05, 1.5, 2.0, 4.0]:
    A0=t*math.exp(G)*rho
    # scan ell geometric; record last ell where fails
    last_fail=None; ell=30.0
    while ell<1e300:
        r=ratio(ell,A0)
        if r is None or rho*r>=1: last_fail=ell
        ell*=1.05
    print(f"rho={rho:<7g} t={t:<5} A0={A0:10.3f}  inequality holds for all log k > {last_fail:.3e} (log10 k > {last_fail/math.log(10):.3e})" if last_fail else f"rho={rho} t={t}: holds from start")
print("\n== CONTROL (must fail): z = A0 k log k/(loglog k)^e with e=1.5 and e=2 -> ratio should grow without bound ==")
for e in [1.5,2.0]:
    row=[]
    for j in [5,20,100,300]:
        ell=10.0**j; r=ratio(ell,10.0,e); row.append(f"logk=1e{j}: {r*10/math.exp(G):.3f}")
    print(f"e={e}: "+"  ".join(row))
print("== CONTROL 2: e=0 (z=A0 k log k): ratio -> 0 but then Y ~ A0^2 k^2, no loglog saving ==")
for j in [5,20,100,300]:
    ell=10.0**j; r=ratio(ell,10.0,0.0); print(f"logk=1e{j}: R*A0/e^g={r*10/math.exp(G):.4f}  vs 1/loglogk={1/math.log(ell):.4f}")
