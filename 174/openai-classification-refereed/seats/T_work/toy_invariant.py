"""Seat T sanity check: Prop 5.1's hypothesis can never hold for a NON-spherical set.
Homomorphism K -> (R,+), xi_z -> ||z||^2.  For lambda with sum l_i = 0, sum l_i a_i = 0
(an affine dependency), phi(endpoint) = sum_i l_i * image(role i) = weight * sum_i l_i ||a_i||^2,
for EVERY path (diagonal factors cancel; copy-factor cross terms cancel).  If A is not
spherical, sum l_i ||a_i||^2 != 0 for some such lambda, so equal endpoints force equal weights.
Checked exactly on random paths for the collinear triple 0,1,2 (non-spherical) and, as the
contrast, the same identity gives 0 = 0 for a cyclic quadrilateral (no constraint)."""
import random, sympy as sp
random.seed(5)
def path_phi(A, lam, nfac=6):
    D = len(A[0]); total = 0; weight = 0
    phi = 0
    for _ in range(nfac):
        if random.random() < .4:     # diagonal factor: random word, same in every role
            word = [(tuple(sp.Rational(random.randint(-4,4),3) for _ in range(5)), random.choice((1,-1))) for _ in range(3)]
            img = sum(e*sum(x*x for x in z) for z,e in word)
            phi += sum(lam)*img
        else:                        # copy factor: b_i = c + sqrt(u) Q a_i, Q orthogonal (rational, 2x2 block) in R^5
            u = sp.Rational(random.randint(1,9), random.randint(1,9))
            c = [sp.Rational(random.randint(-6,6),5) for _ in range(5)]
            cs, sn = random.choice([(sp.Rational(3,5),sp.Rational(4,5)), (sp.Rational(-5,13),sp.Rational(12,13)), (1,0)])
            for i,a in enumerate(A):
                a2 = list(a)+[0]*(2-len(a))
                q = [cs*a2[0]-sn*a2[1], sn*a2[0]+cs*a2[1], 0, 0, 0]
                b = [c[k] + sp.sqrt(u)*q[k] for k in range(5)]
                phi += lam[i]*sp.expand(sum(x*x for x in b))
            weight += u
    return sp.simplify(phi), weight
for name, A, lam in [("collinear 0,1,2", [(0,0),(1,0),(2,0)], [1,-2,1]),
                     ("cyclic quadrilateral (square)", [(1,0),(0,1),(-1,0),(0,-1)], [1,-1,1,-1])]:
    q = sp.simplify(sum(l*sum(x*x for x in a) for l,a in zip(lam,A)))
    ok = 0
    for trial in range(40):
        phi, w = path_phi(A, lam)
        assert sp.simplify(phi - w*q) == 0, (name, phi, w, q)
        ok += 1
    print(f"{name}: sum l_i||a_i||^2 = {q}; phi(endpoint) = weight*{q} held on {ok}/40 random paths")
