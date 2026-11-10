#!/usr/bin/env python3
# Inline SVG for the #912 entry (n = 10^18): per t-bin excess of occupied intervals over the Cramér expectation —
# real primes, the Hardy–Littlewood pair term (nothing fitted), and the fixed-depth z = 19 sieve model.
rows = [l.split() for l in open('model_1e18.out') if l.startswith('B ')]
pairb = {round(float(a), 2): float(b) for a, b in (l.split() for l in open('pair_bins_1e18.txt'))}
pts = []
for r in rows:
    t = float(r[1]); nk = int(r[2]); act = int(r[3]); cr = float(r[4]); z19 = float(r[12])
    if t >= 6: continue
    pts.append((t + 0.025, (act - cr) / nk, pairb[round(t, 2)] / nk, (z19 - cr) / nk))
W, H = 640, 300; L, R, T, B = 52, 14, 40, 46
X = lambda t: L + (W - L - R) * t / 6.0
Y = lambda y: T + (H - T - B) * (1 - y / 0.036)
def path(i): return ' '.join(('M' if k == 0 else 'L') + f'{X(p[0]):.1f},{Y(p[i]):.1f}' for k, p in enumerate(pts))
o = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:{W}px;display:block;margin:1em 0" role="img" aria-label="Excess of occupied intervals over the Cramér model at n = 10^18, by t: real primes, the Hardy–Littlewood pair term, and the z = 19 sieve model">']
o.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#1b2120"/>')
o.append(f'<text x="{L}" y="18" fill="#ece9df" font-size="13">Share of intervals holding a prime, minus the Cramér prediction (n = 10¹⁸)</text>')
for yv in (0, 0.01, 0.02, 0.03):
    o.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(yv):.1f}" y2="{Y(yv):.1f}" stroke="#ece9df" stroke-opacity="0.15"/>')
    o.append(f'<text x="{L-8}" y="{Y(yv)+4:.1f}" fill="#ece9df" font-size="12" text-anchor="end">{int(yv*100)}%</text>')
for tv in range(0, 7):
    o.append(f'<text x="{X(tv):.1f}" y="{H-B+18}" fill="#ece9df" font-size="12" text-anchor="middle">{tv}</text>')
o.append(f'<text x="{(L+W-R)/2:.0f}" y="{H-8}" fill="#ece9df" font-size="12" text-anchor="middle">t = k/(n/log n)^½ · an interval at t holds about 2/t² primes</text>')
o.append(f'<path d="{path(3)}" fill="none" stroke="#8fc6ea" stroke-width="1.6" stroke-dasharray="6 4"/>')
o.append(f'<path d="{path(2)}" fill="none" stroke="#a2d69c" stroke-width="1.8"/>')
o.append(f'<path d="{path(1)}" fill="none" stroke="#f3d46c" stroke-width="2.4"/>')
lx = X(3.0)
o.append(f'<text x="{lx:.1f}" y="{Y(0.031):.1f}" fill="#f3d46c" font-size="13">real primes</text>')
o.append(f'<text x="{lx:.1f}" y="{Y(0.0275):.1f}" fill="#a2d69c" font-size="13">Hardy–Littlewood pair term (nothing fitted)</text>')
o.append(f'<text x="{lx:.1f}" y="{Y(0.024):.1f}" fill="#8fc6ea" font-size="13">sieve model, depth 19</text>')
o.append('</svg>')
s = ''.join(o)
assert '`' not in s and '${' not in s
open('fig_1e18.svg', 'w').write(s); print(len(s))
