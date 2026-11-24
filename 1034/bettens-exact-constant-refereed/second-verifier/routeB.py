"""Route B: an independent exact cross-check on a random sample of order-7 graphs.

Different from route A in every combinatorial step:
  * H is taken straight from model['graph_slack_flags'] (route A used our geng representatives + bijection);
  * coefficients are averages over ALL 7! = 5040 vertex orderings pi of H: roots sit at positions 0..k-1 and the
    extension sets at the next positions (lower-order terms simply ignore the leftover positions);
  * flags are identified by looking the LABELLED sub-mask up in a dict of all root-fixing relabellings of each
    model flag (route A canonicalised by a min over orderings);
  * each block term is the bilinear form v_A^T Q v_B evaluated directly with Q (route A used P = C^T Q C);
  * the Bollobas term is built generically from the descriptor's indicators [m sector vertices, e edges];
  * arithmetic: exact Q(sqrt3) with Fractions.
Compares every term with route A's exact per-term values, and runs convention controls (variants of the
semantics that must break the identity).

usage: python3 routeB.py NSAMPLE SEED [--variants]
"""
import os
import itertools
import pickle
import random
import sys
import time
from collections import Counter
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import PIDX, kparse, kadd, kmul, kscale, kiszero, kfloat, load_model, load_cert, relabel, ZERO

T0 = time.time()
N = 7


def log(*a):
    print(f'[{time.time() - T0:7.1f}s]', *a, flush=True)


def sub(adj, verts):
    ell = len(verts)
    m = 0
    for (i, j), b in PIDX[ell].items():
        if adj[verts[i]][verts[j]]:
            m |= 1 << b
    return m


def orbit(mask, k, ell):
    out = set()
    for o in itertools.permutations(range(k, ell)):
        out.add(relabel(mask, ell, list(range(k)) + list(o)))
    return out


class Setup:
    def __init__(self, model, cert):
        self.cstar = kparse(model['definitions']['c_star'])
        self.blocks = []
        for bi, blk in enumerate(model['matrix_blocks']):
            k, tm = blk['type']
            ell = blk['flag_order']
            fdict, phi = {}, []
            for r, row in enumerate(blk['basis']):
                for mask, c in row:
                    if mask not in fdict:
                        fid = len(phi)
                        phi.append([])
                        for lm in orbit(mask, k, ell):
                            assert lm not in fdict
                            fdict[lm] = fid
                    phi[fdict[mask]].append((r, Fraction(c)))
            Q = [[kparse(x) for x in row] for row in cert['matrices'][bi]]
            self.blocks.append({'k': k, 'type': tm, 'ell': ell, 'fdict': fdict, 'phi': phi, 'Q': Q})
        self.lam = [kparse(x) for x in cert['scalar_multipliers']]
        self.slack = [kparse(x) for x in cert['graph_slacks']]
        self.pdict = {}
        for j, g in enumerate(model['scalar_generators'][:816]):
            for lm in orbit(g[2], 3, 6):
                self.pdict.setdefault(lm, []).append(j)
        self.bol = model['definitions']['bollobas']
        self.rho = model['definitions']['rho']

    def bil(self, bi, fa, fb):
        blk = self.blocks[bi]
        acc = ZERO
        for r, ca in blk['phi'][fa]:
            for s, cb in blk['phi'][fb]:
                acc = kadd(acc, kscale(blk['Q'][r][s], ca * cb))
        return acc


def indicator_set(k, tm, sector, m, e, variant):
    """all labelled (k+m)-vertex masks whose roots induce tm and whose m extension vertices are all adjacent to
    every sector root and span exactly e edges among themselves"""
    ell = k + m
    ext_pairs = [p for p in itertools.combinations(range(ell), 2) if p[1] >= k]
    base = 0
    for (i, j), b in PIDX[k].items():
        if (tm >> b) & 1:
            base |= 1 << PIDX[ell][(i, j)]
    out = set()
    for bits in range(2 ** len(ext_pairs)):
        msk = base
        for t, p in enumerate(ext_pairs):
            if (bits >> t) & 1:
                msk |= 1 << PIDX[ell][p]
        ok = all((msk >> PIDX[ell][(s, x)]) & 1 for x in range(k, ell) for s in sector)
        inner = sum((msk >> PIDX[ell][(x, y)]) & 1 for x, y in itertools.combinations(range(k, ell), 2))
        if ok and inner == e:
            out.add(msk)
    return out


