# Abstract single-place check of the per-place inequality used in Prop 5.5:
#   score_v  <=  2 T_v + lam |J_v| 1{b,b' in int J_v}  - (b'-b),
# where positives can only sit at s<b with both bits 1 inside I_- = [b-T,b], or at s>=b' with both
# bits 0 inside I_+ = [b',b'+T] (worst case: N true on the whole flank), the level classes come from a
# MONOTONE global profile pi(s)=P_E(n_e>s), common coefficient c(rho), good-rare coefficient 2 I_x(s)
# only when Y1=Y2=minority bit, damaged 0, negative charge 1{Y1!=Y2} at ALL levels.
# Controls (should FAIL): (A) non-monotone pi (pi values shuffled across pieces);
#                         (B) rare positives allowed regardless of the minority bit.
import random, sys, bisect
seed=int(sys.argv[1]) if len(sys.argv)>1 else 3
MODE=sys.argv[2] if len(sys.argv)>2 else "paper"
DL=sys.argv[3] if len(sys.argv)>3 else "stress"
random.seed(seed)
if DL=="paper": delta=0.01; lam=delta**2/2
else: delta=0.2; lam=0.3
def val(): return random.choice([round(random.uniform(-3,3),2), float(random.randint(-3,3))])
N=40000; viol=0; rarecases=0; excess_cases=0
for it in range(N):
    m=random.randint(2,9)
    ev=[val() for _ in range(m)]
    n1,n2=random.sample(ev,2) if m>=2 else (ev[0],ev[0])
    b,bp=min(n1,n2),max(n1,n2)
    lo=min(ev)-random.uniform(0,2); hi=max(ev)+random.uniform(0,2)
    T=abs(val())*random.random()
    eps=random.uniform(0.01,0.5)
    # conditional law of n_e given the base: random atoms (must include n1,n2 as possible values)
    ca=sorted(set([n1,n2]+[val() for _ in range(random.randint(0,4))]))
    cw=[random.random()**2 for _ in ca]; Z=sum(cw); cw=[x/Z for x in cw]
    # random piece structure for rare-level types and I_x
    cuts=sorted(set([round(random.uniform(lo,hi),2) for _ in range(random.randint(0,6))]))
    bps=sorted(set([lo,hi]+ev+ca+cuts+[b-T,b,bp,bp+T]))
    bps=[x for x in bps if lo<=x<=hi]
    piece_type={}; piece_I={}
    def ptype(s):
        k=bisect.bisect_right(cuts,s)
        if k not in piece_type: piece_type[k]=random.choice(["good","good","damaged"]); piece_I[k]=random.randint(0,1)
        return piece_type[k],piece_I[k]
    def pi_true(s): return sum(1 for x in ev if x>s)/len(ev)
    subs=[(bps[i],bps[i+1]) for i in range(len(bps)-1) if bps[i+1]>bps[i]]
    if MODE=="nonmono":
        pis=[pi_true((u+v)/2) for u,v in subs]; random.shuffle(pis)
        pimap={sv:p for sv,p in zip(subs,pis)}
    score=0.0; Jlen=0.0; Jpieces=[]; rare_pos=False
    for (u,v) in subs:
        s=(u+v)/2; L=v-u
        pi=pimap[(u,v)] if MODE=="nonmono" else pi_true(s)
        f=min(pi,1-pi)
        rho=sum(w for a,w in zip(ca,cw) if a>s)
        Y1=1 if n1>s else 0; Y2=1 if n2>s else 0
        common = f>=eps
        if common and abs(rho-0.5)<=delta: Jlen+=L; Jpieces.append((u,v))
        elig = (Y1==Y2==1 and b-T<=s<=b) or (Y1==Y2==0 and bp<=s<=bp+T)
        coef=0.0
        if common: coef = 1+lam if abs(rho-0.5)<=delta else 1-lam
        else:
            t,Ix=ptype(s)
            r = 1 if pi<0.5 else 0
            if t=="good" and Ix==1 and (Y1==Y2==r or MODE=="anybit"):
                coef=2.0
                if elig: rare_pos=True
        if elig: score+=coef*L
        if Y1!=Y2: score-=L
    if rare_pos: rarecases+=1
    if Jpieces:
        j0=min(u for u,v in Jpieces); j1=max(v for u,v in Jpieces)
        if MODE!="nonmono": assert abs((j1-j0)-Jlen)<1e-9, "J not an interval"
        ind = 1.0 if (j0<b<j1 and j0<bp<j1) else 0.0
    else: ind=0.0
    bound=2*T+lam*Jlen*ind-(bp-b)
    if score>bound+1e-9:
        viol+=1
        if viol<=2: print("  violation: b=%.2f b'=%.2f T=%.2f score=%.4f bound=%.4f rare=%s"%(b,bp,T,score,bound,rare_pos))
    if score>2*T-(bp-b)+1e-9: excess_cases+=1
print("MODE",MODE,"constants",DL,"trials",N,"rare-positive trials",rarecases,"trials using the lam|J| excess",excess_cases,"VIOLATIONS",viol)
