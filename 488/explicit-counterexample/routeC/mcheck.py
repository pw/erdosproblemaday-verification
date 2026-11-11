#!/usr/bin/env python3
import sys,subprocess,itertools
from check import parse,primes_upto
def brute(y,Lam,T,W):
    ps=primes_upto(y); n=Lam*T; m=W*T; sm=[1]
    for p in ps:
        new=[]
        for s in sm:
            while s<=m: new.append(s); s*=p
        sm=new
    A=sorted(s for s in sm if T<s<=n)
    psiT=sum(1 for s in sm if s<=T); psin=sum(1 for s in sm if s<=n)
    # multiples of A up to m: z has smooth part > T  (fact) -- but compute DIRECTLY as union of multiples to be independent
    mark=bytearray(m+1)
    for a in A:
        for z in range(a,m+1,a): mark[z]=1
    return psiT,psin,len(A),sum(mark)
def run(tag,args):
    out=subprocess.run(['./e488m']+[str(x) for x in args],capture_output=True,text=True,env={'OMP_NUM_THREADS':'6'}).stdout
    d={}; 
    for l in out.splitlines():
        p=l.split(None,1)
        if len(p)==2: d[p[0]]=p[1]
    return d
def verify(d,psiT,psin,A,M,tag):
    lo=lambda k:int(d[k])
    ok=lo('Psi_lo_T')<=psiT<=lo('Psi_up_T') and lo('Psi_lo_n')<=psin<=lo('Psi_up_n') and lo('A_lo')<=A<=lo('A_up') and lo('M_lo')<=M<=lo('M_up')
    print(f'  {tag}: Psi(T)={psiT} in[{d["Psi_lo_T"]},{d["Psi_up_T"]}] |A|={A} in[{d["A_lo"]},{d["A_up"]}] M={M} in[{d["M_lo"]},{d["M_up"]}] -> {"OK" if ok else "VIOLATED"}')
    return ok
if __name__=='__main__':
    if sys.argv[1]=='tiny':
        allok=True
        for (y,Lam,T,W) in [(7,11,50,40),(7,11,200,100),(7,10,100,120),(7,8,333,60),(11,13,60,160),(11,12,100,168),(5,7,300,48),(5,6,97,30),(13,17,30,280),(13,16,41,200),(7,9,1000,110)]:
            q=y+1
            while any(q%d==0 for d in range(2,q)): q+=1
            if not (y<=Lam<=q and W>Lam and W<q*q): print('skip',y,Lam,T,W); continue
            d=run('t',[y,Lam,1000000,T,W]); psiT,psin,A,M=brute(y,Lam,T,W)
            allok&=verify(d,psiT,psin,A,M,f'y={y} Lam={Lam} T={T} W={W} (brute M_A(WT) = union of multiples)')
        print('OVERALL','PASS' if allok else 'FAIL')
    else:
        # control y=61, exact values from coordinator
        psiT,psin,A,M=19413722,None,64844856,4242568187
        for f in sys.argv[2:]:
            h,_=parse(f); d=h
            lo=lambda k:int(d[k])
            ok=lo('Psi_lo_T')<=psiT<=lo('Psi_up_T') and lo('A_lo')<=A<=lo('A_up') and lo('M_lo')<=M<=lo('M_up')
            from mpmath import mpf,mp; mp.dps=30
            ratio=mpf(67)*M/(2876*A)
            rok=mpf(d['ratio_lo'])<=ratio<=mpf(d['ratio_up'])
            print(f'  {f}: Psi_T [{d["Psi_lo_T"]},{d["Psi_up_T"]}] vs {psiT}; A [{d["A_lo"]},{d["A_up"]}] vs {A}; M [{d["M_lo"]},{d["M_up"]}] vs {M}; ratio [{d["ratio_lo"][:12]},{d["ratio_up"][:12]}] vs {mp.nstr(ratio,10)} -> {"OK" if ok and rok else "VIOLATED"}')
