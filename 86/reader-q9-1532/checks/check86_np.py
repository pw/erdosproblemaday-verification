# Second instrument: different parser (regex over whole file), adjacency matrix, C4-free <=> offdiag(A^2) <= 1 (Q9 is bipartite & simple).
import re, sys, numpy as np
n=9; N=1<<n
txt=open(sys.argv[1]).read()
pairs=[(int(a),int(b)) for a,b in re.findall(r'^\s*(\d+)\s+(\d+)\s*$',txt,re.M)]
A=np.zeros((N,N),dtype=np.int64)
for a,b in pairs:
    assert bin(a^b).count('1')==1
    A[a,b]+=1; A[b,a]+=1
assert A.max()==1, 'multi-edge'
A2=A@A; np.fill_diagonal(A2,0)
print(sys.argv[1],'rows',len(pairs),'edges',A.sum()//2,'max common nbrs',A2.max(),'degree range',A.sum(1).min(),A.sum(1).max())
# square parity: count edges on each 2-face
cnt=np.zeros(5,dtype=int)
for v in range(N):
    for i in range(n):
        for j in range(i+1,n):
            if v>>i&1 or v>>j&1: continue
            a=v|1<<i; b=v|1<<j; c=a|1<<j
            cnt[A[v,a]+A[v,b]+A[a,c]+A[b,c]]+=1
print('2-faces by #edges [0..4]:',cnt.tolist(),' total',cnt.sum(),'=',36*128)
