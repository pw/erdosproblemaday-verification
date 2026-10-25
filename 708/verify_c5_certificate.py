import itertools
from collections import Counter
from math import prod

def val(n,p):
    c=0
    while n and n%p==0: n//=p; c+=1
    return c

def analyze(u,v,w,q,verbose=True):
    primes=[u,v,w,q]; target=(2,4,2,1)
    A=sorted([u*v,v*v,u*w,v*w,q]); M=max(A)
    # CRT: t = 1 mod uw ; t*uw = v+1 mod v^2 ; t*uvw = 1 mod q
    from sympy.ntheory.modular import crt
    # solve for t directly by search over CRT moduli
    # t ≡ 1 (mod uw); t ≡ (v+1)*inv(uw) (mod v^2); t ≡ inv(uvw) (mod q)
    m1,r1 = u*w, 1
    m2,r2 = v*v, ((v+1)*pow(u*w,-1,v*v))%(v*v)
    m3,r3 = q, pow(u*v*w,-1,q)
    t,_ = crt([m1,m2,m3],[r1,r2,r3])
    t=int(t)
    x=t*u*v*w
    lo,hi = x-u*v+1, x+u*v-1
    ok={}
    ok['uv_uw_vw_unique_x'] = all([y for y in range(lo,hi+1) if y%m==0]==[x] for m in (u*v,u*w,v*w))
    ok['x_val_111'] = (val(x,u),val(x,v),val(x,w))==(1,1,1)
    m2s=[y for y in range(lo,hi+1) if y%(v*v)==0]
    ok['v2_unique_xminusv'] = (m2s==[x-v] and val(x-v,v)==2)
    ok['no_v3'] = not any(y%(v**3)==0 for y in range(lo,hi+1))
    mq=[y for y in range(lo,hi+1) if y%q==0]
    ok['q_unique_xminus1'] = (mq==[x-1])
    ok['q_point_neutral'] = all((x-1)%p for p in (u,v,w))
    # EXACT min cover, multiplicity-respecting: enumerate counts per capped class
    vecs=Counter()
    for y in range(lo,hi+1):
        vc=tuple(min(val(y,p),target[i]) for i,p in enumerate(primes))
        if any(vc): vecs[vc]+=1
    classes=list(vecs.items())
    best=None
    def rec(i,counts,acc):
        nonlocal best
        tot=sum(counts)
        if best is not None and tot>=best: return
        if all(acc[j]>=target[j] for j in range(4)):
            best=tot; return
        if i>=len(classes): return
        vc,mult=classes[i]
        maxtake=min(mult,6)
        for k in range(maxtake,-1,-1):
            na=tuple(acc[j]+vc[j]*k for j in range(4))
            rec(i+1,counts+[k],na)
    rec(0,[],(0,0,0,0))
    ratio=(hi-lo+1)/M
    if verbose:
        print(f"\n=== (u,v,w,q)=({u},{v},{w},{q}) ===")
        print(f"  A={A} M={M}  |I|={hi-lo+1}  ratio={ratio:.6f}  (2u/w-1/(vw)={2*u/w-1/(v*w):.6f})")
        for k,val_ in ok.items(): print(f"  {k}: {val_}")
        print(f"  EXACT min cover (multiplicity-respecting DP) = {best}   [need 6 for the claim]")
    return best, ratio, all(ok.values()), (t,x,lo,hi,A,M)

print("### INSTANCE 1 — the paper's exact certificate ###")
b,r,s,info = analyze(17,19,23,331)
print("  t,x,I:",info[0],info[1],(info[2],info[3]))
print("  matches claimed t=14257816, x=105921315064:", info[0]==14257816 and info[1]==105921315064)

print("\n### INDEPENDENT INSTANCES — does the construction generalize? ###")
for (u,v,w) in [(29,31,37),(41,43,47),(101,103,107)]:
    # need prime q with uv<q<vw
    import sympy
    q=sympy.nextprime(u*v)
    if q>=v*w: print(f"  ({u},{v},{w}): no q in range"); continue
    b2,r2,s2,_=analyze(u,v,w,int(q))
