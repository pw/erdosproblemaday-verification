from math import comb, log10
from decimal import Decimal, getcontext
getcontext().prec=60
d=41; M=comb(4*d-1,d); T=comb(M,3); k=T*T+1
alpha=45435*k+16
# digits of (400k^2)^alpha = floor(alpha*log10(400k^2))+1
lk=Decimal(len(str(k))-1)+Decimal(str(k)[:40]).log10()-Decimal(39)
l=Decimal(400).log10()+2*lk
dig=Decimal(alpha)*l
print("log10(400k^2)=",l)
print("digits of (400k^2)^alpha ~ %.6E"%dig)
# R0 = max(r0,400k^2)+2; n0 = R0^alpha + 1
print("k ~ %.6E"%Decimal(k), "alpha ~ %.6E"%Decimal(alpha))
# U digits
U_log= Decimal(3).log10()+30*Decimal(2).log10()+(3029*Decimal(k)+1)*(Decimal(200).log10()+2*lk)
print("log10 U ~ %.4E"%U_log)
