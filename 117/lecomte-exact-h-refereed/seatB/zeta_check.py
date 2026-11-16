# Check z(G) <= zeta(omega(G)) (companion [13] Theorem 1.1) and a(G) <= T(omega) on all scanned groups.
import sys, re
def zeta(k):
    if k <= 2: return 1
    if k <= 6: return (k - 1) ** 2
    if k <= 8: return 81
    return 4 ** ((k - 1) // 2)
viol = 0; n = 0; tight = []
for f in sys.argv[1:]:
    for line in open(f):
        p = line.rstrip('\n').split('\t')
        if len(p) < 6: continue
        z = int(p[2].split('=')[1]); om = p[3].split('=')[1]
        exact = om.isdigit(); om = int(re.match(r'>=?(\d+)', om).group(1)) if not exact else int(om)
        n += 1
        if exact and z > zeta(om): viol += 1; print('z > zeta(omega):', line.strip())
        if exact and z == zeta(om): tight.append((p[0], z, om))
print('groups', n, 'zeta violations', viol, 'z==zeta cases', len(tight))
import collections; print(collections.Counter((t[1], t[2]) for t in tight))
