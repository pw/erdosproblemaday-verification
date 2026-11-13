"""Positive control: carry the submission's 33-set witness (which contains v and u) down OUR tree for s=32.
At each internal node with orbit O and representative r: if the (moved) witness W meets O, map a met vertex x to r
with an explicit product of the node's generators (BFS), apply it to W, go to the include child; otherwise go to
the exclude child. Lemma: W stays independent and inside each node's forced+residual sets. At the leaf, solve with
./clq2 at the leaf's tau: it must say SAT. (Also checks the moved W is still independent and contains F.)"""
import sys, json, subprocess
from itertools import combinations
out = sys.argv[1]
man = json.load(open(out + '/manifest.json'))
n = man['n']
V = [frozenset(c) for c in combinations(range(n), 5)]; I = {x: i for i, x in enumerate(V)}
W0 = [{1,2,3,4,5},{1,2,3,4,6},{1,2,3,5,6},{1,2,4,5,6},{1,3,4,5,6},{2,3,4,5,6},{3,6,9,10,12},{3,6,9,10,13},{3,6,9,12,13},{3,6,10,12,13},{3,9,10,12,13},{6,9,10,12,13},{4,5,7,8,9},{4,5,7,8,10},{4,5,7,9,10},{4,5,8,9,10},{4,7,8,9,10},{5,7,8,9,10},{1,3,7,11,12},{1,4,7,11,12},{1,5,7,11,12},{1,6,7,11,12},{1,7,9,11,12},{1,7,10,11,12},{1,2,8,11,13},{2,3,8,11,13},{2,4,8,11,13},{2,5,8,11,13},{2,6,8,11,13},{2,7,8,11,13},{2,8,9,11,13},{2,8,10,11,13},{2,8,11,12,13}]
W = {I[frozenset(x - 1 for x in s)] for s in W0}
assert man['v'] in W and man['u'] in W and len(W) == 33
nodes = {nd['id']: nd for nd in man['nodes']}
kids = {}
for nd in man['nodes']:
    if nd['parent'] is not None: kids.setdefault(nd['parent'], {})[nd['kind']] = nd['id']
def apply(perm_ground, w): return I[frozenset(perm_ground[x] for x in V[w])]
cur = 1; path = []
while cur in kids:
    nd = nodes[cur]; r = nd['r']; O = set(nodes[kids[cur]['exclude']]['excluded_orbit'])
    meet = sorted(W & O)
    if not meet:
        cur = kids[cur]['exclude']; path.append('X'); continue
    x = meet[0]
    # BFS over vertices with ground permutations from generator transpositions
    from collections import deque
    prev = {x: list(range(n))}; dq = deque([x])
    while dq and r not in prev:
        w = dq.popleft()
        for (a, b) in nd['gens']:
            t = list(range(n)); t[a], t[b] = b, a
            y = apply(t, w)
            if y not in prev:
                p = prev[w]; prev[y] = [t[p[i]] for i in range(n)]; dq.append(y)
    g = prev[r]; assert apply(g, x) == r
    W = {apply(g, w) for w in W}
    assert all(len(V[a] & V[b]) != 3 for a, b in combinations(W, 2)) and len(W) == 33
    cur = kids[cur]['include']; path.append('I')
leaf = nodes[cur]
F = set(leaf['F']) | {man['v'], man['u']}
assert F <= W, 'forced vertices not in moved witness'
line = [l for l in open(out + '/leaves.txt') if l.split()[0] == str(cur)][0]
t = list(map(int, line.split())); R = {x - 1 for x in t[3:]}
rest = W - F
assert rest <= R and len(rest) >= t[1], (len(rest), t[1])
open('/tmp/track_leaf.txt', 'w').write(line)
o = subprocess.run(['./clq2', out + '/gbar.col', '/tmp/track_leaf.txt'], capture_output=True, text=True).stdout.strip()
print('TRACK leaf', cur, 'path', ''.join(path), 'tau', t[1], 'size', t[2], 'moved-witness-rest', len(rest), '-> clq2:', o.split()[1])
