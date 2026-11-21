#!/usr/bin/env python3
"""Step 4: compare our side's dfs/*.out and profile/*.log, value by value, with the referee's profiles."""
import re, json, glob, os
base = os.path.expanduser('~/MathDyad/erdos301/')
mine = {}
for M, src in [(5040, '_dfs'), (55440, '_dfs'), (720720, '_ihs')]:
    mine[M] = {r['t']: r['F'] for r in json.load(open('/tmp/ref301/prof_%d%s.json' % (M, src)))}
for f in sorted(glob.glob(base + 'dfs/*.out') + glob.glob(base + 'profile/*.log')):
    txt = open(f).read()
    m = re.search(r'M=(\d+)', txt)
    if not m: print(os.path.basename(f), 'no M header'); continue
    M = int(m.group(1))
    vals = {int(d): int(F) for d, F in re.findall(r'd=\s*(\d+)\s+(?:grow|jump)\s+F=\s*(\d+)', txt)}
    if M not in mine:
        print('%-28s M=%-7d %3d values (no referee profile for this M)' % (os.path.basename(f), M, len(vals))); continue
    ov = sorted(set(vals) & set(mine[M]))
    bad = [(d, vals[d], mine[M][d]) for d in ov if vals[d] != mine[M][d]]
    print('%-28s M=%-7d %3d values, overlap %3d (to d=%s), disagreements %s' % (os.path.basename(f), M, len(vals), len(ov), ov[-1] if ov else '-', bad))
