import numpy as np, math, sys
N = int(sys.argv[1]) if len(sys.argv)>1 else 10**7
M = N+2
gpf = np.zeros(M, dtype=np.int32)
gpf[1] = 1
# primes by simple sieve
is_p = np.ones(M, dtype=bool); is_p[:2]=False
for p in range(2, int(M**0.5)+1):
    if is_p[p]: is_p[p*p::p] = False
primes = np.nonzero(is_p)[0]
for p in primes:
    gpf[p::p] = p
n = np.arange(2, N+1, dtype=np.float64)
Pn = gpf[2:N+1].astype(np.float64)
Pn1 = gpf[3:N+2].astype(np.float64)
ln = np.log(n)
U = np.log(Pn)/ln
V = np.log(Pn1)/ln

# Dickman rho via fine grid
h = 1e-4
umax = 12.0
K = int(umax/h)+1
u = np.arange(K)*h
rho = np.ones(K)
m = int(round(1/h))
for i in range(m+1, K):
    # u rho'(u) = -rho(u-1); trapezoid on rho' = -rho(u-1)/u
    a = -rho[i-1-m]/u[i-1]; b = -rho[i-m]/u[i]
    rho[i] = rho[i-1] + h*(a+b)/2
def R(x):
    return float(np.interp(x, u, rho))
print("rho(2)=",R(2), "exact 1-log2=",1-math.log(2))
print("rho(3)=",R(3))
print("N =",N)
for (a,b) in [(0.5,0.5),(1/3,0.5),(0.6,0.4),(0.7,0.7),(0.25,0.75),(0.4,0.4)]:
    A = U<=a; Bm = V<=b
    joint = np.mean(A&Bm); ma=np.mean(A); mb=np.mean(Bm)
    print(f"a={a:.3f} b={b:.3f}: joint={joint:.5f}  margA={ma:.5f} margB={mb:.5f} prod_emp={ma*mb:.5f}  rho*rho={R(1/a)*R(1/b):.5f}  joint/prod_emp={joint/(ma*mb):.4f}")
lt = np.mean(Pn < Pn1); gt = np.mean(Pn > Pn1)
print("P(P(n)<P(n+1)) =",lt, " P(P(n)>P(n+1)) =",gt)
# by dyadic-ish ranges, to see drift
for lo,hi in [(10**4,10**5),(10**5,10**6),(10**6,10**7)]:
    if hi>N: break
    sl = slice(lo-2, hi-2)
    print(f"[{lo},{hi}): P(P(n)<P(n+1))={np.mean(Pn[sl]<Pn1[sl]):.5f}", 
          " joint(1/2,1/2)=%.5f prodemp=%.5f"%(np.mean((U[sl]<=.5)&(V[sl]<=.5)), np.mean(U[sl]<=.5)*np.mean(V[sl]<=.5)))
