"""summarize_probe.py FILE.jsonl... -- per (p,d,e,family) table of the bilinear-map probe."""
import sys, json, collections
recs = []
for fn in sys.argv[1:]:
    recs += [json.loads(l) for l in open(fn)]
g = collections.defaultdict(list)
for r in recs:
    g[(r['p'], r['d'], r['e'], r['family'])].append(r)
print('total maps: %d' % len(recs))
print('p d e family      maps  z-values           omega_lb[min,max] #omega_exact  max_a_ub  worst a_ub/T(omega_lb)  uncert_A uncert_Z  nontrivial_eq(omega>=7,a_lb>=T,omega exact)')
tot_ua = tot_uz = 0
eqs = []
for k in sorted(g):
    L = g[k]
    ua = sum(not r['cert_a'] for r in L); uz = sum(not r['cert_z'] for r in L)
    tot_ua += ua; tot_uz += uz
    zs = sorted(set(r['z'] for r in L))
    worst = max(r['a_ub'] / r['T'] for r in L)
    neq = [r for r in L if r['omega_lb'] >= 7 and r['a_lb'] >= r['T'] and r['omega_proven']]
    eqs += neq
    print('%d %2d %d %-11s %4d  %-18s [%d,%d]  %4d  %5d  %.4f  %d %d  %d' % (k[0], k[1], k[2], k[3], len(L), ','.join(map(str, zs)),
          min(r['omega_lb'] for r in L), max(r['omega_lb'] for r in L), sum(r['omega_proven'] for r in L),
          max(r['a_ub'] for r in L), worst, ua, uz, len(neq)))
print('TOTAL uncertified a<=T(omega): %d ; uncertified z<=(T(omega)-1)^2: %d' % (tot_ua, tot_uz))
c = collections.Counter((r['p'], r['d'], r['e'], r['family'], r['z'], r['omega_lb'], r['a_lb'], r['a_ub']) for r in eqs)
print('nontrivial equality cases (p,d,e,family,z,omega,a_lb,a_ub): %s' % dict(c))
for r in recs:
    if not r['cert_a'] or not r['cert_z']:
        print('UNCERTIFIED:', json.dumps({k: r[k] for k in r if k != 'matrices'}))
