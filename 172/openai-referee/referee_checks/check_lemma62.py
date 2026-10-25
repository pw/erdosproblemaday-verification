import random
from fractions import Fraction
random.seed(11)
def lagrange(nodes, vals):
    n = len(nodes); coeffs = [Fraction(0)]*n
    for j in range(n):
        num = [Fraction(1)]; den = Fraction(1)
        for k in range(n):
            if k == j: continue
            new = [Fraction(0)]*(len(num)+1)
            for i, c in enumerate(num):
                new[i+1] += c; new[i] -= nodes[k]*c
            num = new; den *= (nodes[j]-nodes[k])
        for i in range(len(num)): coeffs[i] += vals[j]*num[i]/den
    return coeffs
def peval(c, x):
    r = Fraction(0)
    for ci in reversed(c): r = r*x + ci
    return r
def pderiv(c): return [i*c[i] for i in range(1, len(c))]
def pmul(a, b):
    out = [Fraction(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): out[i+j] += x*y
    return out
def polydiv(num, den):
    num = num[:]; out = [Fraction(0)]*max(len(num)-len(den)+1, 1)
    while len(num) >= len(den):
        sh = len(num)-len(den); f = num[-1]/den[-1]; out[sh] = f
        for i in range(len(den)): num[sh+i] -= f*den[i]
        num.pop()
    return out, num
def run(Zexp, trials=60):
    passed = failed = 0
    for _ in range(trials):
        e = random.randint(1, 2); qd = random.randint(0, 2); q = e + qd
        H = 2*q + 2 + random.randint(0, 6)
        S = 10**5
        m = 210*random.choice([1, 2, 4, 6])            # w-smooth, W | m  (w = 7)
        t0 = S + random.randint(0, S//2)
        while any((t0 + m*z) % p == 0 for z in range(H) for p in (2, 3, 5, 7)): t0 += 1
        Z = S**Zexp
        # integral-valued rational M (binomial basis), plus noise of size ~ Z^{-e}
        M = [Fraction(0)]
        for k in range(qd+1):
            b = [Fraction(1)]
            for i in range(k): b = pmul(b, [Fraction(-i), Fraction(1)])
            fk = 1
            for i in range(1, k+1): fk *= i
            ck = random.randint(-5, 5)
            M = [ (M[i] if i < len(M) else 0) + (b[i]/fk if i < len(b) else 0)*ck for i in range(max(len(M), len(b)))]
        theta = [M[i] + Fraction(random.randint(-50, 50), 7)/Fraction(Z)**e for i in range(len(M))]
        te = [Fraction(1)]
        for _ in range(e): te = pmul(te, [Fraction(t0), Fraction(m)])
        T = pmul(te, theta)
        nodes = [round(j*(H-1)/q) for j in range(q+1)]
        R = lagrange(nodes, [Fraction(round(peval(T, z))) for z in nodes])
        a = Fraction(-t0, m); d = R[:]; good = True
        for j in range(e):
            if peval(d, a) != 0: good = False; break
            d = pderiv(d)
        if good:
            Mrec, rem = polydiv(R, te)
            good = (not any(rem)) and all(peval(Mrec, z).denominator == 1 for z in range(H))
        passed += good; failed += (not good)
    return passed, failed
print("Z = S^14 (Z dominates powers of S):", run(14))
print("negative control Z = S^1.2-ish (Z = S*10):", end=" ")
# negative control: Z barely above S, the exactness step should fail sometimes
import math
def run_small():
    global S
    return run(1, 60)
print(run_small())
