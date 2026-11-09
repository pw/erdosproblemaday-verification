"""All page numbers for the #282 entry come from here (reads sweep_3000.txt, big_N.txt, scan outputs)."""
import json, collections
from sympy import isprime, nextprime, factorint
def load(path):
    rows=[]
    for line in open(path):
        if '|' not in line: continue
        head,tail=line.split('|'); h=head.split()
        if len(h)<6: continue
        N,m,L,mx,R,nt=map(int,h[:6]); tail=[int(x) for x in tail.strip().split(',') if x]
        assert nt==L, line
        rows.append(dict(N=N,m=m,L=L,max=mx,R=R,tail=tail))
    return rows
def how(r):
    c=r['R']+1; t=r['tail']
    if t==[1]: return 'fatal' if isprime(c) else 'ends-composite'
    f=factorint(c)
    if isprime(c): return 'break-prime'
    return 'break-composite'
sweep=load('sweep_3000.txt'); big=load('big_N.txt') if True else []
out={}
for fam in (1,2):
    rs=sorted([r for r in sweep if r['m']==fam], key=lambda r:r['N'])
    Ns=[r['N'] for r in rs]
    assert Ns==list(range(3,3001)), (fam, len(Ns), [n for n in range(3,3001) if n not in Ns][:10])
    st=dict(count=len(rs), all_odd=all(r['L']%2==1 for r in rs), brown=all(r['L']>=r['N']-2 for r in rs))
    b100=[r for r in rs if r['N']>=100]
    st['over_max']=max(r['R']-r['N'] for r in rs); st['over_argmax']=[r['N'] for r in rs if r['R']-r['N']==st['over_max']]
    st['over_mean100']=round(sum(r['R']-r['N'] for r in b100)/len(b100),2)
    st['L_minus_N_max']=max(r['L']-r['N'] for r in rs); st['L_minus_N_argmax']=[r['N'] for r in rs if r['L']-r['N']==st['L_minus_N_max']]
    st['after_ramp_max']=max(len(r['tail']) for r in rs); st['after_ramp_argmax']=[r['N'] for r in rs if len(r['tail'])==st['after_ramp_max']][:5]
    st['maxnum_max']=max(r['max'] for r in rs)
    st['how']=dict(collections.Counter(how(r) for r in b100))
    fp=collections.Counter()
    for r in b100:
        p=nextprime(r['N']); fp['before' if r['R']+1<p else ('at' if r['R']+1==p else 'past')]+=1
    st['vs_first_prime_100']=dict(fp)
    out[f'family{fam}']=st
out['big']=[(r['N'],r['m'],r['L'],r['R'],r['tail']) for r in big]
sel={}
for r in sweep+big:
    if r['N'] in (10,20,50,100,200,500,1000,2000,3000,5000,10000,20000): sel[(r['N'],r['m'])]=(r['L'],r['R'],r['tail'][:8],how(r))
out['selected']={f"{k[0]}/{k[1]}":v for k,v in sorted(sel.items())}
print(json.dumps(out,indent=1))
