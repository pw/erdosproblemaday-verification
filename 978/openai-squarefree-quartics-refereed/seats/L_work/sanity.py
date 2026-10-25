# Sanity instance f = X^4+2, k = 2, using the Lean Model definitions literally.
from sympy import primerange, isprime
f = lambda n: n**4 + 2
def rho(q):  # Lean: ((Finset.range q).filter fun a => (q:Z) | f a).card
    return sum(1 for a in range(q) if f(a) % q == 0)
# LocallyAdmissible: rho(p^k) < p^k for every prime p. For p^2 > 3 and p not 2... check small p by definition,
# and argue large p: f(0)=2 is not divisible by p^2 for any p, so rho(p^2) <= p^2-1.
bad = [p for p in primerange(2, 200) if not rho(p*p) < p*p]
print("primes p<200 violating LocallyAdmissible:", bad)
print("rho(4)=", rho(4), " rho(9)=", rho(9), " rho(p^2) for p<60:", [(p, rho(p*p)) for p in primerange(3, 60)])
# density constant: prod over p of (1 - rho(p^2)/p^2); for odd p (p does not divide disc=2^11) rho(p^2)=#roots of x^4+2 mod p
import math
def roots_mod_p(p):
    return sum(1 for a in range(p) if (a**4 + 2) % p == 0)
logc = math.log(1 - rho(4)/4)
for p in primerange(3, 300000):
    r = roots_mod_p(p) if p < 3000 else None
    if r is None:
        # count roots via pow trick: x^4 = -2 mod p
        # number of solutions = number of x with x^4 == p-2
        g = math.gcd(4, p-1)
        t = (p - 2) % p
        r = g if pow(t, (p-1)//g, p) == 1 else 0
    logc += math.log(1 - r/(p*p))
print("density constant c (primes < 3e5) ~", math.exp(logc))
# empirical: n <= N with n^4+2 having no p^2 | n^4+2 for p < B (large p^2 contribution heuristically negligible)
N, B = 20000, 20000
ps = list(primerange(2, B))
cnt = 0
for n in range(1, N+1):
    v = f(n); ok = True
    for p in ps:
        if p*p > v: break
        if v % (p*p) == 0: ok = False; break
    cnt += ok
print(f"N={N}: #(n<=N, n^4+2 free of p^2 for p<{B}) = {cnt}, ratio {cnt/N:.5f}")
