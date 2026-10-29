"""Mixed-colour control: random 2-colourings of [N] with a bias; brute force over ALL 5-sets with
sum<=N, computing the 31 subset sums explicitly. Writes colouring files for the two checkers."""
import sys, random, itertools
N = int(sys.argv[1]); seed = int(sys.argv[2]); p1 = float(sys.argv[3]); out = sys.argv[4]
rng = random.Random(seed)
col = [None] + [1 if rng.random() < p1 else 0 for _ in range(N)]
open(out, 'w').write(''.join(str(col[i]) for i in range(1, N+1)) + '\n')
cnt = [0, 0]
for A in itertools.combinations(range(1, N+1), 5):
    if sum(A) > N: continue
    ss = set()
    for r in range(1, 6):
        for B in itertools.combinations(A, r):
            ss.add(sum(B))
    cs = {col[s] for s in ss}
    if len(cs) == 1:
        cnt[cs.pop()] += 1
print(f'BRUTE N={N} seed={seed} p1={p1} mono_total={sum(cnt)} (colour0={cnt[0]} colour1={cnt[1]})')
