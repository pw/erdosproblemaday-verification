# Seat P, task 2: the degree-five norm decomposition, numerically over F_{r^5}, built literally from the patch.
#  N = Nm_{K/F_r} det(Z(X1),Z(X2),Z(X3))   vs   sum_{w in [18]^2, s in 9 nodes} det( f_{i,w,s}(X^(j)) )
#  f_{1,w,s} = 3^{-2} * coordpoly(F_{1w})(s),  f_{2,w,s} = coordpoly(F_{2w})(s),  f_{3,w,s} = l(c_s F_{3w})
#  F_{iw} = Z_i * H_w,  H_w = h_{w1}(sZ, s^2Z) * h_{w2}(s^3Z, s^4Z)   (s = Frobenius)
import random, sys, itertools
random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 20261022)

def find_root_u(r):
    return [x for x in range(r) if (x*x - x + 1) % r == 0]

# ---- polynomial helpers over F_r (lists, low degree first) ----
def ptrim(a):
    while a and a[-1] == 0: a.pop()
    return a
def pmod(a, m, r):
    a = [x % r for x in a]; ptrim(a)
    inv = pow(m[-1], r-2, r)
    while len(a) >= len(m):
        c = a[-1] * inv % r; sh = len(a) - len(m)
        for i, mi in enumerate(m): a[sh+i] = (a[sh+i] - c*mi) % r
        ptrim(a)
    return a
def pmul(a, b, r):
    if not a or not b: return []
    out = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): out[i+j] = (out[i+j] + x*y) % r
    return ptrim(out)
def psub(a, b, r):
    n = max(len(a), len(b)); out = [((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % r for i in range(n)]
    return ptrim(out)
def pgcd(a, b, r):
    a = ptrim([x % r for x in a]); b = ptrim([x % r for x in b])
    while b:
        a, b = b, pmod(a, b, r)
    return a
def ppowmod(base, e, m, r):
    result = [1]; base = pmod(base, m, r)
    while e:
        if e & 1: result = pmod(pmul(result, base, r), m, r)
        base = pmod(pmul(base, base, r), m, r); e >>= 1
    return result
def irreducible_quintic(m, r):
    # monic degree-5: irreducible iff gcd(T^{r^i}-T, m)=1 for i=1,2
    T = [0, 1]
    x = T
    for i in (1, 2):
        x = ppowmod(x, r, m, r)
        g = pgcd(m, psub(x, T, r), r)
        if len(g) > 1: return False
    return True

class Field:
    def __init__(self, r):
        self.r = r
        while True:
            m = [random.randrange(r) for _ in range(5)] + [1]
            if irreducible_quintic(m, r): break
        self.m = m
    def mul(self, a, b):
        r = self.r
        prod = [0]*9
        for i in range(5):
            ai = a[i]
            if ai:
                for j in range(5): prod[i+j] += ai*b[j]
        # reduce by monic quintic: T^5 = -(m0 + ... + m4 T^4)
        for d in range(8, 4, -1):
            c = prod[d] % r
            if c:
                prod[d] = 0
                for i in range(5): prod[d-5+i] -= c*self.m[i]
        return tuple(x % r for x in prod[:5])
    def add(self, a, b): return tuple((x+y) % self.r for x, y in zip(a, b))
    def sub(self, a, b): return tuple((x-y) % self.r for x, y in zip(a, b))
    def scal(self, c, a): return tuple(c*x % self.r for x in a)
    def const(self, c): return (c % self.r, 0, 0, 0, 0)
    def pw(self, a, e):
        res = self.const(1)
        while e:
            if e & 1: res = self.mul(res, a)
            a = self.mul(a, a); e >>= 1
        return res
    def frob(self, a, j=1): return self.pw(a, self.r**j)
    def det3(self, M):  # M[i][j] in K
        def t(i0, i1, i2): return self.mul(self.mul(M[0][i0], M[1][i1]), M[2][i2])
        s = self.const(0)
        for (p, sg) in (((0,1,2),1), ((1,2,0),1), ((2,0,1),1), ((0,2,1),-1), ((2,1,0),-1), ((1,0,2),-1)):
            term = t(*p)
            s = self.add(s, term) if sg == 1 else self.sub(s, term)
        return s
    def norm(self, a):
        res = self.const(1)
        for j in range(5): res = self.mul(res, self.frob(a, j))
        assert all(x == 0 for x in res[1:]), 'norm not in base field'
        return res[0]

def det3_base(M, r):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1]) - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
            + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0])) % r

