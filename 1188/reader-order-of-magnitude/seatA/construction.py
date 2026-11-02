#!/usr/bin/env python3
"""Referee A: literal implementation of Construction 3.1 + exact checker over Z/L.

Usage: python3 construction.py
"""
import itertools, math, random, sys, time
from functools import reduce
import numpy as np

def lcm(a, b):
    return a // math.gcd(a, b) * b

def is_prime(n):
    if n < 2:
        return False
    for d in range(2, math.isqrt(n) + 1):
        if n % d == 0:
            return False
    return True

def prime_power(n):
    """return (j,k) if n=j^k (k>=1, j prime) else None"""
    if n < 2:
        return None
    for j in range(2, n + 1):
        if n % j == 0:
            k = 0; m = n
            while m % j == 0:
                m //= j; k += 1
            return (j, k) if m == 1 else None

# ------------------------------------------------------------------ checker
def check(system, xmax=None, verbose=False):
    """system: list of (a, n). Returns (ok, reasons). Independent of the paper:
    distinct moduli >= 2, union of classes = Z (tested on Z/L, L = lcm of moduli),
    minimal (each class has a residue covered by it alone), max modulus <= xmax."""
    reasons = []
    mods = [n for _, n in system]
    if any(n < 2 for n in mods):
        reasons.append("modulus < 2")
    if len(set(mods)) != len(mods):
        reasons.append("moduli not distinct")
    if xmax is not None and max(mods) > xmax:
        reasons.append(f"max modulus {max(mods)} > {xmax}")
    L = reduce(lcm, mods, 1)
    cnt = np.zeros(L, dtype=np.int32)
    for a, n in system:
        cnt[a % n::n] += 1
    if cnt.min() < 1:
        reasons.append(f"not a covering: {int((cnt == 0).sum())} residues mod {L} uncovered")
    else:
        for a, n in system:
            if not (cnt[a % n::n] == 1).any():
                reasons.append(f"class {a % n} mod {n} has no private residue (not minimal)")
                break
    return (len(reasons) == 0, reasons, L)

# ------------------------------------------------------------------ Construction 3.1
def crt0(r, m, s):
    """z ≡ r (mod m), z ≡ 0 (mod s), gcd(m,s)=1 -> residue mod m*s"""
    assert math.gcd(m, s) == 1
    # z = s*k, s*k ≡ r mod m
    k = (r * pow(s, -1, m)) % m if m > 1 else 0
    return (s * k) % (m * s), m * s

def setup(P):
    assert is_prime(P) and P >= 5
    Q = [q for q in range(2, P) if prime_power(q)]
    dstars = [d for d in (P + 1, P + 3) if prime_power(d) is None]
    return Q, dstars

def build(P, sigma, iota, tau):
    """sigma[q] = dict u -> sigma_q(u); iota[q]; tau = list of length P. Returns list of (a,n)."""
    Q, dstars = setup(P)
    sysm = []
    for q in Q:
        j, k = prime_power(q)
        qo = q // j
        for u in range(1, j):
            s = sigma[q][u]
            sysm.append(crt0((qo * u) % q, q, s))
    for t in range(P):
        sysm.append(crt0(t % P, P, tau[t]))
    return sysm

def valid_data(P, sigma, iota, tau, dstar):
    Q, _ = setup(P)
    for q in Q:
        j, _ = prime_power(q)
        vals = [sigma[q][u] for u in range(1, j)]
        assert len(set(vals)) == j - 1 and all(1 <= s <= q - 1 and s % j for s in vals), (q, vals)
    assert len(set(iota[q] for q in Q)) == len(Q) and all(1 <= iota[q] <= P - 1 for q in Q)
    assert sorted(tau) == sorted(list(range(1, P)) + [dstar]) and tau[0] == 1
    assert all(tau[iota[q]] == q for q in Q)

def all_sigma_choices(q):
    j, _ = prime_power(q)
    target = [s for s in range(1, q) if s % j]
    for img in itertools.permutations(target, j - 1):
        yield {u: img[u - 1] for u in range(1, j)}

def all_iota(P, Q):
    for img in itertools.permutations(range(1, P), len(Q)):
        yield dict(zip(Q, img))

def all_tau(P, Q, iota, dstar):
    used_args = {0} | set(iota.values())
    free_args = [t for t in range(P) if t not in used_args]
    free_vals = [v for v in list(range(1, P)) + [dstar] if v != 1 and v not in Q]
    assert len(free_args) == len(free_vals)
    for img in itertools.permutations(free_vals):
        tau = [None] * P
        tau[0] = 1
        for q in Q:
            tau[iota[q]] = q
        for t, v in zip(free_args, img):
            tau[t] = v
        yield tau

def random_data(P, rng, dstar=None):
    Q, dstars = setup(P)
    dstar = dstar or rng.choice(dstars)
    sigma = {}
    for q in Q:
        j, _ = prime_power(q)
        target = [s for s in range(1, q) if s % j]
        img = rng.sample(target, j - 1)
        sigma[q] = {u: img[u - 1] for u in range(1, j)}
    img = rng.sample(range(1, P), len(Q))
    iota = dict(zip(Q, img))
    taus = list(all_tau(P, Q, iota, dstar)) if math.factorial(P - 1 - len(Q)) <= 5040 else None
    if taus is None:
        used = {0} | set(iota.values())
        free_args = [t for t in range(P) if t not in used]
        free_vals = [v for v in list(range(1, P)) + [dstar] if v != 1 and v not in Q]
        rng.shuffle(free_vals)
        tau = [None] * P; tau[0] = 1
        for q in Q: tau[iota[q]] = q
        for t, v in zip(free_args, free_vals): tau[t] = v
    else:
        tau = rng.choice(taus)
    return sigma, iota, tau, dstar

