#!/usr/bin/env python3
"""Part 2: high-precision exact binary search for the true t0, compared EXACTLY with T(alpha).
Plus monotonicity sanity (prereq) and structural verification of the 2^j prefix (Task 2)."""
from fractions import Fraction

def F(x, y=None): return Fraction(x) if y is None else Fraction(x, y)

def T_formula(alpha, kmax=24):
    return min(Fraction(2**k + 1) / (alpha ** k) for k in range(0, kmax + 1))

def argmin_k(alpha, kmax=24):
    best=None; bestk=[]
    for k in range(kmax+1):
        v=Fraction(2**k+1)/(alpha**k)
        if best is None or v<best: best=v; bestk=[k]
        elif v==best: bestk.append(k)
    return best,bestk

def my_greedy(t, alpha, nterms):
    C=0; p=Fraction(1)
    for j in range(nterms):
        x=t*p; s=x.numerator//x.denominator
        if s>=1:
            if s>C+1: return False,j,s,C
            C+=s
        p*=alpha
    return (C>=1),None,None,C

def bisect_t0(alpha, nterms=100, iters=70):
    lo=F(1); hi=F(2)
    pok,_,_,_=my_greedy(lo,alpha,nterms)
    if not pok: return None,"P(1) not true"
    for _ in range(iters):
        mid=(lo+hi)/2
        ok,_,_,_=my_greedy(mid,alpha,nterms)
        if ok: lo=mid
        else: hi=mid
    return (lo+hi)/2,None

def check_monotone(alpha, nterms=80, step=2000):
    seen_false=False
    for i in range(step+1):
        t=F(1)+Fraction(i,step)
        ok,_,_,_=my_greedy(t,alpha,nterms)
        if not ok: seen_false=True
        elif seen_false: return False
    return True

if __name__=="__main__":
    print("="*92)
    print("PART 2a — monotonicity of P(t)=greedy-no-gap (single True->False switch, no re-entrance)")
    print("="*92)
    for als in ["1.55","1.6","1.7","1.8","1.85","1.9","1.95","1.99","1.999",
                "1618/1000","3/2","5/3","9/5","17/9","1999999/1000000"]:
        a=F(als)
        print(f"  alpha={als:>16}: monotone = {check_monotone(a)}")

    print()
    print("="*92)
    print("PART 2b — exact t0 (binary search 2^-70) vs exact T(alpha); adversarial alpha set")
    print("="*92)
    alphas=[]
    for n in range(150,200): alphas.append(F(n,100))
    trans=["5/3","9/5","17/9","33/17","65/33","129/65"]
    for tr in trans:
        a=F(tr); alphas.append(a)
        for d in [F(1,10000),F(-1,10000),F(1,100000),F(-1,100000),F(7,10**6),F(-3,10**6),
                  F(1,10**8),F(-1,10**8)]:
            alphas.append(a+d)
    phis=[F(16180339,10**7),F(16180340,10**7),F(16180339887,10**10),
          F(161803398874989,10**14),F(16180339887498948482,10**19)]
    for ph in phis:
        for d in [F(0),F(1,10**12),F(-1,10**12)]: alphas.append(ph+d)
    for den in [1009,7919,10007]:
        for num in range(int(den*1.5),int(den*1.99),max(1,den//30)):
            alphas.append(F(num,den))
    for eps_d in [1000,10000,100000,10**6,10**7]:
        alphas.append(F(2*eps_d-1,eps_d))
    seen=set(); AL=[]
    for a in alphas:
        if 1<a<2 and a not in seen: seen.add(a); AL.append(a)
    print(f"  testing {len(AL)} distinct alphas (incl. transitions, near-ties, large-denom, near-2)")
    maxerr=Fraction(0); worst=None; bad=0
    for a in AL:
        t0,err=bisect_t0(a)
        if err: print("  ERR",float(a),err); bad+=1; continue
        T=T_formula(a)
        e=abs(t0-T)
        if e>maxerr: maxerr=e; worst=(a,t0,T)
        if e>F(1,10**12):
            print(f"  !!! DISCREPANCY alpha={a} ({float(a):.10f}) t0={float(t0):.14f} "
                  f"T={float(T):.14f} |diff|={float(e):.3e} argmin_k={argmin_k(a)[1]}")
            bad+=1
    print(f"  max |t0 - T| over {len(AL)} alphas = {float(maxerr):.3e}")
    if worst:
        wa,wt0,wT=worst
        print(f"    worst at alpha={wa} ({float(wa):.12f}), argmin_k={argmin_k(wa)[1]}, T={float(wT):.14f}")
    print(f"  discrepancies > 1e-12: {bad}")
