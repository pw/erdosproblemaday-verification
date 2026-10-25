# At the phase wrap psi(B) = m+1 exactly, G_{m+1}(B)/G_m(B) = B/((m+1) g_{m+1}); claim: -> lam/gamma.
from mpmath import mp, mpf, log, findroot, exp
mp.dps=50
def a(j): j=mpf(j); return (j+1)*log(j+1)-(j*log(j) if j>0 else 0)-1
A=[mpf(0)]+[a(j) for j in range(1,4001)]
rho=mpf('0.5425985860984710219593846')
# refine rho
for _ in range(60):
    f=sum(A[j]*rho**j for j in range(1,4001))-1; fp=sum(j*A[j]*rho**(j-1) for j in range(1,4001)); rho-=f/fp
lam=log(1/rho); gam=1/(rho*sum(j*A[j]*rho**(j-1) for j in range(1,4001)))
g=[mpf(1)]
for n in range(1,2101): g.append(sum(A[d]*g[n-d] for d in range(1,n+1)))
print('lam/gamma =',mp.nstr(lam/gam,15))
for m in [5,10,50,100,500,1000,2000]:
    # solve (log B - log log B)/lam = m+1 for L=log B: L - log L = lam(m+1)
    t=lam*(m+1); L=findroot(lambda L: L-log(L)-t, t+log(t)); B=exp(L)
    r=B/((m+1)*g[m+1])
    print('m=%5d  G_{m+1}/G_m at wrap = %s'%(m,mp.nstr(r,12)))
