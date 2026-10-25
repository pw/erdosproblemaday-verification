import numpy as np, json, sys
A=np.unpackbits(np.fromfile('runs/A9.bits',dtype=np.uint8),bitorder='little')[:10**9+1]
B=np.unpackbits(np.fromfile('runs/B8.bits',dtype=np.uint8),bitorder='little')[:10**8+1]
print('bits A vs B on [0,1e8]: identical =', bool(np.array_equal(A[:10**8+1],B)))
eA=np.fromfile('runs/A9.ell',dtype=np.uint64); eB=np.fromfile('runs/B8.ell',dtype=np.uint64)
print('ell A vs B on [0,1e8]: identical =', bool(np.array_equal(eA,eB)))
BS=10**5
blk=np.add.reduceat(A[1:].astype(np.uint32), np.arange(0,10**9,BS)).astype(np.int64)  # blk[i] = #totients in [i*BS+1,(i+1)*BS]
cb=np.concatenate([[0],np.cumsum(blk)])
small=np.cumsum(A[:BS+1].astype(np.int64))
class Cum:
    def __getitem__(self,x):
        if x<=BS: return int(small[x])
        q,r=divmod(x,BS); return int(cb[q])+int(np.count_nonzero(A[q*BS+1:x+1]))
cum=Cum()
out={}
for k in range(1,10):
    for mlt in (1,2,5):
        x=mlt*10**k
        if x<=10**9: out[x]=int(cum[x])
for x in sorted(out): print('V(%d) = %d'%(x,out[x]))
print('V(2x)/V(x):')
for k in range(1,9):
    for mlt in (1,2,5):
        x=mlt*10**k
        if 2*x<=10**9: print('  x=%d  %.6f'%(x,cum[2*x]/cum[x]))
# least-preimage analysis on v <= 1e8
NL=10**8
tot=np.nonzero(B)[0]; tot=tot[tot>=1]
ell=eA[tot].astype(np.float64); r=ell/tot
i=np.argmax(r); print('max ell(d)/d for d<=1e8: d=%d ell=%d ratio=%.6f'%(tot[i],int(eA[tot[i]]),r[i]))
for k in (1,2,3,4):
    idx=np.nonzero(eA[tot] > np.uint64(k)*tot.astype(np.uint64))[0]
    print('k=%d: #seeds d<=1e8 with ell(d)>k d = %d; smallest = %s'%(k,len(idx), (int(tot[idx[0]]), int(eA[tot[idx[0]]])) if len(idx) else None))
# record-setters of ell(d)/d
rec=[];best=0
for d,e in zip(tot.tolist(), eA[tot].tolist()):
    q=e/d
    if q>best: best=q; rec.append((d,e,round(q,6)))
print('records of ell(d)/d:',rec[-25:])
# N_k(x)/V(x) at x = 1e7, 1e8 (ell(v) up to ~6x fits: ell recorded exactly for v <= 1e8)
for x in (10**6,10**7,10**8):
    m=tot<=x; t=tot[m]; e=eA[t]
    V=len(t); s=[]
    for k in range(0,6):
        c=int(np.count_nonzero((e> np.uint64(k*x)) & (e<= np.uint64((k+1)*x))))
        s.append(c)
    print('x=%d V=%d  N_k(x)/V for k=0..5:'%(x,V), [round(c/V,6) for c in s], 'counts', s)
json.dump({str(k):v for k,v in out.items()}, open('V_table.json','w'))
