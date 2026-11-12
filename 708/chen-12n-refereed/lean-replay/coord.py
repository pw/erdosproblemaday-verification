#!/usr/bin/env python3
# Dependency-aware, one-owner-per-module builder for the H97 certificate modules, 3 at a time; then FinalCheck.
import subprocess, time, os, sys
os.chdir('/tmp/e708/lean'); env = dict(os.environ, PATH=os.path.expanduser('~/.elan/bin') + ':' + os.environ['PATH'])
STEPS = '/tmp/e708/run/steps.tsv'
def log(name, rc, secs): open(STEPS, 'a').write(f"{name}\t{rc}\t{secs}\t{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n")
running_ext = [int(p) for p in sys.argv[1].split(',')]          # lake PIDs already building (one module each)
ext_mods = sys.argv[2].split(',')
done = set(['Numeric4_256Rows'])
class Ext:                                                        # an externally-started lake: occupies a slot, no blocking
    def __init__(s, pid): s.pid, s.returncode = pid, None
    def poll(s):
        if os.path.exists(f'/proc/{s.pid}'): return None
        s.returncode = 0; return 0                                    # success is re-checked by the FinalCheck build itself
done |= set(m for m, pid in zip(ext_mods, running_ext) if not os.path.exists(f'/proc/{pid}'))
todo = []
for j in (4, 5, 6, 7):
    for L in (256, 512):
        for r in ('Rows', ''):
            m = f'Numeric{j}_{L}{r}'
            if m not in done: todo.append(m)
dep = lambda m: None if m.endswith('Rows') else m + 'Rows'
active = {m: (Ext(pid), time.time()) for m, pid in zip(ext_mods, running_ext) if os.path.exists(f'/proc/{pid}')}
todo = [m for m in todo if m not in active]
fail = False
while todo or active:
    for m, (p, t0) in list(active.items()):
        if p.poll() is not None:
            log('coord_' + m, p.returncode, int(time.time() - t0)); del active[m]
            if p.returncode == 0: done.add(m)
            else: fail = True
    if fail and not active: break
    while len(active) < 3 and not fail:
        ready = [m for m in todo if dep(m) is None or dep(m) in done]
        if not ready: break
        m = ready[0]; todo.remove(m)
        f = open(f'/tmp/e708/run/coord_{m}.log', 'w')
        active[m] = (subprocess.Popen(['lake', 'build', f'Erdos708.H97.Proofs.{m}'], stdout=f, stderr=subprocess.STDOUT, env=env), time.time())
    time.sleep(5)
if fail: log('coord_ABORT', 1, 0); sys.exit(1)
for name, cmd in (('final_build', ['lake', 'build', 'Erdos708.FinalCheck']), ('finalcheck', ['lake', 'env', 'lean', 'Erdos708/FinalCheck.lean'])):
    t0 = time.time(); f = open(f'/tmp/e708/run/{name}.log', 'w')
    rc = subprocess.call(cmd, stdout=f, stderr=subprocess.STDOUT, env=env); log(name, rc, int(time.time() - t0))
    if rc: sys.exit(rc)
log('DONE', 0, 0)
