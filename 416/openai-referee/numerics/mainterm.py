# Erdős #416 / OpenAI family 24: recompute the paper's scale constants and test the explicit main term against Ford's (1.1).
# Definitions copied from the comparator (ComparatorChallenges/TotientAsymptotic.lean): a_j, rho (root of sum a_{j} z^j = 1 on (0,1)),
# lam = log(1/rho), gamma = (sum_j j a_j rho^j)^{-1}, g_0 = 1, g_n = sum_{d=1}^n a_d g_{n-d}, G(B,j) = B^j/(j! prod_{i<=j} g_i),
# psi(b) = (log b - log log b)/lam, m = floor(psi(B)), theta = psi(B) - m, with B = log log x.
# Ford 1998 Thm 1: C = -1/(2 log rho), D = 2C(1 + log F'(rho) - log 2C) - 3/2 (we compute it, not quote it).
from mpmath import mp, mpf, log, floor, factorial, findroot, nsum, inf
mp.dps = 60
def a(j): j=mpf(j); return (j+1)*log(j+1) - (j*log(j) if j>0 else 0) - 1
J=4000
A=[mpf(0)]+[a(j) for j in range(1,J+1)]
def F(z): return sum(A[j]*z**j for j in range(1,J+1))
def Fp(z): return sum(j*A[j]*z**(j-1) for j in range(1,J+1))
# bisection on (0,1): F increasing, F(0)=0
lo,hi=mpf('0.1'),mpf('0.9')
for _ in range(200):
    mid=(lo+hi)/2
    if F(mid)<1: lo=mid
    else: hi=mid
rho=(lo+hi)/2
tail = A[J]*rho**J
lam=log(1/rho); C0=1/(2*lam); gam=1/(rho*Fp(rho)); D0=2*C0*(1+log(Fp(rho))-log(2*C0))-mpf(3)/2
print('rho  =',mp.nstr(rho,25),' (last series term',mp.nstr(tail,3),')')
print('lam  =',mp.nstr(lam,20)); print('C0   =',mp.nstr(C0,20)); print('gamma=',mp.nstr(gam,20)); print('D0   =',mp.nstr(D0,20))
g=[mpf(1)]
for n in range(1,2200): g.append(sum(A[d]*g[n-d] for d in range(1,n+1)))
print('g_n rho^n at n=10,100,500,1000,1499:',[mp.nstr(g[n]*rho**n,15) for n in (10,100,500,1000,2199)])
from mpmath import loggamma
lpg=[mpf(0)]
for i in range(1,len(g)): lpg.append(lpg[-1]+log(g[i]))
def logG(B,j): return j*log(B) - loggamma(j+1) - lpg[j]
def ford(B): L3=log(B); L4=log(L3); return C0*(L3-L4)**2 + D0*L3 - (D0+mpf(1)/2-2*C0)*L4
rows=[]
import math
for e in [1,2,3,5,8,12,20,30,50,80,120,200,300,400,500]:
    for frac in [0.0,0.25,0.5,0.75]:
        B=mpf(10)**(e+frac)
        psi=(log(B)-log(log(B)))/lam; m=int(floor(psi)); th=psi-m
        if m<1: continue
        d=logG(B,m)-ford(B)
        rows.append((float(e+frac),m,float(th),float(d)))
for r in rows: print('log10 B=%7.2f m=%5d theta=%.4f  logG_m - Ford = %+.6f'%r)
ds=[r[3] for r in rows if r[0]>=20]
print('range of logG_m - Ford for log10 B >= 20:', min(ds), max(ds))
