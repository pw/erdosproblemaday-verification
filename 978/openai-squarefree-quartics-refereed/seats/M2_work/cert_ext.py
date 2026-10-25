from fractions import Fraction as F
G=100000


def _p(d):
    k = d - 2
    for i in range(1, 500):
        t = F(i, 50)
        values = [sum(comb(d-r, j-s) * comb(k, j-1)
                      * k**(j-1) * t**(j-s)
                      for j in range(1, d))
                  for r, s in [(0, 0), (1, 0), (1, 1)]]
        yield (t, *values)

def upper(x, e):
    assert 0 <= x < 1
    l, r = 0, G
    while r > l + 1:
        middle = (l + r) // 2
        if F(middle, G)**e > x:
            r = middle
        else:
            l = middle
    return F(r, G)



epsilon = F(1, 10**6)
etaL, etaH = 1-epsilon, F(3001, 3000)
bL, bH = 4-2*etaH, 2+2*epsilon
t, w = F(1, 2), F(24809, 100000)
m = 3*w
u, v = (etaH-m)/4, (bH-m)/4
assert 0 < epsilon < F(1, 2)
assert 0 < m < 1 and m < min(etaL, bL)
assert w**3*10 > (F(5, 16)*(etaH+bH*t))**4
assert w**2*5 > ((etaH+bH*t)/3)**3
assert min(u, v) > 0 and F(3, 20) <= v/u <= 5
def quartic_delta(h, D):
    return upper((u*v)**h/((2*u+v)**(h-1)*D), h)
P = [quartic_delta(4, u+v), quartic_delta(3, v),
     max(quartic_delta(2, min(3*u, 2*v, u+v)),
         upper(u*u/3, 2)), max(u/2, min(u, v/4))]
assert P == [F(4729, 100000), F(5097, 100000),
             F(6899, 100000), F(76819, 1200000)]
gap = 1-m-sum(max(P[:i]) for i in range(1, 5))
tau = F(1, 50000)
assert gap-4*tau == F(1941, 100000)
assert 1-m-2*u-2*tau == F(15319, 120000)

print('EXT CERT OK', P, gap)
