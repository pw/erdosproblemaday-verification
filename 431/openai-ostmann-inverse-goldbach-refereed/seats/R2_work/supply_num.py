import numpy as np, itertools, math, random
rng=np.random.default_rng(1)

# ---------- (a) energy identity (5.3) ----------
def check_energy(ps, use_inverse_kappa=False, nA=400):
    S={p:set(rng.choice(p, size=(p+1)//2 if p>2 else 1, replace=False).tolist()) for p in ps}
    q=math.prod(ps)
    A=[]
    while len(A)<nA:
        a=int(rng.integers(10**6,10**7))
        if all(a%p in S[p] for p in ps): A.append(a)
    A=np.array(A)
    # LHS
    lhs=0.0
    for h in range(q):
        if math.gcd(h,q)!=1: continue
        lhs+=abs(np.mean(np.exp(2j*np.pi*h*A/q)))**2
    # RHS
    kappa={p:(p-len(S[p]))/len(S[p]) for p in ps}
    if use_inverse_kappa: kappa={p:1/k for p,k in kappa.items()}
    rhs=0.0
    for r in range(len(ps)+1):
        for sub in itertools.combinations(ps,r):
            t=math.prod(sub)
            # B_A(t) = || (1/m) sum_a tensor_{p in sub} Q_S e_{a mod p} ||^2
            # inner product of tensors factorizes: <Q e_x,Q e_y> = 1[x=y]-1/|S|
            # B = E_{a,a'} prod_p (1[a=a' mod p] - 1/|S_p|)
            M=np.ones((len(A),len(A)))
            for p in sub:
                ap=A%p
                M*= (ap[:,None]==ap[None,:]).astype(float)-1/len(S[p])
            B=M.mean()
            other=[p for p in ps if p not in sub]
            rhs+=t*B*math.prod(kappa[p] for p in other)
    return lhs,rhs

for ps in ([3,5,7],[5,7,11],[3,7,13]):
    l,r=check_energy(ps); li,ri=check_energy(ps,use_inverse_kappa=True)
    print('energy',ps,'lhs=%.10f rhs=%.10f diff=%.2e | control(kappa^-1) diff=%.2e'%(l,r,l-r,li-ri))
