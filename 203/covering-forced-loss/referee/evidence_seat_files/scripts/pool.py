# Complete enumeration of primes p>=5 with e_p | N, where e_p = |<2,3> mod p|.
# Route: p | g_N := gcd(2^N-1, 3^N-1)  <=>  2^N==1 and 3^N==1 mod p  <=>  exponent of H_p divides N
#        <=> e_p | N  (H_p cyclic, so |H_p| = exponent = lcm(ord2, ord3)).
# Factor g_N by splitting along d | N: g_N = prod_d gcd(Phi_d(2), g_N) up to the usual non-primitive
# overlaps; we then CERTIFY completeness by dividing every found prime out of g_N to multiplicity
# and asserting the cofactor is exactly 1.
import sys, math, json
from fractions import Fraction
from sympy import divisors, factorint, isprime, n_order, mobius

def phi_d_at(d, x):
    num, den = 1, 1
    for e in divisors(d):
        mu = mobius(d // e)
        if mu == 1: num *= x**e - 1
        elif mu == -1: den *= x**e - 1
    assert num % den == 0
    return num // den

def pool(N):
    g = math.gcd(2**N - 1, 3**N - 1)
    primes = set()
    for d in divisors(N):
        part = math.gcd(phi_d_at(d, 2), g)
        # strip primes already found
        for p in list(primes):
            while part % p == 0: part //= p
        if part > 1:
            f = factorint(part)
            for p in f: primes.add(p)
    rem = g
    for p in primes:
        while rem % p == 0: rem //= p
    assert rem == 1, ("incomplete", rem)
    out = []
    for p in sorted(primes):
        assert isprime(p) and p >= 5
        a, b = n_order(2, p), n_order(3, p)
        e = a * b // math.gcd(a, b)
        assert N % e == 0
        out.append((p, a, b, e))
    return g, out

if __name__ == "__main__":
    N = int(sys.argv[1])
    g, out = pool(N)
    S = sum(Fraction(1, e) for _, _, _, e in out)
    print(f"N={N}  g_N has {len(str(g))} digits; #primes={len(out)}")
    for p, a, b, e in out:
        print(f"  p={p}  ord2={a} ord3={b} e_p={e}")
    print(f"  Sum 1/e_p = {S}  ~ {float(S):.6f}")
    json.dump({"N": N, "g_digits": len(str(g)), "primes": out, "sum": [S.numerator, S.denominator]},
              open(f"/tmp/evidence203/pool_{N}.json", "w"))
