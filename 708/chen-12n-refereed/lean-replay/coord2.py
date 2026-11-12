#!/usr/bin/env python3
# Weight-budgeted, dependency-aware, one-owner-per-module builder (512-Rows modules peak ~18-22 GB RSS each).
import subprocess, time, os, sys
os.chdir('/tmp/e708/lean'); env = dict(os.environ, PATH=os.path.expanduser('~/.elan/bin') + ':' + os.environ['PATH'])
STEPS = '/tmp/e708/run/steps.tsv'
def log(name, rc, secs): open(STEPS, 'a').write(f"{name}\t{rc}\t{secs}\t{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n")
OUT = '/tmp/e708/lean/.lake/build/lib/lean/Erdos708/H97/Proofs/'
W = lambda m: 22 if m.endswith('512Rows') else 12 if m.endswith('_512') else 8
BUDGET = 34
class Ext:
    def __init__(s, pid): s.pid, s.returncode = pid, None
    def poll(s):
        if os.path.exists(f'/proc/{s.pid}'): return None
        s.returncode = 0; return 0
ext = dict(zip(sys.argv[2].split(','), map(int, sys.argv[1].split(','))))
allm = [f'Numeric{j}_{L}{r}' for j in (4, 5, 6, 7) for L in (256, 512) for r in ('Rows', '')]
done = set(m for m in allm if os.path.exists(OUT + m + '.olean') and m not in ext)
active = {m: (Ext(p), time.time()) for m, p in ext.items()}
todo = [m for m in allm if m not in done and m not in active]
# heavy first so the long serial chain of 512-Rows modules starts as early as possible
todo.sort(key=lambda m: (0 if m.endswith('512Rows') else 1, m))
dep = lambda m: None if m.endswith('Rows') else m + 'Rows'
log('coord2_start todo=' + ','.join(todo), 0, 0)
fail = False
while todo or active:
    for m, (p, t0) in list(active.items()):
        if p.poll() is not None:
            ok = p.returncode == 0 and os.path.exists(OUT + m + '.olean')
            log('coord2_' + m, 0 if ok else (p.returncode or 9), int(time.time() - t0)); del active[m]
            if ok: done.add(m)
            else: fail = True
    if fail and not active: break
    while not fail:
        used = sum(W(m) for m in active)
        ready = [m for m in todo if (dep(m) is None or dep(m) in done) and used + W(m) <= BUDGET]
        if not ready: break
        m = ready[0]; todo.remove(m)
        f = open(f'/tmp/e708/run/coord2_{m}.log', 'w')
        active[m] = (subprocess.Popen(['lake', 'build', f'Erdos708.H97.Proofs.{m}'], stdout=f, stderr=subprocess.STDOUT, env=env), time.time())
    time.sleep(10)
if fail: log('coord_ABORT', 1, 0); sys.exit(1)
for name, cmd in (('final_build', ['lake', 'build', 'Erdos708.FinalCheck']), ('finalcheck', ['lake', 'env', 'lean', 'Erdos708/FinalCheck.lean'])):
    t0 = time.time(); f = open(f'/tmp/e708/run/{name}.log', 'w')
    rc = subprocess.call(cmd, stdout=f, stderr=subprocess.STDOUT, env=env); log(name, rc, int(time.time() - t0))
    if rc: sys.exit(rc)
log('DONE', 0, 0)
