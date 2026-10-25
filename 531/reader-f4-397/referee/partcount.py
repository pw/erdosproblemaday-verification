# number of 4-sets of distinct positive integers with sum <= N, via partitions:
# 4 distinct parts summing to m  <->  (subtract 0,1,2,3 and 1 each) partitions of m-10 into parts of size <=4 (conjugation)
import sys
N = int(sys.argv[1])
p = [1] + [0]*N
for part in (1,2,3,4):
    for n in range(part, N+1): p[n] += p[n-part]
print(N, sum(p[m-10] for m in range(10, N+1)))
