# Robustness probe: reading the problem with REPEATED elements allowed (excluded by Erdos-Spencer's "k-set", "a_i distinct").
import sys; sys.path.insert(0,'/tmp/ref531')
from bitcheck import parse
from itertools import combinations
s = parse('/tmp/ref531/w396.txt','strip'); N=len(s); col=[None]+[int(c) for c in s]
cnt=0; first=None
for a in range(1,N+1):
  for b in range(a,N+1):
    if a+b>N: break
    for c in range(b,N+1):
      if a+b+c>N: break
      for d in range(c,N+1):
        if a+b+c+d>N: break
        if len({a,b,c,d})==4: continue
        A=(a,b,c,d)
        sums={sum(A[i] for i in I) for r in range(1,5) for I in combinations(range(4),r)}
        if len({col[x] for x in sums})==1:
            cnt+=1; first=first or A
print("multiset quadruples with a repeat that are mono:", cnt, "first:", first)
