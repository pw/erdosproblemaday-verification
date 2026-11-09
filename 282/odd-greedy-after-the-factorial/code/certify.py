"""Certificate checker for an odd greedy trajectory (distinct odd denominators).
Input: a/b and a CLAIMED numerator sequence (the hand-off numerators printed by og).  The claim is
used ONLY to size a modulus; every s_k, g_k, a_{k+1} is recomputed here from b and compared.
Exit 0 = claim certified (length printed), 1 = claim WRONG, 2 = CANNOT DECIDE (modulus too small).
Own exact prefix phase for x >= 1/3 (no code shared with og.c or check_fixedmod.py)."""
import sys
from math import gcd
import gmpy2
from gmpy2 import mpz

def lcm_upto(n):
    L = mpz(1)
    for k in range(2, n+1): L = L * k // gmpy2.gcd(L, k)
    return L

def prefix(a, b):
    """exact steps while the not-used-before rule could bind; returns (terms, a, b, numerators of the executed steps),
    with a = b = 0 if it terminated inside the prefix."""
    a, b = mpz(a), mpz(b); prev = mpz(1); terms = 0; nums = []
    while True:
        g = gmpy2.gcd(a, b); a //= g; b //= g
        nu = -((-b) // a)                    # ceil(b/a)
        if nu % 2 == 0: nu += 1
        if nu >= prev + 2 and nu >= 5: return terms, a, b, nums
        n = max(nu, prev + 2)
        nums.append(int(a))
        a, b = a*n - b, b*n; terms += 1; prev = n
        if a == 0: return terms, 0, 0, nums

def certify(a0, b0, claim, steps=None):
    """steps: optional list; receives (a_k, s_k, g_k) for every modular step, recomputed here."""
    t, a, b, pnums = prefix(a0, b0)
    if claim[:t] != pnums: return 1, None      # the claimed prefix numerators must match our own exact prefix
    if a == 0: return (0, t) if len(claim) == t else (1, None)
    claim = claim[t:]          # og prints the t prefix numerators first; the rest starts at the hand-off numerator
    if [int(a)] != claim[:1]: return 1, None
    # modulus: per step 2*a_k * a_k * a_{k+1} * lcm(1 .. floor((2a_k-1)/a_{k+1}))  (covers every s = a_{k+1} g < 2a_k)
    M = mpz(1)
    for k in range(len(claim) - 1):
        ak, an = claim[k], claim[k+1]
        M *= 2*ak*ak*an*lcm_upto((2*ak - 1)//an)
    M *= 2*claim[-1]
    bm = b % M; a = int(a); k = 0
    while a != 1:
        if M % (2*a): return 2, None
        r = int((-bm) % a); assert r != 0
        q2 = int(((bm + r) % (2*a)) // a)
        s = r if q2 == 1 else r + a
        if M % (a*s): return 2, None
        n = ((bm + s) % M); assert n % a == 0; n //= a; M //= a
        bn = (bm % M) * (n % M) % M
        g = gcd(s, int(bn % s))
        if M % g: return 2, None
        if steps is not None: steps.append((a, s, g))
        bm = bn // g; M //= g; a = s // g; k += 1
        if k >= len(claim) or a != claim[k]: return 1, None
    return 0, t + k + 1

if __name__ == "__main__":
    import subprocess
    for frac in sys.argv[1:]:
        a0, b0 = map(int, frac.split('/'))
        out = subprocess.run(["./og", "one", str(a0), str(b0)], capture_output=True, text=True).stdout.split("\n")
        claim = [int(x) for x in out[0].split(",")] if out[0] else []
        L_og = int(out[1].split("length=")[1].split()[0])
        rc, L = certify(a0, b0, claim)
        print(f"{frac}: og length {L_og}; certificate rc={rc} length {L} -> {'OK' if rc==0 and L==L_og else 'PROBLEM'}")
