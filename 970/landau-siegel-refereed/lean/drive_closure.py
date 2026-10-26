#!/usr/bin/env python3
# Seat D (2026-10-26): compile ONLY the 67 closure modules of dirichlet_real_zero_bound, in closure-file order,
# plain `lean -o`, LEAN_NUM_THREADS=2, at most 2 lean processes at once, each under rsscap (12 GB RSS, 40 min).
# Gates before each launch: MemAvailable >= 28 GB (8 GB for it + 20 GB), disk free >= 8 GB.
import os, subprocess, time, re, sys, threading, shutil
W=2; OUT='/tmp/oaimath/003/lean/out'; D='/tmp/oaimath/003/seats/D_work'
ML='/tmp/erdos0300/lean/mathlib4'; H='/tmp/oaimath/003/lean/home'; TB=H+'/.elan/toolchains/leanprover--lean4---v4.34.1/bin'
ROOTS={'OAI':'/tmp/oaimath/013/repo/lean','PrimeNumberTheoremAnd':'/tmp/oaimath/013/ext/PrimeNumberTheoremAnd'}
LP=[OUT]+open(D+'/mathlib_path.txt').read().strip().split(':')
env=dict(os.environ,HOME=H,ELAN_HOME=H+'/.elan',ELAN_TOOLCHAIN_GC_DISABLE='1',PATH=TB+':/usr/local/bin:/usr/bin:/bin',LEAN_NUM_THREADS='2',LEAN_PATH=':'.join(LP))
open(D+'/closure_lean_path.txt','w').write(env['LEAN_PATH']+'\n')
def log(*a):
    with open(D+'/logs/drive_closure.log','a') as f: f.write(time.strftime('[%Y-%m-%dT%H:%M:%SZ] ',time.gmtime())+' '.join(map(str,a))+'\n')
def memavail():
    for l in open('/proc/meminfo'):
        if l.startswith('MemAvailable'): return int(l.split()[1])/1048576
order=[l.strip() for l in open('/tmp/oaimath/003/lean/closure_DRZB.txt') if l.strip()]; S=set(order)
def root(m): return ROOTS[m.split('.')[0]]
def imports(m):
    out=[]
    for x in open(f"{root(m)}/{m.replace('.','/')}.lean"):
        t=x.split()
        if len(t)>=2 and t[0]=='import' and t[-1] in S: out.append(t[-1])
    return out
deps={m:imports(m) for m in order}
done=set(); failed=set(); running=set(); lock=threading.Lock()
if os.path.exists(D+'/modules.tsv'):
    for l in open(D+'/modules.tsv'):
        m=l.split()[0]
        if ' rc=0 errors=0 ' in l and os.path.exists(f"{OUT}/{m.replace('.','/')}.olean"): done.add(m)
def build(m):
    o=f"{OUT}/{m.replace('.','/')}"; os.makedirs(os.path.dirname(o),exist_ok=True)
    lg=f"{D}/logs/mods/{m}.txt"; t0=time.time()
    with open(lg,'w') as f:
        rc=subprocess.call([D+'/rsscap.sh','12000000','2400','/usr/bin/time','-f','maxrss_kb=%M wall_s=%e','nice','-n','19','ionice','-c2','-n7','lean','-DautoImplicit=false',m.replace('.','/')+'.lean','-o',o+'.olean','-i',o+'.ilean'],cwd=root(m),env=env,stdout=f,stderr=subprocess.STDOUT)
    t=open(lg).read(); rs=re.findall(r'maxrss_kb=\d+ wall_s=[\d.]+',t)
    errs=len(re.findall(r'(?m)^\S+:\d+:\d+: error',t)); warns=len(re.findall(r'(?m)^\S+:\d+:\d+: warning',t))
    sha=subprocess.run(['sha256sum',o+'.olean'],capture_output=True,text=True).stdout[:16] if os.path.exists(o+'.olean') else '-'
    with lock:
        with open(D+'/modules.tsv','a') as f: f.write(f"{m} rc={rc} errors={errs} warnings={warns} {rs[-1] if rs else ''} sha={sha}\n")
        running.discard(m); (done if rc==0 and errs==0 else failed).add(m)
    log(('built' if rc==0 and errs==0 else 'FAILED'),m,f'{time.time()-t0:.0f}s',f'{len(done)}/{len(order)}')
log(f'start W={W} done={len(done)} memavail={memavail():.1f}G pid={os.getpid()}')
while True:
    with lock:
        if failed or len(done)==len(order): break
        ready=[m for m in order if m not in done and m not in running and all(d in done for d in deps[m])]
        nrun=len(running)
    if ready and nrun<W and memavail()>=28 and shutil.disk_usage('/').free/1e9>=8:
        m=ready[0]
        with lock: running.add(m)
        threading.Thread(target=build,args=(m,),daemon=True).start(); time.sleep(2); continue
    time.sleep(3)
while running: time.sleep(3)
st='0' if not failed and len(done)==len(order) else '1'
with open(D+'/steps.tsv','a') as f: f.write(f"closure_build {st} {len(done)}/{len(order)} failed={','.join(sorted(failed))}\n")
log('BUILD END',st,len(done),'failed',sorted(failed))
