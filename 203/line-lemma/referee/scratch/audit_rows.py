import json, glob, os
from fractions import Fraction as F
D='/home/exedev/MathDyad/erdos203/lines'
for f in sorted(glob.glob(D+'/ll_*.jsonl')):
    rows=[json.loads(l) for l in open(f)]
    print('==', os.path.basename(f), len(rows), 'rows')
    for r in rows:
        if 'skipped' in r: print('   SKIPPED', r['dir'], r['M']); continue
        c=r['cpsat']
        V=F(c['V']) if c.get('V') else None; B=F(c['bound']) if c.get('bound') else None
        rc=F(c['recount']) if c.get('recount') else None
        flag=[]
        if c['status']!='OPTIMAL': flag.append('NOT-OPTIMAL')
        if rc is not None and rc!=V: flag.append(f'recount {float(rc):.6f}{">" if rc>V else "<"}V')
        if B is not None and B>=1: flag.append('BOUND>=1')
        if r.get('pp'): flag.append('PP=%s'%r['pp'])
        if 'brute' in r: flag.append('brute_agree=%s'%r['brute']['agrees_cpsat'])
        if 'milp' in r: flag.append('milp=%s'%{k:r['milp'].get(k) for k in ('status','V','bound','agrees_cpsat')})
        print('  ', r['dir'], 'Mp',r['Mp'], 'M',r['M'], c['status'], 'V=%.4f'%float(V) if V is not None else 'V=None', 'B=%.4f'%float(B) if B is not None else 'B=None', 'dens=%.4f'%r['density_f'], '%.0fs'%c['wall'], ' '.join(flag), '| verdict:', r.get('verdict'))
