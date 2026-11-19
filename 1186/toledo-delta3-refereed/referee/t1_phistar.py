import sys; sys.path.insert(0, '.')
from d3 import *
H = hnodes()
# Q(phi*) route 1 (non-symmetrised b-section): Q = int_0^1 phi*(a) [Phi((1+a)/2) - Phi(a/2)] da
# integrand is piecewise linear with kinks on the 1/1096 lattice (a/2, (1+a)/2 hit edges at lattice points) and
# phi* constant on each unit piece; use Simpson on each unit piece to be safe against hidden kinks? -> use 4 sub-points & check linearity
Q1 = F(0)
for x in range(U):
    s = sign_on(x, x+1)
    a0, a1, am = F(x, U), F(x+1, U), F(2*x+1, 2*U)
    f = lambda a: s*(Phi((1+a)/2) - Phi(a/2))
    f0, f1, fm = f(a0), f(a1), f(am)
    assert 2*fm == f0 + f1, 'nonlinear piece'
    Q1 += (a1-a0)*(f0+f1)/2
print('Q(phi*) route b-section =', Q1)
# route 2: block-pair areas with my own area routine
Q2 = F(0)
for b in range(12):
    for c in range(12):
        Q2 += SIGNS[b]*SIGNS[c]*area_in(F(EDGES[b],U), F(EDGES[b+1],U), F(EDGES[c],U), F(EDGES[c+1],U))
print('Q(phi*) route block areas (my integrate-in-b area) =', Q2)
print('1/16 + Q/4 =', F(1,16)+Q1/4, ' target 117/2192 =', F(117,2192))
# h facts
assert all(v >= 0 for v in H)
zeros = [x for x in range(U+1) if H[x] == 0]
print('zeros of h (units 1/1096):', zeros, ' edges:', EDGES[1:-1], zeros == EDGES[1:-1])
print('zeros as fractions:', [str(F(z, U)) for z in zeros])
# linearity between nodes: evaluate h directly at midpoints and quarter points
bad = 0
for x in range(U):
    for num in (1, 2, 3):
        t = F(4*x+num, 4*U)
        hv = h_at(t)
        interp = H[x] + (H[x+1]-H[x])*F(num, 4)
        if hv != interp: bad += 1
print('nonlinear between nodes (quarter-point test):', bad)
sl = set()
for z in zeros:
    sl.add((H[z]-H[z-1])*U); sl.add((H[z+1]-H[z])*U)
print('one-sided slopes at zeros:', sorted(sl))
print('min nonzero node value:', min(v for v in H if v > 0), float(min(v for v in H if v > 0)))
I = sum((H[x]+H[x+1])/2 for x in range(U)) / U
print('int h =', I, ' -Q(phi*) =', -Q1)
flats = [x for x in range(U) if H[x] == H[x+1]]
print('flat pieces of h:', flats)
# symmetry h(1-a) = h(a)?
print('h symmetric under a->1-a:', all(H[x] == H[U-x] for x in range(U+1)))
print('max h', max(H), float(max(H)))
