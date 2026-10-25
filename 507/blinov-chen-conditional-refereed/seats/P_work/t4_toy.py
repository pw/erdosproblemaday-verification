# Seat P, task 4: independent exact small-model of Lemma orb:tagged-moment's mechanism.
# Own toy (not the author's): label space F_r^m, row-1 residue 1 at position 0, row-2 tags at sparse positions,
# label-dependent arbitrary residues ABOVE the tag span in rows 1-2 and in every row-3 position,
# L1=L2=r (deterministic top rows), row-3 digits: M choices each, base B prime > L3.
# Everything is computed GENERICALLY from the 3x3 digit matrix: b from all nine 2x2 minors mod B^k,
# F_{k-1} from the cofactor expansion along row 3 (no use of the U(Z1-Z2) factorisation).
import sys, itertools, random
from fractions import Fraction
import numpy as np

def run(r, tags, k, M, B, label_pairs, seed=1, check_three=True, verbose=True, row3='random', topkey='full'):
    rng = random.Random(seed)
    m = len(tags); span = max(tags) + 1
    L3 = r * M
    assert B > L3
    hk = B**k
    assert hk < 2**31, 'keep products in int64'
    # label-dependent arbitrary residues
    table = {}
    def res(label, row, pos):
        key = (label, row, pos)
        if key not in table: table[key] = rng.randrange(r)
        return table[key]
    def top_rows(label):
        A = []; Q = []
        for p in range(k):
            if p < span:
                ra = 1 if p == 0 else 0
                rq = label[tags.index(p)] if p in tags else 0
            else:
                key = label if topkey == 'full' else tuple(label[:len(tags)])
                ra = res(key, 1, p); rq = res(key, 2, p)
            A.append(ra if ra else r); Q.append(rq if rq else r)   # unique rep in {1..r}
        return A, Q
    def third_choices(label):
        if row3 == 'random': reps = [(res(label, 3, p) or r) for p in range(k)]
        elif row3 == 'zero': reps = [r for p in range(k)]
        else: reps = [(res('shared', 3, p) or r) for p in range(k)]
        opts = []
        for choice in itertools.product(range(M), repeat=k):
            opts.append([reps[p] + r*choice[p] for p in range(k)])
        return np.array(opts, dtype=np.int64)          # shape (M^k, k)
    def val_at_B(digs):  # digits -> integer mod B^k
        return sum(int(d) * B**p for p, d in enumerate(digs)) % hk
    powB = np.array([B**p for p in range(k)], dtype=np.int64)
    def vB(x):  # B-adic valuation mod B^k, array
        x = x % hk
        v = np.zeros(x.shape, dtype=np.int64); y = x.copy()
        zero = (y == 0)
        for _ in range(k):
            nz = (y % B == 0) & (~zero)
            v += nz; y = np.where(nz, y // B, y)
        v[zero] = k
        return v
    def polymul(a, b):
        out = [0]*(len(a)+len(b)-1)
        for i, x in enumerate(a):
            for j, y in enumerate(b): out[i+j] += x*y
        return out
    results = []
    for (lam_list) in label_pairs:
        labels = lam_list
        tops = [top_rows(l) for l in labels]
        Zopts = [third_choices(l) for l in labels]
        Zval = [ (Z * powB[None, :]).sum(axis=1) % hk for Z in Zopts ]   # each digit < B so this is the base-B value
        # cofactor weights for F_{k-1} along row 3: F = sum_j (-1)^{3+j} z_j(Y) * minor_{3j}(Y)
        Ys = [ (tops[j][0], tops[j][1]) for j in range(3)]
        W = []
        for j in range(3):
            o = [c for c in range(3) if c != j]
            Ap, Qp = Ys[o[0]]; Aq, Qq = Ys[o[1]]
            minor = [x - y for x, y in zip(polymul(Ap, Qq), polymul(Aq, Qp))]
            sgn = (-1)**(3 + (j+1))
            # coefficient of Y^{k-1} in z_j(Y)*minor(Y): sum_p z_j[p] * minor[k-1-p]
            W.append(np.array([sgn * (minor[k-1-p] if 0 <= k-1-p < len(minor) else 0) for p in range(k)], dtype=np.int64))
        # integer entries mod B^k of the top rows
        Cv = [[val_at_B(tops[j][0]) for j in range(3)], [val_at_B(tops[j][1]) for j in range(3)]]
        nZ = Zopts[0].shape[0]
        total = nZ**3
        maxj = k
        cnt_bj_F = np.zeros(maxj+2, dtype=np.int64)   # count of (b>=j and F_{k-1}=0)
        cnt_bj = np.zeros(maxj+2, dtype=np.int64)
        cnt_F = 0; bmax = 0
        sumD_F = 0
        f1 = Zopts[0] @ W[0]; f2 = Zopts[1] @ W[1]; f3 = Zopts[2] @ W[2]
        for i1 in range(nZ):
            z1 = Zval[0][i1]
            z2 = Zval[1][:, None]; z3 = Zval[2][None, :]
            C = [[np.int64(Cv[0][0]), np.int64(Cv[0][1]), np.int64(Cv[0][2])],
                 [np.int64(Cv[1][0]), np.int64(Cv[1][1]), np.int64(Cv[1][2])],
                 [z1, z2, z3]]
            vmin = None
            for (ra, rb) in ((0,1),(0,2),(1,2)):
                for (ca, cb) in ((0,1),(0,2),(1,2)):
                    mnr = (C[ra][ca] * C[rb][cb] - C[ra][cb] * C[rb][ca]) % hk
                    mnr = np.broadcast_to(mnr, (nZ, nZ))
                    vv = vB(np.array(mnr))
                    vmin = vv if vmin is None else np.minimum(vmin, vv)
            b = vmin
            F = (f1[i1] + f2[:, None] + f3[None, :])
            Fz = (F == 0)
            cnt_F += int(Fz.sum())
            bmax = max(bmax, int(b.max()))
            for j in range(1, maxj+1):
                cnt_bj[j] += int((b >= j).sum()); cnt_bj_F[j] += int(((b >= j) & Fz).sum())
            sumD_F += int((np.power(B, b, dtype=object)[Fz]).sum()) if Fz.any() else 0
        results.append((labels, total, cnt_F, cnt_bj, cnt_bj_F, bmax, sumD_F, W))
    return results

def report(name, r, tags, k, M, B, label_triples, **kw):
    print(f'== {name}: r={r} tags={tags} k={k} M={M} B={B} {kw}')
    res = run(r, tags, k, M, B, label_triples, **kw)
    allok = True
    for (labels, total, cnt_F, cnt_bj, cnt_bj_F, bmax, sumD_F, W) in res:
        lam, lam2, mu = labels
        # a = tag position of first differing coordinate (only meaningful for (l,l,m))
        if lam == lam2 and lam != mu:
            s = next(i for i in range(len(lam)) if lam[i] != mu[i]); a = tags[s]
        else:
            a = None
        PF = Fraction(cnt_F, total)
        line = f'  labels {labels}: a={a} P(F=0)={PF}'
        ok = True
        if a is not None:
            ok &= PF <= Fraction(1, M)
            ok &= bmax <= a
            fac = (list(W[2]) == [0]*k) and (list(W[0]) == [-x for x in W[1]])
            line += f' b_max={bmax} (<=a: {bmax<=a}) factorisation-shape={fac}'
            for j in range(1, a+1):
                p = Fraction(int(cnt_bj_F[j]), total); bound = Fraction(1, M**(2*j+1))
                line += f' | j={j}: P(b>=j,F=0)={p} vs M^-(2j+1)={bound} {"OK" if p <= bound else "FAIL"}'
                ok &= p <= bound
            ED = Fraction(sumD_F, total); thb = Fraction(B, M*M)
            bnd = Fraction(1, M) * (1 + sum(thb**j for j in range(1, a+1)))
            line += f' | E[D1_F]={float(ED):.3g} <= {float(bnd):.3g}: {ED <= bnd}'
            ok &= ED <= bnd
        for j in range(1, 4):
            p = Fraction(int(cnt_bj[j]), total)
            ok &= p <= Fraction(1, M**(2*j))
        line += '  ' + ('OK' if ok else 'FAIL')
        allok &= ok
        print(line)
    print('  ALL OK' if allok else '  SOME FAIL')
    return allok

if __name__ == '__main__':
    which = sys.argv[1]
    if which == 'main':
        r, tags, k, M = 5, (0, 1, 3), 8, 2
        lam = (2, 0, 4)
        triples = [ (lam, lam, (3, 0, 4)),     # differ at s=0 -> a=0
                    (lam, lam, (2, 1, 4)),     # s=1 -> a=1
                    (lam, lam, (2, 0, 1)),     # s=2 -> a=3
                    ((0, 0, 0), (0, 0, 0), (0, 0, 1)),   # zero coords -> rep r; a=3
                    ((1, 2, 3), (1, 2, 3), (1, 2, 3)),   # all equal (uniform bound only)
                    ((1, 2, 3), (4, 2, 3), (1, 0, 3)) ]  # distinct
        for B in (13,):
            for row3 in ('random', 'zero', 'shared'):
                report('main toy', r, tags, k, M, B, triples, row3=row3)
    elif which == 'M3':
        r, tags, k, M = 7, (0, 2), 5, 3
        triples = [((1, 5), (1, 5), (1, 6)), ((1, 5), (1, 5), (2, 5)), ((0, 0), (0, 0), (0, 3))]
        for row3 in ('random', 'zero', 'shared'):
            report('M=3 toy', r, tags, k, M, 23, triples, row3=row3)
    elif which == 'neg_prefix':
        # NEGATIVE CONTROL: fresh position inside the low prefix: tags (0,1), a=1, k=2 -> v=k-1-a=0 < j=1
        r, tags, k, M = 5, (0, 1), 2, 2
        report('NEG fresh digit inside prefix', r, tags, k, M, 11, [((2, 3), (2, 3), (2, 4))], row3='zero')
        r, tags, k, M = 5, (0, 1), 2, 3
        report('NEG fresh digit inside prefix (M=3)', r, tags, k, M, 17, [((2, 3), (2, 3), (2, 4))], row3='zero')
        r, tags, k, M = 5, (0, 1, 3), 6, 2
        report('NEG fresh digit inside prefix, a=3, k=6 (v=2<j=3)', r, tags, k, M, 11, [((2, 3, 1), (2, 3, 1), (2, 3, 4))], row3='zero')
        report('POS same labels, k=8 (v=4>=j)', r, tags, 8, M, 11, [((2, 3, 1), (2, 3, 1), (2, 3, 4))], row3='zero')
    elif which == 'neg_notag':
        # NEGATIVE CONTROL: labels differ only in an UNTAGGED coordinate (tag omitted): top rows agree below span,
        # emulate by tags (0,1,3) but labels differing only in coordinate that we do not place: use tags (0,1) with
        # a 3-coordinate label whose 3rd coordinate is not tagged -> top rows identical -> no U_a.
        r, k, M = 5, 6, 2
        res = run(r, (0, 1), k, M, 11, [((2, 3, 1), (2, 3, 1), (2, 3, 4))], row3='zero', topkey='tagged')
        for (labels, total, cnt_F, cnt_bj, cnt_bj_F, bmax, sumD_F, W) in res:
            print(f'== NEG omitted tag: labels {labels}: P(F=0)={Fraction(cnt_F,total)} (lemma would claim <=1/{M}), '
                  f'P(b>=1,F=0)={Fraction(int(cnt_bj_F[1]),total)} vs M^-3={Fraction(1,M**3)}, b_max={bmax}')
