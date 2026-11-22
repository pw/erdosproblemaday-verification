from fractions import Fraction as F
import math
from mpmath import mp, mpf, log, e, sqrt
mp.dps = 60
B = 9797*10**15
lhs = 9797**15 * 10**225 * 500**656
rhs = 1359**656
print("B^15 < (1359/500)^656 :", lhs < rhs, " ratio rhs/lhs (log) =", float(mp.log(rhs) - mp.log(lhs)))
s6 = sum(F(1, math.factorial(j)) for j in range(7))
print("1359/500 < sum_{j<=6} 1/j! :", F(1359,500) < s6, float(s6))
print("log B =", log(B), " 656/15 =", mpf(656)/15)
print("B^2 < 9.6e37 :", B*B < 96*10**36, B*B)
d = 512*(mpf(656)/15)**2/B
print("512 (656/15)^2/B =", d, " < 1e-13:", d < mpf('1e-13'))
print("512 (log B)^2/B =", 512*log(B)**2/B)
# Section 2 constants
print("|B_I| coefficient: 3*4*16/9 / 512 * 64?", F(3*4*16,9)/512, "should be 1/24 ->", F(3*4*16,9)/512 == F(1,24)*F(64,64))
print("|B_I| = 3d(2N)^2L^2/(3dN/4)^2 = (12*16/9) L^2/d = ", F(12*16,9), "L^2/d ; with L^2/d = N/512 ->", F(12*16,9)/512)
print("|B_J| = 3d(4/9)N^2L^2/(dN/4)^2 = ", F(3*4*16,9), "L^2/d ->", F(3*4*16,9)/512)
print("G >=", F(1,2)-F(1,24)-4*F(1,24))
print("count = 7/24 * 1/16 / 2 * 512 =", F(7,24)*F(1,16)/2*512)
print("weight =", F(7,24)*F(1,16)/2*512/3)
# Section 3 lemma
print("Lemma3.1 diag+off:", 2 + 8*F(9,4))
print("|E| >= ", (F(1,4))**2/20, " b=1/2500 <", F(1,320))
print("(9/4)log4 =", 9/4*math.log(4))
# Thm1.2 lower
print("808*16 =", 808*16, " 12928*2 =", 12928*2, " 25856*2 =", 25856*2)
print("bS eta T/(32L^2): S T = N^2/2, eta=CL^2/N -> b C N/64 :", F(1,2)/32)
print("CH variant: 3*4*16 =", 3*4*16, " 48*2 =", 96, " 96*2 =", 192)
# Section 4
print("A moment: 80*(3/2)*4 =", 80*F(3,2)*4)
print("B moment: 16*80*(7/4)*36 =", 16*80*F(7,4)*36)
print("sum =", 480+80640, " *2 (weight 2S/x) =", 81120*2, " *4N =", 81120*2*4, " *4C =", 81120*2*4*4)
print("small primes: 2*(4L)/(L/2) =", 2*4*2)
# A.3
print("A.3:", F(1,2)-F(320*808, 9*131072), float(F(1,2)-F(320*808, 9*131072)))
print("A.3 B_I coeff 808*4*16/9 =", F(808*64,9), " 5x =", 5*F(808*64,9), "=", F(320*808,9))
print("A.3 count delta N^2/(128 L^2) = 131072/128 =", 131072//128, "  window 3*131072 =", 3*131072, " 98304*4 =", 98304*4)
print("Thm1.1 window 3*512 =", 3*512, " 384*4 =", 384*4)
# A.2
print("A.2: 4D(1+1/K)/K <= 8D/K; 8+16 =", 24, "; K>=192D -> 24D/K <= 1/8;  1/(64*4*3) =", 64*4*3)
print("t + x/t max on [3/2,2]:", max(t + 1/t for t in [1.5, 2.0]), "<= 8/3", 8/3)
