# Check the (outer:second-weight) analysis:
#  (a) f(h) = log(CDh)/h is decreasing for h >= D^2 once D is large (C >= 1);
#  (b) sup_{h > D^2} 6D log(CDh)/h <= 6 log(C D^3)/D;
#  (c) threshold D* with 6 log(C D^3)/D <= 1/128, after which every summand
#      (CDh)^{6D} e^{-h/64} <= e^{-h/128}, and the tail sum_{h>D^2} e^{-h/128} is tiny;
#  explicit C from the proof of count:local: C0 = 9*16005^2 (9(16004Dh+1)^2 <= C0 (Dh)^2), C = C0^{1/3}.
import math, sys

def step_decreasing(C, D, h):
    # sign of f(h) - f(h+1) = [log(CDh) - h*log1p(1/h)] / (h(h+1))
    return math.log(C*D*h) - h*math.log1p(1.0/h) > 0

def check_decreasing(C, D, steps=20000):
    h0 = D*D
    hs = list(range(h0, h0+steps)) + [int(h0*1.37**i) for i in range(1, 120)]
    return all(step_decreasing(C, D, h) for h in hs)

def check_sup(C, D, a=6):
    h0 = D*D
    bound = a*math.log(C*D**3)/D
    hs = [h0+1+i for i in range(5000)] + [int(h0*1.21**i) for i in range(1, 200)]
    return max(a*D*math.log(C*D*h)/h for h in hs) <= bound*(1+1e-12)

def threshold(C, a=6):
    D = 2
    while a*math.log(C*D**3)/D > 1/128: D += 1
    return D

def summand_ok(C, D, a=6):
    # log[(CDh)^{aD} e^{-h/64}] <= -h/128 at h = D^2+1 .. and geometric samples
    h0 = D*D
    hs = [h0+1+i for i in range(2000)] + [int(h0*1.11**i) for i in range(1, 400)]
    worst = max(a*D*math.log(C*D*h) - h/64 + h/128 for h in hs)
    return worst <= 0, worst

def main():
    C0 = 9*16005**2
    Cpf = C0**(1/3)
    print('C0 = 9*16005^2 =', C0, ' C = C0^(1/3) = %.3f  (count:local proof constant)' % Cpf)
    for C in (1, 2, Cpf, 1e6, float(C0)):
        for D in (2, 3, 5, 10, 100, 1000, 30000):
            assert math.log(C*D**3) >= 1, (C, D)
            assert check_decreasing(C, D), (C, D)
            assert check_sup(C, D), (C, D)
    print('(a),(b) verified for C in {1,2,%.1f,1e6,%d}, D in {2,3,5,10,100,1000,30000}' % (Cpf, C0))
    for C, a, name in ((1, 6, 'C=1, (CDh)^{6D}'), (Cpf, 6, 'paper C, (CDh)^{6D}'), (16005, 14, 'Lean (16005Dh)^{14D}')):
        Ds = threshold(C, a)
        ok, worst = summand_ok(C, Ds, a)
        logtail = -(Ds*Ds+1)/128 - math.log(1-math.exp(-1/128))
        print('%-24s D* = %6d (k > (D*-1)^10 ~ 10^%.1f); summand<=e^{-h/128} at D*: %s (max log-excess %.3g); log10(tail sum) <= %.4g'
              % (name, Ds, 10*math.log10(Ds-1), ok, worst, logtail/math.log(10)))
    print('--- CONTROLS (each must FAIL) ---')
    print('CONTROL C=1, D=1 decreasing from h=D^2:', check_decreasing(1, 1), ' f(1)=%.4f f(2)=%.4f' % (math.log(1)/1, math.log(2)/2))
    print('CONTROL C=0.1, D=2 decreasing from h=D^2:', check_decreasing(0.1, 2))
    ok, worst = summand_ok(Cpf, 1000)
    print('CONTROL summand bound at D=1000 (k~10^30), paper C: %s (log-excess %.4g at worst sampled h)' % (ok, worst))
    print('CONTROL sup bound with D^2 replaced by D (h > D) at D=100, C=1: ',
          max(6*100*math.log(100*h)/h for h in range(101, 20000)) <= 1/128)
    return 0
sys.exit(main())
