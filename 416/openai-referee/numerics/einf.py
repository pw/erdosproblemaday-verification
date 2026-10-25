# Check seat O's claim: log G_m - Ford bracket -> E_inf(theta) = theta(log(gam/lam)+lam/2) - lam theta^2/2 - (1/2)log(2pi/lam) - log K,
# K = prod_{i>=1} g_i rho^i / gam. Our own code (not O's), at log B = 300, 600, 1000.
from mpmath import mp, mpf, log, floor, loggamma, pi, exp
mp.dps=40
def a(j): j=mpf(j); return (j+1)*log(j+1)-(j*log(j) if j>0 else 0)-1
J=3000; A=[mpf(0)]+[a(j) for j in range(1,J+1)]
rho=mpf('0.5425985860984710219593846')
for _ in range(50):
    f=sum(A[j]*rho**j for j in range(1,J+1))-1; fp=sum(j*A[j]*rho**(j-1) for j in range(1,J+1)); rho-=f/fp
lam=log(1/rho); gam=1/(rho*sum(j*A[j]*rho**(j-1) for j in range(1,J+1)))
C0=1/(2*lam); D0=(1+log(lam/gam))/lam-mpf(1)/2
NG=1700; g=[mpf(1)]
for n in range(1,NG+1): g.append(sum(A[d]*g[n-d] for d in range(1,n+1)))
lK=sum(log(g[i]*rho**i/gam) for i in range(1,NG+1))
print('K =',mp.nstr(exp(lK),8))
lpg=[mpf(0)]
for i in range(1,NG+1): lpg.append(lpg[-1]+log(g[i]))
def Einf(t): return t*(log(gam/lam)+lam/2)-lam*t**2/2-log(2*pi/lam)/2-lK
for LB in [300,600,1000]:
    for frac in [0.1,0.5,0.9]:
        # choose B with log B = LB + small shift so theta ~ frac
        L=mpf(LB); psi=(L-log(L))/lam; m=int(floor(psi)); target=m+frac
        # solve (L' - log L')/lam = target near L
        for _ in range(30): L=L-((L-log(L))/lam-target)/((1-1/L)/lam)
        B=exp(L); th=(L-log(L))/lam-m
        lg=m*L-loggamma(m+1)-lpg[m]
        ford=C0*(L-log(L))**2+D0*L-(D0+mpf(1)/2-2*C0)*log(L)
        d=lg-ford
        print('logB=%7.2f m=%5d theta=%.3f  diff=%+.5f  Einf=%+.5f  remainder=%+.5f'%(float(L),m,float(th),float(d),float(Einf(th)),float(d-Einf(th))))
