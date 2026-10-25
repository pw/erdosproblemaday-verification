#!/usr/bin/env python3
"""Census of greedy (Dickson, equal-summand) extensions for all seeds A with max A = 13 (4096 seeds containing 13).
For each seed: run fast341 to N1; read the 90%-suffix smallest gap period; if a period <= half the suffix is seen,
try the July finite certificate (certify.py); on failure escalate N (x10) up to NMAX. Survivors are 'E-like'.
Output: census13.tsv (seed, status, N, qgap, q, onset) and survivors.txt."""
import subprocess, sys, os, re, itertools, time
MAXS=int(sys.argv[1]) if len(sys.argv)>1 else 13
N1=200_000; NMAX=2_000_000
out=open(f'census{MAXS}.tsv','a'); surv=open(f'survivors{MAXS}.txt','a')
done=set()
if os.path.exists(f'census{MAXS}.tsv'):
    for l in open(f'census{MAXS}.tsv'):
        done.add(l.split('\t')[0])
def run(seed,N):
    tag=f"tmp_{os.getpid()}"
    r=subprocess.run(['./fast341',str(N),tag,'0']+[str(s) for s in seed],capture_output=True,text=True)
    per=None
    for line in r.stdout.splitlines():
        m=re.match(r'suffix from gap index (\d+) \(len (\d+)\): smallest period (\d+) \(period of THIS SUFFIX only\)',line)
        if m: per=int(m.group(3))   # last line = 90% suffix
    return tag+'_elems.u32',per
t0=time.time(); n=0
for mask in range(0,1<<(MAXS-1)):
    seed=[i+1 for i in range(MAXS-1) if (mask>>i)&1]+[MAXS]
    key=','.join(map(str,seed))
    if key in done: continue
    N=N1; status='UNRESOLVED'; info=''
    while N<=NMAX:
        el,per=run(seed,N)
        if per is not None:
            c=subprocess.run([sys.executable,'certify.py','equal',el,str(per)]+[str(s) for s in seed],capture_output=True,text=True)
            if c.returncode==0:
                m=re.search(r'membership period q=(\d+), onset term index (\d+) \(0-based\), N=(\d+)',c.stdout)
                status='CERTIFIED'; info=f"{N}\t{per}\t{m.group(1)}\t{m.group(3)}"; break
            if not (c.returncode==1 and c.stdout.rstrip().endswith('NOT CERTIFIED')):
                print("TOOL ERROR on",key,N,c.returncode,c.stdout[-200:],c.stderr[-400:],flush=True); status='TOOLERROR'; break
        N*=10
    if status=='UNRESOLVED':
        info=f"{N//10}\t\t\t"; surv.write(key+'\n'); surv.flush()
    out.write(f"{key}\t{status}\t{info}\n"); out.flush()
    try: os.remove(el)
    except: pass
    n+=1
    if n%200==0: print(f"{n} seeds, {time.time()-t0:.0f}s",flush=True)
print("done",n,"seeds",time.time()-t0,"s")
