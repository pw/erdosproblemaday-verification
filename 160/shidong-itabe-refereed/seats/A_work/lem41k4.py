# Exhaustive Lemma 4.1 for k=4 (Q = x0 + N_{F_{p^3}/F_p}(x1,x2,x3)) over all (y0,h) in F_p^4 x F_p^4,
# via per-layer histograms of D = (G(0)-G(3), G(1)-G(2)).  Control: replace the cubic norm by x1^3.
import itertools, sys
import numpy as np
sys.path.insert(0, '.')
def run(p, iso=False):
    # norm table via the cubic from norms.py helpers (recompute here, decorrelated: det of mult-by-z matrix)
    def irr():
        for c2, c1, c0 in itertools.product(range(p), repeat=3):
            if all((t**3+c2*t*t+c1*t+c0) % p for t in range(p)): return c0, c1, c2
    c0, c1, c2 = irr()
    def mulT(x):
        x0, x1, x2 = x
        return [(-x2*c0) % p, (x0 - x2*c1) % p, (x1 - x2*c2) % p]
    def nrm(z):
        a = list(z); b = mulT(a); c = mulT(b)
        d = (a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0]) + a[2]*(b[0]*c[1]-b[1]*c[0])) % p
        return d
    P3 = {z: (pow(z[0], 3, p) if iso else nrm(z)) for z in itertools.product(range(p), repeat=3)}
    def hist(dim, form, v):
        H = np.zeros(p*p, dtype=np.int64)
        for u in itertools.product(range(p), repeat=dim):
            G = [form(tuple((u[j]+i*v[j]) % p for j in range(dim))) for i in range(4)]
            H[((G[0]-G[3]) % p) + p*((G[1]-G[2]) % p)] += 1
        return H
    H1 = {v: hist(1, lambda w: w[0], v) for v in itertools.product(range(p), repeat=1)}
    H3 = {v: hist(3, lambda w: P3[w], v) for v in itertools.product(range(p), repeat=3)}
    neg = [((-(x % p)) % p) + p*((-(x//p)) % p) for x in range(p*p)]
    bad = 0
    for v1, A in H1.items():
        for v3, B in H3.items():
            cnt = int(sum(A[x]*B[neg[x]] for x in range(p*p)))
            if (v1 == (0,) and v3 == (0,0,0)):
                assert cnt == p**4
            elif cnt: bad += 1
    return bad
rc = 0
for p in (5, 7, 11, 13):
    b = run(p); print(f"k=4 p={p}: nonzero h admitting a Q-symmetric 4-AP: {b}"); rc |= b > 0
print("control (isotropic x1^3) p=7:", run(7, iso=True), "(expect >0)")
sys.exit(rc)
