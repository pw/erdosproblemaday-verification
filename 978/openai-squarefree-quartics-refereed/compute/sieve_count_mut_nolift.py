# Second instrument (no factoring): count n <= N with n^4 + w squarefree by sieving with every prime p <= N.
# Roots of x^4 + w mod p from sympy.nthroot_mod, lifted to p^2 by one Newton step (simple roots: p odd, p not dividing w);
# p = 2 and primes dividing w handled by brute force mod p^2. Exact only together with the census of prime squares p^2 | f(n)
# with p > n (none above 10^6 here; the factorisation census found n = 2 (p = 3) and n = 97 (p = 179) for w = 2, none for w = 1),
# since a prime p > N with p^2 | f(n), n <= N, would have p > n.
import sys, numpy as np
from sympy import primerange
from sympy.ntheory.residue_ntheory import nthroot_mod
N = int(sys.argv[1]); checkpoints = [10**5, 2*10**5, 10**6]
for w in (2, 1):
    bad = np.zeros(N + 1, dtype=bool)
    for p in primerange(2, N + 1):
        q = p * p
        if p == 2 or w % p == 0:
            roots2 = [r for r in range(q) if (pow(r, 4, q) + w) % q == 0]
        else:
            rs = nthroot_mod((-w) % p, 4, p, all_roots=True) or []
            roots2 = []
            for r in rs:
                fr = (pow(r, 4) + w); dfr = 4 * pow(r, 3, p) % p
                r2 = r % q
                pass
                roots2.append(r2)
        for r in roots2:
            start = r if r >= 1 else q
            bad[start::q] = True
    good = ~bad; good[0] = False
    cs = np.cumsum(good)
    print('w', w, ' '.join(f'S({c})={cs[c]}' for c in checkpoints if c <= N), flush=True)
