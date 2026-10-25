import sympy as sp
# --- (a) determinant of the 3x3 system in (Hx,Hy,A) from (8.16), rows [2(p-r_l)_x, 2(p-r_l)_y, -R_l]
px,py = sp.symbols('px py')
rx = sp.symbols('rx1:4'); ry = sp.symbols('ry1:4'); R = sp.symbols('R1:4')
Mx = sp.Matrix([[2*(px-rx[l]), 2*(py-ry[l]), -R[l]] for l in range(3)])
det = sp.expand(Mx.det())
m = lambda a,b: (px-rx[a])*(py-ry[b]) - (py-ry[a])*(px-rx[b])   # 2x2 minor of position rows a,b
pred = -4*(R[0]*m(1,2) - R[1]*m(0,2) + R[2]*m(0,1))
print("det - (-4)(R1 m23 - R2 m13 + R3 m12) =", sp.expand(det - pred))
print("control (wrong sign on R2 term):", sp.expand(det - (-4)*(R[0]*m(1,2) + R[1]*m(0,2) + R[2]*m(0,1))) != 0)
# collinear case: 2x2 system [2 s_l, -R_l]
s1,s2 = sp.symbols('s1 s2'); 
print("collinear det =", sp.factor(sp.Matrix([[2*s1,-R[0]],[2*s2,-R[1]]]).det()), " (paper: 2(s2 R1 - s1 R2))")
# --- (b) (8.15): curve (z-u)(w-v)=b, zeta=(z-u)/(a-u), anchor at abscissa a on the same curve
z,u,v,b,a,zeta,am = sp.symbols('z u v b a zeta a_m')
w_of = lambda zz: v + b/(zz-u)
L = (z-a)*(w_of(z)-w_of(a))
L_zeta = sp.simplify(L.subs(z, u + zeta*(a-u)))
print("L_l in zeta:", sp.factor(L_zeta), "| minus paper's -b(zeta-1)^2/zeta:", sp.simplify(L_zeta + b*(zeta-1)**2/zeta))
num = sp.numer(sp.together(L_zeta - 4))
print("numerator of L-4 (up to sign):", sp.factor(num), "| paper: b z^2+(4-2b)z+b ->", sp.expand(-num - (b*zeta**2+(4-2*b)*zeta+b)))
print("discriminant:", sp.factor(sp.discriminant(b*zeta**2+(4-2*b)*zeta+b, zeta)))
print("control discriminant of b z^2+(4+2b)z+b:", sp.factor(sp.discriminant(b*zeta**2+(4+2*b)*zeta+b, zeta)))
# b = 1: L(L-4) is a perfect square
Lb1 = L_zeta.subs(b,1)
print("b=1: L(L-4) - ((zeta^2-1)/zeta)^2 =", sp.simplify(Lb1*(Lb1-4) - ((zeta**2-1)/zeta)**2))
print("b=2: is L(L-4) a square in Q(zeta)?  sqf:", sp.factor(sp.together(L_zeta.subs(b,2)*(L_zeta.subs(b,2)-4))))
# squared distance from s_l to another anchor with abscissa a_m
zs = sp.symbols('z_s')
Lm = (zs-am)*(w_of(zs)-w_of(am))
print("L_m(s_l) - paper formula:", sp.simplify(Lm - (-b*(zs-am)**2/((zs-u)*(am-u)))))
# --- (c) line case (8.13): w = e z + e'
e,ep,al = sp.symbols('e ep a_l')
Lline = (z-al)*((e*z+ep)-(e*al+ep))
print("line case L_l - e(z-a_l)^2 =", sp.expand(Lline - e*(z-al)**2))
