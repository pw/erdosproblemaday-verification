# lake-free DAG build of Blinov's Lean closure. Usage: python3 -I drive.py JOBS
import json, os, subprocess, sys, time
J = int(sys.argv[1]) if len(sys.argv) > 1 else 2
C = json.load(open('closure.json'))
SRC = '/tmp/oaimath/191b/src/blinov-fpc/lean'
ML = '/tmp/oaimath/191b/lean/mathlib4'
OUT = '/tmp/oaimath/191b/lean/replay/out'; os.makedirs(OUT, exist_ok=True); os.makedirs('logs', exist_ok=True)
paths = [OUT, ML + '/.lake/build/lib'] + [ML + '/.lake/packages/%s/.lake/build/lib' % p for p in os.listdir(ML + '/.lake/packages')]
env = dict(os.environ, LEAN_PATH=':'.join(paths), PATH=os.path.expanduser('~/.elan/toolchains/leanprover--lean4---v4.11.0/bin') + ':' + os.environ['PATH'])
done, failed, running = set(), set(), {}
tsv = open('steps.tsv', 'a')
pending = list(C['order'])
while pending or running:
    for m, (p, t0) in list(running.items()):
        rc = p.poll()
        if rc is None: continue
        del running[m]; dt = time.time() - t0
        (done if rc == 0 else failed).add(m)
        tsv.write(f"{m}\t{rc}\t{dt:.1f}\n"); tsv.flush(); print(m, rc, f"{dt:.0f}s", flush=True)
    for m in list(pending):
        if len(running) >= J: break
        deps = C['deps'][m]
        if any(d in failed for d in deps): pending.remove(m); failed.add(m); tsv.write(f"{m}\tSKIP-depfail\t0\n"); continue
        if all(d in done for d in deps):
            pending.remove(m)
            cmd = ['nice', '-n', '19', 'bash', 'rsscap.sh', '12000000', '7200', 'lean', '--root=' + SRC, '-o', f'{OUT}/{m}.olean', '-i', f'{OUT}/{m}.ilean', f'{SRC}/{m}.lean']
            running[m] = (subprocess.Popen(cmd, env=env, stdout=open(f'logs/{m}.log', 'w'), stderr=subprocess.STDOUT), time.time())
    time.sleep(1)
print('DONE', len(done), 'ok', len(failed), 'failed', flush=True)
