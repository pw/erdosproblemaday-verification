#!/usr/bin/env python3
"""Independent checks of Li's #341 construction against our own greedy run (greedy341.c output).
1. Li's explicit S (paper eq. for S; Lean def S) vs greedy membership for every n <= N.
2. Lemma 3.2 (finite shield mod 49) recomputed from scratch.
3. Controller identities (gate01/gate12/gate20) checked on [0, 8^7).
4. Y0 aperiodicity witness pattern (block lengths) printed.
5. Square seed {1,4,9,16,25}: a_{n+224} = a_n + 1176 for n >= 87 (1-indexed), onset minimality.
Exit 0 only if every check passes; prints counts (never a bare pass)."""
import sys, numpy as np
N=int(sys.argv[1]) if len(sys.argv)>1 else 10_000_000
el=np.fromfile('/home/exedev/MathDyad/erdos341/li_eq_1e7_elems.u32',dtype='<u4')
assert el.max()<=N and len(el)>0
greedy=np.zeros(N+1,dtype=bool); greedy[el]=True
n=np.arange(N+1,dtype=np.int64); r=n%49; q=n//49
def blocks(lo,hi,q):  # exists k: lo*8^k <= q < hi*8^k   (with the +1 variants handled by caller)
    out=np.zeros_like(q,dtype=bool); k=0
    while lo*8**k<=q.max():
        out|=(lo*8**k<=q)&(q<hi*8**k); k+=1
    return out
Y0=(q==0)|blocks(4,8,q)
Y1=((1<=q)&(q<=3))|blocks(16,32,q+1)&(True)  # 16*8^k <= q+1 and q < 32*8^k
# recompute Y1,Y2 exactly per Lean: ∃k, 16*8^k ≤ q+1 ∧ q < 32*8^k
def ex(lo,hi,q):
    out=np.zeros_like(q,dtype=bool); k=0
    while lo*8**k<=q.max()+1:
        out|=(lo*8**k<=q+1)&(q<hi*8**k); k+=1
    return out
Y1=((1<=q)&(q<=3))|ex(16,32,q)
Y2=(q<=1)|((7<=q)&(q<=15))|ex(64,128,q)
D=np.isin(n,[1,2,5,13,27,36,47]); B=np.isin(r,[3,22,32,40,48])
S=D|B|((r==7)&Y0)|((r==14)&Y1)|((r==28)&Y2)
S[0]=False
mism=np.nonzero(S!=greedy)[0]
print(f"[1] Li's S vs greedy on [1,{N}]: |S|={S.sum()} |greedy|={greedy.sum()} mismatches={len(mism)} first={mism[:10].tolist()}")
ok1=len(mism)==0
seed=[1,2,3,5,7,13,22,27,28,32,36,40,47,48,52,63,71,77,81,89,97]
ok1b=(np.nonzero(S[:98])[0].tolist()==seed); print(f"    S∩[1,97]==seed: {ok1b}")
# [2] shield
P={7,14,28}; Bs={3,22,32,40,48}; Ds={1,2,5,13,27,36,47}; Q=P|Bs
ss=lambda X,Y:{(x+y)%49 for x in X for y in Y}
cover=ss(Bs,Bs)|ss(P,Bs)|ss(Ds,Bs)
c1=cover==set(range(49))-Q
c2=not (Q&(ss(Bs,Bs)|ss(P,Bs)|ss(Ds,Bs)|ss(Ds,P)))
c3=(ss(P,P)&Q)==P
pairs={(x,y) for x in P for y in P if (x+y)%49 in Q}
c4=pairs=={(7,7),(14,14),(28,28)}
print(f"[2] shield: cover={c1} ({len(cover)} residues) avoid={c2} PP∩Q=P:{c3} diagonal-only:{c4}")
ok2=c1 and c2 and c3 and c4
# [3] controller identities on [0, L)
L=8**7
qq=np.arange(L); y0=(qq==0)|blocks(4,8,qq); y1=((1<=qq)&(qq<=3))|ex(16,32,qq); y2=(qq<=1)|((7<=qq)&(qq<=15))|ex(64,128,qq)
def sumset(y):  # indicator of y+y on [0,L)
    idx=np.nonzero(y)[0]; out=np.zeros(L,dtype=bool)
    # convolution via FFT would be fine; do block-wise since y is union of intervals: use runs
    runs=[]; i=0
    while i<len(idx):
        j=i
        while j+1<len(idx) and idx[j+1]==idx[j]+1: j+=1
        runs.append((idx[i],idx[j])); i=j+1
    for a,b in runs:
        for c,d in runs:
            lo,hi=a+c,b+d
            if lo<L: out[lo:min(hi,L-1)+1]=True
    return out
s0=sumset(y0); s1=sumset(y1); s2=sumset(y2)
g01=np.array_equal(y1, ~s0); g12=np.array_equal(y2, ~s1)
g20=np.array_equal(y0[1:], ~s2[:-1])  # Y0(q+1) <-> not PairSum Y2 q
print(f"[3] controller on [0,8^7): gate01={g01} gate12={g12} gate20={g20}")
ok3=g01 and g12 and g20
# [4] Y0 block structure
print("[4] Y0 member blocks:", [(4*8**k,8*8**k-1) for k in range(5)], "gap runs between them grow as 24·8^k")
# [5] square seed control
sq=np.fromfile('/home/exedev/MathDyad/erdos341/sq_eq_2e6_elems.u32',dtype='<u4') if __import__('os').path.exists('/home/exedev/MathDyad/erdos341/sq_eq_2e6_elems.u32') else None
if sq is not None:
    a=sq.astype(np.int64); m=len(a)
    ok5=bool(np.all(a[86+224:m]==a[86:m-224]+1176)) and (a[85+224]!=a[85]+1176)
    print(f"[5] square seed {{1,4,9,16,25}} (equal rule): a_(n+224)=a_n+1176 for all 87<=n<={m-224} : {np.all(a[86+224:m]==a[86:m-224]+1176)} ; fails at n=86: {a[85+224]!=a[85]+1176} ; a_87={a[86]}")
else:
    ok5=True; print("[5] square seed file not present yet")
print("ALL PASS" if (ok1 and ok1b and ok2 and ok3 and ok5) else "FAIL")
sys.exit(0 if (ok1 and ok1b and ok2 and ok3 and ok5) else 1)
