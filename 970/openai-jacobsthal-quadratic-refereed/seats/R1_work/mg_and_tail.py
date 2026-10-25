# (1) M_g = sum_i int pi_i g exactly (numerically), vs the paper's bound M_g <= 4 e^gamma (4.18).
# (2) invariance check of pi_e, pi_o under the tilted kernel (4.13) by direct numerical integration (control: perturbed pi fails).
# (3) exact value of the paper's tail majorant (6.14) with mpmath, and its claimed bound < 0.34.
import numpy as np, math, mpmath as mp
from sieve_fns import build, A, EG
s, hs, f, F, rho = build(60, 20000)
N = int(round(1/hs))
a = 1 - f; c = F - 1
def at(arr, x): return np.interp(x, s, arr)
# phi_e(s) = s^2 f'(s) (s>=2), phi_o(s) = -s^2 F'(s) (s>=1, = A on [1,3]); compute by finite differences (route 1)
fp = np.gradient(f, hs); Fp = np.gradient(F, hs)
phi_e_fd = s**2*fp; phi_o_fd = -s**2*Fp
# route 2: deficit formulas (4.11)
def phi_e(x): return x*(at(a, x) + at(c, x-1))
def phi_o(x): return x*(at(c, x) + np.where(x-1 <= 2, 1.0, at(a, np.maximum(x-1, 0))))
for x in [2.5, 3.5, 5.0, 7.0]:
    i = int(round(x*N))
    print(f"phi_e({x}): fd {phi_e_fd[i]:.8f} deficit {phi_e(x):.8f} | phi_o({x}): fd {phi_o_fd[i]:.8f} deficit {phi_o(x):.8f}")
ge = lambda x: np.log1p(1/x)
xe = np.linspace(2, 50, 480001); xo = np.linspace(1, 50, 490001)
Mg = np.trapezoid(phi_e(xe)*ge(xe), xe) + np.trapezoid((1-xo**-2)*phi_o(xo)*ge(xo), xo)
print(f"M_g = {Mg:.8f}   paper bound 4e^gamma = {4*EG:.8f}")
# bound pieces with g(s)<=1/s: int_2^inf a + 2 int_1^inf c + int_0^inf a  should equal 2A
x0 = np.linspace(0, 50, 500001); x1 = np.linspace(1, 50, 490001); x2 = np.linspace(2, 50, 480001)
print("int_1^inf c =", np.trapezoid(at(c, x1), x1), "(paper 2);  int_1^inf a =", np.trapezoid(at(a, x1), x1), f"(paper A-2={A-2:.6f})")
# (2) invariance: pi_o(t) =?= int_{s>=2, s-1<=t} pi_e(s) K_e(s,t) ds ; pi_e(t) =?= int_{s>=1, max(2,s-1)<=t} pi_o(s) K_o(s,t) ds
W0 = lambda t: (t+1)/t**2
pi_e = lambda x: phi_e(x); pi_o = lambda x: (1-x**-2)*phi_o(x)
for t in [1.5, 2.5, 4.0]:
    ss = np.linspace(2, t+1, 20001)
    rhs = np.trapezoid(pi_e(ss)*W0(t)*phi_o(t)/phi_e(ss), ss)
    print(f"odd balance t={t}: pi_o {pi_o(t):.8f}  incoming {rhs:.8f}")
for t in [2.2, 3.0, 5.0]:
    ss = np.linspace(1, t+1, 20001)
    rhs = np.trapezoid(pi_o(ss)*W0(t)*phi_e(t)/phi_o(ss), ss)
    rhs_bad = np.trapezoid(phi_o(ss)*W0(t)*phi_e(t)/phi_o(ss), ss)   # control: drop (1-s^-2)
    print(f"even balance t={t}: pi_e {pi_e(t):.8f}  incoming {rhs:.8f}  (control w/o 1-s^-2: {rhs_bad:.8f})")
# (3) tail majorant
mp.mp.dps = 40
lam = mp.log(2)
maj = mp.nsum(lambda m: (m+1)**2*lam**m/mp.factorial(m)*(lam**-2 + (mp.mpf(3)/(2*lam) - lam**-2)/m), [4, mp.inf])/2
print("tail majorant (6.14) exact =", mp.nstr(maj, 12), " (paper: < 0.34)")
# paper's coarse route: braces at m=4 with lambda=0.69, times series at 0.70
br = mp.mpf(3)/(4*mp.mpf('0.69')**2) + mp.mpf(3)/(8*mp.mpf('0.69'))
ser = mp.e**mp.mpf('0.7')*(mp.mpf('0.49')+mp.mpf('2.1')+1) - 1 - 4*mp.mpf('0.7') - mp.mpf(9)/2*mp.mpf('0.49') - mp.mpf(8)/3*mp.mpf('0.343')
print("paper coarse: braces(m=4) =", mp.nstr(br, 8), "<2.14 ;", "series =", mp.nstr(ser, 8), "<0.313 ; product/2 =", mp.nstr(br*ser/2, 8))
# braces monotone in m? (needs 3/(2 lam) > lam^-2)
print("3/(2lam) - lam^-2 =", mp.nstr(mp.mpf(3)/(2*lam) - lam**-2, 8), "(>0 => braces decreasing in m, max at m=4)")
