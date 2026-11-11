#!/usr/bin/env python3
# Containment checker: parses e488c logs, compares to exact values (brute force for tiny cases, given values for controls).
import sys, re
from fractions import Fraction
from mpmath import mp, mpf, log, floor
mp.dps = 60

def parse(path):
    blocks=[]; hdr={}; cur=None
    for line in open(path):
        line=line.strip()
        if line.startswith('--- T'):
            cur={'T':int(line.split()[2])}; blocks.append(cur); continue
        if not line: continue
        parts=line.split(None,1)
        if len(parts)<2: continue
        k,v=parts
        (cur if cur is not None else hdr)[k]=v
    return hdr,blocks

def primes_upto(n):
    s=bytearray([1])*(n+1); s[0:2]=b'\0\0'
    for i in range(2,int(n**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]

def brute(y,T):
    ps=primes_upto(y); q=y+1
    while any(q%d==0 for d in range(2,int(q**.5)+1)): q+=1
    n=q*T; sm=[1]
    for p in ps:
        new=[]
        for s in sm:
            while s<=n: new.append(s); s*=p
        sm=new
    psiT=sum(1 for s in sm if s<=T); psin=len(sm)
    S=sum(Fraction(1,s) for s in sm if s<=T)
    return dict(psiT=psiT,psin=psin,A=psin-psiT,S=S)

def invPi(y):
    r=Fraction(1)
    for p in primes_upto(y): r*=Fraction(p,p-1)
    return r

def check(path, exact_by_T, label):
    hdr,blocks=parse(path); y=int(hdr['y']); q=int(hdr['q']); ok=True
    IP=mpf(invPi(y).numerator)/mpf(invPi(y).denominator)
    # independent rho check with mpmath
    R=int(hdr['R']); unsafe=int(hdr['unsafe'])
    rs=[]
    for p in primes_upto(y):
        x=R*log(p); w=floor(x) if unsafe else floor(x+mpf(1)/2); rs.append(w/x)
    rmax,rmin=max(rs),min(rs)
    if not unsafe:
        c1 = mpf(hdr['rho_max_s'])>=rmax and mpf(hdr['rho_min_s'])<=rmin
        print(f'  [{label}] rho check (C margins enclose mpmath rho): {c1}'); ok&=c1
    for b in blocks:
        T=b['T']; ex=exact_by_T[T]; n=q*T; res={}
        def chk(name,lo,val,hi):
            good=(lo is None or lo<=val) and (hi is None or val<=hi)
            res[name]=good; return good
        psiT,psin,A=ex['psiT'],ex['psin'],ex['A']
        chk('Psi(T)',int(b['Psi_lo_T']),psiT,int(b['Psi_up_T']))
        chk('Psi(n)',int(b['Psi_lo_n']),psin,int(b['Psi_up_n']))
        chk('|A|',int(b['A_lo']),A,int(b['A_up']))
        S=ex['S']; S=mpf(S.numerator)/mpf(S.denominator) if isinstance(S,Fraction) else mpf(S)
        if ex.get('S_digits_only'):  # exact S given to ~20 digits: allow 1e-19 slack in the *favourable-to-checker* direction (i.e. none needed since our bounds are ~1e-6 wide)
            pass
        chk('S(T)',mpf(b['S_lo']),S,mpf(b['S_up']))
        tail=IP-S; delta=1-S/IP
        chk('tail',mpf(b['tail_lo']),tail,None)
        chk('delta',mpf(b['delta_lo']),delta,None)
        ratio=delta*n/A
        chk('ratio',mpf(b['ratio_lo']),ratio,None)
        allg=all(res.values()); ok&=allg
        print(f'  [{label}] y={y} T={T}: '+' '.join(f'{k}={"OK" if v else "VIOLATED"}' for k,v in res.items()))
        print(f'     exact Psi(T)={psiT} Psi(n)={psin} |A|={A} ratio_exact={mp.nstr(ratio,12)} | ours: Psi_T in [{b["Psi_lo_T"]},{b["Psi_up_T"]}] A<={b["A_up"]} ratio_lo={mp.nstr(mpf(b["ratio_lo"]),12)} gap={mp.nstr((ratio-mpf(b["ratio_lo"]))/ratio,3)}')
    return ok

if __name__=='__main__':
    which=sys.argv[1]; path=sys.argv[2]
    if which=='tiny':
        y=int(sys.argv[3]); hdr,blocks=parse(path); ex={b['T']:brute(y,b['T']) for b in blocks}
        print('OVERALL', 'PASS' if check(path,ex,f'brute y={y}') else 'FAIL')
    elif which=='given':
        Sdig={251:{10**4:'8.501928868116436128',10**8:'9.914200348150963610'},509:{10**10:'11.18042568165824045791'}}
        G={251:{10**4:(5508,315875,310367),10**6:(165348,6100029,5934681),10**8:(3401025,91227348,87826323)},
           509:{10**10:(144130349,6657989227,6513858878)}}
        # S for T=1e6 not given: derive from the given exact ratio 1.355149932 only as a sanity print; skip S/tail/delta/ratio exact checks there
        hdr,blocks=parse(path); y=int(hdr['y']); ex={}
        IP=None
        for b in blocks:
            T=b['T']; psiT,psin,A=G[y][T]
            S=mpf(Sdig[y][T]) if T in Sdig[y] else None
            if S is None:
                # back out S from the given 10-digit exact ratio: ratio=delta*n/A -> delta=ratio*A/n ; S=IP*(1-delta)  (accurate ~1e-9 relative on delta)
                RT={10**6:'1.355149932'}[T]; q=int(hdr['q']); n=q*T
                ipf=invPi(y); IPm=mpf(ipf.numerator)/mpf(ipf.denominator); S=IPm*(1-mpf(RT)*A/n)
                ex[T]=dict(psiT=psiT,psin=psin,A=A,S=S); 
            else: ex[T]=dict(psiT=psiT,psin=psin,A=A,S=S)
        print('OVERALL', 'PASS' if check(path,ex,f'given y={y}') else 'FAIL')
