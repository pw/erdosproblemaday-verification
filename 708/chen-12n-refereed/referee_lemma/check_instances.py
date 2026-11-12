#!/usr/bin/env python3
"""Recompute min|B| on the k2t2_run.log instances with refsolve (own code), and scan F1/F2/F3 directly.
Usage: check_instances.py LOG t1 t2 ...   (also runs controls when given --controls)"""
import re, sys, time
from math import prod
from refsolve import dp_types, ilp_types, val

def parse(log):
    out = {}
    for line in open(log):
        mt = re.match(r't=(\d+) w=\[([^\]]*)\] q=\((\d+),(\d+)\) m=(\d+) k=(\d+) x=(\d+)', line)
        if mt:
            t = int(mt[1]); ws = [int(z) for z in mt[2].split(',')]
            out[t] = dict(ws=ws, qu=int(mt[3]), qv=int(mt[4]), m=int(mt[5]), k=int(mt[6]), x=int(mt[7]))
    return out

def scan(ws, qu, qv, x, m):
    D = ws + [qu, qv]
    multi = [b for b in range(x + 1, x + m + 1) if sum(b % p == 0 for p in D) >= 2]
    sq = [(b, q) for b in range(x + 1, x + m + 1) for q in (qu, qv) if b % (q * q) == 0]
    wsq = sum(1 for b in range(x + 1, x + m + 1) for w in ws if b % (w * w) == 0)
    return multi, sq, wsq

def run(name, ws, qu, qv, x, expect=None, use_dp=True):
    t = len(ws); m = ws[-1] * qv
    Pi = prod(ws) * qu * qv
    A = sorted([w * qu for w in ws] + [w * qv for w in ws]); A2 = sorted(A + [qu])
    assert len(set(A)) == 2 * t and max(A) == m and max(A2) == m and len(set(A2)) == 2 * t + 1
    P1 = m < 2 * ws[0] * ws[1]; P2 = qu * qu >= m + qu
    multi, sq, wsq = scan(ws, qu, qv, x, m)
    u = multi[0] if len(multi) == 1 else None
    F1 = u is not None and u % Pi == 0 and all(val(u, p) == 1 for p in ws + [qu, qv])
    F2 = len(multi) == 1 and u % Pi == 0
    F3 = len(sq) == 0
    t0 = time.time()
    gA_ilp = ilp_types(A, x)[0]; gA2_ilp = ilp_types(A2, x)[0]
    gA_dp = dp_types(A, x)[0] if use_dp else None
    gA2_dp = dp_types(A2, x)[0] if use_dp else None
    print(f'{name}: t={t} m={m} P1={P1} P2={P2} | two-prime elements in I: {len(multi)} '
          f'(u=kPi? {F2}, k={u // Pi if u else None}) F1={F1} F3={F3} (q^2-multiples: {sq[:3]}) '
          f'#w_i^2-multiples={wsq} | n={2*t}: dp={gA_dp} ilp={gA_ilp} (3t-1={3*t-1}) '
          f'n={2*t+1}: dp={gA2_dp} ilp={gA2_ilp} (3t={3*t}) [{time.time()-t0:.1f}s]'
          + (f'  expect {expect}' if expect else ''), flush=True)

if __name__ == '__main__':
    log = sys.argv[1]; ts = [int(z) for z in sys.argv[2:] if z.isdigit()]
    inst = parse(log)
    for t in ts:
        d = inst[t]
        assert d['m'] == d['ws'][-1] * d['qv']
        run(f'k2t2 t={t}', d['ws'], d['qu'], d['qv'], d['x'], use_dp=(t <= 7))
    if '--controls' in sys.argv:
        # Chen's printed examples (his k=1 placements)
        run('Chen t=2', [59, 61], 71, 73, 18652287, expect='g=5')
        run('Chen t=3', [67, 73, 79], 97, 101, 3785449127, expect='g=8')
        # RED control: k2t.py's t=9 instance (q_u^2 > m but q_u^2 < m+q_u); exact.py reported 25 < 26
        run('k2t.py t=9 (control)', [127, 131, 137, 139, 149, 151, 157, 163, 167], 173, 179,
            57775007378712079115207133457, expect='25 if a q^2 multiple is in the window', use_dp=False)
