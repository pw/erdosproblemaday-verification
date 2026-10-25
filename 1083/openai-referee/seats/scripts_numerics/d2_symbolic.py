# (d') exact symbolic versions of the identities on pp. 11-13 (sympy), d = 3 and 4
from sympy import symbols, Matrix, expand, simplify, zeros
for d in (3, 4):
    p = Matrix(symbols(f'p1:{d+1}')); q = Matrix(symbols(f'q1:{d+1}'))
    p2 = Matrix(symbols(f'P1:{d+1}')); q2 = Matrix(symbols(f'Q1:{d+1}'))
    zs = symbols(f'z1:{d*(d-1)//2+1}')
    Z = zeros(d, d); k = 0
    for i in range(d):
        for j in range(i+1, d):
            Z[i, j] = zs[k]; Z[j, i] = -zs[k]; k += 1
    v0 = (p+q)/2; y0 = (p-q)/2
    c = y0 - Z*v0                      # generic point of F_{p,q}
    Om = zeros(d+1, d+1); Om[:d, :d] = Z; Om[:d, d] = c; Om[d, :d] = -c.T
    v = Matrix.vstack(v0, Matrix([1])); y = Matrix.vstack(y0, Matrix([-(v0.T*y0)[0]]))
    r1 = (Om*v - y).applyfunc(expand)
    print(f"d={d}: Omega v - y on F_pq  ==", list(r1), " ; v0.Z v0 =", expand((v0.T*Z*v0)[0]))
    # global polarization
    v1 = (p2+q2)/2; y1 = (p2-q2)/2
    X1 = list(v0)+[1]+list(y0)+[-(v0.T*y0)[0]]; X2 = list(v1)+[1]+list(y1)+[-(v1.T*y1)[0]]
    Bf = sum(X1[i]*X2[d+1+i] + X2[i]*X1[d+1+i] for i in range(d+1))
    phys = -(((p-p2).T*(p-p2))[0] - ((q-q2).T*(q-q2))[0])/4
    print(f"  B(X,X') + (v0-v0').(y0-y0') = {expand(Bf + ((v0-v1).T*(y0-y1))[0])};  (v0-v0').(y0-y0') - (|p-p'|^2-|q-q'|^2)/4 = {expand(((v0-v1).T*(y0-y1))[0] - (((p-p2).T*(p-p2))[0] - ((q-q2).T*(q-q2))[0])/4)}")
    # (2.8): subtracting the two flat equations
    c2 = None
    diff = (Z*v0 - y0) - (Z*v1 - y1)        # (c cancels)
    u = p2 - p; w = q2 - q
    print(f"  (Zv0 - y0) - (Zv0' - y0') + (1/2)(Z(u+w) - (u-w)) = {list((diff + (Z*(u+w) - (u-w))/2).applyfunc(expand))}")
    # local polarization
    ui = Matrix(symbols(f'a1:{d+1}')); wi = Matrix(symbols(f'b1:{d+1}')); uj = Matrix(symbols(f'c1:{d+1}')); wj = Matrix(symbols(f'e1:{d+1}'))
    L = ((ui-wi).T*(uj+wj))[0] + ((uj-wj).T*(ui+wi))[0]
    print(f"  local: L - 2(ui.uj - wi.wj) = {expand(L - 2*((ui.T*uj)[0] - (wi.T*wj)[0]))};  x.Zx for skew Z: {expand(((ui).T*Z*ui)[0])}")
