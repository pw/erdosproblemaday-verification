# Check Lemma 5.4 (5.11) and (5.12) numerically, with failing controls.
import random, sys
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)

def inter(a0,a1,b0,b1):
    return max(0.0, min(a1,b1)-max(a0,b0))

def lhs(b,bp,T,J,lam,Tm=None,Tp=None):
    # [(1-lam)(|I-|+|I+|) + 2 lam a - (|I-|+|I+|)]_+ ; Lemma uses Tm=Tp=T
    Tm = T if Tm is None else Tm; Tp = T if Tp is None else Tp
    j0,j1 = J
    a = inter(j0,j1,b-Tm,b) + inter(j0,j1,bp,bp+Tp)
    tot = Tm+Tp
    return max(0.0,(1-lam)*tot + 2*lam*a - tot), a

def rhs(b,bp,J,lam,ind):
    j0,j1 = J
    return lam*(j1-j0)*ind(b,bp,J)

def ind_paper(b,bp,J):   # 1{b,b' in int J}
    j0,j1=J
    return 1.0 if (j0<b<j1 and j0<bp<j1) else 0.0

def ind_one(b,bp,J):     # control: only b' in int J required (weaker indicator)
    j0,j1=J
    return 1.0 if (j0<bp<j1) else 0.0

def rnd():
    return random.choice([random.uniform(-3,3), float(random.randint(-3,3))])

N=100000
viol_paper=0; viol_halfcoef=0; viol_unequalT=0; viol_drop_ind=0; pos_cases=0; eqb_pos=0
for it in range(N):
    b=rnd(); bp=b+random.choice([0.0, abs(rnd())])
    T=abs(rnd())
    j0=rnd(); j1=j0+abs(rnd())
    lam=random.uniform(1e-6,0.999)
    L,a=lhs(b,bp,T,(j0,j1),lam)
    if L>0:
        pos_cases+=1
        if b==bp: eqb_pos+=1
    if L > rhs(b,bp,(j0,j1),lam,ind_paper)+1e-12: viol_paper+=1
    # control 1 (should FAIL): half the coefficient on the right
    if L > 0.5*rhs(b,bp,(j0,j1),lam,ind_paper)+1e-12: viol_halfcoef+=1
    # control 2 (should FAIL): unequal flank lengths with the paper's indicator
    Tm=abs(rnd()); Tp=abs(rnd())
    L2,_=lhs(b,bp,None,(j0,j1),lam,Tm,Tp)
    # natural analogue of the excess over (Tm+Tp):
    if L2 > rhs(b,bp,(j0,j1),lam,ind_paper)+1e-12: viol_unequalT+=1
    # 'drop the indicator' (brief's suggestion) cannot fail: RHS only grows
    if L > lam*(j1-j0)+1e-12: viol_drop_ind+=1
print("cases",N,"positive-excess cases",pos_cases,"of which b==b'",eqb_pos)
print("paper (5.11) violations:",viol_paper)
print("control: dropping the indicator (RHS grows) violations:",viol_drop_ind,"(expected 0: not a failing control)")
print("control A: RHS halved violations:",viol_halfcoef,"(expected >0)")
print("control B: unequal flank lengths Tm!=Tp violations:",viol_unequalT,"(expected >0)")

# (5.12): X arbitrary atomic law, J = maximal set where |P(X>s)-1/2|<=delta (exact, piecewise),
# check P(X in int J) <= 2 delta.  Control C: count atoms at the CLOSED ends of J (should fail).
viol512=0; viol512_closed=0; checked=0
for it in range(100000):
    k=random.randint(1,7)
    atoms=sorted(set(random.choice([round(random.uniform(-2,2),3), float(random.randint(-2,2))]) for _ in range(k)))
    k=len(atoms)
    w=[random.random()**3 for _ in range(k)]; Z=sum(w); w=[x/Z for x in w]
    delta=random.uniform(0.01,0.45)
    # piece m (m=0..k): m=0 is (-inf,a_0) value 1; m>=1 is [a_{m-1},a_m) value sum_{l>=m} w_l
    vals=[sum(w[m:]) for m in range(k+1)]
    good=[m for m in range(k+1) if abs(vals[m]-0.5)<=delta]
    if not good: continue
    assert good==list(range(good[0],good[-1]+1))  # monotone => contiguous
    if good[0]==0 or good[-1]==k: continue  # infinite J impossible for delta<1/2
    j0=atoms[good[0]-1]; j1=atoms[good[-1]] if good[-1]<k else None
    checked+=1
    pint=sum(wi for ai,wi in zip(atoms,w) if j0<ai<j1)
    pcl=sum(wi for ai,wi in zip(atoms,w) if j0<=ai<=j1)
    if pint>2*delta+1e-12: viol512+=1
    if pcl>2*delta+1e-12: viol512_closed+=1
print("(5.12) checked",checked,"violations (open interior):",viol512)
print("control C: same with CLOSED J (endpoint atoms counted) violations:",viol512_closed,"(expected >0)")
