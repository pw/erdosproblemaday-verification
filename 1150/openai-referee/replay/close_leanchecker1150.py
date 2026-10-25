#!/usr/bin/env python3
"""Close the #1150 entry's pending leanchecker sentence + README item once /tmp/oaimath/076/lean-build/steps.tsv carries
`leanchecker_fresh <rc> <secs>` and leanchecker_controls.log has `neg rc=1` / `pos rc=0`.  Usage: close_leanchecker1150.py <worktree> [--dry-run]
Refuses unless rc == 0 (rc != 0 is the headline — edit by hand). Each anchor asserted exactly once; copies logs into the bundle."""
import sys, pathlib, re, shutil, datetime
wt=pathlib.Path(sys.argv[1]); dry='--dry-run' in sys.argv
S=pathlib.Path('/tmp/oaimath/076/lean-build')
rows=[l.split() for l in (S/'steps.tsv').read_text().splitlines() if l.startswith('leanchecker_fresh ')]
assert rows, "no leanchecker_fresh row yet"
rc,secs=int(rows[-1][1]),int(rows[-1][2]); assert rc==0, f"leanchecker rc={rc}: THAT is the headline, edit by hand"
log=(S/'leanchecker_fresh.log').read_text(); nonwarn=[l for l in log.splitlines() if l.strip() and 'has local changes' not in l]
assert not any('error' in l.lower() for l in nonwarn), nonwarn[:5]
ctl=(S/'leanchecker_controls.log').read_text(); assert 'neg rc=1' in ctl and 'pos rc=0' in ctl and 'DONE' in ctl, ctl[-300:]
end=(datetime.datetime(2026,10,12,9,40,20)+datetime.timedelta(seconds=secs)).strftime('%H:%M')
h,m=divmod(secs//60,60)
def edit(path, old, new):
    p=wt/path; s=p.read_text(); assert s.count(old)==1, (path, s.count(old)); assert s.count(new)==0
    s=s.replace(old,new); 
    if not dry: p.write_text(s)
    print(('DRY ' if dry else '')+'edited '+path)
edit('src/index.js',
 "the <code>leanchecker --fresh</code> pass over <code>Main</code>'s import closure, Mathlib\nincluded, started at 09:40Z on 12 October and was still running when this paragraph was written — it is updated when it lands,\nand if it rejects anything, that becomes the headline.</p>",
 f"the <code>leanchecker --fresh</code> pass over <code>Main</code>'s import closure, Mathlib\nincluded, started at 09:40Z on 12 October and <strong>exited 0 after {secs:,} s ({h} h {m:02d} min)</strong> at {end}Z, printing only Lake's\n\"has local changes\" warnings and no error line; the two controls for reading that silence as a pass ran on the same build\n(<code>replay/leanchecker_controls.log</code>): a module that does not exist exits 1, a real module exits 0 printing nothing. So Mathlib's\ncached object files are kernel-checked too, and nothing in the import closure was rejected.</p>")
edit('verification/1150/openai-referee/README.md',
 "**PENDING:** `leanchecker --fresh OAI.Analysis.Littlewood.Main` (Mathlib cache re-check)\n   started 2026-10-12T09:40:20Z — its log, rc and the neg/pos controls (`leanchecker_controls.{sh,log}` shape as on #181/#1083) are added\n   here when it lands (sentence in the /day entry anchored \"it is updated when it lands\").",
 f"`leanchecker --fresh OAI.Analysis.Littlewood.Main` (Mathlib cache re-check) started\n   2026-10-12T09:40:20Z and EXITED 0 after {secs:,} s (`replay/steps.tsv`; `replay/leanchecker_fresh.log` = Lake \"has local changes\"\n   warnings only); controls `replay/leanchecker_controls.log`: NEG non-existent module rc=1, POS real module (non-fresh) rc=0. Nothing pending.")
if not dry:
    for f in ['leanchecker_fresh.log','leanchecker_controls.log','steps.tsv']: shutil.copy(S/f, wt/'verification/1150/openai-referee/replay'/f)
    shutil.copy(__file__, wt/'verification/1150/openai-referee/replay/close_leanchecker1150.py')
    print("copied logs; now: regenerate SHA256SUMS, smoke, deploy, purge, verify live, commit, push")
