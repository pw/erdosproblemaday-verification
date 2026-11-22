# Numerical sanity check of the Lean SiebertBound Prop (a=1, b=d even) at small y.
import math
Y = 200000; DMAX = 600
n = Y + DMAX + 10
sieve = bytearray([1])*(n+1); sieve[0]=sieve[1]=0
for i in range(2, int(n**0.5)+1):
    if sieve[i]: sieve[i*i::i] = bytearray(len(sieve[i*i::i]))
primes = [i for i in range(2, Y+1) if sieve[i]]
omega = 1.0
for p in range(3, 10**6):
    pass
# twin prime constant omega = prod_{p>2} (1-1/(p-1)^2) ~ 0.6601618158
omega = 0.6601618158468696
def g(d):
    r = 1.0; m = d
    q = 3
    while m % 2 == 0: m //= 2
    while q*q <= m:
        if m % q == 0:
            r *= (q-1)/(q-2)
            while m % q == 0: m //= q
        q += 2
    if m > 1: r *= (m-1)/(m-2)
    return r
worst = (0, None)
for d in range(2, DMAX+1, 2):
    c = 0; gd = g(d)
    for p in primes:
        if sieve[p+d]: c += 1
        if p >= 7:
            bound = 16*omega*gd*p/math.log(p)**2
            r = c/bound
            if r > worst[0]: worst = (r, (d, p, c, bound))
print("max count/bound over y=p in [7,%d], even d<=%d: %.4f at %s" % (Y, DMAX, worst[0], worst[1]))
