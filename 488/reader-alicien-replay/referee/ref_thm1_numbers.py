# Exact integer checks of the numerical facts in Theorem 1 (Alicien v2) -- referee scratch.
from fractions import Fraction
from math import prod, log
def primes_upto(N):
    s=bytearray([1])*(N+1); s[0]=s[1]=0
    for i in range(2,int(N**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(N+1) if s[i]]
P=primes_upto(256); S=[p for p in P if p>2]
print("primes<=256:",len(P)," odd:",len(S)," largest:",P[-1])
Q=prod(S); phi=prod(p-1 for p in S)
print("Q digits:",len(str(Q)))
# (a) telescope inequality
lhs=5**3500*28009**53; rhs=6**3500
print("5^3500*28009^53 < 6^3500 :", lhs<rhs, "  log-margin (nats):", 3500*log(6/5)-53*log(28009))
# minimal number of scales J such that 5^J*(8J+1+... ) works: 5^J*(8(J+1)+1)^53 < 6^J
J=1
while not (5**J*(8*(J+1)+1)**53 < 6**J): J+=1
print("smallest J with 5^J*(8(J+1)+1)^53<6^J :",J)
# (b) totient inequality
print("216Q <= 1280phi:",216*Q<=1280*phi," strict:",216*Q<1280*phi)
r=Fraction(phi,Q); print("phi(Q)/Q =",float(r)," 216/1280 =",216/1280, " margin 1280phi/(216Q) =",float(Fraction(1280*phi,216*Q)))
print("certified ratio lower bound  B(m)/m / (B(n)/n) >= 2*1280phi/(216Q) =", float(2*Fraction(1280*phi,216*Q)))
# also Gessel's constants
print("Gessel 3Q<16phi:",3*Q<16*phi, " 2^4096*32769^53<3^4096:", 2**4096*32769**53<3**4096)
print("Gessel certified ratio >= 16phi/(3Q)*... :", float(Fraction(256*phi,48*Q)))
# (c) n bound
print("8*(3500+1) =",8*3501)
# (d) x in A, maxA<n, e-count
j=1; x=2**(8*j); print("x=2^(8j)>=256 for j>=1:",x>=256)
