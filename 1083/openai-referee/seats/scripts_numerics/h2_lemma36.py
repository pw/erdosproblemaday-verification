# (h') two further toys for Lemma 3.6: (3.8) H_V(bL) <= b^n H_V(L) on affine point sets, and isolated points of a
# system that also has a 1-dimensional component (the "other components of any dimension" clause).
import itertools, math, random
random.seed(7)
P = 1000000007
def rank_mod(rows, p=P):
    rows = [[x % p for x in r] for r in rows]; rk = 0
    for c in range(len(rows[0])):
        piv = next((i for i in range(rk, len(rows)) if rows[i][c]), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]; inv = pow(rows[rk][c], p-2, p)
        rows[rk] = [x*inv % p for x in rows[rk]]
        for i in range(len(rows)):
            if i != rk and rows[i][c]:
                f = rows[i][c]; rows[i] = [(a-f*b) % p for a, b in zip(rows[i], rows[rk])]
        rk += 1
    return rk
def H_aff(pts, D):      # affine restriction rank of polynomials of degree <= D
    ms = [e for e in itertools.product(range(D+1), repeat=len(pts[0])) if sum(e) <= D]
    return rank_mod([[math.prod(pow(x, ei, P) for x, ei in zip(pt, e)) for e in ms] for pt in pts])
print("== (3.8) H_V(bL) <= b^n H_V(L), n=2, on k x k grids and on random point sets ==")
viol = 0
for k in (3, 5, 7):
    grid = [(i, j) for i in range(k) for j in range(k)]
    rnd = [(random.randint(1, 10**6), random.randint(1, 10**6)) for _ in range(k*k)]
    for name, pts in (("grid", grid), ("random", rnd)):
        for L in (1, 2, 3):
            for b in (2, 3):
                h1, h2 = H_aff(pts, L), H_aff(pts, b*L)
                ok = h2 <= b**2*h1; viol += (not ok)
                print(f"  {name:6s} k={k} L={L} b={b}: H(L)={h1:3d} H(bL)={h2:3d} b^2 H(L)={b*b*h1:3d} ok={ok}")
print("  violations:", viol)
print("== isolated points of {l*f = l*g = 0}: l a line (1-dim component), f=prod(x-i), g=prod(y-j) of degree L-1 ==")
for L in range(2, 8):
    k = L - 1
    iso = [(i, j) for i in range(k) for j in range(k)]       # the line l: x + 2y = -7 misses all of them
    a = len(iso)
    q = next(q for q in range(0, 4*L) if H_aff(iso, q) == a)   # interpolation degree on the isolated points
    HL = H_aff(iso, L)
    print(f"  L={L}: a={a} isolated points, surjectivity degree q={q} (<= 2L={2*L}: {q<=2*L}), H_V(L)={HL}, H_V(L)/a={HL/a:.3f}")
