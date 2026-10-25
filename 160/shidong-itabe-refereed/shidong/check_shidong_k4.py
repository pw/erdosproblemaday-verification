#!/usr/bin/env python3
"""Independent check of Shi–Dong (arXiv 2607.20752v2) Corollary 1.2 for k = 4.

Colouring of Z/p^4Z (p >= 5 prime):  c(n) = (tau(x0), tau(x1), tau(x2), Q(x0,x1,x2,x3))
  tau(x) = floor(3x/p) in {0,1,2}            (k-1 = 3 intervals)
  Q(x)   = x0 + N_{F_{p^3}/F_p}(x1 + x2*alpha + x3*alpha^2)   (layers u^(1)=x0, u^(3)=(x1,x2,x3))
Symmetrically coloured 4-AP a,a+d,a+2d,a+3d (d != 0 mod p^4): c(a)=c(a+3d) and c(a+d)=c(a+2d).
Claim: none exist. Palette size <= 27p.

Everything is recomputed from the definitions: the irreducible cubic is found by brute force,
the norm by multiplying z * z^p * z^{p^2} in F_p[T]/(f), 'no nontrivial zero' is checked by brute
force, and every (a,d) pair is enumerated. Controls: (i) dropping the Q coordinate must produce
symmetric 4-APs; (ii) replacing the norm by a form WITH a nontrivial zero (x1^3 here, p>=5) must
produce symmetric 4-APs (the proof needs P_3 anisotropic), and so must (iii) dropping tau on one digit.
Exit 0 = claim holds for the requested p and all controls behaved; exit 1 = a violation found;
exit 2 = cannot see (control did not fire).
"""
import sys, itertools

def irreducible_cubic(p):
    # monic T^3 + c2 T^2 + c1 T + c0 with no root in F_p (degree 3 => irreducible iff no root)
    for c2 in range(p):
        for c1 in range(p):
            for c0 in range(p):
                if all((t**3 + c2*t*t + c1*t + c0) % p for t in range(p)):
                    return (c0, c1, c2)
    raise RuntimeError("no irreducible cubic")

def mul(a, b, p, f):
    # a,b in F_p^3 as coefficient tuples (low..high) mod T^3 + c2 T^2 + c1 T + c0
    c0, c1, c2 = f
    r = [0]*5
    for i in range(3):
        for j in range(3):
            r[i+j] = (r[i+j] + a[i]*b[j]) % p
    # reduce T^4 and T^3
    for deg in (4, 3):
        coef = r[deg]
        if coef:
            r[deg] = 0
            # T^deg = T^(deg-3) * T^3 = T^(deg-3) * (-c2 T^2 - c1 T - c0)
            s = deg - 3
            r[s+2] = (r[s+2] - coef*c2) % p
            r[s+1] = (r[s+1] - coef*c1) % p
            r[s]   = (r[s]   - coef*c0) % p
    return (r[0], r[1], r[2])

def powr(a, e, p, f):
    res = (1, 0, 0)
    while e:
        if e & 1: res = mul(res, a, p, f)
        a = mul(a, a, p, f); e >>= 1
    return res

def norm_table(p, f):
    """N(z) = z * z^p * z^{p^2} for every z in F_p^3; returns dict tuple->int in F_p (constant term)."""
    tab = {}
    for z in itertools.product(range(p), repeat=3):
        zp = powr(z, p, p, f); zpp = powr(zp, p, p, f)
        n = mul(mul(z, zp, p, f), zpp, p, f)
        assert n[1] == 0 and n[2] == 0, ("norm not in F_p", z, n)
        tab[z] = n[0]
    return tab

def digits(n, p, L=4):
    xs = []
    for _ in range(L):
        xs.append(n % p); n //= p
    return xs

def build_colouring(p, f, use_Q=True, taus=(0,1,2), normfn=None):
    M = p**4
    ntab = normfn if normfn is not None else norm_table(p, f)
    col = [None]*M
    for n in range(M):
        x = digits(n, p)
        t = tuple((3*x[j])//p for j in taus)
        if use_Q:
            q = (x[0] + ntab[(x[1], x[2], x[3])]) % p
            col[n] = t + (q,)
        else:
            col[n] = t
    return col

def count_symmetric_4aps(col, M, stop_at_first=False):
    bad = 0; first = None
    for a in range(M):
        ca = col[a]
        for d in range(1, M):
            if ca == col[(a+3*d) % M] and col[(a+d) % M] == col[(a+2*d) % M]:
                bad += 1
                if first is None: first = (a, d)
                if stop_at_first: return bad, first
    return bad, first

def main():
    ps = [int(x) for x in sys.argv[1:]] or [5, 7]
    rc = 0
    for p in ps:
        f = irreducible_cubic(p)
        ntab = norm_table(p, f)
        # P_3 anisotropic?
        zeros = [z for z, v in ntab.items() if v == 0 and z != (0,0,0)]
        assert not zeros, ("norm has nontrivial zero", zeros[:3])
        M = p**4
        col = build_colouring(p, f, normfn=ntab)
        palette = len(set(col))
        bad, first = count_symmetric_4aps(col, M)
        print(f"p={p}: f=T^3+{f[2]}T^2+{f[1]}T+{f[0]}  |Z/p^4Z|={M}  palette={palette} (<=27p={27*p}: {palette<=27*p})  "
              f"symmetric 4-APs={bad}  first={first}")
        if bad: rc = 1
        # controls (each must FIRE)
        c1 = build_colouring(p, f, use_Q=False, normfn=ntab)
        b1, _ = count_symmetric_4aps(c1, M, stop_at_first=True)
        # control 2: isotropic 'norm' x1^3 (has zeros, e.g. (0,1,0)); keep everything else
        iso = {z: pow(z[0], 3, p) for z in ntab}
        c2 = build_colouring(p, f, normfn=iso)
        b2, _ = count_symmetric_4aps(c2, M, stop_at_first=True)
        # control 3: drop tau on digit 1
        c3 = build_colouring(p, f, taus=(0,2), normfn=ntab)
        b3, _ = count_symmetric_4aps(c3, M, stop_at_first=True)
        print(f"   controls: no-Q -> {b1} (expect >0)   isotropic form -> {b2} (expect >0)   drop tau(x1) -> {b3} (expect >0)")
        if not (b1 and b2 and b3):
            print("   CANNOT SEE: a control did not fire"); rc = max(rc, 2)
    sys.exit(rc)

if __name__ == "__main__":
    main()
