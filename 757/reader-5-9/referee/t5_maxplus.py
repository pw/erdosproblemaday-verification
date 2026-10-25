import itertools
O=(0,49,75,83,98,101,117,119,121,159,269)
assert 101+18*0/269==101 and 101+18*269/269==119
E=[set(t) for t in itertools.combinations(O,3) if t[0]+t[2]==2*t[1]]
print('APs of O:',sorted(tuple(sorted(e)) for e in E))
# all relations of O incl 4-pt
from collections import Counter
c=Counter(a+b for a,b in itertools.combinations_with_replacement(O,2)); print('max sum multiplicity (with a=b):',max(c.values()))
c2=Counter(a+b for a,b in itertools.combinations(O,2)); print('weak-Sidon (a<b) max multiplicity:',max(c2.values()))
IN=(0,269); OUT=(101,119)
keys=[frozenset(s) for k in range(3) for s in itertools.combinations((0,1),k)]  # index sets
def st(T,pair): return frozenset(i for i,p in enumerate(pair) if p in T)
A={}; v0={}
for k in range(12):
    for T in itertools.combinations(O,k):
        T=set(T)
        if any(e<=T for e in E): continue
        si,so=st(T,IN),st(T,OUT)
        A[(si,so)]=max(A.get((si,so),-99),len(T)-len(si))
        v0[so]=max(v0.get(so,-99),len(T))
print('v0:',{tuple(sorted(k)):v for k,v in v0.items()})
for (si,so),v in sorted(A.items(),key=lambda kv:(sorted(kv[0][0]),sorted(kv[0][1]))): pass
print('A[in][out]:'); 
for si in keys: print('  in',tuple(sorted(si)),[A.get((si,so)) for so in keys])
def step(v): return {so:max(v[si]+A[(si,so)] for si in keys) for so in keys}
v=v0; hs=[max(v0.values())]
v1=step(v0); print('v1-v0:',{tuple(sorted(k)):v1[k]-v0[k] for k in keys})
for K in range(1,200): v=step(v); hs.append(max(v.values()))
print('h(K)==7+5K for K<200:',all(h==7+5*K for K,h in enumerate(hs)))
# also: the 0/269 vs 101/119 sets are disjoint and none of O's APs contains both 0 and 269
print('APs containing 0 and 269:',[e for e in E if {0,269}<=e],' containing 101,119:',[e for e in E if {101,119}<=e])
