# Seat S: exact checks of the Section 6.3-6.4 recursions and closed forms (printed (6.6),(6.7),(6.12),(6.13)).
from fractions import Fraction as F
beta0 = F(1,200)
tau = F(1,4); eta = F(1,100); r = F(1,4)
bad = []
for i in range(0, 1500):
    beta_i = beta0 / 2**i
    delta_i = F(1, 2**(i+6))
    # closed forms printed after (6.13) and after (6.7)
    if tau != F(3,8) - F(1, 2**(i+3)): bad.append(("tau", i))
    if eta != F(1, 100**(i+1)) / F(2**(i*(i-1)//2 + 6*i)): bad.append(("eta", i))
    if r != F(1,4) - 4*beta0*(1 - F(1, 2**i)): bad.append(("r", i))
    if not (F(23,100) < r <= F(1,4)): bad.append(("r-range", i))
    if not (tau < F(3,8) and tau > 0): bad.append(("tau-range", i))
    if not (delta_i <= F(1,64)): bad.append(("delta<=1/64", i))
    # Theorem 5.2 inner inequality (tau+4d)(1-d) > tau+2d, and tau+delta<=1, tau+2delta<1
    if not ((tau+4*delta_i)*(1-delta_i) > tau+2*delta_i): bad.append(("hitprob", i))
    if not (tau + 2*delta_i < 1): bad.append(("tau+2d<1", i))
    # step
    tau, eta, r = tau + 4*delta_i, eta*delta_i/100, r - 2*beta_i
print("recursion/closed-form mismatches over i<1500:", bad[:10], "count", len(bad))
# r_i margin over 0.23 is 0.02*2^{-i} only -- tiny but strictly positive; the band needs only 0.20.
print("r_i - 0.23 at i=500:", float(F(1,4) - 4*beta0*(1-F(1,2**500)) - F(23,100)))
# Negative control: a wrong closed form must be caught
tau=F(1,4); wrong=0
for i in range(50):
    if tau != F(3,8) - F(1, 2**(i+2)): wrong += 1
    tau += 4*F(1,2**(i+6))
print("negative control (wrong tau closed form) mismatches (should be >0):", wrong)
