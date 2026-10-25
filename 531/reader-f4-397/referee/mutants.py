import sys
sys.path.insert(0, '/tmp/ref531')
from bitcheck import parse, count
from itertools import combinations
s = parse('/tmp/ref531/w396.txt', 'strip')
res = {}
for i in range(1, len(s)+1):
    t = s[:i-1] + ('1' if s[i-1]=='0' else '0') + s[i:]
    N, tot, per, first = count(t)
    res[i] = (tot, first)
bad = [i for i in res if res[i][0] > 0]
print("mutants flagged: %d of %d; unflagged positions: %s" % (len(bad), len(s), [i for i in res if res[i][0]==0]))
for i in (1, 100, 200, 396):
    print("flip", i, "->", res[i])
# exhibit the set for flip 200 explicitly
i = 200
t = s[:i-1] + ('1' if s[i-1]=='0' else '0') + s[i:]
a,b,c,d,k = res[i][1]
A = (a,b,c,d)
sums = sorted({sum(T) for r in range(1,5) for T in combinations(A,r)})
print("flip 200: A=%s colour %s; subset sums & colours in mutant: %s" % (A, k, [(x, t[x-1]) for x in sums]))
print("same sums in ORIGINAL witness:", [(x, s[x-1]) for x in sums])
open('/tmp/ref531/mut200.txt','w').write(t)
