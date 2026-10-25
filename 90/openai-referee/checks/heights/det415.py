# Check (4.15), the elimination of Delta Z * Delta W, the Cramer constant, and the 8B*tau bound.
import sympy as sp, random, cmath, math

D1, D2, D3, dZ, dW = sp.symbols('D1 D2 D3 dZ dW')
# (i) the j-th equation: (D_j + dZ)(1/D_j + dW) - 1 == dZ/D_j + D_j dW + dZ dW
for D in (D1, D2, D3):
    assert sp.simplify(sp.expand((D + dZ)*(1/D + dW) - 1) - (dZ/D + D*dW + dZ*dW)) == 0
# (ii) subtracting j=1 from j=2,3 kills dZ*dW exactly
Ej = lambda D: dZ/D + D*dW + dZ*dW
for D in (D2, D3):
    diff = sp.expand(Ej(D) - Ej(D1))
    assert sp.expand(diff - (dZ*(1/D - 1/D1) + dW*(D - D1))) == 0
    assert sp.Poly(sp.together(diff).as_numer_denom()[0], dZ, dW).coeff_monomial(dZ*dW) == 0
# (iii) the determinant (4.15)
M = sp.Matrix([[1/D2 - 1/D1, D2 - D1], [1/D3 - 1/D1, D3 - D1]])
claim = (D1 - D2)*(D1 - D3)*(D2 - D3)/(D1*D2*D3)
print("(4.15) det - claim simplifies to:", sp.simplify(M.det() - claim))
# control: a wrong sign must NOT simplify to 0
print("control (sign flipped) simplifies to:", sp.simplify(M.det() + claim))
# (iv) exact Cramer formula for dZ in terms of E's
E1, E2, E3 = sp.symbols('E1 E2 E3')
sol = sp.solve([dZ*(1/D2 - 1/D1) + dW*(D2 - D1) - (E2 - E1),
                dZ*(1/D3 - 1/D1) + dW*(D3 - D1) - (E3 - E1)], [dZ, dW], dict=True)[0]
dZsol = sp.simplify(sol[dZ])
target = (E1*(D2 - D3) + E2*(D3 - D1) + E3*(D1 - D2))*D1*D2*D3/((D1 - D2)*(D1 - D3)*(D2 - D3))
print("Cramer dZ - closed form:", sp.simplify(dZsol - target))
