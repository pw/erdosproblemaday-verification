"""For a colouring file with N small: for each p, brute-force count mono 5-sets after flipping p."""
import sys, itertools
line = open(sys.argv[1]).read().split('\n')[0]; N = len(line)
col = [None] + [int(ch) for ch in line]
sets = []
for A in itertools.combinations(range(1, N+1), 5):
    if sum(A) > N: continue
    ss = {sum(B) for r in range(1, 6) for B in itertools.combinations(A, r)}
    sets.append(ss)
for p in range(1, N+1):
    c2 = col[:]; c2[p] ^= 1
    n = sum(1 for ss in sets if len({c2[s] for s in ss}) == 1)
    if n: print(p, n)
