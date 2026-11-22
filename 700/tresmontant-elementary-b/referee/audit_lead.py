#!/usr/bin/env python3
"""Stage C: can the lead's check700.py go red? Load ONLY its function definitions (no top-level run) and probe them."""
import ast, math, sys, random
import numpy as np
from ref700 import sieve, f_enum2, hyp

src = open('/home/exedev/MathDyad/erdos700/tresmontant/check700.py').read()
tree = ast.parse(src)
keep = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
ns = {}
exec(compile(ast.Module(body=keep, type_ignores=[]), 'check700_defs', 'exec'), ns)
sge = ns['small_gcd_exists']; fb = ns['f_brute']; ndl = ns['ndigits_le']

PR = sieve(5000); PS = set(PR)

# C-a: positive controls for the reduced test (it must say True where f <= sqrt n and r < pq)
for t in [(103, 107, 113), (457, 461, 463), (101, 107, 109), (1009, 1019, 1021)]:
    p, q, r = t; n = p * q * r; f = f_enum2(t)
    print(f"Ca {t} r<pq:{r<p*q} hyp:{hyp(*t)} small_gcd_exists={bool(sge(*t))} my f={f} f<=sqrt n:{f*f<=n}")

# C-b: agreement of the lead's reduced test with my exact f on random odd-prime triples with r<pq (incl. large r, p=2 too)
random.seed(700); agree = dis = tru = fal = 0
for _ in range(1500):
    p, q, r = sorted(random.sample(PR[:400], 3))
    if r >= p * q: continue
    f = f_enum2((p, q, r)); n = p * q * r; s = bool(sge(p, q, r))
    if s == (f * f <= n): agree += 1
    else: dis += 1; print("Cb DISAGREE", p, q, r, f, s)
    tru += s; fal += (not s)
print(f"Cb random triples (primes<2750, r<pq): agree={agree} disagree={dis}; reduced test True={tru} False={fal}")

# C-c: p=2 triples (excluded from the lead's validation loop, which starts primerange at 3)
agree = dis = 0
for q in PR[1:40]:
    for r in PR:
        if r <= q: continue
        if r >= 2 * q: break
        f = f_enum2((2, q, r)); s = bool(sge(2, q, r))
        if s == (f * f <= 2 * q * r): agree += 1
        else: dis += 1; print("Cc DISAGREE", 2, q, r, f, s)
print(f"Cc p=2 triples with r<2q: agree={agree} disagree={dis}")

# C-d: the lead's validation set (primes in [3,140), n<=3e6, r<pq): how many have f>sqrt n (i.e. could catch a vacuous 'always True')?
P = [x for x in PR if 3 <= x < 140]; cntT = cntF = 0
for i in range(len(P)):
    for j in range(i + 1, len(P)):
        for k in range(j + 1, len(P)):
            p, q, r = P[i], P[j], P[k]
            if p * q * r > 3_000_000 or r >= p * q: continue
            if sge(p, q, r): cntT += 1
            else: cntF += 1
print(f"Cd lead's validation set: reduced test True (f<=sqrt n) {cntT}, False (f>sqrt n) {cntF}")
# and how many triples with r<pq, n<=3e6, odd primes exist without the r<140 cap
tot = 0
for i, p in enumerate(PR):
    if p == 2: continue
    if p ** 3 > 3_000_000: break
    for j in range(i + 1, len(PR)):
        q = PR[j]
        if p * q * q > 3_000_000: break
        for k in range(j + 1, len(PR)):
            r = PR[k]
            if p * q * r > 3_000_000 or r >= p * q: break
            tot += 1
print(f"Cd all odd-prime triples with r<pq and n<=3e6 (no r<140 cap): {tot}")

# C-e: mutation — loosen the hypothesis (2e^2 < 3p, keep h>d) and run the lead's exhaustive loop logic; it must print counterexamples
def lead_loop(pmax, factor):
    cnt = bad = 0; ex = []
    ps = [x for x in PR if x >= 3]
    for a, p in enumerate(ps):
        if p > pmax: break
        for b in range(a + 1, len(ps)):
            q = ps[b]
            if 2 * (q - p) ** 2 >= factor * p: break
            for c in range(b + 1, len(ps)):
                r = ps[c]
                if 2 * (r - p) ** 2 >= factor * p: break
                if r - q <= q - p: continue
                cnt += 1
                if sge(p, q, r):
                    bad += 1
                    if len(ex) < 5: ex.append((p, q, r, f_enum2((p, q, r))))
    return cnt, bad, ex
for fac in (1, 2, 3):
    cnt, bad, ex = lead_loop(2000, fac)
    print(f"Ce lead's exhaustive logic with 2e^2 < {fac}p, p<=2000: triples={cnt}, flagged={bad}, first flagged (with my exact f): {ex}")

# C-f: ndigits_le spot-check against a scalar digit comparison
def dom(a, b, s):
    while b or a:
        if a % s > b % s: return False
        a //= s; b //= s
    return True
random.seed(1); badd = 0
for _ in range(20000):
    s = random.choice(PR[:200]); b = random.randrange(1, 10**9); a = random.randrange(0, b + 1)
    if bool(ndl(np.array([a], dtype=np.int64), b, s)[0]) != dom(a, b, s): badd += 1
print(f"Cf ndigits_le vs scalar dominance on 20000 random cases: mismatches={badd}")
