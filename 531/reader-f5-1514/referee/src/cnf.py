"""Referee's own CNF: var i = colour of i is 1. For each k-set A of distinct positive ints with sum(A)<=N,
two clauses over the DISTINCT values of S(A): not-all-0, not-all-1. Unit clause -1 (colour swap symmetry)."""
import sys, itertools
N, k = int(sys.argv[1]), int(sys.argv[2])
cls = []
def rec(start, chosen, total):
    if len(chosen) == k:
        S = sorted({sum(B) for r in range(1, k+1) for B in itertools.combinations(chosen, r)})
        cls.append(S); return
    x = start
    while total + x * (k - len(chosen)) + (k-len(chosen))*(k-len(chosen)-1)//2 <= N:
        rec(x+1, chosen+[x], total+x); x += 1
rec(1, [], 0)
print(f'p cnf {N} {2*len(cls)+1}')
print('-1 0')
for S in cls:
    print(' '.join(str(s) for s in S) + ' 0')
    print(' '.join(str(-s) for s in S) + ' 0')
