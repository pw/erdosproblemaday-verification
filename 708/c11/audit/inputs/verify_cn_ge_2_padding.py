# Bonus claim: c_n >= 2 for every fixed n >= 4, by padding with r neutral primes.
# For n = 4+r: add r primes q_j in (uv+r, vw), put their unique multiples at x-j, need u > r.
import sympy, itertools
from collections import Counter
def val(n,p):
    c=0
    while n and n%p==0: n//=p; c+=1
    return c

def build(u,v,w,r):
    qs=[]
    cand=sympy.nextprime(u*v+r)
    while len(qs)<r:
        if cand>=v*w: return None
        qs.append(int(cand)); cand=sympy.nextprime(cand)
    if not u>r: return None
    primes=[u,v,w]+qs
    target=[2,4,2]+[1]*r
    # CRT: t=1 mod uw ; t*uw = v+1 mod v^2 ; t*u*v*w = j mod q_j  (so x-j divisible by q_j)
    mods=[u*w, v*v]+qs
    res=[1, ((v+1)*pow(u*w,-1,v*v))%(v*v)]+[ (j+1)*pow(u*v*w,-1,qs[j])%qs[j] for j in range(r)]
    from sympy.ntheory.modular import crt
    t,_=crt(mods,res); t=int(t); x=t*u*v*w
    lo,hi=x-u*v+1,x+u*v-1
    return primes,target,x,lo,hi,qs

def mincover(primes,target,lo,hi):
    vecs=Counter()
    for y in range(lo,hi+1):
        vc=tuple(min(val(y,p),target[i]) for i,p in enumerate(primes))
        if any(vc): vecs[vc]+=1
    classes=list(vecs.items()); best=[None]
    def rec(i,tot,acc):
        if best[0] is not None and tot>=best[0]: return
        if all(acc[j]>=target[j] for j in range(len(target))): best[0]=tot; return
        if i>=len(classes): return
        vc,mult=classes[i]
        # Once every coordinate supplied by this class is capped, further
        # identical points cannot improve the state.
        useful=max((target[j]+vc[j]-1)//vc[j] for j in range(len(target)) if vc[j])
        for k in range(min(mult,useful),-1,-1):
            rec(i+1,tot+k,tuple(acc[j]+vc[j]*k for j in range(len(target))))
    rec(0,0,tuple([0]*len(target)))
    return best[0]

for (u,v,w),r in [
    ((17,19,23),1),
    ((29,31,37),1),
    ((41,43,47),2),
    ((101,103,107),2),
    ((101,103,107),3),
    ((101,103,107),4),
    ((101,103,107),5),
    ((101,103,107),6),
]:
    n=4+r
    b=build(u,v,w,r)
    if not b: print(f"({u},{v},{w}) r={r}: no valid q set"); continue
    primes,target,x,lo,hi,qs=b
    # check each q_j multiple unique & neutral
    okq=all([y for y in range(lo,hi+1) if y%q==0]==[x-(j+1)] for j,q in enumerate(qs))
    neutral=all(all((x-(j+1))%p for p in (u,v,w)) for j in range(len(qs)))
    mc=mincover(primes,target,lo,hi)
    M=max([u*v,v*v,u*w,v*w]+qs)
    print(f"n={n} (u,v,w)=({u},{v},{w}) r={r} qs={qs}: q-multiples unique&placed={okq} neutral={neutral} "
          f"minCover={mc} (need {n+1}) ratio={(hi-lo+1)/M:.4f}  -> claim holds: {mc==n+1}")
