# L2, L3 of (6.13) by mpmath tanh-sinh nested quadrature on the ORIGINAL integrands (x-variables, no reductions),
# vs the paper's closed forms (6.15),(6.16).  Control: the perturbed integrand A_m = sum x + 2 x_m must disagree.
import mpmath as mp
mp.mp.dps = 25
lam = mp.log(2)
def L2(pert=False):
    def inner(x2):
        def g(x1):
            Am = x1 + 2*x2 + (x2 if pert else 0)
            return (1/(x1*x2))*2/x2*((Am**3-8)/24 - (Am-2)/2)
        return mp.quad(g, [x2, 2])
    return mp.quad(inner, [1, 2])
def L3(pert=False):
    def f3(x3):
        def f2(x2):
            def f1(x1):
                Am = x1 + x2 + 2*x3 + (x3 if pert else 0); Ap = 2*x1 + (x1 if pert else 0)
                return 2/x3*(Am**3 - Ap**3)/24/(x1*x2*x3)
            return mp.quad(f1, [x2, 2])
        return mp.quad(f2, [x3, 2])
    return mp.quad(f3, [1, 2])
c2 = -mp.mpf(35)/36 - lam**2 + 3*lam; c3 = mp.mpf(623)/432 - mp.mpf(19)/12*lam + lam**2/3
q2, q3 = L2(), L3()
print("L2 quad", mp.nstr(q2, 15), "closed", mp.nstr(c2, 15), "diff", mp.nstr(q2-c2, 3), "| control", mp.nstr(L2(True), 8))
print("L3 quad", mp.nstr(q3, 15), "closed", mp.nstr(c3, 15), "diff", mp.nstr(q3-c3, 3), "| control", mp.nstr(L3(True), 8))
