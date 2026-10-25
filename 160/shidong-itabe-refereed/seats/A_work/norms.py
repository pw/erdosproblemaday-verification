# Build the norm forms P_t : F_p^t -> F_p (t = 3,4,5) from scratch and check the facts §3 relies on:
#  (1) N(z) lands in F_p; (2) no nontrivial zero; (3) homogeneity P(c x) = c^t P(x);
#  (4) POLYNOMIALITY OF DEGREE t ALONG LINES: s -> P(u + s v) interpolates (over F_p, deg <= p-1)
#      to a polynomial of degree <= t whose s^t coefficient is P(v)  [this is what Lemma 4.1 uses].
# Writes tables norm_p{p}_t{t}.bin (uint8, index = sum x_j p^j).
import itertools, random, sys, struct
def polymulmod(a, b, f, p):
    t = len(f) - 1
    r = [0]*(2*t-1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i+j] = (r[i+j] + ai*bj) % p
    for deg in range(2*t-2, t-1, -1):
        c = r[deg]
        if c:
            r[deg] = 0
            for j in range(t):  # f monic: T^t = -sum f[j] T^j
                r[deg-t+j] = (r[deg-t+j] - c*f[j]) % p
    return r[:t]
def polypow(a, e, f, p):
    t = len(f)-1; res = [1]+[0]*(t-1)
    while e:
        if e & 1: res = polymulmod(res, a, f, p)
        a = polymulmod(a, a, f, p); e >>= 1
    return res
def is_irreducible(f, p):
    t = len(f)-1
    X = [0, 1] + [0]*(t-2)
    # brute force: no factor of degree <= t//2 ; do it via x^{p^i} - x gcd test using rank-free approach:
    # simple: check no monic factor of degree d <= t//2 by trial division over all monic polys (small p,t)
    def divides(g, f):
        r = f[:]  # coefficients low..high
        dg = len(g)-1
        for deg in range(len(r)-1, dg-1, -1):
            c = r[deg]
            if c:
                for j in range(dg+1):
                    r[deg-dg+j] = (r[deg-dg+j] - c*g[j]) % p
        return not any(r[:dg])
    for d in range(1, t//2+1):
        for low in itertools.product(range(p), repeat=d):
            if divides(list(low)+[1], f): return False
    return True
def find_irreducible(p, t):
    for low in itertools.product(range(p), repeat=t):
        f = list(low)+[1]
        if f[0] and is_irreducible(f, p): return f
def norm_table(p, t):
    f = find_irreducible(p, t)
    e = (p**t - 1)//(p - 1)
    tab = bytearray(p**t)
    for idx, z in enumerate(itertools.product(range(p), repeat=t)):
        z = list(z)[::-1]  # make index = sum z_j p^j  (itertools varies last fastest)
        n = polypow(z, e, f, p)
        assert all(c == 0 for c in n[1:]), "norm not in F_p"
        ii = sum(z[j]*p**j for j in range(t))
        tab[ii] = n[0]
    return f, tab
def interp_coeffs(vals, p):
    # coefficients c_0..c_{p-1} of the unique poly of degree <= p-1 with c(s)=vals[s], s in F_p
    n = p; A = [[pow(s, j, p) for j in range(n)] + [vals[s] % p] for s in range(n)]
    for col in range(n):
        piv = next(r for r in range(col, n) if A[r][col])
        A[col], A[piv] = A[piv], A[col]
        inv = pow(A[col][col], p-2, p)
        A[col] = [x*inv % p for x in A[col]]
        for r in range(n):
            if r != col and A[r][col]:
                c = A[r][col]; A[r] = [(x - c*y) % p for x, y in zip(A[r], A[col])]
    return [A[j][n] for j in range(n)]
rc = 0
random.seed(1)
for p, ts in ((7, (3, 4, 5)), (11, (3, 5)), (13, (3, 5))):
    for t in ts:
        f, tab = norm_table(p, t)
        idx = lambda x: sum(x[j]*p**j for j in range(t))
        zeros = sum(1 for i in range(1, p**t) if tab[i] == 0)
        hom = 0
        for x in itertools.product(range(p), repeat=t):
            for c in range(1, p):
                if tab[idx([c*xi % p for xi in x])] != pow(c, t, p)*tab[idx(x)] % p: hom += 1
        degbad = lead_bad = 0; S = 3000
        for _ in range(S):
            u = [random.randrange(p) for _ in range(t)]; v = [random.randrange(p) for _ in range(t)]
            vals = [tab[idx([(u[j]+s*v[j]) % p for j in range(t)])] for s in range(p)]
            c = interp_coeffs(vals, p)
            if any(c[t+1:]): degbad += 1
            if c[t] != tab[idx(v)]: lead_bad += 1
        print(f"p={p} t={t} f={f}: nontrivial zeros={zeros} homogeneity failures={hom} "
              f"deg>t along lines={degbad}/{S} lead coeff != P(v)={lead_bad}/{S}")
        if zeros or hom or degbad or lead_bad: rc = 1
        if p == 7: open(f"norm_p{p}_t{t}.bin", "wb").write(bytes(tab))
# control for (4): a NON-homogeneous anisotropic-looking map (norm composed with a nonlinear bijection)
# must fail the along-lines degree test, else the test can't see anything.
p, t = 7, 5
tab = open("norm_p7_t5.bin","rb").read()
idx = lambda x: sum(x[j]*p**j for j in range(t))
bad = 0
for _ in range(300):
    u = [random.randrange(p) for _ in range(t)]; v = [random.randrange(p) for _ in range(t)]
    vals = [tab[idx([pow((u[j]+s*v[j]) % p, 5, p) for j in range(t)])] for s in range(p)]
    c = interp_coeffs(vals, p)
    if any(c[t+1:]) or c[t] != tab[idx([pow(x,5,p) for x in v])]: bad += 1
print("control (norm o coordinatewise x^5): along-lines failures", bad, "/300 (expect >0)")
sys.exit(rc)
