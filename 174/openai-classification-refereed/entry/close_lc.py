#!/usr/bin/env python3
"""Close the #174 entry's pending leanchecker sentences (LcAll, Bridge174Main) from steps.tsv + logs, in the seat worktree's
src/index.js and the source entry174.js, and the bundle README. Usage: close_lc.py lcall|main. Refuses unless the step is present
and clean (rc 0, missing control nonzero)."""
import re, sys
L='/tmp/oaimath/172/lean-build'; WT='/home/exedev/ErdosProblemADay-1021-2100'; which=sys.argv[1]
st={}
for l in open(L+'/steps.tsv'):
    if l.strip(): st[l.split()[0]]=l.split()
def gib(f):
    m=re.search(r'maxrss_kb=(\d+)',open(f).read()); return int(m.group(1))/2**20 if m else float('nan')
files=[WT+'/src/index.js']
if which=='lcall':
    assert 'leanchecker_fresh' in st and 'leanchecker_missing_control' in st, 'not done'
    rc,secs,mrc=st['leanchecker_fresh'][1],int(st['leanchecker_fresh'][2]),st['leanchecker_missing_control'][1]
    g=gib(L+'/logs/leanchecker_fresh.log'); print('LcAll rc',rc,'secs',secs,'missing rc',mrc,'GiB',g)
    if rc!='0' or mrc=='0': print('NOT CLEAN — write it up by hand'); sys.exit(1)
    old="An independent kernel re-check (<code>leanchecker --fresh</code>) over the whole closure plus our algebraic-coordinates bridge was still running when this page went up; this sentence is updated when it lands."
    new=f"An independent kernel re-check, <code>leanchecker --fresh</code> over the whole closure plus our algebraic-coordinates bridge, exited with code 0 after {secs:,} s (peak memory {g:.1f} GiB); a missing-module control exits {mrc}."
    rold="`leanchecker_fc.sh`: `leanchecker --fresh Bridge174Main`"
    radd=f"\n  RESULT LcAll: rc 0 after {secs:,} s, peak RSS {g:.1f} GiB (`logs/leanchecker_fresh.log`); missing-module control rc {mrc} (`logs/leanchecker_missing.log`)."
else:
    assert 'leanchecker_fresh_fc' in st, 'not done'
    rc,secs=st['leanchecker_fresh_fc'][1],int(st['leanchecker_fresh_fc'][2])
    g=gib(L+'/logs/leanchecker_fresh_fc.log'); print('Main rc',rc,'secs',secs,'GiB',g)
    if rc!='0': print('NOT CLEAN — write it up by hand'); sys.exit(1)
    old="A separate <code>leanchecker --fresh</code> over this bridge's closure was also still running; this sentence is updated when it lands."
    new=f"A separate <code>leanchecker --fresh</code> over <code>Bridge174Main</code>, which imports both FC bridges and OpenAI's closure, exited with code 0 after {secs:,} s (peak memory {g:.1f} GiB)."
    rold="row `leanchecker_fresh_fc_REPLACED`)."
    radd=f"\n  RESULT Bridge174Main: rc 0 after {secs:,} s, peak RSS {g:.1f} GiB (`logs/leanchecker_fresh_fc.log`)."
for p in files:
    s=open(p).read(); assert s.count(old)==1, (p, s.count(old)); open(p,'w').write(s.replace(old,new))
import json
vp='/tmp/oaimath/172/entry/vals.json'; v=json.load(open(vp)); hit=[k for k in v if v[k]==old]; assert len(hit)==1, hit
v[hit[0]]=new; json.dump(v,open(vp,'w'),ensure_ascii=False,indent=1)
r='/tmp/oaimath/172/entry/README.md'; t=open(r).read()
i=t.find(rold); assert i>0, 'readme anchor'; j=t.find('\n',i)
t=t[:j]+radd+t[j:]
if which=='main' or 'RESULT LcAll' in t and 'RESULT Bridge174Main' in t:
    t=t.replace("Both were STILL RUNNING at the first commit (22:0xZ); this line is updated when they land.","Both landed after the first commit; results below.")
open(r,'w').write(t); print('closed:', new)
