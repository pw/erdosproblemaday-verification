#!/usr/bin/env python3
# DAG-parallel lake-free kernel replay of OpenAI family 172 (Euclidean Ramsey classification, Erdős #174), 21:00Z erdos seat 2026-10-21. Copied from the #304 driver (family 25). One source root: openai/math @1581d4c lean/.
# Adapted from the #968 driver. Three source roots: LeanArchitect @468e8f5, PrimeNumberTheoremAnd @c39a751, openai/math @1581d4c lean/.
import os, subprocess, time, re, sys, threading
L='/tmp/oaimath/172/lean-build'; OUT=L+'/out'; ML='/tmp/erdos0300/lean/mathlib4'
ROOTS={'OAI':'/tmp/oaimath/024/repo/lean'}
W=int(sys.argv[1]) if len(sys.argv)>1 else 4; GATE=18
H='/tmp/oaimath/166/lean-build/home'; TB=H+'/.elan/toolchains/leanprover--lean4---v4.34.1/bin'
LP=[OUT, ML+'/.lake/build/lib/lean']+[f'{ML}/.lake/packages/{p}/.lake/build/lib/lean' for p in sorted(os.listdir(ML+'/.lake/packages'))]
env=dict(os.environ, HOME=H, ELAN_HOME=H+'/.elan', ELAN_TOOLCHAIN_GC_DISABLE='1', PATH=TB+':/usr/local/bin:/usr/bin:/bin', LEAN_NUM_THREADS='1', LEAN_PATH=':'.join(LP))
open(L+'/lean_path.txt','w').write(env['LEAN_PATH']+'\n')
def log(*a):
    with open(L+'/driver.log','a') as f: f.write(time.strftime('[%Y-%m-%dT%H:%M:%SZ] ',time.gmtime())+' '.join(map(str,a))+'\n')
def memavail():
    for l in open('/proc/meminfo'):
        if l.startswith('MemAvailable'): return int(l.split()[1])/1048576
order=[l.strip() for l in open(L+'/all_order.txt') if l.strip()]
S=set(order)
OPTS={'OAI':['-DautoImplicit=false']}
def root(m): return ROOTS[m.split('.')[0]]
def imports(m):
    out=[]
    for x in open(f"{root(m)}/{m.replace('.','/')}.lean"):
        x=x.strip().split()
        if len(x)>=2 and x[0] in ('import','public','meta') :
            n=x[-1]
            if n in S: out.append(n)
    return out
deps={m:imports(m) for m in order}
done=set()
if os.path.exists(L+'/modules.tsv'):
    for l in open(L+'/modules.tsv'):
        m=l.split()[0]
        if ' rc=0 errors=0 ' in l and os.path.exists(f"{OUT}/{m.replace('.','/')}.olean"): done.add(m)
failed=set(); running=set(); lock=threading.Lock()
def build(m):
    o=f"{OUT}/{m.replace('.','/')}"; os.makedirs(os.path.dirname(o),exist_ok=True)
    lg=f"{L}/logs/mod_{m}.txt"; t0=time.time()
    with open(lg,'w') as f:
        rc=subprocess.call(['/usr/bin/time','-f','maxrss_kb=%M wall_s=%e','nice','-n','19','ionice','-c2','-n7','lean']+OPTS[m.split('.')[0]]+[m.replace('.','/')+'.lean','-o',o+'.olean','-i',o+'.ilean'],cwd=root(m),env=env,stdout=f,stderr=subprocess.STDOUT)
    t=open(lg).read(); rs=re.findall(r'maxrss_kb=\d+ wall_s=[\d.]+',t)
    errs=len(re.findall(r'(?m)^\S+:\d+:\d+: error',t))
    sha=subprocess.run(['sha256sum',o+'.olean'],capture_output=True,text=True).stdout[:16] if os.path.exists(o+'.olean') else '-'
    with lock:
        with open(L+'/modules.tsv','a') as f: f.write(f"{m} rc={rc} errors={errs} {rs[-1] if rs else ''} sha={sha}\n")
        running.discard(m)
        (done if rc==0 and errs==0 else failed).add(m)
    log(('built' if rc==0 and errs==0 else 'FAILED'), m, f'{time.time()-t0:.0f}s', f'{len(done)}/{len(order)}')
log(f'start W={W} done={len(done)} memavail={memavail():.1f}G')
while True:
    with lock:
        if failed: break
        if len(done)==len(order): break
        ready=[m for m in order if m not in done and m not in running and all(d in done for d in deps[m])]
        nrun=len(running)
    if ready and nrun<W and memavail()>=GATE:
        m=ready[0]
        with lock: running.add(m)
        threading.Thread(target=build,args=(m,),daemon=True).start(); time.sleep(1); continue
    time.sleep(2)
while running: time.sleep(2)
st='0' if not failed and len(done)==len(order) else '1'
with open(L+'/steps.tsv','a') as f: f.write(f"build {st} {len(done)}/{len(order)} failed={','.join(sorted(failed))}\n")
log('BUILD END', st, len(done), 'failed', sorted(failed))
