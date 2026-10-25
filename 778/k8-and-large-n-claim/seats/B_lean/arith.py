from fractions import Fraction as F
k=158
L=125*25**k*(500*k+505); R=2*27**(k+1)
print("extractionGood_158:", L<=R, "ratio R/L =", float(F(R,L)))
for k in range(150,158):
    print(k, 125*25**k*(500*k+505) <= 2*27**(k+1))
r=F(6250,6561)
u=3*r**25
print("3*r^25 =", float(u), "<= 9/10:", u<=F(9,10))
print("(4/3)^3(5/6)^5 =", F(4,3)**3*F(5,6)**5)
print("6/5*(9/10)^10 =", float(F(6,5)*F(9,10)**10), "< 8/9:", F(6,5)*F(9,10)**10 < F(8,9))
import math
print("3^158 ~ 10^%.2f" % (158*math.log10(3)))
eta=-math.log((F(4,3)**3*F(5,6)**5)**F(1,5) if False else float((F(4,3)**3*F(5,6)**5))**0.2)
C=250/math.log(3)
print("eta=%.6f C(ln-scale)=%.3f C*eta=%.3f"%(eta,C,C*eta))
# largeSize mod 5, pairCount divisible by 5
for k in range(0,10):
    l=250*(k+1)+1; H=l*(l-1)//2
    assert H%5==0 and 3*(H//5)*5==3*H
print("largeTarget = 3H/5 exactly: ok")
# smallSize vs paper a
for n in [3**158, 3**158+1, 2*3**158, 3**159-1]:
    k=n.bit_length() # placeholder
