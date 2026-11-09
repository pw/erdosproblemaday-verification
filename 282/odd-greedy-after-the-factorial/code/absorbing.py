"""Brown's ramp map mod p, in denominator coordinates z = 2m-1:  z -> z(z+k+1)/k  (k = current numerator).
Fixed points: z = 0 (p will divide the denominator when the numerator reaches p: the expansion ends there)
and z = -1 (p | m: p is covered, the ramp passes p). Prints, for primes p, how all p starting residues
(at numerator 3) are distributed at numerator p, i.e. the state that decides what happens at p."""
from collections import Counter
def at_p(z, p):
    for k in range(3, p):                       # numerators 3 .. p-1, all invertible mod p
        z = z * ((z + k + 1) % p) % p * pow(k, -1, p) % p
    return z
for p in [11, 13, 101, 103, 503, 1009, 2003]:
    c = Counter(at_p(z, p) for z in range(p))
    cov, fatal = c.get(p - 1, 0), c.get(0, 0)
    print(f"p={p}: covered (z=-1) {cov}, fatal (z=0) {fatal}, neither {p-cov-fatal}; distinct end states {len(c)}")
# the fixed points
for p in [101, 1009]:
    assert all(0 * (0 + k + 1) * pow(k, -1, p) % p == 0 for k in range(3, p))
    assert all((p - 1) * ((p - 1 + k + 1) % p) * pow(k, -1, p) % p == p - 1 for k in range(3, p))
print("fixed points 0 and -1 verified for p = 101, 1009")
