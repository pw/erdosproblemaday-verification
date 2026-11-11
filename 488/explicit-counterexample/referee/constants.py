# Exact recomputation of every finite constant in the Gessel #488 construction.
from fractions import Fraction
from math import log, prod
from decimal import Decimal, getcontext
getcontext().prec = 60

def primes_below(n):
    s = bytearray([1])*n; s[0]=s[1]=0
    for i in range(2,int(n**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(n) if s[i]]

P = primes_below(257)
S = [p for p in P if p != 2]
Q = prod(S); phi = prod(p-1 for p in S)
print("|P| =", len(P), " |S| =", len(S), " max P =", max(P))
assert len(P)==54 and len(S)==53
print("Q has", len(str(Q)), "digits; Q > 128:", Q > 128)
print("3Q < 16 phi:", 3*Q < 16*phi)
r = Fraction(phi, Q)
print("phi/Q =", Decimal(r.numerator)/Decimal(r.denominator))
print("16 phi/(3Q) =", Decimal(16*phi)/Decimal(3*Q), " (needs > 1)")
print("implied density ratio lower bound (32/3)(phi/Q) =", Decimal(32*phi)/Decimal(3*Q), "(needs > 2)")
full = Fraction(prod(p-1 for p in P), prod(P))
print("prod_{p<257}(1-1/p) =", f"{float(full):.6f}", " exact-decimal:", Decimal(full.numerator)/Decimal(full.denominator))
print("  Mertens e^-gamma/ln 256 approx =", f"{0.5614594835668851/log(256):.6f}")
lhs = 2**4096 * 32769**53; rhs = 3**4096
print("8*4096+1 =", 8*4096+1)
print("2^4096*32769^53 < 3^4096:", lhs < rhs)
print("log margin (nats) ln(3^4096) - ln(lhs) =", 4096*log(3) - 4096*log(2) - 53*log(32769))
print("log2 margin (bits) =", (4096*log(3) - 4096*log(2) - 53*log(32769))/log(2))
print("bit lengths: lhs", lhs.bit_length(), " rhs", rhs.bit_length())
# smallest N for which 2^N (8N+1)^53 < 3^N (how much slack the 4096 choice has)
N = 1
while not (2**N * (8*N+1)**53 < 3**N): N += 1
print("smallest N with 2^N (8N+1)^53 < 3^N:", N)
