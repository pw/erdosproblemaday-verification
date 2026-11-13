"""Run OUR solver (./clq) on each of the submission's 200 leaf files at its recorded threshold, and check
threshold = 33 - |forced| and the file's sha256 against their manifest. A decorrelated solver over THEIR decomposition."""
import json, subprocess, hashlib, sys, time
from concurrent.futures import ThreadPoolExecutor
root = '/home/exedev/MathDyad/erdos704/sub-vapywt/rel/'
m = json.load(open(root + 'R/out/solve/cubes/J_13_5_3_s33/manifest.json'))
def go(c):
    p = root + c['cube_dimacs_path']
    ok_sha = hashlib.sha256(open(p, 'rb').read()).hexdigest() == c['cube_dimacs_sha256']
    ok_tau = c['cube_threshold'] == 33 - len(c['forced_vertices'])
    t = time.time()
    o = subprocess.run(['nice', '-n', '19', './clq', p, str(c['cube_threshold'])], capture_output=True, text=True).stdout.split()
    return dict(id=c['id'], n=c['residual_n'], tau=c['cube_threshold'], sha_ok=ok_sha, tau_ok=ok_tau, verdict=o[0] if o else 'ERR', out=' '.join(o[:3]), wall=round(time.time() - t, 2))
with ThreadPoolExecutor(int(sys.argv[1])) as ex:
    res = list(ex.map(go, m['cubes']))
json.dump(res, open('runs/their_leaves_clq.json', 'w'), indent=0)
from collections import Counter
print('their 200 leaves, our clq:', Counter(r['verdict'] for r in res), 'sha_ok', sum(r['sha_ok'] for r in res), 'tau_ok', sum(r['tau_ok'] for r in res), 'cpu', round(sum(r['wall'] for r in res)), 'max', max(r['wall'] for r in res))
