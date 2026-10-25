# Exact-rational recomputation of every displayed constant in Prop 3.3 and Lemma 4.5 (seat MATH).
from fractions import Fraction as Fr
import sympy as sp

print("== Prop 3.1 Clebsch numbers ==")
rho = Fr(5,16); t = Fr(1040, 16**4)
print("t(C4,Clebsch)=", t, " rho^3-3/64 rho =", rho**3 - Fr(3,64)*rho, " equal:", t == rho**3-Fr(3,64)*rho)
# Razborov Thm 3.1a in hom normalisation: 3t >= 3/2 rho^2 - 81/256 rho
print("Razborov 3.1a at Clebsch (3t vs bound):", 3*t, Fr(3,2)*rho**2 - Fr(81,256)*rho)

print("== Prop 3.3 ==")
gamma = Fr(3,64) + Fr(1, 50_000_000_000)
r0 = Fr(7,22)
hd = lambda r, g: r/8 - r**2/4 + g/4
print("gamma < 293/6250:", gamma < Fr(293,6250), " 293/6250 - gamma =", Fr(293,6250)-gamma)
print("rho/8-rho^2/4 at 7/22 =", r0/8 - r0**2/4, " ==7/484:", r0/8-r0**2/4 == Fr(7,484),
      " 7/176-49/1936=", Fr(7,176)-Fr(49,1936))
print("7/484+293/25000 =", Fr(7,484)+Fr(293,25000), " == 79203/3025000:", Fr(7,484)+Fr(293,25000)==Fr(79203,3025000))
print("131/5000 =", Fr(131,5000), "== 79255/3025000:", Fr(131,5000)==Fr(79255,3025000))
print("exact high-density bound at 7/22 with true gamma:", hd(r0,gamma), float(hd(r0,gamma)))
print("  < 131/5000:", hd(r0,gamma) < Fr(131,5000))
print("high-density bound at 5/16 with gamma=3/64:", hd(Fr(5,16),Fr(3,64)), "== 27/1024:", hd(Fr(5,16),Fr(3,64))==Fr(27,1024))
# derivative 1/8 - rho/2 <0 for rho>1/4
print("1/4 < 7/22:", Fr(1,4) < r0)

print("== Lemma 4.5 ==")
I0 = Fr(2,47)
astar = I0/(r0/2 + I0)
print("a* =", astar, " ==88/417:", astar == Fr(88,417))
delta = r0/2 - I0
print("delta =", delta, "==241/2068:", delta==Fr(241,2068), " delta<1/8:", delta < Fr(1,8))
P = lambda a: a*r0/2 + (1-a)*I0
c = lambda a: 1-a
print("P(a*) =", P(astar), "==28/417:", P(astar)==Fr(28,417), " <7/100:", P(astar) < Fr(7,100))
hp = lambda a: (r0/2 - 2*I0 - 2*delta*a)/2
print("h'(a*) =", hp(astar), "==455/36696:", hp(astar)==Fr(455,36696), " >1/100:", hp(astar) > Fr(1,100))
# symbolic check h' formula
A = sp.symbols('a')
Ps = A*sp.Rational(7,44) + (1-A)*sp.Rational(2,47)
hs = (1-A)*Ps/2
print("sympy h' - stated:", sp.simplify(sp.diff(hs,A) - (sp.Rational(7,44) - 2*sp.Rational(2,47) - 2*sp.Rational(241,2068)*A)/2))
# envelope subtracted-term derivatives
g1 = 32*A**2*(1-A)*Ps**3
g1_stated = 32*A*Ps**2*((2-3*A)*Ps + 3*A*(1-A)*sp.Rational(241,2068))
print("g1' - stated:", sp.simplify(sp.diff(g1,A)-g1_stated))
g2 = 8*A*(1-A)**2*Ps**3
g2_stated = 8*(1-A)*Ps**2*((1-3*A)*Ps + 3*A*(1-A)*sp.Rational(241,2068))
print("g2' - stated:", sp.simplify(sp.diff(g2,A)-g2_stated))
E3 = sp.Rational(2,47)*(1-A)**2 - 64*sp.Rational(2,47)**3*A*(1-A)**5
E3_stated = -2*sp.Rational(2,47)*(1-A)*(1 - 32*sp.Rational(2,47)**2*(1-A)**3*(6*A-1))
print("E3' - stated:", sp.simplify(sp.diff(E3,A)-E3_stated))
b1 = 32*Fr(1,5)*Fr(7,100)**2*(2*Fr(7,100)+Fr(3,40))
print("first-line bound value:", b1, float(b1), " <7/1000:", b1 < Fr(7,1000))
b2 = 8*Fr(4,5)*Fr(7,100)**2*(Fr(2,5)*Fr(7,100) + 3*Fr(17,80)*Fr(4,5)*Fr(1,8))
print("second-line bound value:", b2, float(b2), " <1/300:", b2 < Fr(1,300))
print("a* < 17/80:", astar < Fr(17,80), "  c<=4/5 on a>=1/5 ok")
print("64 I0^2 =", 64*I0**2, "==256/2209:", 64*I0**2==Fr(256,2209))
print("12 I0^2 =", 12*I0**2, "==48/2209:", 12*I0**2 == Fr(48,2209), " 1/4-48/2209>0:", Fr(1,4)-Fr(48,2209) > 0)
cs = 1-astar
mus = 4*I0*cs**2
print("c* =", cs, "mu* =", mus, "==18424/173889:", mus==Fr(18424,173889), " a*/c* =", astar/cs)
print("I0 c*^2 =", I0*cs**2, "==4606/173889:", I0*cs**2==Fr(4606,173889), " <2649/100000:", I0*cs**2 < Fr(2649,100000))
sav = astar/cs*mus**3
print("saving (a*/c*) mu*^3 =", float(sav), " > (4/15)(21/200)^3 =", float(Fr(4,15)*Fr(21,200)**3), sav > Fr(4,15)*Fr(21,200)**3,
      " (4/15)(21/200)^3 > 29/100000:", Fr(4,15)*Fr(21,200)**3 > Fr(29,100000))
print("88/329>4/15:", Fr(88,329)>Fr(4,15), " 18424/173889>21/200:", Fr(18424,173889)>Fr(21,200))
Fstar = I0*cs**2 - sav
print("F(a*,mu*) exact =", Fstar, "=", float(Fstar), " < 131/5000:", Fstar < Fr(131,5000), " margin:", float(Fr(131,5000)-Fstar))
print("2649/100000-29/100000 == 131/5000:", Fr(2649-29,100000)==Fr(131,5000))
# also check the other two envelope branches agree at a* and at 1/5 (continuity)
L = lambda a: min(4*min(a,1-a)**2, min(a,1-a)*(1-min(a,1-a)))
env = lambda a: (min(2*c(a)*P(a), 4*I0*c(a)**2))
def Fval(a, mu):
    return min(P(a) - (1+a)/(4*c(a))*mu, mu/4) - L(a)/c(a)**2*mu**3
print("F at a*, mu=nu(a*):", float(Fval(astar, 2*c(astar)*P(astar))), " nu(a*)==4I0c*^2:", 2*c(astar)*P(astar)==mus)
print("L(1/5) both forms:", 4*Fr(1,5)**2, Fr(1,5)*Fr(4,5))