def canon(system):
    return frozenset((n, a % n) for a, n in system)

# ------------------------------------------------------------------ main
if __name__ == "__main__":
    out = []
    def say(*a):
        s = " ".join(str(x) for x in a); print(s, flush=True); out.append(s)

    # controls
    good = [(0, 2), (0, 3), (1, 4), (5, 6), (7, 12)]
    say("POS CONTROL classical system:", check(good, 12))
    say("NEG CONTROL drop 7 mod 12:", check(good[:-1], 12))
    say("NEG CONTROL add redundant 0 mod 8:", check(good + [(0, 8)], 12))
    say("NEG CONTROL repeated modulus (add 3 mod 6 -> 6 used twice):", check(good + [(3, 6)], 12))
    say("NEG CONTROL modulus over xmax (xmax=11):", check(good, 11))
    say("NEG CONTROL shift a class (1 mod 4 -> 3 mod 4):", check([(0, 2), (0, 3), (3, 4), (5, 6), (7, 12)], 12))

    # Example 3.3, literally
    P = 5
    sigma = {2: {1: 1}, 3: {1: 1, 2: 2}, 4: {1: 1}}
    iota = {2: 1, 3: 2, 4: 3}
    tau = [1, 2, 3, 4, 6]
    valid_data(P, sigma, iota, tau, 6)
    ex = build(P, sigma, iota, tau)
    say("Example 3.3 built:", sorted((n, a % n) for a, n in ex))
    say("Example 3.3 printed: [(2,1),(3,1),(6,2),(4,2),(5,0),(10,6),(15,12),(20,8),(30,24)]")
    say("Example 3.3 matches print:", canon(ex) == canon([(1,2),(1,3),(2,6),(2,4),(0,5),(6,10),(12,15),(8,20),(24,30)]))
    say("Example 3.3 check:", check(ex, P * (P + 3)))

    # full enumeration of all data for P = 5 and P = 7
    for P in (5, 7):
        Q, dstars = setup(P)
        t0 = time.time()
        nd = 0; bad = 0; systems = set(); maxmod = 0
        for dstar in dstars:
            sig_lists = [list(all_sigma_choices(q)) for q in Q]
            for iota in all_iota(P, Q):
                for tau in all_tau(P, Q, iota, dstar):
                    for sigs in itertools.product(*sig_lists):
                        sigma = dict(zip(Q, sigs))
                        valid_data(P, sigma, iota, tau, dstar)
                        s = build(P, sigma, iota, tau)
                        ok, why, L = check(s, P * (P + 3))
                        nd += 1
                        if not ok:
                            bad += 1
                            if bad <= 3: say("  FAIL", P, why)
                        systems.add(canon(s)); maxmod = max(maxmod, max(n for _, n in s))
        bound = math.prod(math.factorial(p - 1) for p in range(2, P) if is_prime(p))
        say(f"P={P}: Q={Q}, d* options={dstars}; data enumerated={nd}, failures={bad}, "
            f"distinct systems={len(systems)}, prod_(p<P)(p-1)!={bound}, max modulus={maxmod} <= P(P+3)={P*(P+3)}  [{time.time()-t0:.1f}s]")
        nclass = sum(prime_power(q)[0] - 1 for q in Q) + P
        say(f"   classes per system: {nclass} (paper: sum (j(q)-1) + P)")

    # P = 11: fix iota, tau, sigma_q (q not prime); vary sigma_p over all permutations (Theorem 1.2's count)
    rng = random.Random(11880)
    for P in (11,):
        Q, dstars = setup(P)
        for dstar in dstars:
            sigma0, iota, tau, _ = random_data(P, rng, dstar)
            primesQ = [q for q in Q if is_prime(q)]
            t0 = time.time(); nd = 0; bad = 0; systems = set()
            for perms in itertools.product(*[list(itertools.permutations(range(1, p))) for p in primesQ]):
                sigma = dict(sigma0)
                for p, img in zip(primesQ, perms):
                    sigma[p] = {u: img[u - 1] for u in range(1, p)}
                valid_data(P, sigma, iota, tau, dstar)
                s = build(P, sigma, iota, tau)
                ok, why, L = check(s, P * (P + 3))
                nd += 1
                if not ok:
                    bad += 1
                    if bad <= 3: say("  FAIL", P, why)
                systems.add(canon(s))
            bound = math.prod(math.factorial(p - 1) for p in primesQ)
            say(f"P={P}, d*={dstar}: sigma_p varied over all {nd} choices (others fixed, iota={iota}, tau={tau}); "
                f"failures={bad}; distinct systems={len(systems)}; prod (p-1)!={bound}; L={L}  [{time.time()-t0:.1f}s]")

    # random data for P = 11, 13, 17 (exhaustive check over Z/L for each)
    for P, reps in ((11, 300), (13, 60), (17, 6)):
        Q, dstars = setup(P)
        t0 = time.time(); bad = 0; Ls = set()
        for _ in range(reps):
            sigma, iota, tau, dstar = random_data(P, rng)
            valid_data(P, sigma, iota, tau, dstar)
            s = build(P, sigma, iota, tau)
            ok, why, L = check(s, P * (P + 3))
            Ls.add(L)
            if not ok:
                bad += 1
                if bad <= 3: say("  FAIL", P, why)
        say(f"P={P}: {reps} random data, failures={bad}, d* options={dstars}, L values={sorted(Ls)}  [{time.time()-t0:.1f}s]")

    open("construction.out", "w").write("\n".join(out) + "\n")
