from itertools import combinations
N=800
def inX(a):
    while a:
        if a%3==2: return False
        a//=3
    return True
A=sorted(set([2*a+1 for a in range(N) if inX(a) and 2*a+1<=N]+[4*a for a in range(1,N) if inX(a) and 4*a<=N]))
s={1:set(),2:set(),3:set(),4:set()}
for k in range(1,5):
    for c in combinations(A,k):
        if sum(c)<=N: s[k].add(sum(c))
u3=s[1]|s[2]|s[3]; u4=u3|s[4]
print([n for n in range(1,N+1) if n not in u3],[n for n in range(1,N+1) if n not in u4])
