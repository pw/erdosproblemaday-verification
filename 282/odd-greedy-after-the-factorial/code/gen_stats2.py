"""Corrected climb-ending classification (blind-read fix): uses certify.py's OWN recomputed s, g at the climb's last
numerator R (certify_sweep.txt: N t L_og L_cert rc R s g next) plus tails from sweep_3000.txt."""
import json, collections, sys
from sympy import isprime, nextprime
cert = {}
import os
for line in open('certify_sweep.txt').read().splitlines() + (open('certify_sweep_asc.txt').read().splitlines() if os.path.exists('certify_sweep_asc.txt') else []):
    x = line.split()
    if len(x) != 9: continue
    N, t, Lo, Lc, rc, R, s, g, nxt = map(int, x); cert[(N, t)] = dict(N=N, t=t, Lo=Lo, Lc=Lc, rc=rc, R=R, s=s, g=g, nxt=nxt)
tails = {}
for line in open('sweep_3000.txt'):
    h, tl = line.split('|'); h = h.split()
    tails[(int(h[0]), int(h[1]))] = ([int(v) for v in tl.strip().split(',') if v], int(h[2]), int(h[4]))
missing = [k for k in tails if k not in cert]
bad = [k for k, c in cert.items() if c['rc'] != 0 or c['Lo'] != c['Lc'] or c['Lo'] != tails[k][1] or c['R'] != tails[k][2]]
def kind(c):
    R, s, g = c['R'], c['s'], c['g']
    if s == R + 1:
        if g == R + 1: return 'ends-prime' if isprime(R + 1) else 'ends-composite'
        return 'cut'                       # numerator R+1 reduced by g to (R+1)/g
    return 'break-at-R-prime' if isprime(R) else 'break-at-R-composite'
def obstacle(c): return c['R'] + 1 if c['s'] == c['R'] + 1 else c['R']
out = dict(rows=len(cert), missing=len(missing), problems=bad[:20], n_problems=len(bad))
big = [c for c in cert.values() if c['N'] >= 100]
out['kinds_N100'] = dict(collections.Counter(kind(c) for c in big))
out['n_N100'] = len(big)
fp = collections.Counter()
for c in big:
    p = nextprime(c['N']); o = obstacle(c)
    fp['at first prime past N' if o == p else ('before it' if o < p else 'past it')] += 1
out['vs_first_prime'] = dict(fp)
out['cut_examples'] = sorted([(c['N'], c['t'], c['R'] + 1, c['g']) for c in big if kind(c) == 'cut'])[:6]
sel = {}
for k in [(10,1),(10,2),(20,1),(20,2),(50,1),(50,2),(100,1),(100,2),(200,1),(200,2),(500,1),(500,2),(1000,1),(1000,2),(2000,1),(2000,2),(3000,1),(3000,2)]:
    c = cert[k]; sel[f"{k[0]}/{k[1]}"] = dict(L=c['Lo'], R=c['R'], s=c['s'], g=c['g'], kind=kind(c), tail=tails[k][0])
out['selected'] = sel
print(json.dumps(out, indent=1))
