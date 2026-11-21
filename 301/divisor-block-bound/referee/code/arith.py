from fractions import Fraction as F
def dens(M):
    d = F(1); m = M; p = 2
    fac = {}
    while m > 1:
        while m % p == 0: fac[p] = fac.get(p, 0) + 1; m //= p
        p += 1
    for p, e in fac.items(): d *= (1 - F(1, p)) / (1 - F(1, p ** (e + 1)))
    return d
iv = lambda a, b, c: c * (F(1, a) - F(1, b))
claimed = [(36,42,1,F(1,252)),(55,77,1,F(2,385)),(77,80,2,F(3,3080)),(80,84,1,F(1,1680)),(84,90,2,F(1,630)),(90,105,1,F(1,630))]
tot = 0
for a,b,c,w in claimed:
    print([a,b], c, iv(a,b,c), 'stated', w, 'OK' if iv(a,b,c)==w else 'MISMATCH'); tot += iv(a,b,c)
print('sum', tot, '== 257/18480?', tot == F(257,18480))
W5040 = F(3907,5040)
W55440 = F(12,11)*W5040 + tot; print('W55440 >=', W55440, W55440 == F(1059,1232))
W720720 = F(14,13)*W55440 + iv(65,66,1); print('W720720 >=', W720720, W720720 == F(15889,17160))
for M in (5040,55440,720720): print('delta', M, dens(M))
C = 1 - dens(720720)*W720720; print('C', C, float(C), C == F(61487,77376))
C2 = 1 - dens(55440)*W55440; print('C at 55440', C2, float(C2)); C1 = 1-dens(5040)*W5040; print('C at 5040', C1, float(C1))
print('claimed improvement', F(92413,116064) - C, F(121717,77376000))
