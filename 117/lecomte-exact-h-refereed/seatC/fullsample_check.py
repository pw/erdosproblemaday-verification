"""fullsample_check.py -- twin-reduction / pipeline cross-check on a sample of groups of order 65..255:
full noncentral-coset graph (no twin reduction) -> networkx omega and alpha, chi by minisat22 with no
symmetry breaking starting from max(omega, ceil(n/alpha)); compare with the census (twin-reduced) row."""
import time
import networkx as nx
from graphlib import parse_rows, dsatur, check_colouring, colour_sat
from controls import nxg, sat_chi_plain
census = {}
for line in open('census/census_le255.tsv'):
    if line.startswith('n\t'):
        continue
    f = line.rstrip('\n').split('\t')
    census[(int(f[0]), int(f[1]))] = (int(f[2]), int(f[4]), int(f[5]))
bad = cnt = 0
t0 = time.time()
for line in open('census/exportFULL_sample.txt'):
    body = line.split('#')[0].split()
    n, i, z, k = map(int, body[:4])
    if k == 0:
        got = (z, 1, 1)
    else:
        kk, adj = parse_rows(body[4:])
        assert kk == z - 1
        G = nxg(kk, adj)
        C, w = nx.max_weight_clique(G, weight=None)
        I, al = nx.max_weight_clique(nx.complement(G), weight=None)
        lo = max(w, -(-kk // al))
        d = max(dsatur(kk, adj)) + 1
        if kk <= 64 or lo == d:
            a = sat_chi_plain(kk, adj, lo, d, solver='minisat22')   # no symmetry breaking
        else:   # glucose4, seeded with the networkx clique (sound symmetry breaking)
            a = d
            while a > lo:
                c = colour_sat(kk, adj, a - 1, C, solver='glucose4')
                if c is None:
                    break
                a = max(c) + 1
        got = (z, w, a)
        print('  ', (n, i), got, 'alpha=%d' % al, flush=True)
    cnt += 1
    if census[(n, i)] != got:
        bad += 1
        print('MISMATCH', (n, i), census[(n, i)], got)
print('full-graph sample: %d groups checked, %d mismatches (%.0fs)' % (cnt, bad, time.time() - t0))
