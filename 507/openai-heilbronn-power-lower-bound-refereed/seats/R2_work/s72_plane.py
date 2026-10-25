# Lemma 7.2: J_x = I|x|/g(x), g^3/I <= h^2, and Lambda_x -> Pi_x mod q surjective (q prime not dividing B).
import random, math, itertools
from math import gcd
exec(open('s7_lattice.py').read().split('rng = random.Random(7)')[0])

def int_kernel_rowvec(c):
    """basis (2 vectors) of {a in Z^3 : a.c = 0} via unimodular column ops."""
    U = [[1,0,0],[0,1,0],[0,0,1]]  # columns transform
    v = list(c)
    # reduce v to (g,0,0) with column operations tracked in U (U columns)
    while sum(1 for t in v if t != 0) > 1:
        idx = sorted([i for i in range(3) if v[i] != 0], key=lambda i: abs(v[i]))
        p = idx[0]
        for i in idx[1:]:
            f = v[i] // v[p]
            v[i] -= f*v[p]
            for r in range(3): U[r][i] -= f*U[r][p]
    nzi = [i for i in range(3) if v[i] != 0]
    ker = [i for i in range(3) if i not in nzi]
    return [[U[r][i] for r in range(3)] for i in ker]

def rank_mod(rows, q):
    A = [[x % q for x in r] for r in rows]; r = 0
    for c in range(3):
        piv = next((i for i in range(r, len(A)) if A[i][c]), None)
        if piv is None: continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], -1, q); A[r] = [(x*inv) % q for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c]:
                f = A[i][c]; A[i] = [(A[i][j]-f*A[r][j]) % q for j in range(3)]
        r += 1
    return r

rng = random.Random(11)
fails = {"J": 0, "g3I": 0, "surj": 0, "plane": 0}; n = 0
for B, k in [(2, 3), (3, 2), (5, 2), (2, 5), (7, 2)]:
    h = B**k
    for trial in range(40):
        b0 = rng.randrange(k+1); e0 = rng.randrange(b0, k+1)
        C = random_C(B, k, b0, e0, rng)
        b, e, I, basis = analyse(C, B, k)
        for _ in range(10):
            while True:
                x = [rng.randrange(-60, 61) for _ in range(3)]
                if any(x) and gcd(gcd(abs(x[0]), abs(x[1])), abs(x[2])) == 1: break
            c = [sum(row[j]*x[j] for j in range(3)) for row in basis]
            g = abs(gcd(gcd(c[0], c[1]), c[2]))
            K = int_kernel_rowvec(c)
            Lx = [[sum(a[i]*basis[i][j] for i in range(3)) for j in range(3)] for a in K]
            u, v = Lx
            cr = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
            J = math.sqrt(sum(t*t for t in cr))
            xn = math.sqrt(sum(t*t for t in x))
            if abs(J - I*xn/g) > 1e-6*J: fails["J"] += 1
            if g**3 > I*h*h: fails["g3I"] += 1
            for qq in [11, 13, 101]:
                if B % qq == 0: continue
                if any(sum(w[j]*x[j] for j in range(3)) for w in Lx): fails["plane"] += 1
                if rank_mod(Lx, qq) != 2: fails["surj"] += 1
            n += 1
print("checked", n, "primitive x; failures:", fails)
