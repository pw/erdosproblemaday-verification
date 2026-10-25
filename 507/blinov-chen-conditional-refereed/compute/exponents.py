from fractions import Fraction as F
def bt(j):
    v,p=0,1
    while j: v+=(j&1)*p; j>>=1; p*=3
    return v
# packing: binary-ternary words below X
words=[bt(j) for j in range(4096)]
assert sum(w<10 for w in words)==5 and sorted(w for w in words if w<10)==[0,1,3,4,9]
assert sum(w<204391 for w in words)==2921
k=2*204391-1; assert k==408781
T=2916; assert T==9*18**2
# Blinov: N=(hq)^4, q~h^6, h=B^k, tau~B^(k-1)/2..3, n ~ r^gamma * N^(3/2)/sqrt(tau)
beta=F(4*3,2)*(k+6*k)-F(k-1,2)          # N^{3/2} = (hq)^6 = B^{6k}*q^6 = B^{6k+36k}
assert beta==42*k-F(k-1,2)==F(83*k+1,2)
rho=6*beta; assert rho==249*k+3
gamma=F(rho,rho+1); alpha=gamma+6*beta
eta=2*gamma/alpha
assert eta==F(2,rho+2)==F(2,249*k+5)==F(1,50893237), eta
print("Blinov eta =", eta, float(eta))
# OpenAI baseline for comparison: eta=2/(45435k0+16)
# Chen: N=(hq)^4/B^s0
s0=102195
beta_c=42*k-F(3*s0,2)-F(k-1,2); assert beta_c==F(83*k-3*s0+1,2)
rho_c=6*beta_c; assert rho_c==249*k+3-9*s0==100866717
eta_c=F(2,rho_c+2); assert eta_c==F(2,100866719)
print("Chen eta =", eta_c, float(eta_c), "  ratio to Blinov:", float(eta_c/eta))
# Chen's proportional-pair term ~ r^gamma * B^{(3 s0 - k + 1)/2}: needs 3 s0 - k + 1 < 0 ... and gamma<1 vs B ~ r^6 means
# any s0 with 3*s0 - (k-1) <= -1 suffices (B^{-1/2} <= r^{-3} beats r^gamma).
s0max=max(s for s in range(0,k) if 3*s-(k-1)<=-1); print("s0 max (3 s0 < k-1):", s0max)
rho_m=249*k+3-9*s0max; print("rho at s0max:", rho_m, " eta(gamma=rho/(rho+1)) = 2/", rho_m+2, float(F(2,rho_m+2)), " sup over gamma<1: 2/", rho_m+1)
# ceiling of the family: N free (multiple of hq), gamma->1: eta -> 2/(246k+8)
print("family ceiling 2/(246k+8) = 1/", (246*k+8)//2, float(F(2,246*k+8)))
# with the better packing max 178077
k2=2*178077+1; s0m2=max(s for s in range(0,k2) if 3*s-(k2-1)<=-1); rho2=249*k2+3-9*s0m2
print("k'=",k2," Blinov-form eta=2/(249k'+5) = 1/",(249*k2+5)/2, "  with Chen box at s0max:", "2/",rho2+2, float(F(2,rho2+2)), " ceiling 1/",(246*k2+8)//2)
