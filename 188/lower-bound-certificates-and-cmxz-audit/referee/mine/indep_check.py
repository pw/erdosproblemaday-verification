"""Independent exact re-check of a config188 core, no sympy simplify.
Numbers in Q(sqrt3, sqrt11) as 4-tuples of Fractions on basis (1, r3, r11, r33)."""
import sys, json, math, itertools
from fractions import Fraction as F
B = {}  # product table of basis indices -> (coef, index)
# basis 0=1, 1=r3, 2=r11, 3=r33
T = {(0,0):(1,0),(0,1):(1,1),(0,2):(1,2),(0,3):(1,3),
     (1,1):(3,0),(1,2):(1,3),(1,3):(3,2),
     (2,2):(11,0),(2,3):(11,1),(3,3):(33,0)}
def mul(x, y):
    out = [F(0)]*4
    for i in range(4):
        if x[i] == 0: continue
        for j in range(4):
            if y[j] == 0: continue
            c, k = T[(min(i,j), max(i,j))]
            out[k] += c*x[i]*y[j]
    return tuple(out)
def add(x, y): return tuple(a+b for a, b in zip(x, y))
def sub(x, y): return tuple(a-b for a, b in zip(x, y))
def num(q): return (F(q), F(0), F(0), F(0))
def fl(x): return float(x[0]) + float(x[1])*math.sqrt(3) + float(x[2])*math.sqrt(11) + float(x[3])*math.sqrt(33)
R3 = (F(0), F(1), F(0), F(0)); R11 = (F(0), F(0), F(1), F(0))
def lat(a, b):  # a + b w, w = (-1 + i sqrt3)/2
    return (num(F(a) - F(b, 2)), mul(num(F(b, 2)), R3))
def rot(center, d2, sign):
    assert d2 == 3, d2   # sin = sqrt(11)/6 only
    c = num(F(5, 6)); s = mul(num(F(sign, 6)), R11)
    cx, cy = center
    def f(p):
        x, y = sub(p[0], cx), sub(p[1], cy)
        return (add(cx, sub(mul(c, x), mul(s, y))), add(cy, add(mul(s, x), mul(c, y))))
    return f
core = json.load(open(sys.argv[1])); k = core['k']
gd = core['gen_desc']; words = core['iso_words']
pts = {}
for key, (gi, a, b) in core['tags'].items():
    p = lat(a, b)
    for h in reversed(words[gi]):
        cen, d, sign = gd[h]
        bb = round(cen[1]*2/math.sqrt(3)); aa = round(cen[0] + bb/2)
        assert abs(cen[0] - (aa - bb/2)) < 1e-12 and abs(cen[1] - bb*math.sqrt(3)/2) < 1e-12
        p = rot(lat(aa, bb), round(d*d), sign)(p)
    i = int(key); pts[i] = p
    assert abs(fl(p[0]) - core['points'][key][0]) < 1e-9 and abs(fl(p[1]) - core['points'][key][1]) < 1e-9
def n2(v): return add(mul(v[0], v[0]), mul(v[1], v[1]))
ONE = num(1); ZERO = num(0)
cl = core['core_clauses']; bad = 0; npair = nrun = nunit = 0
for c in cl:
    if len(c) == 2 and all(l < 0 for l in c):
        i, j = -c[0]-1, -c[1]-1
        if n2((sub(pts[i][0], pts[j][0]), sub(pts[i][1], pts[j][1]))) != ONE: bad += 1; print('bad pair', c)
        npair += 1
    elif len(c) == k and all(l > 0 for l in c):
        ids = [l-1 for l in c]
        # clause order is irrelevant: find an ordering making a unit-spaced collinear run
        ok = False
        for perm in itertools.permutations(ids):
            u = (sub(pts[perm[1]][0], pts[perm[0]][0]), sub(pts[perm[1]][1], pts[perm[0]][1]))
            if n2(u) != ONE: continue
            if all((sub(pts[perm[t]][0], pts[perm[t-1]][0]), sub(pts[perm[t]][1], pts[perm[t-1]][1])) == u for t in range(2, k)):
                ok = True; break
        if not ok: bad += 1; print('bad run', c)
        nrun += 1
    elif len(c) == 1:
        l = c[0]; i = abs(l) - 1
        if l > 0:
            if pts[i] != (ZERO, ZERO): bad += 1; print('positive unit not origin', c)
        else:
            print('negative unit: point', [fl(x) for x in pts[i]], 'r^2 =', fl(n2(pts[i])))
        nunit += 1
    else:
        bad += 1; print('UNCLASSIFIED clause', c)
# distinctness of points
keys = {}
for i, p in pts.items(): keys.setdefault(p, []).append(i)
dup = [v for v in keys.values() if len(v) > 1]
print(f'pairs {npair} runs {nrun} units {nunit} clauses {len(cl)} bad {bad} duplicate-point groups {len(dup)}')
print('max |p| =', max(math.sqrt(fl(n2(p))) for p in pts.values()))
print('negative units:', [c for c in cl if len(c)==1 and c[0]<0], 'positive units:', [c for c in cl if len(c)==1 and c[0]>0])
