# K. S. Brown's "coverage" (MathPages kmath478): iterate m -> (m/n)(2m+n-1) mod p for n = n0..p-1; p is covered iff
# m == 0 (mod p) when the numerator reaches p.  Compares EVERY row of Brown's favorable-residue table (parsed from a
# saved copy of the page, kmath478.htm) and his three prime counts.
import re, html, sys
from sympy import primerange, factorial
def covered(m0, n0, p):
    m = m0 % p
    for n in range(n0, p):
        if m == 0: return True
        m = m * pow(n, -1, p) % p * ((2*m + n - 1) % p) % p
    return m == 0
page = sys.argv[1] if len(sys.argv) > 1 else '/tmp/e1109/kmath478.htm'
t = html.unescape(re.sub(r'<[^>]+>', ' ', open(page, errors='replace').read()))
rows = {}
for line in t.split('\n'):
    x = line.split()
    if len(x) == 11 and all(v.isdigit() for v in x): rows[int(x[0])] = list(map(int, x[1:]))
match = []
for p, row in sorted(rows.items()):
    got = [sum(covered(r, n0, p) for r in range(p)) if n0 < p else 0 for n0 in range(1, 11)]
    if got == row: match.append(p)
    else: print(f"p={p}: Brown {row} ours {got}")
print(f"Brown's table: {len(match)} of {len(rows)} rows identical (p = {match[0]} .. {match[-1]} except those printed above)")
for N, lo, hi, claim in [(50, 50, 100, '6 of 10'), (100, 100, 200, '10 of 20'), (500, 500, 1000, '32 of 64')]:
    ps = list(primerange(lo, hi))
    for lab, m0 in [('m=N!', factorial(N)), ('m=N!/2', factorial(N)//2)]:
        c = sum(covered(int(m0 % p), 3, p) for p in ps)
        print(f"{N}! counts, {lab}: covered {c} of {len(ps)} primes in ({lo},{hi})   [Brown wrote: {claim}]")
