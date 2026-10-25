#!/usr/bin/env python3
"""Check that every "double-quoted" string in REPORT.md occurs verbatim (whitespace-normalised) in some source.
Suggested replacement wording in REPORT.md is written in «guillemets» and is NOT checked."""
import re, sys, html
srcs = {
 'PROOF.md': '/home/exedev/MathDyad/erdos341q/PROOF.md',
 'green': '/home/exedev/ErdosProblemADay-main/verification/341/li-disproof-refereed/live/green_problem7_excerpt.txt',
 'EG80': '/home/exedev/ErdosProblemADay-main/verification/341/li-disproof-refereed/live/pg-049.txt',
 'li': '/home/exedev/ErdosProblemADay-main/verification/341/li-disproof-refereed/li/Erdos341.tex',
 'vbb16843': '/tmp/erdos1200/lit/2609.16843.txt', 'vbb18522': '/tmp/erdos1200/lit/2609.18522.txt',
 'headline': '/home/exedev/MathDyad/erdos341q/entry/headline.json',
 'body': '/home/exedev/MathDyad/erdos341q/entry/body.html',
 'vcf.log': '/home/exedev/MathDyad/erdos341q/runs/verify_closed_form.log',
 'their_ctl': '/home/exedev/MathDyad/erdos341q/referee/their_gates_control.log',
 'PROOF.md(old Thm1 para)': '/home/exedev/MathDyad/erdos341q/referee/proof_old_theorem1_paragraph.txt',
 'entry_old_1238Z': '/home/exedev/MathDyad/erdos341q/referee/entry_old_excerpts_1238Z.txt',
 'PROOF.md(v0 excerpts)': '/home/exedev/MathDyad/erdos341q/referee/proof_old_excerpts_v0.txt',
 'commit_msg': '/home/exedev/MathDyad/erdos341q/entry/COMMIT_MSG.txt',
 'live341': '/home/exedev/MathDyad/erdos341q/live/341.html', 'live341c': '/home/exedev/MathDyad/erdos341q/live/341-claims.html',
 'live342': '/home/exedev/MathDyad/erdos341q/live/342.html',
 'certify_log': '/home/exedev/MathDyad/erdos341/certify_runs.log',
}
def norm(s):
    return re.sub(r'\s+', ' ', s)
def load(path):
    t = open(path, errors='replace').read()
    if path.endswith('.html'):          # strip tags ONLY in html; in markdown '<' ... '>' is math
        t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    return norm(t)
text = {k: load(v) for k, v in srcs.items()}
rep = open('REPORT.md').read()
bad = 0
for q in re.findall(r'"([^"\n]*)"', rep):
    if len(q) < 8: continue
    hits = [k for k, t in text.items() if norm(q) in t]
    bad += not hits
    print(('OK  ' if hits else 'MISS') + f" [{','.join(hits)}] {q[:110]}")
print("missing:", bad); sys.exit(1 if bad else 0)
