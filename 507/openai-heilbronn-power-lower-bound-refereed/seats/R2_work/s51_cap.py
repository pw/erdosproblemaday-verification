# Lemma 5.1 / 5.2 checks.
import itertools, random, math, sys
from sympy import isprime, nextprime

def nonsquare(q):
    sq = {(x*x) % q for x in range(q)}
    for v in range(1, q):
        if v not in sq: return v

def gamma(q):
    nu = nonsquare(q)
    return [(x, y, (x*x - nu*y*y) % q) for x in range(q) for y in range(q)]

def collinear(p, r, s, q):
    # p,r,s distinct points in F_q^3; collinear iff r-p, s-p linearly dependent
    u = [(r[i]-p[i]) % q for i in range(3)]
    v = [(s[i]-p[i]) % q for i in range(3)]
    cr = [(u[1]*v[2]-u[2]*v[1]) % q, (u[2]*v[0]-u[0]*v[2]) % q, (u[0]*v[1]-u[1]*v[0]) % q]
    return cr == [0, 0, 0]

# (1) line property of Gamma, exhaustive for small odd q
for q in [3, 5, 7, 11, 13]:
    G = gamma(q)
    bad = 0
    for p, r, s in itertools.combinations(G, 3):
        if collinear(p, r, s, q): bad += 1
    # also: Q vanishes only at (0,0)
    nu = nonsquare(q)
    zeros = [(x, y) for x in range(q) for y in range(q) if (x*x - nu*y*y) % q == 0]
    print(f"q={q}: |Gamma|={len(G)} collinear triples={bad} zeros of Q={zeros}")

# (2) averaging over translates: exact max over b of |(b+Gamma) cap box| vs w^3/q
def best_translate(q, w):
    nu = nonsquare(q)
    box = [(X, Y, Z) for X in range(w) for Y in range(w) for Z in range(w)]
    best = (-1, None)
    tot = 0
    for b1 in range(q):
        for b2 in range(q):
            hist = {}
            for X, Y, Z in box:
                x, y = (X - b1) % q, (Y - b2) % q
                b3 = (Z - (x*x - nu*y*y)) % q
                hist[b3] = hist.get(b3, 0) + 1
            tot += sum(hist.values())
            m = max(hist.values())
            if m > best[0]: best = (m, (b1, b2, max(hist, key=hist.get)))
    avg = tot / q**3
    return best, avg

for q, w in [(11, 6), (13, 5), (17, 9), (31, 7), (2003, 2)]:
    (m, b), avg = best_translate(q, w)
    print(f"q={q} w={w}: max over translates {m}, average {avg:.6f}, w^3/q={w**3/q:.6f}  ok={m>=w**3/q and abs(avg-w**3/q)<1e-9}")
