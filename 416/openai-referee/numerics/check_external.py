# Bank the outside-table comparisons (blind-read item 32): our route-A bitset vs OEIS A264810 b-file (V(n), n <= 1e4) and vs the
# sixteen V(2^k) values in our July report (/report/416); route C (invphi.py) vs OEIS A049283 b-file (ell(n), n <= 1e4).
import numpy as np, re
from invphi import ell
A=np.unpackbits(np.fromfile('runs/A9.bits',dtype=np.uint8),bitorder='little')[:2**25+1]
cum=np.cumsum(A.astype(np.int64))
n=bad=0
for l in open('oeis_A264810_b.txt'):
    l=l.strip()
    if not l or l.startswith('#'): continue
    k,v=map(int,l.split()[:2]); n+=1; bad+=(int(cum[k])!=v)
print(f'A264810 b-file: compared {n}, mismatches {bad}')
t=open('/home/exedev/ErdosProblemADay-main/src/ledger_data.js').read(); i=t.find('{n:416,'); s=t[i:t.find('\n',i)]
bad=0
for k in range(10,26):
    v=int(cum[2**k]); hit=(str(v) in s) or (f'{v:,}' in s) or (f'{v:,}'.replace(',','{,}') in s)
    bad+=(not hit); print(f'  V(2^{k}) = {v:>9}  {"in July report" if hit else "NOT FOUND in July report"}')
print(f'July report V(2^10..2^25): 16 compared, {bad} not found')
n=bad=0
for l in open('oeis_A049283_b.txt'):
    l=l.strip()
    if not l or l.startswith('#'): continue
    k,a=map(int,l.split()[:2]); e=ell(k); e=0 if e is None else e; n+=1; bad+=(e!=a)
print(f'A049283 b-file vs route C: compared {n}, mismatches {bad}')
