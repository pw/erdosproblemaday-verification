# Independent recomputation: Lemma 3.2 (shield mod 49) and controller identities by brute-force convolution.
import numpy as np, itertools, sys
M=49
P={7,14,28}; B={3,22,32,40,48}; D={1,2,5,13,27,36,47}; Q=P|B
def ss(X,Y): return {(x+y)%M for x in X for y in Y}
allr=set(range(M))
cover=ss(B,B)|ss(P,B)|ss(D,B)
print("cover == Z49\\Q :", cover==allr-Q, " missing:", sorted((allr-Q)-cover), " extra(in Q):", sorted(cover&Q))
avoid=Q&(ss(B,B)|ss(P,B)|ss(D,B)|ss(D,P))
print("avoid empty:", not avoid, sorted(avoid))
print("(P+P)∩Q == P:", (ss(P,P)&Q)==P, sorted(ss(P,P)))
print("ordered P pairs into Q:", sorted((x,y) for x in P for y in P if (x+y)%M in Q))
# extra: D+D residues hitting Q (paper excludes D+D by size, check whether residue argument would also be needed)
print("D+D residues ∩ Q:", sorted(ss(D,D)&Q), " max D+D:", max(D)*2)
# Do residue classes of D, B, P overlap?  (classification of summand types must be a partition)
print("D∩B, D∩P, B∩P:", D&B, D&P, B&P)
# Which r not in Q are covered ONLY by D+B or P+B (i.e. need those types)?
only=[r for r in sorted(allr-Q) if r not in ss(B,B)]
print("non-Q residues not in B+B (need P+B or D+B):", only)
# controller identities by brute force on [0, L)
L=8**6+1000
q=np.arange(L)
def Y0f(n):
    if n==0: return True
    k=0
    while 4*8**k<=n:
        if 4*8**k<=n<8*8**k: return True
        k+=1
    return False
def Y1f(n):
    if 1<=n<=3: return True
    k=0
    while 16*8**k-1<=n:
        if 16*8**k-1<=n<=32*8**k-1: return True
        k+=1
    return False
def Y2f(n):
    if n<=1 or 7<=n<=15: return True
    k=0
    while 64*8**k-1<=n:
        if 64*8**k-1<=n<=128*8**k-1: return True
        k+=1
    return False
y0=np.array([Y0f(n) for n in range(L)]); y1=np.array([Y1f(n) for n in range(L)]); y2=np.array([Y2f(n) for n in range(L)])
def sumset(y):
    # exact integer convolution via FFT then round; counts <= L
    n=1<<int(np.ceil(np.log2(2*L)))
    f=np.fft.rfft(y.astype(np.float64),n); c=np.fft.irfft(f*f,n)[:L]
    return c>0.5
s0,s1,s2=sumset(y0),sumset(y1),sumset(y2)
print("gate01 Y1 = ~(Y0+Y0) on [0,%d):"%L, np.array_equal(y1,~s0), " first mismatch:", np.nonzero(y1!=~s0)[0][:5])
print("gate12 Y2 = ~(Y1+Y1):", np.array_equal(y2,~s1), np.nonzero(y2!=~s1)[0][:5])
print("gate20 Y0 = {0} ∪ (1+~(Y2+Y2)):", y0[0] and np.array_equal(y0[1:],~s2[:-1]), np.nonzero(y0[1:]!=~s2[:-1])[0][:5])
# displayed interval formulas (eq Y0-square etc.)
def runs(b):
    idx=np.nonzero(b)[0]; out=[]; s=idx[0]; p=idx[0]
    for i in idx[1:]:
        if i!=p+1: out.append((s,p)); s=i
        p=i
    out.append((s,p)); return out
print("Y0+Y0 runs:", runs(s0)[:6])
print("Y1+Y1 runs:", runs(s1)[:6])
print("Y2+Y2 runs:", runs(s2)[:6])
print("Y0 runs:", runs(y0)[:6]); print("Y1 runs:", runs(y1)[:6]); print("Y2 runs:", runs(y2)[:6])
