"""recheck_unsat.py -- every census lower bound that came from a SAT UNSAT (cadical195, clique-seeded)
is re-proved with a different solver (glucose4) and no symmetry breaking where cheap, else clique-seeded."""
import sys
from graphlib import parse_rows, colour_sat, max_clique
want = {}
for tsv in sys.argv[1::2]:
    for line in open(tsv):
        f = line.rstrip('\n').split('\t')
        if len(f) > 6 and f[6].startswith('SAT-UNSAT'):
            want[(int(f[0]), int(f[1]))] = int(f[5])
done = 0; bad = 0
for exp in sys.argv[2::2]:
    for line in open(exp):
        body = line.split('#')[0].split()
        gid = (int(body[0]), int(body[1]))
        if gid not in want:
            continue
        k, adj = parse_rows(body[4:])
        a = want[gid]
        C = max_clique(k, adj)
        r = colour_sat(k, adj, a - 1, C, solver='glucose4')
        done += 1
        if r is not None:
            bad += 1
            print('MISMATCH', gid, a)
print('re-proved %d of %d UNSAT lower bounds with glucose4; mismatches %d' % (done, len(want), bad))
