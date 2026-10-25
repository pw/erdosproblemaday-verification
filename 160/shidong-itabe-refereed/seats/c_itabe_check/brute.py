# Independent (decorrelated from Lean) brute-force of Itabe's construction at small parameters.
# Checks: (1) cubic factor nu_p ABBA-free on [0,p^3); (2) mod-24 label no-three-equal + ABAB-free;
# (3) dyadic label AABB-free; (4) full product gives >=3 colours on every nontrivial 4-AP.
# Every check is paired with a negative control that MUST find violations.
import sys, itertools
import numpy as np

def digits(n, P, L1):           # L1 = L+1 digits, low to high
    out = []
    for _ in range(L1):
        out.append(n % P); n //= P
    return out

def ids_from_tuples(rows):
    d = {}
    return np.array([d.setdefault(r, len(d)) for r in rows], dtype=np.int64)

def min_distinct_over_aps(c, N, want_pattern=None):
    """Return (#APs, #APs with <=2 distinct colours). c: int array length>=N."""
    tot = bad = 0
    for d in range(1, (N - 1) // 3 + 1):
        m = N - 3 * d
        c0, c1, c2, c3 = c[0:m], c[d:d+m], c[2*d:2*d+m], c[3*d:3*d+m]
        k = 1 + (c1 != c0) + ((c2 != c0) & (c2 != c1)) + ((c3 != c0) & (c3 != c1) & (c3 != c2))
        tot += m; bad += int((k <= 2).sum())
    return tot, bad

def pattern_count(c, N, pat):
    """count nontrivial APs whose colours satisfy the equality pattern pat."""
    cnt = 0
    for d in range(1, (N - 1) // 3 + 1):
        m = N - 3 * d
        c0, c1, c2, c3 = c[0:m], c[d:d+m], c[2*d:2*d+m], c[3*d:3*d+m]
        if pat == 'ABBA':   mask = (c0 == c3) & (c1 == c2)
        elif pat == 'AABB': mask = (c0 == c1) & (c2 == c3)
        elif pat == 'ABAB': mask = (c0 == c2) & (c1 == c3)
        elif pat == 'THREE':
            mask = ((c0 == c1) & (c1 == c2)) | ((c0 == c1) & (c1 == c3)) | ((c0 == c2) & (c2 == c3)) | ((c1 == c2) & (c2 == c3))
        cnt += int(mask.sum())
    return cnt

# ---------- cubic factor ----------
def irreducible_cubic(p):
    for a, b, c in itertools.product(range(p), repeat=3):
        if all((x**3 + a*x*x + b*x + c) % p for x in range(p)):
            return (a, b, c)
def gf_mul(g, h, p, f):
    a, b, c = f  # alpha^3 = -(a alpha^2 + b alpha + c)
    prod = [0]*5
    for i in range(3):
        for j in range(3):
            prod[i+j] += g[i]*h[j]
    for k in (4, 3):
        t = prod[k]; prod[k] = 0
        prod[k-1] -= a*t; prod[k-2] -= b*t; prod[k-3] -= c*t
    return [x % p for x in prod[:3]]
def det3(M, p):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1]) - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0]) + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0])) % p
def norm(g, p, f):
    cols = [gf_mul(g, e, p, f) for e in ([1,0,0],[0,1,0],[0,0,1])]
    M = [[cols[j][i] for j in range(3)] for i in range(3)]
    return det3(M, p)
