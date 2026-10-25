#!/usr/bin/env python3
"""Referee seat D: §6 and §7.3 arithmetic, exact integers where feasible."""
import math
from fractions import Fraction
from sympy import nextprime, isprime

def clog2(N): return 0 if N<=1 else (N-1).bit_length()
def isqrt(x): return math.isqrt(max(x,0))
bad=0
# (6.2)-(6.5) for every q up to 4000 (m up to 64) and m up to 3000 for the palette inequalities
for q in range(0,4001):
    m=isqrt(q-1)+1 if q>=1 else 1
    if not q<=m*m: print("q<=m^2 fails",q); bad+=1
for m in range(1,3001):
    P=24*2**m+1
    S=24**(m-1)*(m*P*P+1)
    if not S<=2**(8*m+11): print("6.3 fails m=",m); bad+=1
    D=(m+1)**(m-1)*(m*2**(2*m)+1)
    r=math.ceil(math.log2(m+1)); r=(m).bit_length() if 2**((m).bit_length()-1)!=m+1 else r
    r=(m+1-1).bit_length()  # = clog2(m+1)
    assert 2**r>=m+1 and (r==0 or 2**(r-1)<m+1)
    if not D<=2**(m*r+2*m+1): print("6.5a fails m=",m); bad+=1
    if not m*r+2*m+1<=5*m*isqrt(m): print("6.5b (floor sqrt, as in Lean) fails m=",m); bad+=1
    if not m*r+2*m+1<=5*m*math.sqrt(m): print("6.5b (real sqrt) fails m=",m); bad+=1
print("6.2-6.5 scan done, failures:",bad)
# tightness of 6.5b with floor sqrt
tight=[(m,(m+1-1).bit_length()*m+2*m+1,5*m*isqrt(m)) for m in range(1,40)]
print("6.5b slack (m, mr+2m+1, 5m*isqrt(m)) smallest-slack cases:",sorted(tight,key=lambda t:t[2]-t[1])[:4])

# threshold lemma (6.6) and (6.8): evaluate at the boundary q = T^2+1 (smallest N exceeding 2^{T^2} has clog2 = T^2+1)
def check_thresholds(k):
    out=[]
    # (6.7): A=8,B0=11,K=2k, T=76k
    T=76*k; q=T*T+1; m=isqrt(q-1)+1
    out.append(("S_N^{2k} exponent",(8*m+11)*2*k, "q-1",q-1, (8*m+11)*2*k<=q-1))
    # (6.9): (20K)^4 with K=2k
    K=2*k; q2=(20*K)**4+1; m2=isqrt(q2-1)+1; s=m2-1
    lhs=5*(s+1)*isqrt(s+1)*K
    out.append(("D_N^{2k} exponent (floor sqrt)",lhs,"s^2",s*s,lhs<=s*s<=q2-1))
    lhs_real=5*(s+1)*math.sqrt(s+1)*K
    out.append(("D_N^{2k} exponent (real sqrt)",lhs_real,"s^2",s*s,lhs_real<=s*s))
    # exact log2 of D_N at that m2 vs q2-1
    D=(m2+1)**(m2-1)*(m2*2**(2*m2)+1)
    out.append(("exact 2k*log2 D_N",2*k*math.log2(D),"q-1",q2-1,2*k*math.log2(D)<q2-1))
    return out
for k in (1,2,3):
    for row in check_thresholds(k): print(f"k={k}",row)

# Is (40k)^4 ever smaller than (76k)^2? (which threshold binds)
print("binding threshold: (40k)^4 >= (76k)^2 for all k>=1:", all((40*k)**4>=(76*k)**2 for k in range(1,1000)))

# Whole theorem in log form at N = 2^{T^2}+1 (worst case: smallest admissible N), k=1,2, with p<=2y (Bertrand upper end)
C=2985984
print("729*4096 =",729*4096, " == 2,985,984:",729*4096==C)
for k in (1,2):
    T2=max((76*k)**2,(40*k)**4); q=T2+1; log2N=T2  # N slightly above 2^{T2}: log2 N > T2; use T2 (worst)
    m=isqrt(q-1)+1; B=2**m; P=24*B+1
    logS=math.log2(24)*(m-1)+math.log2(m*P*P+1)
    logD=(m-1)*math.log2(m+1)+math.log2(m*2**(2*m)+1)
    e=(q+2)//3+2; logp_max=e+1  # p<=2y
    logU=math.log2(9)+logp_max
    lhs=3*k*(logS+logD+logU); rhs=k*math.log2(C)+(k+3)*log2N
    print(f"k={k}: q={q} m={m}  3k*log2(S D U) = {lhs:.1f}  vs  log2(C^k N^(k+3)) >= {rhs:.1f}  margin {rhs-lhs:.1f} bits")

# §7.3: y, e, Bertrand, p^3 < 4096 N, worst N = 2^{q-1}+1
fails=0
for q in range(1,400):
    e=(q+2)//3+2; y=2**e
    Nmin=2**(q-1)+1; Nmax=2**q
    if not (y>3 and Nmax<=y**3 and 3*e<=q+8 and y**3<=2**(q+8) and y**3<512*Nmin and (2*y)**3<4096*Nmin): fails+=1; print("7.3 fail q",q)
    if q<=120:
        p=nextprime(y)
        if not (p<=2*y and p>3 and Nmax<=p**3 and (9*p)**3 < C*Nmin): fails+=1; print("7.3 prime fail q",q)
print("§7.3 scan q=1..399 (Bertrand prime computed for q<=120): failures",fails)
# N=1 edge (q=0)
q=0; e=(q+2)//3+2; y=2**e; p=nextprime(y); print("N=1: e,y,p =",e,y,p," (9p)^3 < C*1:",(9*p)**3<C)
# 7/20 vs log3/log22
print("22^7 =",22**7," 3^20 =",3**20," 22^7<3^20:",22**7<3**20, " (60+3)/180 =",Fraction(63,180))
print("log3/log22 =",math.log(3)/math.log(22))
