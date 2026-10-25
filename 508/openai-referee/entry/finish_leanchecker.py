#!/usr/bin/env python3
"""When `leanchecker_fresh` lands in steps.tsv: close the entry's pending sentence and the Labels addendum, reassemble body508.html,
re-apply the entry to a clean index.js in the given worktree. Usage: finish_leanchecker.py <worktree> [--dry-run]. Refuses if the row is absent."""
import sys,os,subprocess
W=sys.argv[1]; dry='--dry-run' in sys.argv
L='/tmp/oaimath/158/lean-build'; D='/tmp/oaimath/158/entry'
rows=[l.split() for l in open(f'{L}/steps.tsv') if l.startswith('leanchecker_fresh ')]
assert rows, "no leanchecker_fresh row yet — refusing"
rc,secs=int(rows[-1][1]),int(rows[-1][2])
ctl=[l.split() for l in open(f'{L}/steps.tsv') if l.startswith('leanchecker_missing_control ')]
ctl_rc=int(ctl[-1][1]) if ctl else None
log=open(f'{L}/logs/leanchecker_fresh.log').read()
m=round(secs/60)
if rc==0:
    sent=(f"<code>leanchecker --fresh OAI.Geometry.PlaneColoring.Five</code> — the whole import closure re-checked from the .olean files, Mathlib included — exited 0 after {secs:,} s "
          f"({m} minutes; an empty log is the pass)" + (f", and the missing-module control exited {ctl_rc}" if ctl_rc is not None else "") + ".")
    label=" The <code>leanchecker --fresh</code> pass over the whole closure, Mathlib included, is what completes the (d)."
else:
    sent=(f"<code>leanchecker --fresh OAI.Geometry.PlaneColoring.Five</code> — the whole import closure re-checked from the .olean files — exited {rc} after {secs:,} s; "
          f"its log begins: {log[:300]!r}. THIS IS THE HEADLINE until it is understood.")
    label=" ⚠ The <code>leanchecker --fresh</code> pass did NOT exit 0 — see the Lean paragraph; (d) is withheld until that is understood."
k=open(f'{D}/draft_kernel.html',encoding='utf-8').read()
old="<code>leanchecker --fresh</code> over the whole import closure, Mathlib included, is running as this is written and its line is updated when it lands."
assert k.count(old)==1; k=k.replace(old,sent); 
lab=open(f'{D}/draft_labels.html',encoding='utf-8').read(); assert lab.count('{{LEANCHECKER_LABEL}}')==1
rd=lambda n: open(f'{D}/{n}',encoding='utf-8').read()
seats=rd('draft_seats.html').replace('{{WHOLE}}',rd('draft_whole.html').strip())
lean=rd('draft_lean.html').replace('{{KERNEL}}',k.strip())
labels=lab.replace('{{LEANCHECKER_LABEL}}',label)
body="\n\n".join(x.strip() for x in [rd('draft_problem_claim.html'),rd('draft_architecture.html'),lean,seats,rd('draft_world.html'),labels])
assert '{{' not in body and '`' not in body and '${' not in body and 'updated when it lands' not in body
print("rc",rc,"secs",secs,"control",ctl_rc); print(sent)
if dry: sys.exit(0)
open(f'{D}/draft_kernel.html','w',encoding='utf-8').write(k); open(f'{D}/draft_labels.html','w',encoding='utf-8').write(labels)
open(f'{D}/body508.html','w',encoding='utf-8').write(body+"\n")
subprocess.run(['git','-C',W,'checkout','--','src/index.js'],check=True)
subprocess.run(['python3',f'{D}/apply508.py',f'{W}/src/index.js'],check=True); print("re-applied")
