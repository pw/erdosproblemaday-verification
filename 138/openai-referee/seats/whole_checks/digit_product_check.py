#!/usr/bin/env python3
"""Brute-force check of Prop transfer:product (07-transfers.tex) on tiny cyclic colourings.
(1) find 2-colourings C of Z/NZ with no monochromatic a, a+d, ..., a+(k-1)d (d != 0 mod N,
    wrap-around allowed, repeated terms allowed) -- the hypothesis of the proposition;
(2) build the digit-product colouring n -> (C(floor(n/N^i) mod N))_{i<m} of [0, N^m) and
    brute-force every progression a, a+d, ..., a+(k-1)d with d >= 1 inside [0, N^m);
CONTROL A (must FAIL): a colouring of Z/NZ that avoids every NON-wrapping k-AP in {0..N-1}
    but has a wrapping cyclic mono k-AP; its digit product must contain a mono k-AP.
CONTROL B (must FAIL): identity (transfer:division) with N^i NOT dividing d.
EXTERNAL CONTROL: W_2(3) = 9, so no cyclic 3-AP-free 2-colouring of Z/9Z ... Z/12Z may exist."""
import itertools, random, sys

def cyclic_avoids(C, N, k):
    for a in range(N):
        for d in range(1, N):
            c0 = C[a]
            if all(C[(a + j * d) % N] == c0 for j in range(1, k)):
                return False
    return True

def interval_avoids(col, L, k):
    for a in range(L):
        for d in range(1, (L - 1 - a) // (k - 1) + 1 if k > 1 else 1):
            c0 = col[a]
            if all(col[a + j * d] == c0 for j in range(1, k)):
                return (a, d)
    return None

def digit_colour(C, N, m):
    out = []
    for n in range(N ** m):
        out.append(tuple(C[(n // N ** i) % N] for i in range(m)))
    return out

def search(N, k, limit=4):
    found = []
    for bits in range(1 << (N - 1)):          # fix C[0]=0 (colour swap symmetry)
        C = [0] + [(bits >> i) & 1 for i in range(N - 1)]
        if cyclic_avoids(C, N, k):
            found.append(C)
            if len(found) >= limit: break
    return found

print("EXTERNAL CONTROL (W_2(3)=9): cyclic 3-AP-free 2-colourings of Z/NZ, N=3..12:")
for N in range(3, 13):
    print(f"  N={N}: {'some' if search(N, 3, 1) else 'none'}")

for (N, k, ms) in [(3, 3, (1, 2, 3, 4, 5)), (4, 3, (1, 2, 3, 4)), (11, 4, (1, 2, 3))]:
    cols = search(N, k, 2)
    if not cols:
        print(f"N={N},k={k}: no cyclic avoiding colouring found"); continue
    C = cols[0]
    for m in ms:
        bad = interval_avoids(digit_colour(C, N, m), N ** m, k)
        print(f"N={N},k={k},C={''.join(map(str,C))},m={m}: interval [0,{N**m}) with 2^{m} colours: "
              f"{'NO mono k-AP (W_{2^m}(k) > N^m)' if bad is None else 'MONO AP FOUND ' + str(bad)}")

print("\nCONTROL A: colourings avoiding all NON-wrapping k-APs on {0..N-1} but not cyclically:")
for (N, k) in [(8, 3), (16, 4)]:
    ctrl = None
    for bits in range(1 << (N - 1)):
        C = [0] + [(bits >> i) & 1 for i in range(N - 1)]
        if interval_avoids(C, N, k) is None and not cyclic_avoids(C, N, k):
            ctrl = C; break
    if ctrl is None:
        print(f"  N={N},k={k}: none found"); continue
    for m in (2,):
        bad = interval_avoids(digit_colour(ctrl, N, m), N ** m, k)
        print(f"  N={N},k={k},C={''.join(map(str,ctrl))},m={m}: digit product "
              f"{'has NO mono AP (control did not fail!)' if bad is None else 'has mono k-AP (a,d)=' + str(bad) + '  [control FAILS as it must]'}")

print("\nIdentity (transfer:division): floor((a+jd)/N^i) == floor(a/N^i) + j*d/N^i")
random.seed(1)
ok = bad = 0
for _ in range(20000):
    N = random.randint(2, 12); i = random.randint(0, 3); e = random.randint(1, 50)
    d = N ** i * e; a = random.randint(0, 10 ** 6); j = random.randint(0, 40)
    ok += ((a + j * d) // N ** i == a // N ** i + j * e)
print(f"  N^i | d: {ok}/20000 hold")
fails = 0
for _ in range(20000):
    N = random.randint(2, 12); i = random.randint(1, 3); d = random.randint(1, 10 ** 4)
    if d % N ** i == 0: continue
    a = random.randint(0, 10 ** 6); j = random.randint(1, 40)
    # with N^i not dividing d, j*d/N^i is not an integer for j=1: the identity cannot hold
    if (a + j * d) // N ** i * N ** i != (a // N ** i) * N ** i + j * d: fails += 1
print(f"  CONTROL B (N^i does not divide d): identity fails in {fails} random cases [must be > 0]")
