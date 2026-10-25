# Toy check of the Section 4.4 cancellation bookkeeping with the approximation step made EXACT
# (delta kernel: comparison multiplier = raw multiplier evaluated with A-coords taken from the TARGET
#  and B-coords taken from the SOURCE).  Claim to test:
#   raw(F',H') + sum_{A,B nonempty} -(-1)^{|A|+|B|} comp_{A,B}(F',H')
#     == R(F_full,H') + R(F'-F_full,H_full)      (exactly, for ANY F',H', ANY multiplier Phi)
# and the "wrong-asymmetry" variants fail.
import itertools, random, cmath
random.seed(1)
K=3                      # alphabet size per coordinate
p=[0.5,0.3,0.2]          # label law (same in every coord for simplicity)
I1=[0,1]; I2=[2,3]; NP=[4]   # block-1 probes, block-2 probes, one non-probe shared slot
n=5
coords=list(range(n))
X=list(itertools.product(range(K),repeat=n))
def P(x): 
    r=1.0
    for a in x: r*=p[a]
    return r
def rc(): return complex(random.gauss(0,1),random.gauss(0,1))
F={x:rc() for x in X}; H={x:rc() for x in X}
Phi={x:cmath.exp(2j*cmath.pi*random.random()) for x in X}
def E_i(G,i):
    out={}
    for x in X:
        s=0
        for a in range(K):
            y=list(x); y[i]=a; s+=p[a]*G[tuple(y)]
        out[x]=s
    return out
def one_minus_E(G,i):
    e=E_i(G,i); return {x:G[x]-e[x] for x in X}
def R(Fa,Ha):
    return sum(P(x)*Fa[x].conjugate()*Ha[x]*Phi[x] for x in X)
def comp(A,B,Fa,Ha,mode):
    # source x ~ product; target y: equal to x outside A∪B, fresh on A∪B.
    # multiplier argument z: outside from x; A-coords from (mode[0]) ; B-coords from (mode[1])
    free=sorted(A|B); tot=0
    for x in X:
        px=P(x)
        for fr in itertools.product(range(K),repeat=len(free)):
            y=list(x); pf=1.0
            for c,a in zip(free,fr): y[c]=a; pf*=p[a]
            y=tuple(y)
            z=list(x)
            for c in A: z[c]= y[c] if mode[0]=='T' else x[c]
            for c in B: z[c]= y[c] if mode[1]=='T' else x[c]
            tot+=px*pf*Fa[x].conjugate()*Ha[y]*Phi[tuple(z)]
    return tot
def subsets(s):
    s=list(s)
    for r in range(1,len(s)+1):
        for c in itertools.combinations(s,r): yield set(c)
Ffull=F
for i in I1: Ffull=one_minus_E(Ffull,i)
Hfull=H
for i in I2: Hfull=one_minus_E(Hfull,i)
target=R(Ffull,H)+R({x:F[x]-Ffull[x] for x in X},Hfull)
for mode in [('T','S'),('S','T'),('T','T'),('S','S')]:
    tot=R(F,H)
    for A in subsets(I1):
        for B in subsets(I2):
            tot+= -(-1)**(len(A)+len(B))*comp(A,B,F,H,mode)
    print("mode A-from-%s B-from-%s : total=%s  exceptional=%s  |diff|=%.3e"%(
        'target' if mode[0]=='T' else 'source','target' if mode[1]=='T' else 'source',
        complex(round(tot.real,6),round(tot.imag,6)),complex(round(target.real,6),round(target.imag,6)),abs(tot-target)))
