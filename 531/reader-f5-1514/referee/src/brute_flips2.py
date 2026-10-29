"""usage: brute_flips2.py COLOURFILE K CHKD_OUT
Brute force (itertools, explicit subset sums): for every p, the number of mono K-sets after flipping p,
compared to chkD's prediction  defect[p] + |mono| - |{mono A : p in S(A)}|."""
import sys, itertools
line = open(sys.argv[1]).read().split('\n')[0]; N = len(line); K = int(sys.argv[2])
col = [None] + [int(ch) for ch in line]
d = {}
for l in open(sys.argv[3]):
    p, n = map(int, l.split()); d[p] = n
sets = []
for A in itertools.combinations(range(1, N+1), K):
    if sum(A) > N: continue
    sets.append({sum(B) for r in range(1, K+1) for B in itertools.combinations(A, r)})
mono = [ss for ss in sets if len({col[s] for s in ss}) == 1]
bad = 0; nz = 0
for p in range(1, N+1):
    c2 = col[:]; c2[p] ^= 1
    b = sum(1 for ss in sets if len({c2[s] for s in ss}) == 1)
    pred = d.get(p, 0) + len(mono) - sum(1 for ss in mono if p in ss)
    if b != pred: bad += 1; print('MISMATCH', p, b, pred)
    if d.get(p, 0): nz += 1
print(f'N={N} K={K} eligible={len(sets)} mono={len(mono)} positions_with_defect={nz} mismatches={bad}')