def coeffs(S, Hmask, variant=None):
    adj = [[0] * N for _ in range(N)]
    for (i, j), b in PIDX[N].items():
        if (Hmask >> b) & 1:
            adj[i][j] = adj[j][i] = 1
    k_b, tm_b = S.bol['type']
    sector = S.bol['sector_roots'] if variant != 'bol_sector_23' else [2, 3]
    isets = {name: indicator_set(k_b, tm_b, sector, m, e, variant) for name, (m, e) in S.bol['indicators'].items()}
    bterms = [(Fraction(c), names) for c, names in S.bol['terms']]
    blocks_by_type = {}
    for bi, blk in enumerate(S.blocks):
        blocks_by_type.setdefault((blk['k'], blk['type'], blk['ell']), []).append(bi)
    pair_counts = Counter()  # (bi, fa, fb, weight-kind) -> count
    lam_counts = Counter()   # (j, D) -> count
    rho_num = 0
    bol_num = Fraction(0)
    for pi in itertools.permutations(range(N)):
        A = [[adj[pi[s]][pi[t]] for t in range(N)] for s in range(N)]
        P = list(range(N))
        rho_num += A[0][1]
        for k in (1, 3, 5):
            t = sub(A, P[:k])
            if k == 5:
                for bi in blocks_by_type.get((5, t, 6), []):
                    fd = S.blocks[bi]['fdict']
                    fa, fb = fd.get(sub(A, P[:5] + [5])), fd.get(sub(A, P[:5] + [6]))
                    if fa is not None and fb is not None:
                        pair_counts[(bi, fa, fb, 'plain')] += 1
            if k == 3:
                for bi in blocks_by_type.get((3, t, 5), []):
                    fd = S.blocks[bi]['fdict']
                    fa, fb = fd.get(sub(A, P[:5])), fd.get(sub(A, P[:3] + [5, 6]))
                    if fa is not None and fb is not None:
                        pair_counts[(bi, fa, fb, 'plain')] += 1
                if t == 7:
                    def Dval(x):
                        nb = A[x][0] + A[x][1] + A[x][2]
                        if variant == 'D_exactly2':
                            return int(nb == 2)
                        if variant == 'D_atleast1':
                            return int(nb >= 1)
                        return int(nb >= 2)
                    fd = S.blocks[0]['fdict']
                    fa, fb = fd.get(sub(A, P[:4])), fd.get(sub(A, P[:3] + [4]))
                    if fa is not None and fb is not None:
                        pair_counts[(0, fa, fb, 'D' if Dval(5) else 'noD')] += 1
                    js = S.pdict.get(sub(A, P[:6]))
                    if js:
                        for j in js:
                            lam_counts[(j, Dval(6))] += 1
            if k == 1:
                for bi in blocks_by_type.get((1, t, 4), []):
                    fd = S.blocks[bi]['fdict']
                    if variant == 'labelled_flags':
                        # identify flags only by their exact labelled mask (no non-root symmetry)
                        fa, fb = fd.get(sub(A, P[:4])), fd.get(sub(A, [0, 4, 5, 6]))
                        ma, mb = sub(A, P[:4]), sub(A, [0, 4, 5, 6])
                        if fa is not None and ma != S.blocks[bi]['rep'][fa]:
                            fa = None
                        if fb is not None and mb != S.blocks[bi]['rep'][fb]:
                            fb = None
                    else:
                        fa, fb = fd.get(sub(A, P[:4])), fd.get(sub(A, [0, 4, 5, 6]))
                    if fa is not None and fb is not None:
                        pair_counts[(bi, fa, fb, 'plain')] += 1
        if sub(A, P[:k_b]) == tm_b:
            for c, names in bterms:
                pos = k_b
                val = 1
                for nm in names:
                    m = S.bol['indicators'][nm][0]
                    val *= int(sub(A, P[:k_b] + list(range(pos, pos + m))) in isets[nm])
                    pos += m
                    if not val:
                        break
                bol_num += c * val
    nperm = 5040
    terms = {}
    rho_c = Fraction(S.rho['coefficient'])
    if variant == 'rho_no_half':
        rho_c = Fraction(1)
    terms['rho'] = (rho_c * Fraction(rho_num, nperm), Fraction(0))
    for bi in range(len(S.blocks)):
        terms[f'block{bi}'] = ZERO
    for (bi, fa, fb, kind), n in pair_counts.items():
        v = kscale(S.bil(bi, fa, fb), Fraction(n, nperm))
        if bi == 0:
            w = S.cstar if kind == 'noD' else kadd(S.cstar, (Fraction(-1), Fraction(0)))
            v = kmul(w, v)
        terms[f'block{bi}'] = kadd(terms[f'block{bi}'], v)
    acc = ZERO
    for (j, d), n in lam_counts.items():
        w = S.cstar if not d else kadd(S.cstar, (Fraction(-1), Fraction(0)))
        acc = kadd(acc, kscale(kmul(S.lam[j], w), Fraction(n, nperm)))
    terms['lambda'] = acc
    terms['beta'] = kscale(S.lam[816], bol_num / nperm)
    terms['const'] = kadd(S.lam[817], kscale(S.lam[818], -1))
    return terms


