# Positive control for the exact identity used by the explicit counterexample:
#   A = {P-smooth a : T < a <= qT}  (P = primes <= y, q = next prime)
#   (i)  B = multiples of A  equals  {z : P-part(z) > T}           (checked over a full period L = lcm(A))
#   (ii) |B cap [1,L]| / L  =  1 - prod(1-1/p) * S(T),  S(T) = sum_{s<=T, P-smooth} 1/s   (exact rationals)
#   (iii) M_A(qT) = |A|
# plus a NEGATIVE control: band (T, (q+1)T] (cofactor q allowed) must break (iii).
from fractions import Fraction
from math import lcm, prod
import sys
def primes_upto(y): return [p for p in range(2,y+1) if all(p%d for d in range(2,int(p**.5)+1))]
def nextprime(y):
    k=y+1
    while any(k%d==0 for d in range(2,int(k**.5)+1)): k+=1
    return k
def smooth(x,P):
    out=[1]
    for p in P:
        new=[]
        for s in out:
            t=s
            while t<=x: new.append(t); t*=p
        out=new
    return sorted(out)
def ppart(z,P):
    r=1
    for p in P:
        while z%p==0: z//=p; r*=p
    return r
bad=0; cases=0
for y,Ts in [(2,[1,2,3,5]),(3,[1,2,4,7,10]),(5,[1,3,6,10]),(7,[1,2,5,10,12])]:
    P=primes_upto(y); q=nextprime(y)
    for T in Ts:
        A=[a for a in smooth(q*T,P) if a>T]
        L=lcm(*A)
        if L>3*10**7: print('skip',y,T,L); continue
        cov=bytearray(L+1)
        for a in A: cov[a::a]=b'\x01'*len(cov[a::a])
        okI=all((cov[z]==1)==(ppart(z,P)>T) for z in range(1,L+1))
        S=sum(Fraction(1,s) for s in smooth(T,P))
        c=prod(Fraction(p-1,p) for p in P)
        dens=Fraction(sum(cov[1:]),L)
        okII= dens==1-c*S
        okIII= sum(cov[1:q*T+1])==len(A)
        cases+=1; bad+= not(okI and okII and okIII)
        R=dens*q*T/len(A)
        print(f"y={y} q={q} T={T} |A|={len(A)} L={L} (i)={okI} (ii)={okII} (iii)={okIII}  ratio delta*n/|A|={float(R):.4f}")
print(f"POSITIVE: {cases} cases, {bad} failures")
# negative control: band (T,2qT]: cofactor q (not P-smooth) now fits under n=2qT, so M_A(n) must exceed |A|
neg=0
for y,T in [(3,4),(5,3),(7,2)]:
    P=primes_upto(y); q=nextprime(y); n=2*q*T
    A=[a for a in smooth(n,P) if a>T]
    cov=bytearray(n+1)
    for a in A: cov[a::a]=b'\x01'*len(cov[a::a])
    neg+= sum(cov[1:])!=len(A)
    print(f"NEG y={y} T={T}: M_A(n)={sum(cov[1:])} vs |A|={len(A)} -> identity (iii) {'BROKEN (expected)' if sum(cov[1:])!=len(A) else 'holds (control failed)'}")
print(f"NEGATIVE: {neg}/3 broke as expected")

# (iv) Liu's Lemma 12(iii): M_A(WT) = sum_{u rough, u < W} (Psi(WT/u) - Psi(T)), checked by direct sieving for many W
print("== (iv) finite-m formula, direct count vs formula ==")
bad4=0; c4=0
for y,Ts in [(3,[2,4,7]),(5,[3,6,10]),(7,[2,5,10])]:
    P=primes_upto(y); q=nextprime(y)
    for T in Ts:
        A=[a for a in smooth(q*T,P) if a>T]
        for W in [q+1, 2*q, 3*q+1, 5*q, q*q-1]:
            m=W*T
            cov=bytearray(m+1)
            for a in A: cov[a::a]=b'\x01'*len(cov[a::a])
            direct=sum(cov[1:])
            psi=lambda x: sum(1 for s in smooth(x,P) if s<=x)
            rough=[u for u in range(1,W) if all(u%p for p in P)]
            formula=sum(max(0,psi(m//u)-psi(T)) for u in rough)
            c4+=1; bad4+= direct!=formula
print(f"(iv): {c4} cases, {bad4} mismatches")
# negative control for (iv): drop the u=1 term -> must mismatch
y,T,W=5,6,20; P=primes_upto(y); q=nextprime(y); A=[a for a in smooth(q*T,P) if a>T]; m=W*T
cov=bytearray(m+1)
for a in A: cov[a::a]=b'\x01'*len(cov[a::a])
psi=lambda x: sum(1 for s in smooth(x,P) if s<=x)
wrong=sum(max(0,psi(m//u)-psi(T)) for u in range(2,W) if all(u%p for p in P))
print("NEG (iv) without u=1:", "mismatch (expected)" if wrong!=sum(cov[1:]) else "MATCH (control failed)")

# (v) Lambda < q (Gessel's case has Lambda = 256 < q = 257): band (T, Lambda*T] with y <= Lambda < q
print("== (v) Lambda < q: (i) M_A(n)=|A|, (ii) B = {P-part > T}, (iv) finite-m formula ==")
bad5=0; c5=0
for y,Lams,Ts in [(7,[7,8,9,10],[1,2,5,10]),(13,[13,14,15,16],[1,3,7]),(23,[23,24,26,28],[1,2,4])]:
    P=primes_upto(y); q=nextprime(y)
    for Lam in Lams:
        for T in Ts:
            A=[a for a in smooth(Lam*T,P) if a>T]; n=Lam*T
            L=lcm(*A)
            if L>3*10**7: continue
            cov=bytearray(L+1)
            for a in A: cov[a::a]=b'\x01'*len(cov[a::a])
            okI = sum(cov[1:n+1])==len(A)
            okII= all((cov[z]==1)==(ppart(z,P)>T) for z in range(1,L+1))
            psi=lambda x: sum(1 for s in smooth(x,P) if s<=x)
            okIV=True
            for W in [Lam+1, 3*Lam, q*q-1]:
                m=W*T
                if m>L: continue
                rough=[u for u in range(1,W) if all(u%p for p in P)]
                okIV &= sum(cov[1:m+1])==sum(max(0,psi(m//u)-psi(T)) for u in rough)
            c5+=1; bad5+= not(okI and okII and okIV)
print(f"(v): {c5} cases, {bad5} failures")