TABLE = [((1,2,3), ['-u,-1,v', '-v,-1,u', '-v,v,v']), ((1,3,2), ['-1,-u,-v', 'v,-u,1', 'u,-u,-u']),
 ((2,1,3), ['-u,v,1', '-v,v,-v', '-v,u,1']), ((3,1,2), ['-1,-u,v', '-1,-v,u', '-1,1,-1']),
 ((2,3,1), ['-1,-1,1', 'v,u,1', 'u,v,1']), ((3,2,1), ['1,-u,v', '-v,-v,v', '1,-v,u'])]

def forms_mod_r(r, uval):
    vval = (1 - uval) % r
    val = {'u': uval, 'v': vval, '1': 1}
    out = []
    for p, ts in TABLE:
        for t in ts:
            cs = []
            for x in t.split(','):
                sg = -1 if x.startswith('-') else 1
                cs.append(sg*val[x.lstrip('-')] % r)
            out.append((p, cs))
    return out

def build(r, uval, nodes, use_norm_factor=True, drop_node=None):
    K = Field(r)
    forms = forms_mod_r(r, uval)
    # Lagrange basis c_s = L_s(theta) in K
    def lagrange_elem(s):
        num = [1]; den = 1
        for t in nodes:
            if t == s: continue
            num = pmul(num, [(-t) % r, 1], r); den = den*(s-t) % r
        num = [x*pow(den, r-2, r) % r for x in num]
        num = num + [0]*(9-len(num))
        # evaluate polynomial (deg<=8) at theta in K
        acc = K.const(0); thp = K.const(1); theta = (0, 1, 0, 0, 0)
        for coef in num:
            acc = K.add(acc, K.scal(coef, thp)); thp = K.mul(thp, theta)
        return acc
    cs = {s: lagrange_elem(s) for s in nodes}
    inv9 = pow(9, r-2, r)
    def coordpoly_eval(x, s):  # x in K (power-basis coords), evaluate sum x_i s^i
        return sum(xi*pow(s, i, r) for i, xi in enumerate(x)) % r
    def ell(x): return x[0]
    def Zvec(X):  # X: 3x5 over F_r -> Z(X) in K^3 (power basis: beta_nu = theta^{nu-1})
        return [tuple(X[i]) for i in range(3)]
    def h(form, a, b):
        p, c = form
        acc = K.const(0)
        for i in range(3): acc = K.add(acc, K.scal(c[i], K.mul(a[p[i]-1], b[i])))
        return acc
    def construction_sum(Xs):
        cols = []
        for X in Xs:
            Z = Zvec(X)
            conj = [[K.frob(z, j) for z in Z] for j in range(5)]
            h1 = [h(f, conj[1], conj[2]) for f in forms]
            h2 = [h(f, conj[3], conj[4]) for f in forms]
            cols.append((Z, h1, h2))
        total = 0
        used_nodes = [s for s in nodes if s != drop_node]
        for w1 in range(18):
            for w2 in range(18):
                Fcol = []
                for (Z, h1, h2) in cols:
                    Hw = K.mul(h1[w1], h2[w2])
                    Fcol.append([K.mul(Z[i], Hw) for i in range(3)])
                for s in used_nodes:
                    M = [[0]*3 for _ in range(3)]
                    for j in range(3):
                        F1, F2, F3 = Fcol[j]
                        M[0][j] = (inv9 if use_norm_factor else 1) * coordpoly_eval(F1, s) % r
                        M[1][j] = coordpoly_eval(F2, s)
                        M[2][j] = ell(K.mul(cs[s], F3))
                    total = (total + det3_base(M, r)) % r
        return total
    def direct_norm(Xs):
        Zs = [Zvec(X) for X in Xs]
        M = [[Zs[j][i] for j in range(3)] for i in range(3)]
        return K.norm(K.det3(M))
    return K, construction_sum, direct_norm, Zvec

def label_X(K, xi):
    one = K.const(1); xi2 = K.mul(xi, xi)
    return [list(one), list(xi), list(xi2)]