def main():
    nsample = int(sys.argv[1])
    seed = int(sys.argv[2])
    variants = '--variants' in sys.argv
    model, cert = load_model(), load_cert()
    S = Setup(model, cert)
    for blk, raw in zip(S.blocks, model['matrix_blocks']):
        rep = {}
        for row in raw['basis']:
            for mask, c in row:
                rep.setdefault(blk['fdict'][mask], mask)
        blk['rep'] = rep
    A = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'termsA.pkl'), 'rb'))
    pos_of = {r['model_index']: i for i, r in enumerate(A['basis'])}
    rng = random.Random(seed)
    sample = set(rng.sample(range(1044), nsample))
    if '--include-beta' in sys.argv:
        # add 6 graphs on which the rooted Bollobas term has nonzero coefficient (per route A)
        bz = [r['model_index'] for r, t in zip(A['basis'], A['termsE']) if not kiszero(t['beta'])]
        sample |= set(rng.sample(bz, 6))
    sample = sorted(sample)
    log(f'sample (model indices, seed {seed}): {sample}')
    mism = 0
    for h in sample:
        t = time.time()
        Hmask = model['graph_slack_flags'][h]
        terms = coeffs(S, Hmask)
        terms['slack'] = S.slack[h]
        tot = ZERO
        for v in terms.values():
            tot = kadd(tot, v)
        TA = A['termsE'][pos_of[h]]
        diff = [name for name in terms if terms[name] != TA[name]]
        mism += bool(diff) or not kiszero(tot)
        nz = sum(1 for v in terms.values() if not kiszero(v))
        log(f'H#{h:4d} edges={bin(Hmask).count("1"):2d}: residual exactly zero: {kiszero(tot)}; '
            f'per-term agreement with route A: {"ALL " + str(len(terms)) if not diff else "MISMATCH " + str(diff)}; '
            f'nonzero terms {nz}; rho={kfloat(terms["rho"]):.4f} lambda={kfloat(terms["lambda"]):.3e} '
            f'beta={kfloat(terms["beta"]):.3e} slack={kfloat(terms["slack"]):.3e} ({time.time() - t:.1f}s)')
    print('ROUTE B OK' if not mism else f'ROUTE B: {mism} graphs disagree')
    if not variants:
        return
    log('--- convention controls (each variant must break the identity on some sampled graph) ---')
    for variant in ['D_exactly2', 'D_atleast1', 'rho_no_half', 'bol_sector_23', 'labelled_flags']:
        broken = []
        for h in sample:
            Hmask = model['graph_slack_flags'][h]
            terms = coeffs(S, Hmask, variant)
            terms['slack'] = S.slack[h]
            tot = ZERO
            for v in terms.values():
                tot = kadd(tot, v)
            if not kiszero(tot):
                broken.append((h, f'{kfloat(tot):.3e}'))
        log(f'variant {variant}: identity broken on {len(broken)}/{len(sample)} sampled graphs; e.g. {broken[:4]}')


if __name__ == '__main__':
    main()
