"""Controls for the classifier: the nauty certificate of the incidence graph is equal on 200 random relabellings of the
Appendix A family W and differs on 33 families with one set changed."""
import random, pynauty
from itertools import combinations
W0 = [{1,2,3,4,5},{1,2,3,4,6},{1,2,3,5,6},{1,2,4,5,6},{1,3,4,5,6},{2,3,4,5,6},{3,6,9,10,12},{3,6,9,10,13},{3,6,9,12,13},{3,6,10,12,13},{3,9,10,12,13},{6,9,10,12,13},{4,5,7,8,9},{4,5,7,8,10},{4,5,7,9,10},{4,5,8,9,10},{4,7,8,9,10},{5,7,8,9,10},{1,3,7,11,12},{1,4,7,11,12},{1,5,7,11,12},{1,6,7,11,12},{1,7,9,11,12},{1,7,10,11,12},{1,2,8,11,13},{2,3,8,11,13},{2,4,8,11,13},{2,5,8,11,13},{2,6,8,11,13},{2,7,8,11,13},{2,8,9,11,13},{2,8,10,11,13},{2,8,11,12,13}]
W = [frozenset(x - 1 for x in s) for s in W0]
def cert(fam):
    adj = {i: [] for i in range(13 + len(fam))}
    for j, S in enumerate(fam):
        for x in S: adj[x].append(13 + j)
    return pynauty.certificate(pynauty.Graph(13 + len(fam), adjacency_dict=adj, vertex_coloring=[set(range(13)), set(range(13, 13 + len(fam)))]))
c0 = cert(W); random.seed(3); same = 0
for t in range(200):
    p = list(range(13)); random.shuffle(p); F = [frozenset(p[x] for x in S) for S in W]; random.shuffle(F); same += cert(F) == c0
V = [frozenset(c) for c in combinations(range(13), 5)]
diff = 0; tried = 0
for i in range(33):
    for Snew in V:
        if Snew in W: continue
        tried += 1; diff += cert(W[:i] + [Snew] + W[i + 1:]) != c0; break
print(f'relabelled copies with equal certificate: {same}/200; one-set-changed families with a different certificate: {diff}/{tried}')
