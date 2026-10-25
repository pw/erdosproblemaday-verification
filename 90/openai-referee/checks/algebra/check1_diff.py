# Check (8.9)-(8.10): differentiate (8.1) and (8.8) with an abstract derivation D.
# D(i)=0, D(chi)=0, D(x_p)=Hx, D(y_p)=Hy, D(x_r)=Ux, D(y_r)=Uy, D(g)=A*g, D(h)=Ap*h.
import sympy as sp
xp,yp,xr,yr,g,h,chi = sp.symbols('xp yp xr yr g h chi', nonzero=True)
Hx,Hy,Ux,Uy,A,Ap,dchi = sp.symbols('Hx Hy Ux Uy A Ap dchi')
I = sp.I
base = [xp,yp,xr,yr,g,h,chi]
def D(expr, dchi_val=0):
    rules = {xp:Hx, yp:Hy, xr:Ux, yr:Uy, g:A*g, h:Ap*h, chi:dchi_val}
    return sum(sp.diff(expr, v)*rules[v] for v in base)   # D(i)=0: I is a constant
zp, wp = xp+I*yp, xp-I*yp
zr, wr = xr+I*yr, xr-I*yr
lam = g/h*chi                       # (8.8)
L = (zp-zr)*(wp-wr)                 # L_l(p_i)
R = 1/lam - lam                     # R_il
# (8.1) as an identity F=0 on the variety; its derivative D(F) must vanish there.
F = L - (2 - lam - 1/lam)
dF = sp.simplify(sp.expand(D(F)))
claim = 2*((xp-xr)*(Hx-Ux) + (yp-yr)*(Hy-Uy)) - R*(A-Ap)   # (8.9) as LHS-RHS
print("D(8.1) - [(8.9) LHS-RHS] =", sp.simplify(dF - claim))
# control 1: a deliberately wrong (8.9) (sign of A' flipped) must FAIL
bad = 2*((xp-xr)*(Hx-Ux) + (yp-yr)*(Hy-Uy)) - R*(A+Ap)
print("control (A+A'):", sp.simplify(dF - bad))
# control 2: chi NOT a constant (D chi = dchi != 0) leaves an extra term
dF2 = sp.expand(D(F, dchi))
print("control (D chi != 0): residual =", sp.factor(sp.simplify(dF2 - claim)))
# (8.10): R^2 = L(L-4) on the variety L = 2 - lam - 1/lam
lamS = sp.symbols('lamS', nonzero=True)
LS = 2 - lamS - 1/lamS
RS = 1/lamS - lamS
print("(8.10) R^2 - L(L-4) =", sp.simplify(RS**2 - LS*(LS-4)))
print("control: R^2 - L(L+4) =", sp.simplify(RS**2 - LS*(LS+4)))
# also confirm (z_p-z_r)(w_p-w_r) is the bilinear squared length (no conjugation)
print("L - [(dx)^2+(dy)^2] =", sp.expand(L - ((xp-xr)**2+(yp-yr)**2)))
