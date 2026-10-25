import itertools, random
# 1) Def 2.1 satisfiability: h_i = W^{w e_i}, e_i = 2^{n-i}; need e_P+e_j-e_T-e_i >= 1 for all P<T<j<i
def subsets(s):
    s=list(s)
    for r in range(1,len(s)+1):
        for c in itertools.combinations(s,r): yield c
n=7
e={i:2**(n-i) for i in range(1,n+1)}
worst=10**9
for i in range(1,n+1):
    for T in subsets(range(1,i)):
        for j in range(max(T)+1,i):
            for P in subsets(range(1,min(T))):
                d=sum(e[p] for p in P)+e[j]-sum(e[t] for t in T)-e[i]
                worst=min(worst,d)
print("min exponent gap (units of w):",worst, " max h_B exponent:", max(sum(e[x] for x in B) for B in subsets(range(1,n+1))), "<= 2^n =",2**n)
# 2) chain property: for chains T1<...<Tm<i1<...<im, B_k in E_{B_d} for k<d
def in_E(A,B):
    T=sorted(B)[:-1]; i=max(B)
    j=max(A); P=sorted(A)[:-1]
    return len(P)>0 and len(T)>0 and max(P)<min(T) and max(T)<j<i
random.seed(1)
bad=0
for trial in range(2000):
    m=random.randint(2,5); sizes=[random.randint(1,3) for _ in range(m)]
    idx=1; tails=[]
    for s in sizes: tails.append(list(range(idx,idx+s))); idx+=s
    piv=list(range(idx,idx+m))
    Bs=[tails[d]+[piv[d]] for d in range(m)]
    for d in range(m):
        for k in range(d):
            if not in_E(Bs[k],Bs[d]): bad+=1
print("chain violations:",bad)
# 3) negative control: Alweiss-style anti-ordered tails (larger pivot <-> smaller tail) must FAIL E_B membership
bad=0; tot=0
for trial in range(500):
    m=random.randint(2,5); sizes=[random.randint(1,3) for _ in range(m)]
    idx=1; tails=[]
    for s in reversed(sizes): tails.append(list(range(idx,idx+s))); idx+=s
    tails=list(reversed(tails))  # tails[0] is the HIGHEST tail block
    piv=list(range(idx,idx+m))   # piv[0] lowest pivot
    Bs=[tails[d]+[piv[d]] for d in range(m)]
    for d in range(m):
        for k in range(d):
            tot+=1
            if not in_E(Bs[k],Bs[d]): bad+=1
print("anti-ordered: violations",bad,"of",tot)
