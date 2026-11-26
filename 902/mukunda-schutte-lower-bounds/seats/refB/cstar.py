"""Referee B: c* of Definition 4.2 (printed p.5) by three routes.
Route 1: closed form Phi = F(a)-F(a-b), mpmath.findroot (Newton), dps 80.
Route 2: Phi as the INTEGRAL int_0^1 ln((a-y)/(a-b-y)) dy by mpmath.quad (tanh-sinh), root by
         plain bisection on a in [2b, 2b+1] (bracket from Lemma 4.1(ii)), dps 40.
Route 3: asymptotic series F(x)=ln x+1-sum_k x^-k/(k(k+1)) and d = a-2b solved by fixed-point in d,
         float128-free, mpmath dps 60 (independent of both closed-form and quadrature code paths).
c* = a_J/2^J + tail, tail = sum_{j>J} d_j/2^j where d_j = a_j - 2a_{j-1} -> 1/2."""
import mpmath as mp

def route1(J=160, dps=80):
    mp.mp.dps = dps
    F = lambda x: mp.mpf(0) if x == 1 else mp.log(x) - (x - 1) * mp.log1p(-1 / x)   # = x ln x-(x-1)ln(x-1), cancellation-free
    Fp = lambda x: -mp.log1p(-1 / x)
    a = [None, mp.mpf(1)]
    for j in range(2, J + 1):
        b = a[-1]
        g = lambda x: F(x) - F(x - b) - mp.log(2)
        x = mp.findroot(g, 2 * b + mp.mpf(1) / 2, df=lambda x: Fp(x) - Fp(x - b))
        assert 2 * b < x < 2 * b + 1
        a.append(x)
    return a

def route2(J=70, dps=40):
    mp.mp.dps = dps
    L2 = mp.log(2)
    a = [None, mp.mpf(1)]
    for j in range(2, J + 1):
        b = a[-1]
        def Phi(x):
            return mp.quad(lambda y: mp.log((x - y) / (x - b - y)), [0, 1])
        lo, hi = 2 * b, 2 * b + 1
        assert Phi(lo) > L2 > Phi(hi)
        for _ in range(dps * 4):
            mid = (lo + hi) / 2
            if Phi(mid) > L2:
                lo = mid
            else:
                hi = mid
        a.append((lo + hi) / 2)
    return a

def route3(J=160, dps=60, K=200):
    mp.mp.dps = dps
    L2 = mp.log(2)
    def Fs(x):  # only used for x >= 2b >= 2 -> series converges geometrically (ratio 1/x)
        s = mp.log(x) + 1
        t = mp.mpf(1)
        for k in range(1, K):
            t /= x
            s -= t / (k * (k + 1))
        return s
    # j=2 has b=1 -> a-b ~1.56 where the series converges slowly; use 400 terms there
    a = [None, mp.mpf(1)]
    for j in range(2, J + 1):
        b = a[-1]
        d = mp.mpf(1) / 2
        KK = K if b > 3 else 3000
        def Fs2(x, KK=KK):
            s = mp.log(x) + 1
            t = mp.mpf(1)
            for k in range(1, KK):
                t /= x
                s -= t / (k * (k + 1))
            return s
        # secant iteration on d in [0,1]
        f = lambda d: Fs2(2 * b + d) - Fs2(b + d) - L2
        d = mp.findroot(f, (mp.mpf('0.4'), mp.mpf('0.6')), solver='secant')
        a.append(2 * b + d)
    return a

def cstar_from(a):
    J = len(a) - 1
    # tail estimate: d_j ~ 1/2 for j > J ; bound |tail - 2^-(J+1)| <= sum 2^-j * |d_j - 1/2|
    return a[J] / mp.mpf(2) ** J + mp.mpf(2) ** (-(J + 1)), a[J] / mp.mpf(2) ** J

if __name__ == '__main__':
    a1 = route1()
    mp.mp.dps = 80
    c1, c1raw = cstar_from(a1)
    print('route1 a_2..a_6 =', [mp.nstr(x, 8) for x in a1[2:7]])
    d = [a1[j] - 2 * a1[j - 1] for j in range(2, len(a1))]
    print('route1 d_j = a_j-2a_{j-1}, j=2..10:', [mp.nstr(x, 10) for x in d[:9]])
    print('route1 d_j strictly decreasing for j=2..160:', all(d[i] > d[i + 1] for i in range(len(d) - 1)),
          ' d_160 - 1/2 =', mp.nstr(d[-1] - mp.mpf(1) / 2, 5))
    print('route1 a_j/2^j strictly increasing:', all(a1[j] / 2 ** j < a1[j + 1] / 2 ** (j + 1) for j in range(1, len(a1) - 1)))
    print('route1 (a_j+1)/2^j < 1 for all j>=2:', all((a1[j] + 1) / mp.mpf(2) ** j < 1 for j in range(2, len(a1))))
    print('route1 c* (J=160, +tail 2^-161) =', mp.nstr(c1, 45))
    print('route1 a_160/2^160            =', mp.nstr(c1raw, 45))
    a2 = route2()
    mp.mp.dps = 40
    c2, c2raw = cstar_from(a2)
    print('route2 (quad+bisection) a_2..a_6 =', [mp.nstr(x, 8) for x in a2[2:7]])
    print('route2 c* (J=70, +tail)       =', mp.nstr(c2, 30))
    a3 = route3()
    mp.mp.dps = 60
    c3, _ = cstar_from(a3)
    print('route3 (series) c* (J=160)    =', mp.nstr(c3, 45))
    print('paper:                          0.76950 32191 50489 43269 90652')
    mp.mp.dps = 80
    print('|route1-route3| =', mp.nstr(abs(c1 - c3), 3), ' |route1-route2| =', mp.nstr(abs(c1 - c2), 3))