def main(r, trials):
    roots = find_root_u(r)
    print(f'r={r}: roots of u^2-u+1 in F_r: {roots}')
    if not roots:
        print('   non-split prime: construction impossible (no u)'); return
    uval = roots[0]
    nodes = list(range(9))
    K, csum, dnorm, Zvec = build(r, uval, nodes)
    print('   irreducible quintic m(T) =', K.m, '(low->high)')
    ok = 0; nz = 0
    for t in range(trials):
        Xs = [[[random.randrange(r) for _ in range(5)] for _ in range(3)] for _ in range(3)]
        a, b = csum(Xs), dnorm(Xs)
        ok += (a == b); nz += (b != 0)
    print(f'   random inputs: construction == direct norm in {ok}/{trials} (nonzero norms: {nz})')
    # the other root of u^2-u+1 must work too
    K2, csum2, dnorm2, _ = build(r, roots[1], nodes)
    ok2 = 0
    for t in range(10):
        Xs = [[[random.randrange(r) for _ in range(5)] for _ in range(3)] for _ in range(3)]
        ok2 += csum2(Xs) == dnorm2(Xs)
    print(f'   other root u={roots[1]}: {ok2}/10')
    # nodes other than 0..8 (arbitrary 9 distinct)
    nodes2 = random.sample(range(r), 9)
    K3, csum3, dnorm3, _ = build(r, uval, nodes2)
    ok3 = 0
    for t in range(10):
        Xs = [[[random.randrange(r) for _ in range(5)] for _ in range(3)] for _ in range(3)]
        ok3 += csum3(Xs) == dnorm3(Xs)
    print(f'   random nodes {sorted(nodes2)}: {ok3}/10')
    # homogeneity of degree 5 in each group: scale X1 by lam -> sum scales by lam^5
    lam = 5
    hom = 0
    for t in range(5):
        Xs = [[[random.randrange(r) for _ in range(5)] for _ in range(3)] for _ in range(3)]
        Ys = [[[lam*x % r for x in row] for row in Xs[0]], Xs[1], Xs[2]]
        hom += csum(Ys) == pow(lam, 5, r)*csum(Xs) % r
    print(f'   homogeneity (deg 5 in group 1): {hom}/5')
    # CONTROLS (must fail)
    Kd, csumd, dnormd, _ = build(r, uval, nodes, drop_node=nodes[4])
    okd = 0
    for t in range(20):
        Xs = [[[random.randrange(r) for _ in range(5)] for _ in range(3)] for _ in range(3)]
        okd += csumd(Xs) == dnormd(Xs)
    print(f'   CONTROL drop one node: equal in {okd}/20 (must be ~0)')
    Kn, csumn, dnormn, _ = build(r, uval, nodes, use_norm_factor=False)
    okn = 0
    for t in range(20):
        Xs = [[[random.randrange(r) for _ in range(5)] for _ in range(3)] for _ in range(3)]
        a, b = csumn(Xs), dnormn(Xs)
        okn += (a == b and b != 0)
    print(f'   CONTROL omit 3^-2: equal&nonzero in {okn}/20 (must be 0)')
    # wrong u (not a root)
    badu = next(x for x in range(2, r) if (x*x-x+1) % r)
    Kb, csumb, dnormb, _ = build(r, badu, nodes)
    okb = 0
    for t in range(20):
        Xs = [[[random.randrange(r) for _ in range(5)] for _ in range(3)] for _ in range(3)]
        okb += csumb(Xs) == dnormb(Xs)
    print(f'   CONTROL u={badu} not a root: equal in {okb}/20 (must be ~0)')
    # Vandermonde labels
    dist_nonzero = 0; eq_zero = 0
    for t in range(20):
        xis = [tuple(random.randrange(r) for _ in range(5)) for _ in range(3)]
        if len(set(xis)) < 3: continue
        Xs = [label_X(K, xi) for xi in xis]
        dist_nonzero += csum(Xs) != 0
        Xs2 = [label_X(K, xis[0]), label_X(K, xis[0]), label_X(K, xis[2])]
        eq_zero += csum(Xs2) == 0
    print(f'   distinct labels -> sum != 0: {dist_nonzero}/20;  two equal labels -> sum == 0: {eq_zero}/20')

if __name__ == '__main__':
    r = int(sys.argv[1]); main(r, int(sys.argv[3]) if len(sys.argv) > 3 else 60)