def thirds(r, p): return 0 if 3*r < p else (1 if 3*r < 2*p else 2)
def cubic_colours(p, use_shield=True, use_norm=True):
    f = irreducible_cubic(p)
    rows = []
    for n in range(p**3):
        r, w, u = n % p, (n // p) % p, n // (p*p)
        sh = (thirds(r, p), thirds(w, p)) if use_shield else ()
        nm = norm([r, w, u], p, f) if use_norm else ()
        rows.append((sh, nm))
    return ids_from_tuples(rows), rows

print("== (1) cubic factor nu_p: ABBA-free on [0,p^3) ==")
for p in (5, 7, 11, 13):
    c, _ = cubic_colours(p)
    print(f"p={p}: ABBA count = {pattern_count(c, p**3, 'ABBA')}  palette used = {len(set(c.tolist()))} <= 9p={9*p}")
for p, sh, nm, lab in ((7, False, True, 'norm only (no shield)'), (7, True, False, 'shield only (no norm)')):
    c, _ = cubic_colours(p, sh, nm)
    print(f"NEG CONTROL {lab}: ABBA count = {pattern_count(c, p**3, 'ABBA')} (must be > 0)")
for p in (7, 11):
    rows = [((thirds(n % p, p), thirds((n//p) % p, p)), ((n % p)**2 + ((n//p) % p)**2 + (n//(p*p))**2) % p) for n in range(p**3)]
    c = ids_from_tuples(rows)
    print(f"NEG CONTROL shield x QUADRATIC form mod p (degree 2 instead of 3), p={p}: ABBA count = {pattern_count(c, p**3, 'ABBA')} (must be > 0)")

# ---------- mod-24 label ----------
def lam(n, s, L):
    P = 24*s + 1
    dg = digits(n, P, L+1)
    return (tuple(x % 24 for x in dg[:L]), sum(x*x for x in dg))
def mu(n, B, L):
    dg = digits(n, B, L+1)
    return (tuple((x+1).bit_length()-1 for x in dg[:L]), sum(x*x for x in dg))

print("== (2) mod-24 label lambda: no-three-equal and ABAB-free ==")
for s, L in ((1, 2), (2, 2)):
    P = 24*s+1; N = P**(L+1)
    c = ids_from_tuples([lam(n, s, L) for n in range(N)])
    print(f"s={s} P={P} L={L} N={N}: THREE={pattern_count(c, N, 'THREE')} ABAB={pattern_count(c, N, 'ABAB')}")
# negative control: base without the mod-24 condition (P=26, gcd(P,24)=2) and mod-24 replaced by mod 2
P2 = 26; L = 2; N = P2**3
c = ids_from_tuples([(tuple(x % 2 for x in digits(n, P2, 3)[:2]), sum(x*x for x in digits(n, P2, 3))) for n in range(N)])
print(f"NEG CONTROL (mod-2 carry label, P=26): THREE={pattern_count(c, N, 'THREE')} ABAB={pattern_count(c, N, 'ABAB')} (expect >0 somewhere)")
c = ids_from_tuples([(sum(x*x for x in digits(n, 25, 3)),) for n in range(25**3)])
print(f"NEG CONTROL (square norm only, no carry label, P=25): THREE={pattern_count(c, 25**3, 'THREE')} ABAB={pattern_count(c, 25**3, 'ABAB')} (must be >0)")

print("== (3) dyadic label mu: AABB-free ==")
for B, L in ((4, 3), (8, 3), (16, 2)):
    N = B**(L+1)
    c = ids_from_tuples([mu(n, B, L) for n in range(N)])
    print(f"B={B} L={L} N={N}: AABB={pattern_count(c, N, 'AABB')}")
c = ids_from_tuples([(sum(x*x for x in digits(n, 8, 4)),) for n in range(8**4)])
print(f"NEG CONTROL (norm only, B=8): AABB={pattern_count(c, 8**4, 'AABB')} (must be >0)")

print("== (4) composition logic, exhaustive over equality patterns of 4 positions ==")
def set_partitions(n):
    if n == 0:
        yield []; return
    for part in set_partitions(n - 1):
        for i in range(len(part)):
            yield part[:i] + [part[i] + [n - 1]] + part[i+1:]
        yield part + [[n - 1]]
def labels(part):
    lab = [0]*4
    for b, blk in enumerate(part):
        for x in blk: lab[x] = b
    return tuple(lab)
P = [labels(q) for q in set_partitions(4)]
assert len(P) == 15
three = lambda c: (c[0]==c[1]==c[2]) or (c[0]==c[1]==c[3]) or (c[0]==c[2]==c[3]) or (c[1]==c[2]==c[3])
aabb = lambda c: c[0]==c[1] and c[2]==c[3]
abab = lambda c: c[0]==c[2] and c[1]==c[3]
abba = lambda c: c[0]==c[3] and c[1]==c[2]
viol = ok = 0
for l in P:
    if three(l) or abab(l): continue
    for m in P:
        if aabb(m): continue
        for v in P:
            if abba(v): continue
            prod = [(l[i], m[i], v[i]) for i in range(4)]
            if len(set(prod)) <= 2: viol += 1
            else: ok += 1
print(f"admissible triples={viol+ok}, product with <=2 classes = {viol} (must be 0)")
# negative control: allow ABAB in lambda -> must produce violations
viol2 = 0
for l in P:
    if three(l): continue
    for m in P:
        if aabb(m): continue
        for v in P:
            if abba(v): continue
            if len(set((l[i], m[i], v[i]) for i in range(4))) <= 2: viol2 += 1
print(f"NEG CONTROL (lambda may be ABAB): violations = {viol2} (must be > 0)")
