# Independent recomputation of Prop "no threshold below 2" explicit instance.
from fractions import Fraction as Fr
import math

def isprime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True

ps = [p for p in range(503, 642) if isprime(p)]
print("cluster primes:", ps, "count", len(ps))
assert len(ps) == 21 and ps[0] == 503 and ps[-1] == 641
print("641/503 =", 641/503, "< sqrt2 =", math.sqrt(2), 641*641 < 2*503*503)
# primes immediately outside, to confirm 503..641 is a full run
print("prev prime < 503:", max(p for p in range(400,503) if isprime(p)), " next prime > 641:", min(p for p in range(642,800) if isprime(p)))
m = ps[-2] * ps[-1]
print("m = p20*p21 =", m)
assert m == 404471
P = 1
for p in ps: P *= p
x = P - 202236
c = Fr(19, 10)
print("I = [x+1, x+m] = [P-%d, P+%d]" % (P-(x+1), x+m-P))

# ---- S-version (atom system alpha_{p,1}=1 for p in cluster; S(n)=#cluster primes dividing n)
def S_small(k):
    return sum(1 for p in ps if k % p == 0)
def W_small(k):  # w_z(k) = sum_p v_p(k) (completely additive, z_p=1)
    t = 0
    for p in ps:
        kk = k
        while kk % p == 0:
            kk //= p; t += 1
    return t

LHS_S = Fr(0); LHS_W = Fr(0)
cntS = {}; sq = []
for k in range(1, m + 1):
    s = S_small(k)
    if s:
        cntS[s] = cntS.get(s, 0) + 1
        if s > c: LHS_S += s - c
        w = W_small(k)
        if w > c: LHS_W += w - c
        if w >= 2 and s == 1: sq.append(k)
print("S-value histogram on [1,m]:", cntS)
print("LHS (S version)  =", LHS_S, "  C(21,2)*(2-c) =", math.comb(21, 2) * (2 - c))
print("LHS (w_z version)=", LHS_W, "  #k<=m with w>=2 but S=1 (prime-square multiples):", len(sq), sq[:5])

# window side via residues: v_p(x+i) for i in 1..m
# x+i mod p^e computed from P mod p^e and offset
RHS_S = Fr(0); RHS_W = Fr(0)
Sw = {}  # i -> (S, W)
for p in ps:
    Pm = P % (p**4)
    for e in (1, 2, 3):
        pass
# For each prime, enumerate i in [1,m] with p | x+i
info = {}
for p in ps:
    q = p
    # x + i ≡ 0 mod p  <=> i ≡ -x mod p
    r = (-x) % p
    i0 = r if r >= 1 else p
    for i in range(i0, m + 1, p):
        b_mod = (x + i)
        # valuation using exact big int arithmetic on residue mod p^6
        v = 0
        t = (x + i) % (p**6)
        if t == 0:
            v = 6  # cap (only P itself could reach high; checked separately)
        else:
            while t % p == 0:
                t //= p; v += 1
        s, w = info.get(i, (0, 0))
        info[i] = (s + 1, w + v)
for i, (s, w) in info.items():
    if s - 1 > 0: RHS_S += s - 1
    if w - 1 > 0: RHS_W += w - 1
big = sorted([(i, sw) for i, sw in info.items() if sw[0] >= 2 or sw[1] >= 2])
print("window points with S>=2:", [(i - 202236, sw) for i, sw in big if sw[0] >= 2])
print("window points with w>=2 (offset from P, (S,w)):", len([1 for i, sw in big if sw[1] >= 2]))
print("RHS (S version)  =", RHS_S)
print("RHS (w_z version)=", RHS_W)
print("S-version hinge at c=19/10 fails:", LHS_S > RHS_S)
print("w_z-version hinge at c=19/10 fails:", LHS_W > RHS_W)
# check P squarefree w.r.t. cluster (trivially) and P in window
assert x + 1 <= P <= x + m
