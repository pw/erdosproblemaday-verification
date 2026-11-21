#!/usr/bin/env python3
"""Parse refdfs output -> prof_<M>_dfs.json; verify every witness set independently; compare to IHS."""
import sys, json, re
sys.path.insert(0, '/tmp/ref301')
from ihs import verify_int_sets
for M, f in [(5040, 'dfs_5040.out'), (55440, 'dfs_55440.out'), (720720, 'dfs_720720.out')]:
    try: lines = open('/tmp/ref301/c/' + f).read().split('\n')
    except FileNotFoundError: continue
    res, kept, Fprev, D = [], [], 0, [d for d in range(1, M + 1) if M % d == 0]
    for ln in lines:
        m = re.match(r't=(\d+) n=(\d+) F=(\d+) h=(\d+) nodes=(\d+)(?: set=([\d,]+))?$', ln.strip())
        if not m: continue
        t, n, F, h = map(int, m.groups()[:4])
        assert t == D[n - 1] and F + h == n
        if m.group(6):
            kept = sorted(map(int, m.group(6).split(',')))
            assert len(kept) == F == Fprev + 1 and max(kept) == t and all(M % d == 0 for d in kept)
            assert verify_int_sets(kept), ('WITNESS FAILS', t)
        else:
            assert F == Fprev
        Fprev = F
        res.append({'t': t, 'n': n, 'F': F, 'h': h, 'kept': kept})
    json.dump(res, open('/tmp/ref301/prof_%d_dfs.json' % M, 'w'))
    try:
        ihs = {r['t']: r['F'] for r in json.load(open('/tmp/ref301/prof_%d_ihs.json' % M))}
        ov = [(r['t'], r['F'], ihs[r['t']]) for r in res if r['t'] in ihs]
        bad = [x for x in ov if x[1] != x[2]]
        print('M=%d dfs to t=%d; overlap with IHS %d points (to t=%d); disagreements: %s; all witnesses verified' % (M, res[-1]['t'], len(ov), ov[-1][0] if ov else 0, bad))
    except FileNotFoundError: pass
