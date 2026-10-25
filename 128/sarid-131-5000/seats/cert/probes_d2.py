#!/usr/bin/env python3
"""(d) continued in a parallel process (the main probes.py run would hit its 1-hour wall before reaching these):
Higman-Sims and the small named graphs, fewer starts.  Same objective code as probes.py (imported functions)."""
import sys, time, functools
import numpy as np
print = functools.partial(print, flush=True)
sys.argv = ['probes_d2']
# re-use constructions + optimiser from probes.py without re-running its main body
src = open('/tmp/erdos1800/seats/cert/probes.py').read()
head = src[:src.index("t0 = time.time()")]
body_defs = src[src.index("def check_srg"):src.index("BL = steiner_3_6_22()")]
opt_defs = src[src.index("def make_funcs"):src.index("rng = np.random.default_rng(2026)")]
named_defs = src[src.index("def andrasfai"):src.index("named = SRG +")]
gp_def = src[src.index("def gp(n, k):"):src.index("named[-2] =")]
exec(head + body_defs + opt_defs + named_defs + gp_def)
t0 = time.time(); rng = np.random.default_rng(7)
BL = steiner_3_6_22()
items = [('Grotzsch', mycielski(cycle(5)), 20), ('Andrasfai(3)', andrasfai(3), 20), ('Andrasfai(4)', andrasfai(4), 20),
         ('Andrasfai(5)', andrasfai(5), 20), ('Mobius-Kantor GP(8,3)', gp(8, 3), 20), ('Kneser(7,3)', kneser(7, 3), 3),
         ('Kneser(8,3)', kneser(8, 3), 2), ('Higman-Sims', higman_sims(BL), 1)]
for name, A, starts in items:
    n = len(A); u = np.full(n, 1 / n)
    k = 4 if n <= 20 else 2
    extra = [np.clip(u * (1 + rng.normal(0, s, n)), 1e-9, None) for s in (0.01, 0.05, 0.2) for _ in range(k)]
    extra = [x / x.sum() for x in extra]
    (vg, wg), (vh, wh) = multistart(A, starts, rng, extra=extra)
    gu, hu, parts = make_funcs(A)
    print(f'  {name:22s} n={n:3d}: uniform h={hu(u)[0]: .9f};  min g found={vg: .3e};  min h found={vh: .9f}'
          f'  (margin to -gamma {vh + GF: .3e}); max|w - uniform| at min h = {np.abs(wh - u).max():.2e}  [{time.time()-t0:.0f}s]')
print(f'PROBES_D2 COMPLETE ({time.time()-t0:.0f}s)')
