#!/usr/bin/env python3
"""Step 3: reader's claims vs the referee's own profiles (prof_M.json from ihs.py)."""
import json, sys, bisect, os
SRC = json.loads(os.environ.get('SRC', '{}'))
SRC = {int(k): v for k, v in SRC.items()}
from fractions import Fraction as Fr

def load(M):
    P = json.load(open('/tmp/ref301/prof_%d%s.json' % (M, SRC.get(M, ''))))
    ts = [r['t'] for r in P]; hs = [r['h'] for r in P]; Fs = [r['F'] for r in P]
    return ts, hs, Fs

def hfun(ts, hs):
    tmax = ts[-1]
    def h(t):  # h at real t; None if beyond computed range
        if t < 1: return 0
        if t > tmax: return None
        i = bisect.bisect_right(ts, t) - 1
        return hs[i]
    return h, tmax

def jumps(ts, hs):
    J, prev = [], 0
    for t, h in zip(ts, hs):
        assert h - prev in (0, 1), (t, h, prev)
        if h > prev: J.append(t)
        prev = h
    return J

def divs(M): return [d for d in range(1, M + 1) if M % d == 0]

def excess(Mbig, Msmall, p, upto=None):
    tb, hb, _ = load(Mbig); ts, hs, _ = load(Msmall)
    Hb, tbmax = hfun(tb, hb); Hs, tsmax = hfun(ts, hs)
    D = [d for d in divs(Mbig) if d <= tbmax]
    rows = []
    for i, d in enumerate(D):
        hi = D[i + 1] if i + 1 < len(D) else None
        a, b, c = Hb(d), Hs(d), Hs(Fr(d, p))
        if b is None or c is None: break
        rows.append((d, hi, a - b - c, a, b, c))
    return rows

if __name__ == '__main__':
    for M in (5040, 55440, 720720):
        try: ts, hs, Fs = load(M)
        except FileNotFoundError: continue
        J = jumps(ts, hs)
        print('M=%d computed to t=%d (%d divisors). jumps at %s' % (M, ts[-1], len(ts), J))
        print('  F:', list(zip(ts, Fs)))
        print('  partial W (jumps <= %d) = %s = %.6f' % (ts[-1], sum(Fr(1, d) for d in J), float(sum(Fr(1, d) for d in J))))
    rows = excess(55440, 5040, 11)
    if rows:
        print('\nexcess e(t)=h55440(t)-h5040(t)-h5040(t/11) on [d, next d):')
        print('  ' + ' '.join('%s:%d' % (d, e) for d, hi, e, a, b, c in rows))
        tot = sum((Fr(1, d) - (Fr(1, hi) if hi else 0)) * e for d, hi, e, a, b, c in rows if hi)
        print('  integral over computed range [1,%s) = %s = %.6f' % (rows[-1][0], tot, float(tot)))
        claimed = [(36,42,1),(55,77,1),(77,80,2),(80,84,1),(84,90,2),(90,105,1)]
        for a, b, c in claimed:
            seg = [(d, e) for d, hi, e, *_ in rows if a <= d < b]
            if not seg or seg[-1][0] < max(x for x in [d for d,*_ in rows if d < b]): pass
            covered = rows[-1][0] >= max(d for d in divs(55440) if d < b)
            print('  claim +%d on [%d,%d): ours %s %s' % (c, a, b, seg, '' if covered else '(range not fully computed)'),
                  'HOLDS' if covered and all(e >= c for d, e in seg) else ('FAILS' if any(e < c for d, e in seg) else 'PENDING'))
    import os
    rows = excess(720720, 55440, 13) if os.path.exists('/tmp/ref301/prof_720720.json') else []
    if rows:
        print('\nexcess e(t)=h720720(t)-h55440(t)-h55440(t/13):')
        print('  ' + ' '.join('%s:%d' % (d, e) for d, hi, e, a, b, c in rows))
        tot = sum((Fr(1, d) - Fr(1, hi)) * e for d, hi, e, a, b, c in rows if hi)
        print('  integral over computed range = %s = %.6f' % (tot, float(tot)))
