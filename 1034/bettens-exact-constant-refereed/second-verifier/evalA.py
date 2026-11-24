"""Route A, arithmetic half: rebuild every generator from the model descriptors, then evaluate the residual
  R_H = rho + sum_b block_b + sum_j lambda_j g_j + beta*B5root + (lambda_817 - lambda_818) + s_H
for all 1044 order-7 graphs H
  (i) EXACTLY over Q(sqrt3) (integer numerators over a per-block common denominator), and
  (ii) MODULO three random large primes p = +-1 mod 12, at BOTH square roots of 3 mod p, computing from the
       data reduced mod p (Q mod p, basis coefficients mod p), never from the exact results.
Also the descriptor sanity checks and the negative controls (mutations) for the identity.

usage: python3 evalA.py [--controls]
"""
import os
import itertools
import json
import math
import pickle
import random
import sys
import time
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import (PIDX, kparse, kadd, kmul, kscale, ksign, kiszero, load_model, load_cert, relabel, restrict,
                  ZERO)

T0 = time.time()


def log(*a):
    print(f'[{time.time() - T0:7.1f}s]', *a, flush=True)


# ---------------------------------------------------------------- flags
_PERMS = {}


def ext_perms(k, ell):
    key = (k, ell)
    if key not in _PERMS:
        ps = []
        for o in itertools.permutations(range(k, ell)):
            ps.append(list(range(k)) + list(o))
        _PERMS[key] = ps
    return _PERMS[key]


def canon_flag(mask, k, ell):
    """min over relabellings fixing the roots 0..k-1"""
    return min(relabel(mask, ell, p) for p in ext_perms(k, ell))


def check_root_type(mask, k, ell, tmask_):
    return restrict(mask, ell, list(range(k))) == tmask_


