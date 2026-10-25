import re
L=[tuple(map(int,l.split())) for l in open('/tmp/oaimath/012/compute/b070089.txt') if re.match(r'^\d+\s+\d+',l)]
def P(n):
    if n==1: return 1
    p=2; last=1
    while p*p<=n:
        while n%p==0: last=p; n//=p
        p+=1
    return n if n>1 else last
mx=L[-1][1]
ours=[n for n in range(1,mx+1) if P(n)<P(n+1)]
print(len(L), L[-1], len(ours), ours==[v for _,v in L])
