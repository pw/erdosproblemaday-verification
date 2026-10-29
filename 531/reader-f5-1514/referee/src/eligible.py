"""Number of k-sets of distinct positive integers with sum <= N, two independent ways:
 (1) partition DP: a_i = b_i + i, 0<=b_1<=...<=b_k, sum b = m-k(k+1)/2 -> partitions into parts <= k;
 (2) brute force itertools (small N only)."""
import sys, itertools
def via_partitions(N, k):
    M = N - k*(k+1)//2
    if M < 0: return 0
    p = [1] + [0]*M
    for part in range(1, k+1):
        for m in range(part, M+1):
            p[m] += p[m-part]
    return sum(p)
def brute(N, k):
    return sum(1 for A in itertools.combinations(range(1, N+1), k) if sum(A) <= N)
k = int(sys.argv[1])
for N in map(int, sys.argv[2:]):
    b = brute(N, k) if N <= 60 else None
    print(f'k={k} N={N} partitions={via_partitions(N,k)} brute={b}')