# ---------------------------------------------------------------- model parsing + descriptor checks
def parse_model(model, report):
    sq = model['field']
    assert sq == {'radicand': 3, 'embedding': 'positive'}, sq
    assert model['target_order'] == 7 and model['target_bound'] == '1/4'
    d = model['definitions']
    assert d['triangle_type'] == [3, 7]
    # c* must be (36 - 5 sqrt3)/66
    cstar = kparse(d['c_star'])
    assert cstar == (Fraction(36, 66), Fraction(-5, 66)), cstar
    # rho = 1/2 * density of K2
    assert d['rho'] == {'flag': [2, 1], 'coefficient': '1/2'}, d['rho']
    # D derived from the paper: one-vertex tau-flags whose new vertex has >= 2 root neighbours
    myD = set()
    for adjbits in range(8):
        m = 0b0 | (1 << PIDX[4][(0, 1)]) | (1 << PIDX[4][(0, 2)]) | (1 << PIDX[4][(1, 2)])
        for i in range(3):
            if (adjbits >> i) & 1:
                m |= 1 << PIDX[4][(i, 3)]
        if bin(adjbits).count('1') >= 2:
            myD.add(m)
    assert d['D']['flag_order'] == 4
    modelD = {}
    for mask, c in d['D']['terms']:
        assert check_root_type(mask, 3, 4, 7)
        modelD[canon_flag(mask, 3, 4)] = modelD.get(canon_flag(mask, 3, 4), 0) + Fraction(c)
    assert modelD == {m: 1 for m in myD}, (modelD, myD)
    report.append(f'D: model terms == derived set {sorted(myD)} (new vertex adjacent to >=2 roots), coefficient 1 each')
    # Bollobas descriptor == paper (13) with w(y) = W(x0,y)W(x1,y), type K4 - 01
    b = d['bollobas']
    assert b['type'] == [4, 62] and b['sector_roots'] == [0, 1]
    assert b['indicators'] == {'X': [1, 0], 'E': [2, 1], 'T': [3, 3], 'P3': [3, 2]}, b['indicators']
    assert b['terms'] == [['1', ['X', 'X', 'X']], ['-11', ['X', 'E']], ['30', ['T']], ['15', ['P3']]], b['terms']
    # 62 = all pairs of 4 vertices except (0,1)
    assert 62 == sum(1 << PIDX[4][p] for p in itertools.combinations(range(4), 2) if p != (0, 1))
    report.append('Bollobas descriptor == paper: type K4-01 (62), sector N(0)&N(1), X^3 - 11 X E + 30 T + 15 P3')

    blocks = []
    merged_rows = 0
    for bi, blk in enumerate(model['matrix_blocks']):
        k, tm = blk['type']
        ell = blk['flag_order']
        assert 2 * ell - k <= 7 + (1 if blk['kind'] == 'triangle_localizer_psd' else 0)
        if bi == 0:
            assert blk['kind'] == 'triangle_localizer_psd' and blk['type'] == [3, 7] and ell == 4
        else:
            assert blk['kind'] == 'flag_psd'
        rows = []
        for row in blk['basis']:
            vec = {}
            for mask, c in row:
                assert 0 <= mask < 2 ** (ell * (ell - 1) // 2)
                assert check_root_type(mask, k, ell, tm), (bi, mask)
                cf = canon_flag(mask, k, ell)
                if cf in vec:
                    merged_rows += 1
                vec[cf] = vec.get(cf, 0) + Fraction(c)
            vec = {f: c for f, c in vec.items() if c != 0}
            rows.append(vec)
        blocks.append({'k': k, 'type': tm, 'ell': ell, 'rows': rows, 'kind': blk['kind']})
    report.append(f'basis rows: every flag mask has roots inducing its labelled type; '
                  f'{merged_rows} rows contained two masks of the same flag (merged)')

    gens = model['scalar_generators']
    assert len(gens) == 819
    Pflags = []
    for j, g in enumerate(gens[:816]):
        assert g[0] == 'P_flag' and g[1] == 6
        assert check_root_type(g[2], 3, 6, 7), j
        Pflags.append(canon_flag(g[2], 3, 6))
    assert gens[816] == ['bollobas'] and gens[817] == ['constant', '1'] and gens[818] == ['constant', '-1']
    ndup = len(Pflags) - len(set(Pflags))
    # how many order-6 tau-flags exist?  enumerate all labelled ones and canonicalise
    allF = set()
    base = 7  # root triangle in the 6-vertex indexing
    rootbits = sum(1 << PIDX[6][p] for p in [(0, 1), (0, 2), (1, 2)])
    extpairs = [p for p in itertools.combinations(range(6), 2) if p[1] >= 3]
    for bits in range(2 ** len(extpairs)):
        m = rootbits
        for t, p in enumerate(extpairs):
            if (bits >> t) & 1:
                m |= 1 << PIDX[6][p]
        allF.add(canon_flag(m, 3, 6))
    report.append(f'816 P_flag generators: all valid order-6 tau-flags; {ndup} duplicates; '
                  f'{len(set(Pflags))} distinct of {len(allF)} order-6 tau-flags in existence')
    return cstar, blocks, Pflags


def parse_cert(cert, blocks):
    Q = []
    for bi, M in enumerate(cert['matrices']):
        n = len(blocks[bi]['rows'])
        assert len(M) == n and all(len(r) == n for r in M), bi
        QM = [[kparse(x) for x in r] for r in M]
        for i in range(n):
            for j in range(i):
                assert QM[i][j] == QM[j][i], ('not symmetric', bi, i, j)
        Q.append(QM)
    lam = [kparse(x) for x in cert['scalar_multipliers']]
    slack = [kparse(x) for x in cert['graph_slacks']]
    assert len(lam) == 819 and len(slack) == 1044
    return Q, lam, slack


# ---------------------------------------------------------------- arithmetic back-ends
class Exact:
    """Q(sqrt3) as (Fraction, Fraction)"""
    name = 'exact'

    def __init__(self):
        pass

    def conv(self, x):
        return x

    def rat(self, q):
        return (Fraction(q), Fraction(0))

    add = staticmethod(kadd)
    mul = staticmethod(kmul)
    zero = ZERO

    def scale_int(self, x, n):
        return (x[0] * n, x[1] * n)

    def iszero(self, x):
        return kiszero(x)


class Modp:
    """F_p via the homomorphism sqrt3 -> r (r^2 = 3 mod p)"""

    def __init__(self, p, r):
        assert (r * r - 3) % p == 0
        self.p, self.r = p, r
        self.name = f'mod p={p} sqrt3->{r}'
        self.zero = 0

    def rq(self, q):
        q = Fraction(q)
        if q.denominator % self.p == 0:
            raise ValueError('denominator divisible by p')
        return q.numerator % self.p * pow(q.denominator, -1, self.p) % self.p

    def conv(self, x):
        return (self.rq(x[0]) + self.rq(x[1]) * self.r) % self.p

    def rat(self, q):
        return self.rq(q)

    def add(self, x, y):
        return (x + y) % self.p

    def mul(self, x, y):
        return x * y % self.p

    def scale_int(self, x, n):
        return x * n % self.p

    def iszero(self, x):
        return x % self.p == 0


NORM = {'b5': 2520 * 2, 'b3': 210 * 6, 'b1': 7 * 20, 't0': 210 * 24, 't6': 210 * 4, 'bol': 840 * 3}


def block_pair_values(F, Qb, rows):
    """P[(f,g)] = sum_{r,s} c_r(f) Q[r][s] c_s(g) over flags f,g in the block's support, in field F"""
    n = len(rows)
    Qc = [[F.conv(Qb[i][j]) for j in range(n)] for i in range(n)]
    phi = {}
    for r, vec in enumerate(rows):
        for f, c in vec.items():
            phi.setdefault(f, []).append((r, F.rat(c)))
    P = {}
    for f, pf in phi.items():
        for g, pg in phi.items():
            acc = F.zero
            for r, cr in pf:
                for s, cs in pg:
                    acc = F.add(acc, F.mul(F.mul(cr, Qc[r][s]), cs))
            P[(f, g)] = acc
    return P


def dot(F, counts, P):
    acc = F.zero
    for key, n in counts.items():
        v = P.get(key)
        if v is not None:
            acc = F.add(acc, F.scale_int(v, n))
    return acc


def evaluate(F, cstar, blocks, Pflags, Q, lam, slack, counts, basis, want_terms=False):
    """returns per-H residual (and optionally per-term contributions) in field F"""
    Pb = [block_pair_values(F, Q[bi], blocks[bi]['rows']) for bi in range(len(blocks))]
    cs = F.conv(cstar)
    lamc = [F.conv(x) for x in lam]
    slc = [F.conv(x) for x in slack]
    inv = {k: F.rat(Fraction(1, v)) for k, v in NORM.items()}
    gen_of = {}
    for j, f in enumerate(Pflags):
        gen_of.setdefault(f, []).append(j)
    res = []
    terms_all = []
    for H, C in zip(basis, counts):
        terms = {}
        terms['rho'] = F.rat(Fraction(C['edges'], 42))
        for bi, blk in enumerate(blocks):
            if bi == 0:
                a = dot(F, C['t0all'], Pb[0])
                d = dot(F, C['t0D'], Pb[0])
                v = F.mul(F.add(F.mul(cs, a), F.mul(F.rat(-1), d)), inv['t0'])
            elif blk['k'] == 5:
                v = F.mul(dot(F, C['b5'].get(blk['type'], {}), Pb[bi]), inv['b5'])
            elif blk['k'] == 3:
                v = F.mul(dot(F, C['b3'].get(blk['type'], {}), Pb[bi]), inv['b3'])
            elif blk['k'] == 1:
                assert blk['type'] == 0 and blk['ell'] == 4
                v = F.mul(dot(F, C['b1'], Pb[bi]), inv['b1'])
            else:
                raise AssertionError(blk)
            terms[f'block{bi}'] = v
        acc = F.zero
        for f, nall in C['t6all'].items():
            js = gen_of.get(f)
            if not js:
                continue
            g = F.mul(F.add(F.mul(cs, F.rat(nall)), F.rat(-C['t6D'].get(f, 0))), inv['t6'])
            for j in js:
                acc = F.add(acc, F.mul(lamc[j], g))
        terms['lambda'] = acc
        terms['beta'] = F.mul(lamc[816], F.mul(F.rat(C['bol3']), inv['bol']))
        terms['const'] = F.add(lamc[817], F.mul(F.rat(-1), lamc[818]))
        terms['slack'] = slc[H['model_index']]
        tot = F.zero
        for v in terms.values():
            tot = F.add(tot, v)
        res.append(tot)
        if want_terms:
            terms_all.append(terms)
    return (res, terms_all) if want_terms else res


# ---------------------------------------------------------------- primes
def is_prime(n):
    if n < 2:
        return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    for q in small:
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in small:  # deterministic for n < 3.3e24
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def sqrt_mod(a, p):
    """Tonelli-Shanks"""
    a %= p
    assert pow(a, (p - 1) // 2, p) == 1
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i, tt = 0, t
        while tt != 1:
            tt = tt * tt % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    assert r * r % p == a
    return r


def random_primes(rng, count, bits=62):
    out = []
    while len(out) < count:
        p = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if p % 12 not in (1, 11):
            continue
        if is_prime(p):
            out.append(p)
    return out


# ---------------------------------------------------------------- main
def run_all(cstar, blocks, Pflags, Q, lam, slack, counts, basis, fields, want_terms=False):
    out = {}
    for F in fields:
        out[F.name] = evaluate(F, cstar, blocks, Pflags, Q, lam, slack, counts, basis, want_terms)
    return out


def nonzero_list(F, res, basis):
    return [basis[i]['model_index'] for i, v in enumerate(res) if not F.iszero(v)]


def main():
    controls = '--controls' in sys.argv
    report = []
    model = load_model()
    cert = load_cert()
    assert cert['source_sha256'] == model['certificate_sha256']
    cstar, blocks, Pflags = parse_model(model, report)
    Q, lam, slack = parse_cert(cert, blocks)
    basis = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'basis.json')))
    counts = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'counts.pkl'), 'rb'))
    for line in report:
        log(line)
    # multipliers that the paper states explicitly
    beta = lam[816]
    assert beta == (Fraction(1917, 10), Fraction(-1648, 15)), beta
    const = kadd(lam[817], kscale(lam[818], -1))
    log(f'beta = {beta[0]} + {beta[1]} sqrt3 (== paper (32)); constant term lambda817 - lambda818 = '
        f'{const[0]} + {const[1]} sqrt3')
    assert const == (Fraction(-1, 4), Fraction(0))

    seed = random.SystemRandom().getrandbits(64)
    rng = random.Random(seed)
    primes = random_primes(rng, 3)
    fields = [Exact()]
    for p in primes:
        r = sqrt_mod(3, p)
        fields += [Modp(p, r), Modp(p, p - r)]
    log(f'prime seed {seed}; primes {primes} (all = +-1 mod 12)')

    # ---- positive run
    t = time.time()
    resE, termsE = evaluate(fields[0], cstar, blocks, Pflags, Q, lam, slack, counts, basis, want_terms=True)
    nzE = nonzero_list(fields[0], resE, basis)
    log(f'EXACT residual: {1044 - len(nzE)}/1044 coefficients exactly zero ({time.time() - t:.1f}s)')
    for F in fields[1:]:
        t = time.time()
        resF = evaluate(F, cstar, blocks, Pflags, Q, lam, slack, counts, basis)
        nz = nonzero_list(F, resF, basis)
        # exact residual reduced mod p must agree (sanity of both back-ends)
        agree = all(F.conv(e) == m for e, m in zip(resE, resF))
        log(f'{F.name}: {1044 - len(nz)}/1044 zero; agrees with exact residual reduced mod p: {agree} '
            f'({time.time() - t:.1f}s)')
    # per-term magnitudes (floats only for the report)
    pickle.dump({'termsE': termsE, 'basis': basis}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'termsA.pkl'), 'wb'))
    log('wrote termsA.pkl (exact per-term contributions for every H)')
    if nzE:
        log(f'NONZERO exact residuals at model indices: {nzE[:30]}')
        print('IDENTITY FAILED')
    else:
        print('IDENTITY OK (exact, all 1044) ')

    if not controls:
        return
    # ---- negative controls: each mutation must make the identity fail
    F2 = fields[1]  # first modular field
    FE = fields[0]

    def mut_run(label, Qm, lamm, slackm, cstarm):
        out = {}
        for F in (FE, F2, fields[2]):
            res = evaluate(F, cstarm, blocks, Pflags, Qm, lamm, slackm, counts, basis)
            out[F.name] = nonzero_list(F, res, basis)
        sizes = {k: len(v) for k, v in out.items()}
        same = len({tuple(v) for v in out.values()}) == 1
        ex = out['exact']
        log(f'CONTROL {label}: nonzero residual on {sizes} graphs; exact & both roots mod p agree on the set: {same}; '
            f'first model indices {ex[:12]}')
        return out

    eps = (Fraction(1, 10 ** 6), Fraction(0))
    # 1 slack
    h = 517
    sl2 = list(slack)
    sl2[h] = kadd(sl2[h], eps)
    o = mut_run(f'slack[{h}] += 1e-6', Q, lam, sl2, cstar)
    assert o['exact'] == [h]
    # 1b slack sqrt3-part only (checks the sqrt3 coordinate is not ignored)
    sl3 = list(slack)
    sl3[h] = kadd(sl3[h], (Fraction(0), Fraction(1, 10 ** 6)))
    o = mut_run(f'slack[{h}] += 1e-6*sqrt3', Q, lam, sl3, cstar)
    assert o['exact'] == [h]
    # 2 lambda: pick a nonzero one
    j = next(i for i in range(816) if not kiszero(lam[i]) and i > 100)
    l2 = list(lam)
    l2[j] = kadd(l2[j], eps)
    mut_run(f'lambda[{j}] += 1e-6', Q, l2, slack, cstar)
    # 2b a lambda that is zero in the certificate
    j0 = next(i for i in range(816) if kiszero(lam[i]))
    l3 = list(lam)
    l3[j0] = eps
    mut_run(f'lambda[{j0}] (was 0) := 1e-6', Q, l3, slack, cstar)
    # 3 off-diagonal Q entry, symmetric
    for bi, (r, s) in [(0, (1, 2)), (5, (3, 17)), (40, (0, 1))]:
        Q2 = [M if b != bi else [row[:] for row in M] for b, M in enumerate(Q)]
        Q2[bi][r][s] = kadd(Q2[bi][r][s], eps)
        Q2[bi][s][r] = kadd(Q2[bi][s][r], eps)
        mut_run(f'Q{bi}[{r},{s}] and [{s},{r}] += 1e-6', Q2, lam, slack, cstar)
    # 4 beta
    l4 = list(lam)
    l4[816] = kadd(l4[816], eps)
    mut_run('beta += 1e-6', Q, l4, slack, cstar)
    # 5 c*
    mut_run('c* += 1e-6', Q, lam, slack, kadd(cstar, eps))
    # 6 the constant
    l5 = list(lam)
    l5[817] = kadd(l5[817], eps)
    mut_run('lambda817 (constant) += 1e-6', Q, l5, slack, cstar)
    log('controls done')


if __name__ == '__main__':
    main()
