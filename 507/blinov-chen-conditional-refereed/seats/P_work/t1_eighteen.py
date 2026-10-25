# Seat P, task 1: symbolic check of the 18-form identity
#   3 det A det C = sum_{t=1}^{18} prod_{j=1}^{3} h_t(A_{.j}, C_{.j})  over Z[u]/(u^2-u+1)
# h_{p,c}(x,y) = sum_i c_i x_{p(i)} y_i,  p in one-line notation.
# Table parsed from the patch text (Blinov) and hand-transcribed from Chen's rendered PDF page 2.
import re, sys, itertools
import sympy as sp

u = sp.Symbol('u')
v_ = 1 - u
MINPOLY = u**2 - u + 1

def parse_patch_table(path):
    txt = open(path).read()
    i = txt.index(r'\sigma & c^{(1)} & c^{(2)} & c^{(3)}')
    j = txt.index(r'\end{array}', i)
    body = txt[i:j]
    rows = []
    for line in body.splitlines():
        line = line.lstrip('+').strip()
        m = re.match(r'\((\d),(\d),(\d)\)&(.*?)(?:\\\\)?$', line)
        if not m: continue
        p = tuple(int(m.group(k)) for k in (1,2,3))
        trip = re.findall(r'\(([^()]*)\)', m.group(4))
        assert len(trip) == 3, line
        rows.append((p, [tuple(t.split(',')) for t in trip]))
    return rows

def tok(s):
    s = s.strip()
    sign = 1
    if s.startswith('-'): sign, s = -1, s[1:]
    val = {'u': u, 'v': v_, '1': sp.Integer(1)}[s]
    return sign * val

# Chen table, transcribed by eye from chen-02.png (rendered at 150 dpi)
CHEN = [
 ((1,2,3), ['-u,-1,v', '-v,-1,u', '-v,v,v']),
 ((1,3,2), ['-1,-u,-v', 'v,-u,1', 'u,-u,-u']),
 ((2,1,3), ['-u,v,1', '-v,v,-v', '-v,u,1']),
 ((3,1,2), ['-1,-u,v', '-1,-v,u', '-1,1,-1']),
 ((2,3,1), ['-1,-1,1', 'v,u,1', 'u,v,1']),
 ((3,2,1), ['1,-u,v', '-v,-v,v', '1,-v,u']),
]
CHEN = [(p, [tuple(t.split(',')) for t in ts]) for p, ts in CHEN]

A = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'a{i+1}{j+1}'))
C = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'c{i+1}{j+1}'))

def forms(rows, inverse=False):
    out = []
    for p, trips in rows:
        pp = p
        if inverse:  # alternative reading: x_{p^{-1}(i)}
            inv = [0]*3
            for i in range(3): inv[p[i]-1] = i+1
            pp = tuple(inv)
        for t in trips:
            c = [tok(x) for x in t]
            out.append((pp, c))
    return out

def lhs_minus_rhs(fs):
    tot = sp.Integer(0)
    for p, c in fs:
        prod = sp.Integer(1)
        for j in range(3):
            h = sum(c[i] * A[p[i]-1, j] * C[i, j] for i in range(3))
            prod *= h
        tot += prod
    diff = sp.expand(tot - 3 * A.det() * C.det())
    # reduce coefficients mod u^2-u+1
    poly = sp.Poly(diff, *(list(A) + list(C)))
    bad = 0
    nterms = 0
    for mon, coeff in poly.terms():
        nterms += 1
        r = sp.rem(sp.expand(coeff), MINPOLY, u)
        if sp.simplify(r) != 0:
            bad += 1
    return bad, nterms

patch = parse_patch_table('/tmp/oaimath/191b/src/blinov-fpc/patches/reserved-tags.patch')
print('patch table rows parsed:', len(patch))
for p, t in patch: print('  ', p, t)
same = [(p, list(t)) for p, t in patch] == [(p, list(t)) for p, t in CHEN]
print('Blinov patch table == Chen table (token-for-token):', same)

fsB = forms(patch)
assert len(fsB) == 18
bad, n = lhs_minus_rhs(fsB)
print(f'Blinov table, one-line p: {bad} nonzero residual monomials (of {n} in LHS-RHS before reduction)')
badC, nC = lhs_minus_rhs(forms(CHEN))
print(f'Chen table,   one-line p: {badC} nonzero residual monomials')
badI, nI = lhs_minus_rhs(forms(patch, inverse=True))
print(f'Blinov table, inverse-p reading: {badI} nonzero residual monomials (control on notation)')

# also: factor must be exactly 3 (not 1, not -3)
fs = fsB
tot = sp.Integer(0)
for p, c in fs:
    prod = sp.Integer(1)
    for j in range(3):
        prod *= sum(c[i] * A[p[i]-1, j] * C[i, j] for i in range(3))
    tot += prod
for k in (1, -3, 6):
    d = sp.Poly(sp.expand(tot - k*A.det()*C.det()), *(list(A)+list(C)))
    nb = sum(1 for _, cf in d.terms() if sp.rem(sp.expand(cf), MINPOLY, u) != 0)
    print(f'  multiplier {k}: residual monomials {nb} (must be >0)')

# Mutation controls: flip each single coefficient sign in turn; every mutation must break the identity
fails = 0
total = 0
for idx in range(18):
    for ci in range(3):
        fsm = [(p, list(c)) for p, c in fsB]
        fsm[idx][1][ci] = -fsm[idx][1][ci]
        b, _ = lhs_minus_rhs(fsm)
        total += 1
        if b > 0: fails += 1
print(f'mutation control: {fails}/{total} single-sign flips break the identity (must be {total}/{total})')
# replace u by v in one entry
fsm = [(p, list(c)) for p, c in fsB]
fsm[0][1][0] = -v_
b, _ = lhs_minus_rhs(fsm)
print('mutation u->v in form 1 coeff 1: residual', b, '(must be >0)')
