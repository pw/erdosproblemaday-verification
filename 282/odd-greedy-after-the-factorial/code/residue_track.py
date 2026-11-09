"""Track the denominator b_k mod a prime q along the odd greedy expansion of a/b (x < 1/3), with the modulus sized
from og's claimed numerators (claim only sizes the modulus; every step is recomputed and checked against it)."""
import sys, math, subprocess, gmpy2
from gmpy2 import mpz
from math import gcd
def lcm_upto(n):
    L = mpz(1)
    for k in range(2, n+1): L = L*k//gmpy2.gcd(L, k)
    return L
def track(a, b, claim, q):
    M = mpz(q)
    for k in range(len(claim)-1):
        ak, an = claim[k], claim[k+1]; M *= 2*ak*ak*an*lcm_upto((2*ak-1)//an)
    M *= 2*claim[-1]; bm = mpz(b) % M; out = []
    for k, ak in enumerate(claim):
        out.append((ak, int(bm % q)))
        if ak == 1: break
        r = int((-bm) % ak); q2 = int(((bm + r) % (2*ak)) // ak); s = r if q2 == 1 else r + ak
        n = ((bm + s) % M); assert n % ak == 0; n //= ak; M //= ak
        bn = (bm % M) * (n % M) % M; g = gcd(s, int(bn % s)); assert M % g == 0 and bn % g == 0
        bm = bn // g; M //= g; assert s // g == claim[k+1]
    return out
if __name__ == "__main__":
    N, t, q = map(int, sys.argv[1:4])
    b = t*math.factorial(N) - 1
    subprocess.run(['./og','fact','3',str(N),'100000','/dev/shm/rt.txt',str(t)], capture_output=True, env={'OG_FAST':'1'})
    claim = [int(x) for x in open('/dev/shm/rt.txt').read().split(',')]
    tr = track(3, b, claim, q)
    zero_from = None
    for i, (ak, r) in enumerate(tr):
        if r == 0 and zero_from is None: zero_from = ak
        if r != 0: zero_from = None
    first_off_minus1 = next((ak for ak, r in tr if ak > q and r != q-1), None)
    print(f"3/({t}*{N}!-1) mod {q}: b_k = -1 (mod {q}) holds until numerator {first_off_minus1}; "
          f"b_k = 0 (mod {q}) from numerator {zero_from} onward to the end" if zero_from else
          f"3/({t}*{N}!-1) mod {q}: never settles at 0; residues at the last 4 numerators: {tr[-4:]}")
