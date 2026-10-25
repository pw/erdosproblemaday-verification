import itertools, random
from fractions import Fraction
from math import prod
random.seed(7)

# Corollary 1.2: sequences with a1 > 2, a_d > 2(sum_{k<d} a_k + prod_{k<d} a_k)
def seq(m, minimal=True):
    a = [3 if minimal else random.randint(3, 50)]
    for d in range(1, m):
        lo = 2*(sum(a) + prod(a)) + 1
        a.append(lo if minimal else lo + random.randint(0, 10**3))
    return a
for trial in range(300):
    m = random.randint(1, 6)
    a = seq(m, minimal=(trial % 3 == 0))
    S = {}; P = {}
    for r in range(1, m+1):
        for B in itertools.combinations(range(m), r):
            s = sum(a[i] for i in B); p = prod(a[i] for i in B)
            assert s not in S, ("sum collision", a, B, S[s]); S[s] = B
            assert p not in P, ("prod collision", a, B, P[p]); P[p] = B
    inter = set(S) & set(P)
    assert inter == set(a), (a, inter)
    assert len(set(S) | set(P)) == 2*(2**m - 1) - m
print("Cor 1.2: 300 sequences, injectivity and FS∩FP = A confirmed")

# Lemma 6.2: exactness after interpolation.
# Build theta(z) = Mpoly(z) + noise with |noise| <= A Z^{-e}; check ||t_z^e theta|| small, then run the
# paper's algorithm (nearest-integer interpolation at q+1 nodes, exact rational arithmetic) and confirm
# R^{(j)}(a)=0 for j<e and R = t^e * M with M integral at nodes.
def lagrange(nodes, vals):
    # returns coefficient list (low->high) as Fractions
    n = len(nodes); coeffs = [Fraction(0)]*n
    for j in range(n):
        num = [Fraction(1)]; den = Fraction(1)
        for k in range(n):
            if k == j: continue
            num = [Fraction(0)] + num
            for idx in range(len(num)-1):
                num[idx] -= nodes[k]*num[idx+1]
            den *= (nodes[j]-nodes[k])
        for idx in range(len(num)):
            coeffs[idx] += vals[j]*num[idx]/den
    return coeffs
def peval(c, x):
    return sum(ci * x**i for i, ci in enumerate(c))
def pderiv(c):
    return [i*c[i] for i in range(1, len(c))]
def polydiv(num, den):
    num = num[:]; out = [Fraction(0)]*(max(len(num)-len(den)+1, 1))
    while len(num) >= len(den) and any(num):
        sh = len(num)-len(den); f = num[-1]/den[-1]; out[sh] = f
        for i in range(len(den)): num[sh+i] -= f*den[i]
        num.pop()
    return out, num
ok = 0
for trial in range(40):
    e = random.randint(1, 2); qd = random.randint(0, 2); q = e + qd
    H = 2*q + 2 + random.randint(0, 6)
    W = 2*3*5*7
    S = 10**6
    m = random.choice([2, 4, 6, 12, 30, 60])           # w-smooth step
    t0 = S + random.randint(0, S//2)
    while any((t0 + m*z) % p == 0 for z in range(H) for p in (2,3,5,7)): t0 += 1
    Z = S**(3*q + 6)
    Mpoly = [Fraction(random.randint(-5, 5)) for _ in range(qd+1)]
    # make M integral at integers via binomial-type? use integer coeffs (integral everywhere)
    noise = [Fraction(random.randint(-10, 10), 7) / Fraction(Z)**e for _ in range(qd+1)]
    theta = [Mpoly[i] + noise[i] for i in range(qd+1)]
    lin = [Fraction(t0), Fraction(m)]
    te = [Fraction(1)]
    for _ in range(e):
        te = [sum(te[i]*lin[k-i] for i in range(len(te)) if 0 <= k-i < 2) for k in range(len(te)+1)]
    T = [sum(te[i]*theta[k-i] for i in range(len(te)) if 0 <= k-i < len(theta)) for k in range(len(te)+len(theta)-1)]
    nodes = [round(j*(H-1)/q) for j in range(q+1)]
    vals = [Fraction(round(peval(T, z))) for z in nodes]
    R = lagrange(nodes, vals)
    a = Fraction(-t0, m)
    d = R[:]
    for j in range(e):
        assert peval(d, a) == 0, "R^(j)(a) != 0"
        d = pderiv(d)
    Mrec, rem = polydiv(R, te)
    assert not any(rem)
    for z in range(H):
        assert peval(Mrec, z).denominator == 1
        assert abs(peval(theta, z) - peval(Mrec, z)) * Fraction(Z)**e < 100
    ok += 1
print("Lemma 6.2: %d random instances, exact root multiplicity and integral M recovered" % ok)
