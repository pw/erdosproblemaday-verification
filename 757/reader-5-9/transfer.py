# Exact max Sidon of S_K for ALL K, given (relations.py) that every additive relation lies in one copy and is one of
# the 9 images of O's 3-APs. Chain DP over the 2-point overlaps {phi^j(101),phi^j(119)} = {phi^{j+1}(0),phi^{j+1}(269)}.
import itertools
O=[0,49,75,83,98,101,117,119,121,159,269]
APs=[(a,b,c) for a,b,c in itertools.combinations(O,3) if a+c==2*b]
assert len(APs)==9
def ok(T): return not any(set(t)<=T for t in APs)
NEG=-10**9
# M[L][R] = max over AP-free T⊆O with T∩{0,269}=L, T∩{101,119}=R of |T|-|L|   (L,R as bitmasks: bit0 = 0/101, bit1 = 269/119)
def mask(T,a,b): return (a in T)|((b in T)<<1)
M=[[NEG]*4 for _ in range(4)]; first=[NEG]*4
for r in range(len(O)+1):
    for T in itertools.combinations(O,r):
        T=set(T)
        if not ok(T): continue
        L=mask(T,0,269); R=mask(T,101,119)
        M[L][R]=max(M[L][R],len(T)-bin(L).count('1'))
        first[R]=max(first[R],len(T))
print('first (copy 0, by R state):',first)
print('transfer M[L][R]:'); [print('  ',row) for row in M]
def step(v): return [max(v[L]+M[L][R] for L in range(4)) for R in range(4)]
v=first; g=[max(v)]
for K in range(1,40):
    v=step(v); g.append(max(v))
print('g(K) K=0..12:',g[:13])
assert all(g[K]==7+5*K for K in range(40)), 'g != 7+5K'
# max-plus periodicity: find K0 with v_{K0+1} = v_{K0} + 5 componentwise => holds for all larger K
v=first; prev=None
for K in range(0,30):
    nv=step(v)
    if all(nv[i]-v[i]==5 for i in range(4) if v[i]>NEG//2):
        print('stationary at K=',K,': v_{K+1}=v_K+5 componentwise; v_K=',v); break
    v=nv
else: raise SystemExit('no stationarity found')
