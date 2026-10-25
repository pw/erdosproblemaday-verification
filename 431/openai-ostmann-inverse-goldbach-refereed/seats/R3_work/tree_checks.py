# Numerical controls for §6 identities (Lemma 6.1 machinery). Each check has a perturbed control that must FAIL.
import numpy as np, sys
rng = np.random.default_rng(1)

def prim_root(q):
    for g in range(2, q):
        if all(pow(g, (q-1)//f, q) != 1 for f in set(fac(q-1))):
            return g
def fac(n):
    out=[];d=2
    while d*d<=n:
        while n%d==0: out.append(d); n//=d
        d+=1
    if n>1: out.append(n)
    return out

q = int(sys.argv[1]) if len(sys.argv)>1 else 31
gen = prim_root(q)
dlog = {}
x=1
for k in range(q-1):
    dlog[x]=k; x=x*gen%q
inv = lambda a: pow(a, q-2, q)
def chi(j, x):  # character j evaluated at x, zero at 0
    if x % q == 0: return 0.0
    return np.exp(2j*np.pi*j*dlog[x%q]/(q-1))
def e(x): return np.exp(2j*np.pi*(x % q)/q)

# random g with g(0)=0, E|g|^2 = 1, deliberately very non-uniform pointwise
g = np.zeros(q, complex)
g[1:] = rng.standard_normal(q-1)*np.exp(rng.standard_normal(q-1)) + 1j*rng.standard_normal(q-1)
g[3] *= 8  # spike
g /= np.sqrt(np.mean(np.abs(g)**2))
assert abs(np.mean(np.abs(g)**2)-1)<1e-12
CH = np.array([[chi(j,x) for x in range(q)] for j in range(q-1)])   # CH[j,x]
E = np.array([[e(a*x) for x in range(q)] for a in range(q)])        # E[a,x]=e_q(ax)
def hat(f):  # prob-normalised Fourier: hat f(a) = E_x f(x) e(-ax)
    return np.array([np.mean(f*np.conj(E[a])) for a in range(q)])
eps = max(abs(np.mean(g*CH[j]*E[a])) for j in range(q-1) for a in range(q))
print("q",q,"eps_q",round(eps,4))

worst = {}
def rec(name, val):
    worst[name] = max(worst.get(name,0), val)

for sigma in (1,-1):
  for gstar in (g, np.conj(g)):
    # h(d,t) and its Mellin coefficients vs P_chi(d)
    for d in range(1,q):
        h = np.zeros(q, complex)  # h as function of t in U
        for t in range(1,q):
            if t==1: continue
            x = sigma*d*t*inv(t-1) % q; z = sigma*d*inv(t-1) % q
            h[t] = gstar[x]*np.conj(gstar[z])
        for j in range(q-1):
            mel = sum(h[t]*np.conj(CH[j,t]) for t in range(1,q))/(q-1)
            f = gstar*np.conj(CH[j])
            P = q/(q-1)*np.mean([f[x]*np.conj(f[(x-sigma*d)%q]) for x in range(q)])
            Pbad = q/(q-1)*np.mean([f[x]*np.conj(f[(x+sigma*d)%q]) for x in range(q)])  # perturbed control
            rec("Mellin==P_chi", abs(mel-P)); rec("CONTROL Mellin vs wrong-shift (must be large)", abs(mel-Pbad))
    # w_chi formula and Sum r_chi bound
    tot_r = 0
    for j in range(q-1):
        f = gstar*np.conj(CH[j])
        Pfun = np.array([q/(q-1)*np.mean([f[x]*np.conj(f[(x-sigma*d)%q]) for x in range(q)]) for d in range(q)])
        w = hat(Pfun)
        fh = hat(f)
        w_formula = q/(q-1)*np.abs(np.array([fh[(sigma*a)%q] for a in range(q)]))**2
        w_bad = q/(q-1)*np.abs(np.array([fh[(-sigma*a)%q] for a in range(q)]))**2
        rec("w_chi formula", np.max(np.abs(w-w_formula)))
        rec("CONTROL w_chi wrong sign (must be large)", np.max(np.abs(w-w_bad)))
        rec("max w_chi / eps^2 (claim <= q/(q-1))", np.max(w.real)/eps**2)
        tot_r += np.sum(np.abs(w)**2)
    rec("sum_chi r_chi (claim <= 2q/(q-1)=%.3f)"%(2*q/(q-1)), tot_r)
    # uniform Mellin estimate (src42): identity + bound
    Pall = []
    for j in range(q-1):
        f = gstar*np.conj(CH[j])
        Pall.append(np.array([q/(q-1)*np.mean([f[x]*np.conj(f[(x-sigma*d)%q]) for x in range(q)]) for d in range(q)]))
    for eta in range(q-1):
        for a in range(q):
            lhs = sum(abs(np.mean(Pall[j]*CH[j]*CH[eta]*np.conj(E[a])))**2 for j in range(q-1))
            # E_lambda | E_d h(d, lambda d) eta(d) e(-ad) |^2
            acc=0
            for lam in range(1,q):
                s=0
                for d in range(1,q):
                    t = lam*d % q
                    if t==1: continue
                    x = sigma*d*t*inv(t-1) % q; z = sigma*d*inv(t-1) % q
                    s += gstar[x]*np.conj(gstar[z])*CH[eta,d]*np.conj(E[a,d])
                acc += abs(s/q)**2
            rhs_id = acc/(q-1)
            rec("src42 identity", abs(lhs-rhs_id))
            # CONTROL: wrong parametrisation t = lambda/d must break the identity
            acc2=0
            for lam in range(1,q):
                s2=0
                for d in range(1,q):
                    t = lam*inv(d) % q
                    if t==1: continue
                    x = sigma*d*t*inv(t-1) % q; z = sigma*d*inv(t-1) % q
                    s2 += gstar[x]*np.conj(gstar[z])*CH[eta,d]*np.conj(E[a,d])
                acc2 += abs(s2/q)**2
            rec("CONTROL src42 identity with t=lambda/d (must be large)", abs(lhs-acc2/(q-1)))
            rec("src42 lhs/eps^4 (>1 shows q^-1/2 term needed)", lhs/eps**4)
            rec("src42 ratio lhs/bound", lhs/((q/(q-1))*(eps**4+np.sqrt(3)/np.sqrt(q))))
            # control: drop the zero convention at lambda d = 1 -> identity should break (generically)
for k,v in worst.items(): print(f"{k:55s} {v:.3e}")
