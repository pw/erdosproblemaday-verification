# Exact sizes of the paper's fixed parameters (d=41, M=C(163,41), T=C(M,3), k=T^2+1) and the exponents.
from math import comb, log10
from fractions import Fraction
d=41; M=comb(4*d-1,d); T=comb(M,3); k=T*T+1
print("M digits", len(str(M)), "M =", M)
print("T digits", len(str(T)))
print("k digits", len(str(k)))
alpha=45435*k+16
eta=Fraction(2,alpha); lean=Fraction(1,100000*k)
def lg(fr): return log10(fr.numerator) - log10(fr.denominator) if fr.denominator < 10**300 else -(len(str(fr.denominator))-1) - log10(int(str(fr.denominator)[:15])/10**14) + log10(fr.numerator)
print("alpha digits", len(str(alpha)))
print("log10 eta_paper ≈", round(lg(eta),4))
print("log10 eta_lean  ≈", round(lg(lean),4))
print("ratio eta_paper/eta_lean =", float(eta/lean))
print("lean < paper:", lean < eta)
# h = B^k with B ~ 100 k^2 r^30: digits of log10 h at r=3 (just the order of magnitude)
