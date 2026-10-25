import math, random, itertools, cmath
random.seed(2)
def set_partitions(lst):
    if not lst: yield []; return
    first=lst[0]
    for smaller in set_partitions(lst[1:]):
        for n,sub in enumerate(smaller):
            yield smaller[:n]+[[first]+sub]+smaller[n+1:]
        yield [[first]]+smaller
def structure_sum(r,m,tmin):
    # sum over left partition PL, right partition PR, size-preserving bijection of blocks, #blocks>tmin, of prod (a_i m)!
    tot=0
    parts=list(set_partitions(list(range(r))))
    for PL in parts:
        if len(PL)<=tmin: continue
        sizesL=sorted(len(b) for b in PL)
        for PR in parts:
            if sorted(len(b) for b in PR)!=sizesL: continue
            # number of size-preserving bijections
            from collections import Counter
            nb=1
            for s,c in Counter(sizesL).items(): nb*=math.factorial(c)
            tot+=nb*math.prod(math.factorial(len(b)*m) for b in PL)
    return tot
def components(r,assign1,assign2):
    parent=list(range(2*r))
    def f(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    for v in range(len(assign1)):
        a=f(assign1[v]); b=f(r+assign2[v])
        if a!=b: parent[a]=b
    return len({f(x) for x in range(2*r)})
for r,m in [(4,1),(4,2),(4,3),(8,1)]:
    n=r*m; first=[i//m for i in range(n)]
    bad=0; tot=0
    if math.factorial(n)>5e6: continue
    for perm in itertools.permutations(range(n)):
        second=[0]*n
        for slot,var in enumerate(perm): second[var]=slot//m
        tot+=1
        if components(r,first,second)>3*r/4: bad+=1
    S=structure_sum(r,m,3*r/4)
    Sall=structure_sum(r,m,0)
    print(f"r={r} m={m}: bad={bad}  structure-bound={S}  holds={bad<=S}   [control: total={tot} vs same bound -> {'exceeds (control fails as it should)' if tot>S else 'does not exceed'}; all-structures sum={Sall}]")
# CRT identity with proper control: un-centred F gives g(0)!=0 and the sum drops below C
def make_g(l, centred=True):
    S=set(random.sample(range(l), l//2)); sigma=len(S)/l
    if centred: F=[((1 if x in S else 0)-sigma)/math.sqrt(sigma*(1-sigma)) for x in range(l)]
    else: F=[(1 if x in S else 0)/math.sqrt(sigma) for x in range(l)]   # E|F|^2=1 but mean !=0
    return [math.sqrt(l)*sum(F[x]*cmath.exp(-2j*math.pi*b*x/l) for x in range(l))/l for b in range(l)]
for centred in (True,False):
    ls=[5,7,11]; C=385; gs={l:make_g(l,centred) for l in ls}
    s,d,q=3,2,13; tot=0
    for a in range(C):
        if math.gcd(a,C)!=1: continue
        val=1
        for l in ls:
            al=(s*pow(d*q*(C//l),-1,l))%l
            val*=abs(gs[l][(al*pow(a,-1,l))%l])**2
        tot+=val
    print("CRT sum", "centred" if centred else "CONTROL uncentred", round(tot,6), "C=",C)
