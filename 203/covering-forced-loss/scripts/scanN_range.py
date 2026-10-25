#!/usr/bin/env python3
"""All-N density scan: for every N in [1, NMAX], density(N) = sum 1/e_p over primes p | G_N = gcd(2^N-1, 3^N-1)
(exactly the primes with e_p | N).  Full factorisation via factorint (ECM); if a cofactor stays composite the N is
reported UNFACTORED with the rigorous upper bound: cofactor Q has at most floor(log_B Q) prime factors each with
e_p > log2(B)... (we only need density < 1 + L; reported separately).  Output scanN.tsv: N density npr complete."""
import sys, signal
from math import gcd, lcm, log2, floor
from sympy import factorint, isprime
A=int(sys.argv[1]); B=int(sys.argv[2])
out=open(sys.argv[3],"w"); out.write("N\tdensity\tnprimes\tstatus\tmaxe\n")
class TO(Exception): pass
def handler(s,f): raise TO()
signal.signal(signal.SIGALRM,handler)
for N in range(A,B+1):
    G=gcd(2**N-1,3**N-1)
    if G==1: out.write(f"{N}\t0\t0\tcomplete\t0\n"); continue
    status="complete"; dens=0.0; npr=0; maxe=0
    try:
        signal.alarm(120); f=factorint(G); signal.alarm(0)
    except TO:
        signal.alarm(0); f=factorint(G,limit=10**6); status="partial"
    for p,mult in f.items():
        if not isprime(p):
            # composite cofactor: bound its contribution. primes q|p have q>10^6 (trial division) and e_q>=20 (q<2^{e_q})
            kmax=floor(log2(p)/log2(10**6)); dens+=kmax/20; status=f"UNFACTORED(cof {p.bit_length()}b,<= {kmax} primes,+{kmax/20:.3f})"; continue
        if p in (2,3): continue
        # e_p = order of <2,3>: lcm of orders dividing N
        def order(a):
            for d in sorted(d for d in range(1,N+1) if N%d==0):
                if pow(a,d,p)==1: return d
        e=lcm(order(2),order(3)); dens+=1/e; npr+=1; maxe=max(maxe,e)
    out.write(f"{N}\t{dens:.6f}\t{npr}\t{status}\t{maxe}\n"); out.flush()
print("done")
