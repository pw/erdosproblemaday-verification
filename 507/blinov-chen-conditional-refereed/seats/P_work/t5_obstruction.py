# Seat P, task 5: end-to-end gamma_{k-1} mod r with the real k=408781 layout, real tags, real f_{ia} (r=37).
#   distinct labels: gamma_{k-1} == Nm(Vandermonde) != 0 (mod r); repeated labels: 0.
#   CONTROL: tag layout (0,1,3,4,8) must break the congruence for some labels.
import sys, random
sys.path.insert(0, '/tmp/oaimath/191b/seats/P_work')
import numpy as np
import t2_norm as T2
random.seed(99)
r = int(sys.argv[1]) if len(sys.argv) > 1 else 37
uval = T2.find_root_u(r)[0]
nodes = list(range(9))
K, csum, dnorm, Zvec = T2.build(r, uval, nodes)
forms = T2.forms_mod_r(r, uval)
inv9 = pow(9, r-2, r)

# re-derive the per-index f values for one column (same literal recipe as t2, exposed per (w,s))
def lag(s):
    num = [1]; den = 1
    for t in nodes:
        if t == s: continue
        num = T2.pmul(num, [(-t) % r, 1], r); den = den*(s-t) % r
    num = [x*pow(den, r-2, r) % r for x in num] + [0]*9
    acc = K.const(0); thp = K.const(1)
    for coef in num[:9]:
        acc = K.add(acc, K.scal(coef, thp)); thp = K.mul(thp, (0,1,0,0,0))
    return acc
cs = {s: lag(s) for s in nodes}
def hform(form, a, b):
    p, c = form; acc = K.const(0)
    for i in range(3): acc = K.add(acc, K.scal(c[i], K.mul(a[p[i]-1], b[i])))
    return acc
def fvals(X):
    Z = Zvec(X); conj = [[K.frob(z, j) for z in Z] for j in range(5)]
    h1 = [hform(f, conj[1], conj[2]) for f in forms]; h2 = [hform(f, conj[3], conj[4]) for f in forms]
    out = []  # list over a of (f1,f2,f3)
    for w1 in range(18):
        for w2 in range(18):
            Hw = K.mul(h1[w1], h2[w2]); F = [K.mul(Z[i], Hw) for i in range(3)]
            for s in nodes:
                f1 = inv9*sum(x*pow(s, i, r) for i, x in enumerate(F[0])) % r
                f2 = sum(x*pow(s, i, r) for i, x in enumerate(F[1])) % r
                f3 = K.mul(cs[s], F[2])[0]
                out.append((f1, f2, f3))
    return out

words = sorted(sum(((m >> j) & 1)*3**j for j in range(12)) for m in range(4096))
norm = [c for c in words if 10 <= c < 204391]; assert len(norm) == 2916
k = 408781

def residue_rows(xi, tags):
    X = T2.label_X(K, xi); f = fvals(X)
    rows = [np.zeros(k, dtype=np.int64) for _ in range(3)]
    rows[0][0] = 1
    for s, t in enumerate(tags): rows[1][t] = xi[s] % r   # power-basis coordinates lambda_s
    for a, c in enumerate(norm):
        assert rows[0][c] == 0 and rows[1][c] == 0
        rows[0][c] = f[a][0]; rows[1][c] = f[a][1]; rows[2][k-1-2*c] = f[a][2]
    return rows

def gamma_k1(cols):
    supp1 = sorted(set(np.nonzero(cols[0][0])[0]) | set(np.nonzero(cols[1][0])[0]) | set(np.nonzero(cols[2][0])[0]) | {0} | set(norm))
    supp2 = np.array(sorted(set(range(10)) | set(norm)))
    tot = 0
    perms = [((0,1,2),1), ((1,2,0),1), ((2,0,1),1), ((0,2,1),-1), ((2,1,0),-1), ((1,0,2),-1)]
    for perm, sg in perms:
        r1, r2, r3 = cols[perm[0]][0], cols[perm[1]][1], cols[perm[2]][2]
        acc = 0
        for p1 in supp1:
            if r1[p1] == 0: continue
            p3 = k - 1 - p1 - supp2
            ok = p3 >= 0
            acc += int(r1[p1]) * int(np.sum(r2[supp2[ok]] * r3[p3[ok]]))
        tot += sg*acc
    return tot % r

def vander_norm(xis):
    d = K.mul(K.mul(K.sub(xis[1], xis[0]), K.sub(xis[2], xis[0])), K.sub(xis[2], xis[1]))
    return K.norm(d)

tags = [0, 1, 3, 4, 9]
ok = 0; n = 0
for t in range(4):
    xis = [tuple(random.randrange(r) for _ in range(5)) for _ in range(3)]
    cols = [residue_rows(x, tags) for x in xis]
    g = gamma_k1(cols); N = vander_norm(xis); n += 1
    ok += (g == N and N != 0)
    print(f'distinct labels {xis}: gamma_(k-1) mod r = {g}, Nm(Vandermonde) = {N}')
xis = [tuple(random.randrange(r) for _ in range(5)) for _ in range(2)]
cols = [residue_rows(xis[0], tags), residue_rows(xis[0], tags), residue_rows(xis[1], tags)]
g0 = gamma_k1(cols)
print(f'distinct: {ok}/{n} agree & nonzero;  labels (l,l,m): gamma_(k-1) mod r = {g0} (must be 0)')
# CONTROL: bad tag layout
badtags = [0, 1, 3, 4, 8]
mism = 0
for t in range(3):
    xis = [tuple(random.randrange(1, r) for _ in range(5)) for _ in range(3)]
    cols = [residue_rows(x, badtags) for x in xis]
    g = gamma_k1(cols); N = vander_norm(xis)
    mism += g != N
    print(f'CONTROL tags {badtags}: gamma = {g}, N = {N}')
print(f'CONTROL mismatches {mism}/3 (must be >0)')
