#!/bin/bash
# Assemble verification/978/openai-squarefree-quartics-refereed/ in the 12:00Z seat's worktree. Third-party PDFs are NOT redistributed (listed by sha256).
set -e
WT=$HOME/ErdosProblemADay-1022-1200; D=$WT/verification/978/openai-squarefree-quartics-refereed; S=/tmp/oaimath/020
rm -rf $D; mkdir -p $D/{paper,replay/probe,replay/logs,replay/mut,bridge,compute,seats,live,entry}
( cd $S/paper/src && echo "openai/math @ 1581d4cbdd69a0faf34b2089614fe2a814316a6a, preprints/Squarefree-values-of-quartics-and-power-free-values-of-polynomials-September-24-2026/ (Apache-2.0; not redistributed here)"; sha256sum manuscript.pdf build/main.tex build/sections/*.tex ) > $D/paper/SOURCE.txt
cp $S/paper/lean_doc_020.md $S/paper/fc_978.lean $D/paper/
L=$S/lean-build
cp $L/{drive.py,all_order.txt,modules.tsv,driver.log,steps.tsv,cacheget.sh,cacheget.out,post.sh,after.sh,post.log,statement_match.py,statement_match.txt,probes.json,mutate_matcher.sh,lean_path.txt} $D/replay/
cp $S/closure.py $S/closure_order.txt $D/replay/
cp $L/probe/*.lean $D/replay/probe/
for f in $L/logs/*.log; do cp $f $D/replay/logs/; done
tar -C $L/logs -cJf $D/replay/logs/module_logs.tar.xz $(cd $L/logs && ls mod_*.txt)
cp $L/mut/MUTATIONS.txt $D/replay/mut/
B=$S/bridge
cp $B/{Bridge978.lean,Bridge978.log,FC_978.lean,FC_Powerfree.lean,FC_Density.lean,FC_SHA.txt,AxBridge.lean,AxBridge.log,AxMutSorry.lean,AxMutSorry.log,bridge.sh,lean_env.sh,verbatim_check.py,verbatim.log,verbatim_mut.log} $D/bridge/
for m in BridgeMutSorry BridgeMutExp BridgeMutNoLocal; do cp $B/$m.lean $B/$m.log $D/bridge/; done
C=$S/compute
cp $C/euler.gp $C/euler.out $C/tail.gp $C/tail.out $C/sieve_count.py $C/sieve_count.out $C/sieve_count_mut_nolift.py $C/sieve_count_mut.out $D/compute/
cp $S/seats/{BRIEF.md,M1_report.md,M2_report.md,L_report.md,W_report.md} $D/seats/
[ -f $S/seats/B_BRIEF.md ] && cp $S/seats/B_BRIEF.md $D/seats/
[ -f $S/seats/B_report.md ] && cp $S/seats/B_report.md $D/seats/
for w in M1_work M2_work L_work B_work; do [ -d $S/seats/$w ] && { mkdir -p $D/seats/$w; find $S/seats/$w -maxdepth 1 -type f \( -name '*.py' -o -name '*.gp' -o -name '*.log' -o -name '*.txt' -o -name '*.out' -o -name '*.md' \) -size -2M -exec cp {} $D/seats/$w/ \; ; } ; done
mkdir -p $D/seats/W_work_scripts; cp $S/seats/W_work/scripts/*.py $D/seats/W_work_scripts/ 2>/dev/null || true
( cd $S/seats && find W_work M1_work M2_work B_work -type f \( -name '*.pdf' -o -name '*.ps' -o -name '*.html' -o -name '*.json' -o -name '*.xml' -o -name '*.png' -o -name '*.tex' \) -exec sha256sum {} \; ) > $D/seats/THIRD_PARTY_DOWNLOADS_NOT_REDISTRIBUTED.sha256 2>/dev/null || true
cp $S/seats/receipts.sh $S/seats/MODEL_RECEIPTS.txt $D/seats/ 2>/dev/null || true
cp $S/live/*.txt $D/live/; cp $S/live/p978.html $S/live/p978_thread.html $S/live/p978_claims.html $D/live/ 2>/dev/null || true
python3 -c "
import yaml;P=yaml.safe_load(open('$S/live/teorth_problems.yaml'))
import json;open('$D/live/teorth_978.json','w').write(json.dumps([p for p in P if str(p.get('number'))=='978'],indent=1,default=str))"
cp $S/entry/{body.html,reading.html,m2_items.html,numbers.html,mkentry.py,entry978.js,apply978.py,smoke978.mjs,render.mjs,entry_rendered.txt,fc_issue_title.txt,fc_issue_body.md,closed_by.txt,headline.js,lean_label.txt,make_bundle.sh} $D/entry/ 2>/dev/null || true
[ -f $S/entry/entry978.js.pre-blind ] && cp $S/entry/entry978.js.pre-blind $D/entry/
cp $S/entry/README.md $D/README.md
find $D -name '__pycache__' -prune -exec rm -rf {} \;
( cd $D && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS )
echo "bundle: $(find $D -type f | wc -l) files, $(du -sh $D | cut -f1)"
