# Own bathtub constants (route: m(v) differences, not summed 1/|slope|) and own areas; compare with verify.js
import sys, json; sys.path.insert(0, '.')
from d3 import *
H = hnodes()
d = json.load(open('verify_grids.json'))

def my_bathtub(p, q):
    w = F(q-p, U)
    vals = sorted(set(H[p:q+1]))
    mn = vals[0]
    a = w*mn
    if any(H[x] == H[x+1] for x in range(p, q)): return a, F(0)
    def meas(v):   # |{t in [p,q]/U : h(t) < v}|
        acc = F(0)
        for x in range(p, q):
            lo, hi = min(H[x], H[x+1]), max(H[x], H[x+1])
            if v <= lo: continue
            if v >= hi: acc += F(1, U); continue
            acc += F(1, U)*(v-lo)/(hi-lo)
        return acc
    ms = [meas(v) for v in vals]
    assert ms[0] == 0 and ms[-1] == w
    # m is linear between consecutive node values -> check at midpoints
    sup = F(0)
    for k in range(len(vals)-1):
        mid = (vals[k]+vals[k+1])/2
        assert 2*meas(mid) == ms[k]+ms[k+1]
        sup = max(sup, (ms[k+1]-ms[k])/(vals[k+1]-vals[k]))
    b = w*w/(2*sup)
    return a, b

seen = set()
for f, v in d.items():
    key = json.dumps(v['grid'])
    if key in seen: continue
    seen.add(key)
    grid = v['grid']; n = len(grid)-1
    print('grid', f.split('/')[-1], 'n =', n)
    # every edge a grid point
    print('  all edges in grid:', all(e in grid for e in EDGES))
    nb = 0; maxrel = 0
    nonmono = 0
    for i, c in enumerate(v['cells']):
        p, q = grid[i], grid[i+1]
        assert (c['p'], c['q']) == (p, q)
        s = sign_on(p, q); assert s == c['s']
        a, b = my_bathtub(p, q)
        if a != F(c['a']) or b != F(c['b']): nb += 1; print('  MISMATCH cell', i, a, c['a'], b, c['b'])
        seg = H[p:q+1]
        if not (all(seg[k] <= seg[k+1] for k in range(len(seg)-1)) or all(seg[k] >= seg[k+1] for k in range(len(seg)-1))): nonmono += 1
    print('  bathtub mismatches:', nb, '  non-monotone cells:', nonmono)
    # areas
    full = set(map(tuple, v['full'])); cut = {(i, j): (F(a), F(b)) for i, j, a, b in v['cut']}
    nm = 0; cnt = {'full':0,'cut':0,'absent':0}
    for i in range(n):
        for j in range(n):
            x0, x1, y0, y1 = F(grid[i],U), F(grid[i+1],U), F(grid[j],U), F(grid[j+1],U)
            A = area_in(x0, x1, y0, y1); W = (x1-x0)*(y1-y0)
            assert 0 <= A <= W
            if A == 0:
                cnt['absent'] += 1
                if (i,j) in full or (i,j) in cut: nm += 1
            elif A == W:
                cnt['full'] += 1
                if (i,j) not in full: nm += 1
            else:
                cnt['cut'] += 1
                if (i,j) not in cut or cut[(i,j)] != (A, W-A): nm += 1
    print('  my counts', cnt, ' verify.js: full', len(full), 'cut', len(cut), 'absent', v['absent'], '  area/class mismatches:', nm)
    # cut list order lexicographic?
    print('  cut list lexicographic:', [tuple(x[:2]) for x in v['cut']] == sorted(tuple(x[:2]) for x in v['cut']))
