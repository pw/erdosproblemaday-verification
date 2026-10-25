from math import comb, prod
import itertools
def ff(a,k): return prod(a-i for i in range(k))
bad=0; worst=0
for l in range(1,4):
  for m in range(1,9):
    for M in range(m+l, 60):
      for j in range(0,M+1):
        lhs = comb(M-m-l,j-m)/comb(M,j) if 0<=j-m<=M-m-l else 0.0
        rhs = ff(j,m)*ff(M-j,l)/ff(M,m+l)
        if abs(lhs-rhs)>1e-12: bad+=1
        if M >= (m+l)*(m+l-1):
          th=2*l**l*m**(-l)
          b1=2*(j/M)**m*(1-j/M)**l
          if lhs>b1+1e-12 or b1>th+1e-12: bad+=1
          worst=max(worst,lhs/th if th>0 else 0)
print("identity/bound failures:",bad," max(fraction/theta_m) over M>=(m+l)(m+l-1):",round(worst,4))
# (4.26)
for u in range(1,6):
  for v in range(1,6):
    s=sum((-1)**(a+b)*comb(u,a)*comb(v,b) for a in range(1,u+1) for b in range(1,v+1))
    assert s==1
print("(4.26) sum = 1 for all 1<=|U|,|V|<=5")
