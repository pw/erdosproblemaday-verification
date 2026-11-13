import json, shutil, subprocess, copy, hashlib, sys
from concurrent.futures import ThreadPoolExecutor
base = 'runs/n13_s33_lg350'
man = json.load(open(base + '/manifest.json'))
def mk(name, mut, leafmut=None):
    d = f'/tmp/neg13_{name}'; shutil.rmtree(d, ignore_errors=True); shutil.copytree(base, d, ignore=shutil.ignore_patterns('chunks', 'cliquer', 'enum*'))
    m = copy.deepcopy(man); mut(m)
    if leafmut:
        txt = leafmut(open(d + '/leaves.txt').read()); open(d + '/leaves.txt', 'w').write(txt)
        m['leaves_sha256'] = hashlib.sha256(txt.encode()).hexdigest()
    json.dump(m, open(d + '/manifest.json', 'w')); return name, d
def first(kind, cond):
    def f(m):
        for nd in m['nodes']:
            if nd['kind'] == kind and cond(nd): return nd
    return f
def shrink(m):
    nd = first('exclude', lambda nd: len(nd['excluded_orbit']) > 1)(m); nd['excluded_orbit'] = nd['excluded_orbit'][1:]
def grow(m):
    nd = first('exclude', lambda nd: len(nd['excluded_orbit']) > 1)(m); nd['excluded_orbit'] = nd['excluded_orbit'] + [max(nd['excluded_orbit']) + 1]
def badgen(m):
    nd = [nd for nd in m['nodes'] if 'gens' in nd][0]; nd['gens'][0] = [0, 6]
def badtau(m):
    first('include', lambda nd: True)(m)['tau'] += 1
def dropleaf(m): m['nodes'] = m['nodes'][:-1]
def dropvert(txt):
    L = txt.splitlines(); t = L[0].split(); t[2] = str(int(t[2]) - 1); L[0] = ' '.join(t[:-1]); return ''.join(l + '\n' for l in L)
jobs = [mk('shrink', shrink), mk('grow', grow), mk('badgen', badgen), mk('badtau', badtau), mk('dropleaf', dropleaf), mk('dropvert', lambda m: None, dropvert)]
def run(j):
    r = subprocess.run(['nice', '-n', '15', 'python3', 'replay.py', j[1]], capture_output=True, text=True)
    return j[0], r.returncode, (r.stderr.strip().splitlines() or [''])[-1][:90]
with ThreadPoolExecutor(6) as ex:
    for name, rc, msg in ex.map(run, jobs): print(name, 'REJECTED' if rc else 'ACCEPTED(BAD)', msg)
