# Linear-sieve functions f, F (delay equations of paper §4.1), Dickman rho, derivative weights phi_e, phi_o.
# Route: cumulative trapezoid on a fine grid (hs = 1/N), independent of any closed form.
import numpy as np, math
EG = math.exp(0.5772156649015329)
A = 2*EG

def build(Smax=60.0, N=20000):
    hs = 1.0/N
    s = np.arange(0, int(Smax*N)+1)*hs
    n = len(s)
    sf = np.zeros(n); sF = np.zeros(n)
    # sF = A on [0,3]; f = 0 on [0,2]
    i2, i3 = 2*N, 3*N
    sF[:i3+1] = A
    # march in unit blocks: on [k, k+1] (k>=2) sf' = F(s-1); on [k,k+1] (k>=3) sF' = f(s-1)
    F = np.empty(n); f = np.empty(n)
    F[1:] = sF[1:]/s[1:]; F[0] = np.inf
    f[:i2+1] = 0.0
    k = 2
    while k*N < n-1:
        lo, hi = k*N, min((k+1)*N, n-1)
        # sf on [lo,hi]
        g = F[lo-N:hi-N+1]           # F(s-1)
        sf[lo:hi+1] = sf[lo] + np.concatenate([[0], np.cumsum((g[1:]+g[:-1])*hs/2)])
        f[lo:hi+1] = sf[lo:hi+1]/s[lo:hi+1]
        if k >= 3:
            g2 = f[lo-N:hi-N+1]
            sF[lo:hi+1] = sF[lo] + np.concatenate([[0], np.cumsum((g2[1:]+g2[:-1])*hs/2)])
            F[lo:hi+1] = sF[lo:hi+1]/s[lo:hi+1]
        k += 1
    # Dickman rho: u rho'(u) = -rho(u-1); rho=1 on [0,1]; i.e. rho(u) = rho(k) - int_k^u rho(t-1)/t dt
    rho = np.ones(n)
    k = 1
    while k*N < n-1:
        lo, hi = k*N, min((k+1)*N, n-1)
        g = rho[lo-N:hi-N+1]/s[lo:hi+1]
        rho[lo:hi+1] = rho[lo] - np.concatenate([[0], np.cumsum((g[1:]+g[:-1])*hs/2)])
        k += 1
    return s, hs, f, F, rho

if __name__ == "__main__":
    s, hs, f, F, rho = build(20, 20000)
    N = int(round(1/hs))
    def at(arr, x): return arr[int(round(x*N))]
    # checks against classical closed forms: f(s) = A log(s-1)/s on [2,4]; F(s)=A/s on [1,3]; rho(u)=1-log u on [1,2]
    for x in [2.5, 3.0, 3.7]:
        print(f"f({x}) grid {at(f,x):.12f}  closed {A*math.log(x-1)/x:.12f}")
    for x in [1.5, 2.0]:
        print(f"rho({x}) grid {at(rho,x):.12f} closed {1-math.log(x):.12f}")
    print("f(10), F(10):", at(f,10), at(F,10), " (f->1, F->1)")
    # identity F - f = A rho(s-1)/s (paper (4.6)): check
    for x in [3.5, 5.2, 8.0]:
        print(f"F-f at {x}: {at(F,x)-at(f,x):.3e}  A rho(s-1)/s {A*at(rho,x-1)/x:.3e}")
