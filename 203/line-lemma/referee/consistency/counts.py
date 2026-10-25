import json, os, glob
from fractions import Fraction as F
D='/home/exedev/MathDyad/erdos203/lines/'
Ns=[5040,7920,10080,15120,15840,18480,20160,23760,25200,27720,30240,31680,35280,36960,39600,40320,41580,45360,46800,47520,50400,51480,55440,60480,63360,65520]
tot=dict(opt_lt1=0,bound_lt1=0,feas_only=0,und=0,witness=0,missing=0)
und=[];wit=[];feasonly=[];oneone=[]; worst=None
nfeasdirs=0; feas_cp=0; feas_hi=0; feas_cover=[]
for N in Ns:
    rs={tuple(r['dir']):r for r in (json.loads(l) for l in open(D+f'll_{N}.jsonl')) if 'cpsat' in r}
    rr=D+f'll_{N}_rerun.jsonl'
    if os.path.exists(rr):
        for l in open(rr):
            r=json.loads(l)
            if 'cpsat' in r: rs[tuple(r['dir'])]=r
    fz={}
    for ff in (D+f'feas_{N}.jsonl', D+f'feas_{N}_undecided.jsonl'):
        if os.path.exists(ff):
            for l in open(ff):
                r=json.loads(l)
                if 'feas' in r:
                    k=tuple(r['dir']); f=r['feas']
                    inf=(f.get('cpsat_status')=='INFEASIBLE' or f.get('milp_status')==2)
                    fz.setdefault(k,[]).append(f)
    if fz: feas_cover.append((N,len(fz)))
    if len(rs)!=16: tot['missing']+=16-len(rs); print('MISSING dirs',N,len(rs))
    for k,r in rs.items():
        c=r['cpsat']; V=F(c['V']); b=F(c['bound'])
        finf=any(f.get('cpsat_status')=='INFEASIBLE' or f.get('milp_status')==2 for f in fz.get(k,[]))
        if c['status']=='OPTIMAL' and V<1: tot['opt_lt1']+=1; cls='opt'
        elif b<1: tot['bound_lt1']+=1; cls='bound'
        elif V>=1: tot['witness']+=1; wit.append((N,k,float(V),c['status'])); cls='wit'
        elif finf: tot['feas_only']+=1; feasonly.append((N,k,[ (f.get('cpsat_status'),f.get('milp_status')) for f in fz[k]])); cls='feas'
        else: tot['und']+=1; und.append((N,k,float(V),float(b))); cls='und'
        if cls in ('opt','bound'):
            if worst is None or b>worst[0]: worst=(float(b),N,k,c['status'])
        if k==(1,1): oneone.append((N,cls,c['status'],c['V'],round(float(V),4),c['bound'],round(float(b),4)))
print(tot, 'sum', sum(tot.values()))
print('witness:',wit)
print('feas-only:',feasonly)
print('undecided:',und)
print('worst excluding bound:',worst)
print('(1,1):')
for x in oneone: print('  ',x)
print('feas coverage:',feas_cover)
