import json, sys, hashlib, os, shutil
from itertools import combinations
src = '/home/exedev/MathDyad/erdos704/indep/runs/n13_s33_lg350'
mode, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
if not os.path.exists(dst + '/gbar.col'): os.symlink(src + '/gbar.col', dst + '/gbar.col')
man = json.load(open(src + '/manifest.json')); lines = open(src + '/leaves.txt').read().splitlines()
V = [frozenset(c) for c in combinations(range(13), 5)]
nodes = {nd['id']: nd for nd in man['nodes']}
leafline = {int(l.split()[0]): i for i, l in enumerate(lines)}
# internal node whose exclude child is a SOLVE leaf
for nd in man['nodes']:
    if 'r' not in nd: continue
    kids = [c for c in man['nodes'] if c['parent'] == nd['id']]
    exc = [c for c in kids if c['kind'] == 'exclude'][0]
    if exc['id'] in leafline and nd['orbit_size'] > 1: break
li = leafline[exc['id']]; t = lines[li].split(); vs = [int(x) - 1 for x in t[3:]]
if mode == 'bigorbit':          # add one residual vertex that is NOT in the orbit, consistently propagated
    x = vs[0]; exc['excluded_orbit'] = sorted(exc['excluded_orbit'] + [x]); vs = vs[1:]
elif mode == 'badgen':          # add a cross-block transposition and enlarge the orbit to its closure image of r
    nd['gens'] = nd['gens'] + [[3, 6]]
    r = nd['r']; extra = None
    for w in vs:
        S = V[w]
        if len(S & V[r]) >= 0 and (3 in V[r]) != (6 in V[r]):
            pass
    # image of r under (3 6), if it is in the leaf residual, gets excluded too
    S = V[r]; img = frozenset(6 if e == 3 else 3 if e == 6 else e for e in S); iw = V.index(img)
    if iw in vs:
        exc['excluded_orbit'] = sorted(exc['excluded_orbit'] + [iw]); vs = [w for w in vs if w != iw]
    print('badgen image in leaf residual:', iw in vs or iw in exc['excluded_orbit'])
exc['size'] = len(vs)
t[2] = str(len(vs)); lines[li] = ' '.join(t[:3] + [str(w + 1) for w in vs])
for L in man['leaves']:
    if L['id'] == exc['id']: L['size'] = len(vs)
txt = ''.join(l + '\n' for l in lines); open(dst + '/leaves.txt', 'w').write(txt)
man['leaves_sha256'] = hashlib.sha256(txt.encode()).hexdigest()
json.dump(man, open(dst + '/manifest.json', 'w'))
print(mode, 'node', nd['id'], 'exclude leaf', exc['id'])
