# Lemma 3.4 (general position, p.19-20) exact over N = Q(sqrt2)(i) and over N = Q(i) (rational analogue);
# Lemma 3.5 (addition under a cap, p.20) tested on the MAXIMAL function satisfying (3.12) on a grid.
from fractions import Fraction as Fr
from itertools import combinations
import random, numpy as np
random.seed(158)
# ---- arithmetic in Q(sqrt2)(i): element = (a,b,c,d) meaning a+b*s + i(c+d*s), s=sqrt2
def r2mul(x,y): return (x[0]*y[0]+2*x[1]*y[1], x[0]*y[1]+x[1]*y[0])
def r2inv(x):
    n = x[0]*x[0]-2*x[1]*x[1]; return (x[0]/n, -x[1]/n)
def cmul(z,w):
    zr,zi=(z[0],z[1]),(z[2],z[3]); wr,wi=(w[0],w[1]),(w[2],w[3])
    rr = tuple(p-q for p,q in zip(r2mul(zr,wr),r2mul(zi,wi))); ii = tuple(p+q for p,q in zip(r2mul(zr,wi),r2mul(zi,wr)))
    return (rr[0],rr[1],ii[0],ii[1])
def conj(z): return (z[0],z[1],-z[2],-z[3])
def u_of_t(t):  # t=(p,q) in Q(sqrt2): u=(1+it)^2/(1+t^2)
    one_it = (Fr(1),Fr(0),t[0],t[1]); num = cmul(one_it,one_it)
    den = r2inv((Fr(1)+r2mul(t,t)[0], r2mul(t,t)[1]))
    return cmul(num,(den[0],den[1],Fr(0),Fr(0)))
def rank(vecs):
    M=[list(v) for v in vecs]; rk=0; ncol=len(M[0]) if M else 0
    for c in range(ncol):
        piv=next((i for i in range(rk,len(M)) if M[i][c]!=0),None)
        if piv is None: continue
        M[rk],M[piv]=M[piv],M[rk]
        for i in range(len(M)):
            if i!=rk and M[i][c]!=0:
                f=M[i][c]/M[rk][c]; M[i]=[a-f*b for a,b in zip(M[i],M[rk])]
        rk+=1
    return rk
def build_S(size, d0, gen):
    S=[]
    while len(S)<size:
        u=gen()
        if all(rank(list(sub)+[u])==len(sub)+1 for k in range(0,d0) for sub in combinations(S,k)):
            S.append(u)
    return S
one=(Fr(1),Fr(0),Fr(0),Fr(0))
gen=lambda: u_of_t((Fr(random.randint(-9,9),random.randint(1,9)),Fr(random.randint(-9,9),random.randint(1,9))))
S=build_S(9,4,gen)
assert all(cmul(u,conj(u))==one for u in S), 'not unit modulus'
allind = all(rank(sub)==4 for sub in combinations(S,4))
print('Lemma 3.4, N=Q(sqrt2,i), d0=4: |S|=%d, all elements in K (u*ubar=1): True, every 4-subset a Q-basis: %s (%d subsets)'%(len(S),allind,len(list(combinations(S,4)))))
# FAILING control: replace one element by -S[0] (still in K and N): some 4-subset must be dependent
Sc=S[:-1]+[tuple(-c for c in S[0])]
print('  control (S with -S[0] added): every 4-subset a Q-basis:', all(rank(sub)==4 for sub in combinations(Sc,4)), '(expected False)')
# rational analogue: N0=Q, N=Q(i), d0=2
genQ=lambda: u_of_t((Fr(random.randint(-30,30),random.randint(1,30)),Fr(0)))
SQ=build_S(12,2,genQ)
print('Lemma 3.4 rational analogue N=Q(i), d0=2: |S|=%d, every 2-subset a Q-basis: %s  -> Lemma 3.4 itself does NOT separate F(i) from Q(i)'%(len(SQ),all(rank(sub)==2 for sub in combinations(SQ,2))))
# ---- Lemma 3.5 on the maximal w satisfying w(0)=0, w(p_j)<=H=1, (3.12) for args in [0,P]
def maximal_w(P, inputs):
    INF=10**9; w=np.full(P+1,INF,dtype=np.int64); w[0]=0
    for pj in inputs: w[pj]=min(w[pj],1)
    idx_all=np.arange(P+1)
    while True:
        old=w.copy()
        for A in range(P+1):
            if w[A]>=INF: continue
            vals=w[A]+w; idx=np.abs(A-idx_all); m=vals<INF
            np.minimum.at(w, idx[m], vals[m])
        if np.array_equal(old,w): return w
worst=0.0; worst_case=None; tested=0; ctrl_fail=0
for trial in range(6):
    P=600; q=random.choice([2,3]); inputs=sorted(set([P]+[random.randint(1,P-1) for _ in range(q-1)]))
    w=maximal_w(P,inputs)
    for M in range(1,7):
        # all integer vectors a with sum|a|<=M
        vecs=[()]
        for _ in inputs: vecs=[v+(a,) for v in vecs for a in range(-M,M+1)]
        for a in vecs:
            if sum(map(abs,a))>M or sum(map(abs,a))==0: continue
            z=sum(ai*pi for ai,pi in zip(a,inputs))
            if 0<=z<P:
                tested+=1; ratio=w[z]/(M*1.0)
                assert w[z]<=4*M, ('LEMMA 3.5 VIOLATED',inputs,a,z,w[z])
                if ratio>worst: worst=ratio; worst_case=(inputs,a,z,int(w[z]),M)
                if w[z]>1*M: ctrl_fail+=1
print('Lemma 3.5: %d (inputs, combination) cases, all satisfy w(z)<=4MH; max w(z)/(MH)=%.3f at %s'%(tested,worst,worst_case))
print('  control: the stronger claim w(z)<=1*MH FAILS in %d cases (so the check can fail; constant >1 is needed)'%ctrl_fail)
