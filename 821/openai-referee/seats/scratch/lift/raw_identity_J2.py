# Toy check, J=2 shared slots + l=1 unshared slot per group (M=3), one small + one big group.
import cmath, math, itertools, random
random.seed(7)
G = {'s':[5,7,11,13], 'b':[17,19,23,29]}
allP = G['s']+G['b']; V = {g: sum(1/p for p in G[g]) for g in G}
q=0.55; k=3; Z=500.0; a1=0.4; a2=2.1; J=2; l=1; M=J+l; s=2
def Psi(t): return 0.0 if (t<=1 or t>=3) else math.exp(-1/((t-1)*(3-t)))
def nstar(n):
    for p in allP:
        while n%p==0: n//=p
    return n
c1={};c2={}
def F0(n):
    m=nstar(n); c1.setdefault(m,complex(random.uniform(-1,1),random.uniform(-1,1))); return c1[m]
def G0(n):
    m=nstar(n); c2.setdefault(m,complex(random.uniform(-1,1),random.uniform(-1,1))); return c2[m]
def divs(n,g): return [p for p in G[g] if n%p==0]
def omega(n): return sum(len(divs(n,g)) for g in G)
def Wl(n):
    v=q**(omega(n)-s*l)
    for g in G: v*=len(divs(n,g))/V[g]   # (omega_g)_1 / V_g
    return v
pw=lambda x,a: cmath.exp(1j*a*math.log(x))
Dmax=1
for g in G: Dmax*=sorted(G[g])[-1]*sorted(G[g])[-2]
nmax=int(3*Z*Dmax)+10
cand=set()
for S3 in itertools.combinations(G['s'],3):
    for B3 in itertools.combinations(G['b'],3):
        base=math.prod(S3)*math.prod(B3)
        cand.update(range(base,nmax,base))
LHS=0;LHS_noov=0
for n in sorted(cand):
    ds,db=divs(n,'s'),divs(n,'b')
    for Ls in itertools.permutations(ds,3):
        for Lb in itertools.permutations(db,3):
            sh_s,sh_b=Ls[:2],Lb[:2]; D=math.prod(sh_s)*math.prod(sh_b)
            ps=Psi(n/(Z*D))
            if ps==0: continue
            n2=n+k*D
            tgt=sum(1 for x in divs(n2,'s') if x not in sh_s)*sum(1 for y in divs(n2,'b') if y not in sh_b)
            if tgt==0: continue
            term=(V['s']**-M*V['b']**-M)*(V['s']**-l*V['b']**-l)*tgt*pw(n,a1)*F0(n).conjugate()*pw(n2,a2)*G0(n2)\
                 *pw(D,-(a1+a2))*ps/n*q**(omega(n)-M*s)*q**(omega(n2)-M*s)
            LHS+=term
            w,w2=n//D,n2//D
            if all(w%p and w2%p for p in sh_s+sh_b): LHS_noov+=term
S=0;S_noov=0
for w in range(1,int(3*Z)+5):
    if Psi(w/Z)==0: continue
    w2=w+k
    t=Psi(w/Z)/w*pw(w,a1)*pw(w2,a2)*F0(w).conjugate()*G0(w2)*Wl(w)*Wl(w2)
    S+=t
    for sh_s in itertools.permutations(G['s'],2):        # ordered DISTINCT shared draws
        for sh_b in itertools.permutations(G['b'],2):
            if all(w%p and w2%p for p in sh_s+sh_b):
                wt=1.0
                for p in sh_s: wt/=V['s']*p
                for p in sh_b: wt/=V['b']*p
                S_noov+=t*wt
print("LHS_noov",LHS_noov);print("RHS_noov",S_noov);print("absdiff",abs(LHS_noov-S_noov))
print("LHS",LHS,"S",S)
