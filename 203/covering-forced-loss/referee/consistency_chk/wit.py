import json,sys,numpy as np
D=sys.argv[1]
pool={r["p"]:r for r in json.load(open(D+"/pool_5040.json"))["pool"]}
T=720
k,l=np.meshgrid(np.arange(T),np.arange(T),indexing="ij")
def cos(p,c):
    r=pool[p]; return ((r["u"]*k+r["v"]*l)%r["e"])==c
def count(ps,cs,F=None):
    U=np.zeros((T,T),bool) if F is None else F.copy()
    for p,c in zip(ps,cs): U|=cos(p,c)
    return int(U.sum())
S6=[5,7,11,13,17,19]; S7=S6+[31]
print("S6 witness 0 1 1 0 0 1 ->",count(S6,[0,1,1,0,0,1]))
print("S7 witness 0 1 1 0 0 1 0 ->",count(S7,[0,1,1,0,0,1,0]))
F=((k%3==0)&(l%3==0))|((k%5==0)&(l%5==0))|((k%4==2)&(l%4==0))
print("F_720 count",int(F.sum()), int(F.sum())/T/T)
fb=np.fromfile(D+"/fixed_720.bin",dtype=np.uint8)
bits=np.unpackbits(fb,bitorder="little")[:T*T].reshape(T,T).astype(bool)
print("fixed_720.bin == F:", bool((bits==F).all()), int(bits.sum()))
print("d=720 witness 2 3 5 6 8 9 + F ->",count(S6,[2,3,5,6,8,9],F))
# independent: admissible coset for d=720 directly from definition: 2^k3^l ≡ -1 mod p
for p in S6:
    r=pool[p]; e=r["e"]
    cs={int(((r["u"]*kk+r["v"]*ll)%e)) for kk in range(e) for ll in range(e) if (pow(2,kk,p)*pow(3,ll,p))%p==p-1}
    print(p,"cosets with 2^k3^l=-1:",cs)
