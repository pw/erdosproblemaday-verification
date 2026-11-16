"""analyze.py -- census analysis of export_*.txt lines produced by export.g.

usage: python3 analyze.py OUT_PREFIX [--wrong-table] FILE...

For every group: omega (exact, witness clique re-checked), a = chi (exact: witness
colouring re-checked; optimality by clique = colouring size or SAT UNSAT at chi-1),
z.  Flags
  A-VIOL : a > T(omega)
  Z-VIOL : omega >= 3 and z > (T(omega)-1)^2
  A-EQ   : a == T(omega) (omega >= 3)
  Z-EQ   : omega >= 3 and z == (T(omega)-1)^2
--wrong-table uses T'(7)=9 (deliberately wrong; control).
Writes OUT_PREFIX.tsv (one row per group) and OUT_PREFIX.summary.txt.
"""
import sys, time
from collections import defaultdict
from graphlib import T as T_true, parse_rows, max_clique, chromatic, check_clique, check_colouring


def T_wrong(n):
    return 9 if n == 7 else T_true(n)


def main():
    args = sys.argv[1:]
    prefix = args.pop(0)
    wrong = False
    if '--wrong-table' in args:
        args.remove('--wrong-table')
        wrong = True
    T = T_wrong if wrong else T_true
    rows_out = []
    flags = defaultdict(list)
    dist = defaultdict(lambda: {'count': 0, 'maxa': 0, 'maxa_ids': [], 'maxz': 0, 'maxz_ids': [], 'pairs': defaultdict(int)})
    t0 = time.time()
    ngroups = 0
    lb_src_count = defaultdict(int)
    for fn in args:
        for line in open(fn):
            line = line.strip()
            if not line:
                continue
            body = line.split('#')[0].split()
            n, i, z, k = map(int, body[:4])
            rows = body[4:]
            assert len(rows) == k, (n, i)
            ngroups += 1
            if k == 0:
                assert z == 1
                omega, a, src, clique = 1, 1, 'abelian', []
            else:
                kk, adj = parse_rows(rows)
                clique = max_clique(kk, adj)
                omega = len(clique)
                assert check_clique(adj, clique)
                a, col, src = chromatic(kk, adj, clique)
                assert check_colouring(kk, adj, col) and max(col) + 1 == a
            lb_src_count[src.split('(')[0]] += 1
            gid = (n, i)
            d = dist[omega]
            d['count'] += 1
            d['pairs'][(a, z)] += 1
            if a > d['maxa']:
                d['maxa'], d['maxa_ids'] = a, [gid]
            elif a == d['maxa']:
                d['maxa_ids'].append(gid)
            if z > d['maxz']:
                d['maxz'], d['maxz_ids'] = z, [gid]
            elif z == d['maxz']:
                d['maxz_ids'].append(gid)
            t = T(omega)
            if a > t:
                flags['A-VIOL'].append((gid, omega, a, z, t))
            if omega >= 3 and z > (t - 1) ** 2:
                flags['Z-VIOL'].append((gid, omega, a, z, (t - 1) ** 2))
            if omega >= 3 and a == t:
                flags['A-EQ'].append((gid, omega, a, z))
            if omega >= 3 and z == (t - 1) ** 2:
                flags['Z-EQ'].append((gid, omega, a, z))
            rows_out.append('%d\t%d\t%d\t%d\t%d\t%d\t%s\t%s' % (n, i, z, k, omega, a, src, ','.join(map(str, clique))))
    el = time.time() - t0
    with open(prefix + '.tsv', 'w') as f:
        f.write('n\ti\tz\tk_twinclasses\tomega\ta\ta_proof\tclique_witness(twin-class indices)\n')
        f.write('\n'.join(rows_out) + '\n')
    out = []
    out.append('table: %s   groups analysed: %d   seconds: %.1f' % ('WRONG T\'(7)=9' if wrong else 'paper T', ngroups, el))
    out.append('chi optimality certificates: %s' % dict(lb_src_count))
    out.append('')
    out.append('omega  #groups  T(omega)  max_a  #attaining  max_z  (T-1)^2  #attaining_maxz')
    for w in sorted(dist):
        d = dist[w]
        t = T(w)
        out.append('%5d  %7d  %8d  %5d  %10d  %5d  %7s  %d' % (w, d['count'], t, d['maxa'], len(d['maxa_ids']), d['maxz'],
                                                             str((t - 1) ** 2) if w >= 3 else '-', len(d['maxz_ids'])))
    out.append('')
    for w in sorted(dist):
        d = dist[w]
        out.append('omega=%d: max a=%d attained by %s' % (w, d['maxa'], ' '.join('[%d,%d]' % g for g in d['maxa_ids'][:60]) + (' ...(+%d)' % (len(d['maxa_ids']) - 60) if len(d['maxa_ids']) > 60 else '')))
        out.append('omega=%d: max z=%d attained by %s' % (w, d['maxz'], ' '.join('[%d,%d]' % g for g in d['maxz_ids'][:60]) + (' ...(+%d)' % (len(d['maxz_ids']) - 60) if len(d['maxz_ids']) > 60 else '')))
        out.append('omega=%d: (a,z) -> #groups: %s' % (w, ', '.join('(%d,%d):%d' % (a, z, c) for (a, z), c in sorted(d['pairs'].items()))))
    out.append('')
    for key in ['A-VIOL', 'Z-VIOL', 'A-EQ', 'Z-EQ']:
        L = flags[key]
        out.append('%s: %d groups' % (key, len(L)))
        if key.endswith('VIOL'):
            for x in L:
                out.append('   %s' % (x,))
        else:
            byw = defaultdict(list)
            for x in L:
                byw[x[1]].append(x)
            for w in sorted(byw):
                ids = ' '.join('[%d,%d]' % x[0] for x in byw[w])
                out.append('   omega=%d (%d groups): %s' % (w, len(byw[w]), ids if len(byw[w]) <= 400 else ids[:4000] + ' ...'))
    s = '\n'.join(out) + '\n'
    open(prefix + '.summary.txt', 'w').write(s)
    print(s)


if __name__ == '__main__':
    main()
