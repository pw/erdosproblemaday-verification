#!/usr/bin/env python3
# hfast vs bf at every sampled n <= 1e8 (bf_1e8_samples.log), with three split points K0 per n.
import subprocess
rows=[l.split() for l in open('bf_1e8_samples.log') if l.startswith('S ')]
bad=tot=ref=0
for _,n,h in rows:
    Ks=['0','2'] + ([str(max(3,int(int(n)**0.5)//3))] if int(n)>100 else [])
    for K0 in Ks:
        r=subprocess.run(['./hfast',n,K0],capture_output=True,text=True)
        if ' h=' not in r.stdout:
            ref+=1; assert 'count saturation' in r.stderr, r.stderr; continue
        tot+=1; hh=r.stdout.split(' h=')[1].split()[0]
        if hh!=h: bad+=1; print('MISMATCH',n,K0,h,hh)
print(f'samples={len(rows)} compared={tot} mismatches={bad} refused(count saturation guard)={ref}')
