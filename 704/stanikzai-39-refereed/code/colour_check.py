"""Re-verify the submission's five colouring certificates for J(13,5,3) leaves with our own code: each colouring is
proper on its leaf file (sha256 matched to the certificate) and uses fewer colours than the leaf's threshold."""
import json, glob, hashlib
root = '/home/exedev/MathDyad/erdos704/sub-vapywt/rel/'
m = json.load(open(root + 'R/out/solve/cubes/J_13_5_3_s33/manifest.json'))
tau = {f"s33_{c['id']:04d}": c['cube_threshold'] for c in m['cubes']}
for f in sorted(glob.glob(root + 'R/out/color_certs_s33_leaves/*.json')):
    d = json.load(open(f)); col = d['coloring'] if isinstance(d['coloring'], list) else json.loads(d['coloring'])
    raw = open(root + d['graph_path'], 'rb').read()
    n = 0; E = []
    for line in raw.decode().splitlines():
        if line.startswith('p'): n = int(line.split()[2])
        elif line.startswith('e'): a, b = map(int, line.split()[1:3]); E.append((a - 1, b - 1))
    ok = (hashlib.sha256(raw).hexdigest() == d['graph_sha256'] and len(col) == n and all(col[a] != col[b] for a, b in E)
          and len(set(col)) < tau[d['name']])
    print(d['name'], 'vertices', n, 'edges', len(E), 'colours', len(set(col)), 'threshold', tau[d['name']], 'CERTIFIES' if ok else 'FAILS')
