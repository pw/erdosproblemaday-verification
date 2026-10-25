# Toy check of the per-pattern lift (5.7) for a COMPARISON-type pattern:
# J=2, l=1, M=3. Small group: C_s = {} (slots 1,2 shared, slot 3 unshared). Big group: C_b={1}
# (slot 1 free, slot 2 shared, slots 1&3 unshared, t_b=2). Free label f ~ mu_b. Kernel K = kap(f)*lam(target slot-1 label).
import cmath, math, itertools, random
random.seed(11)
G={'s':[5,7,11,13],'b':[17,19,23,29,31,37]}; allP=G['s']+G['b']; V={g:sum(1/p for p in G[g]) for g in G}
q=0.5;k=-2;Z=600.0;a1=-0.9;a2=1.7;M=3;s=2; t={'s':1,'b':2}
Psi=lambda u: 0.0 if (u<=1 or u>=3) else math.exp(-1/((u-1)*(3-u)))
def nstar(n):
    for p in allP:
        while n%p==0: n//=p
    return n
c1={};c2={}
def F0(n):
    m=nstar(n); c1.setdefault(m,complex(random.uniform(-1,1),random.uniform(-1,1))); return c1[m]
def G0(n):
    m=nstar(n); c2.setdefault(m,complex(random.uniform(-1,1),random.uniform(-1,1))); return c2[m]
kap={p:complex(random.uniform(-1,1),random.uniform(-1,1)) for p in G['b']}
lam={p:complex(random.uniform(-1,1),random.uniform(-1,1)) for p in G['b']}
divs=lambda n,g:[p for p in G[g] if n%p==0]
omega=lambda n: sum(len(divs(n,g)) for g in G)
pw=lambda x,a: cmath.exp(1j*a*math.log(x))
mu=lambda g,p: 1/(V[g]*p)
Dmax=13*11*37*37; nmax=int(3*Z*Dmax)+10
cand=set()
for S3 in itertools.combinations(G['s'],3):
    for B3 in itertools.combinations(G['b'],3):
        base=math.prod(S3)*math.prod(B3); cand.update(range(base,nmax,base))
LHS=0;LHS_clean=0
for n in sorted(cand):
    for (x1,x2,x3) in itertools.permutations(divs(n,'s'),3):
        for (y1,y2,y3) in itertools.permutations(divs(n,'b'),3):
            for f in G['b']:
                if f in (y1,y2,y3): continue                 # ban vs source list
                D=x1*x2*y2*f; ps=Psi(n/(Z*D))
                if ps==0: continue
                n2=n+k*D
                tg=0
                for x3p in divs(n2,'s'):
                    if x3p in (x1,x2): continue
                    for (y1p,y3p) in itertools.permutations([y for y in divs(n2,'b') if y!=y2],2):
                        if f in (y1p,y3p): continue          # ban vs target list
                        tg+=lam[y1p]
                if tg==0: continue
                term=mu('b',f)*(V['s']**-M*V['b']**-M)*(V['s']**-t['s']*V['b']**-t['b'])*kap[f]*tg\
                     *pw(n,a1)*F0(n).conjugate()*pw(n2,a2)*G0(n2)*pw(D,-(a1+a2))*ps/n*q**(omega(n)-M*s)*q**(omega(n2)-M*s)
                LHS+=term
                DR=x1*x2*y2; w=n//DR; w2=n2//DR
                if all(w%p and w2%p for p in (x1,x2,y2)): LHS_clean+=term
def Wsum(w,g_t_lists_weight):
    pass
RHS=0
for f in G['b']:
    for w in range(1,int(3*Z*f)+5):
        ps=Psi(w/(Z*f))
        if ps==0: continue
        w2=w+k*f
        if w2<=0: continue
        # source unshared lists (ban: exclude f); target lists with kernel, ban exclude f
        srcS=len(divs(w,'s')); srcB=[pr for pr in itertools.permutations([y for y in divs(w,'b') if y!=f],2)]
        tgS=len(divs(w2,'s')); tgB=sum(lam[a] for (a,b) in itertools.permutations([y for y in divs(w2,'b') if y!=f],2))
        Wsrc=q**(omega(w)-3)*srcS/V['s']*len(srcB)/V['b']**2
        Wtgt=q**(omega(w2)-3)*tgS/V['s']*tgB/V['b']**2
        if Wsrc==0 or Wtgt==0: continue
        base=mu('b',f)*kap[f]*ps/w*pw(w/f,a1)*pw(w2/f,a2)*F0(w).conjugate()*G0(w2)*Wsrc*Wtgt
        for (x1,x2) in itertools.permutations(G['s'],2):
            for y2 in G['b']:
                if y2==f: continue                            # ban: free != shared
                if all(w%p and w2%p for p in (x1,x2,y2)):
                    RHS+=base*mu('s',x1)*mu('s',x2)*mu('b',y2)
print("LHS_clean",LHS_clean);print("RHS_clean",RHS);print("absdiff",abs(LHS_clean-RHS)); print("LHS total",LHS)
