#!/bin/bash
# Assemble verification/371/openai-joint-dickman-refereed/ in this seat's worktree. Third-party PDFs/sources are NOT redistributed (listed by sha256).
set -e
WT=$HOME/ErdosProblemADay-1022-0600; D=$WT/verification/371/openai-joint-dickman-refereed; S=/tmp/oaimath/012
rm -rf $D; mkdir -p $D/{paper,replay/probe,replay/logs,replay/mut,bridge,compute,seats,live,entry,scripts}
( cd $S/paper && echo "openai/math @ 1581d4cbdd69a0faf34b2089614fe2a814316a6a, preprints/The-joint-Dickman-law-for-consecutive-integers-September-24-2026/ (not redistributed here)"; sha256sum paper.pdf build/main.tex build/sections/*.tex ) > $D/paper/SOURCE.txt
( echo "OpenAI Lean closure copy (from openai/math @ 1581d4c lean/), PNT+ @c39a751 + patch, StrongPNT @2f5835c + patch, LeanArchitect @468e8f5 — sources not redistributed; sha256 of every OAI file:"; cat $S/src/oai_src.sha256 ) > $D/replay/SOURCES.sha256
cp $S/scripts/closure.py $S/scripts/closure2.py $D/scripts/
L=$S/lean-build
cp $L/{drive.py,all_order.txt,all_order_v1_parser_bug.txt,modules.tsv,driver.log,steps.tsv,ESTIMATE.md,cacheget.sh,cacheget.out,post.sh,after.sh,after2.sh,post.log,statement_match.py,statement_match.txt,probes.json,mutate_matcher.sh,lean_path.txt,leanchecker.sh} $D/replay/ 2>/dev/null || true
cp $L/probe/*.lean $D/replay/probe/
for f in $L/logs/*.log; do cp $f $D/replay/logs/; done
tar -C $L/logs -cJf $D/replay/logs/module_logs.tar.xz $(cd $L/logs && ls mod_*.txt)
cp $L/mut/MUTATIONS.txt $D/replay/mut/
B=$S/bridge
cp $B/{Bridge371.lean,BridgeCore.lean,Bridge371.log,BridgeCore.log,FC_371.lean,FC_Density.lean,AxBridge.lean,AxBridge.log,AxCore.lean,build_bridge.sh,make_final.py,verbatim_check.py,verbatim_check.log,steps.tsv} $D/bridge/ 2>/dev/null || true
for m in BridgeMutValue BridgeMutStrict928 BridgeMutDensityDef; do cp $B/$m.lean $B/$m.log $D/bridge/; done
C=$S/compute
cp $C/*.c $C/*.py $C/out_*.txt $C/time_*.txt $C/joint_table_1e10.txt $C/indep_ratio_1e10.txt $D/compute/ 2>/dev/null || true
sha256sum $C/hist_1e10.bin > $D/compute/hist_1e10.bin.sha256; xz -k -c $C/hist_1e10.bin > $D/compute/hist_1e10.bin.xz
cp $S/seats/{BRIEF.md,B_BRIEF.md,main_reading.md,A_report.md,R_report.md,L_report.md,W_report.md,receipts.sh} $D/seats/
[ -f $S/seats/B_report.md ] && cp $S/seats/B_report.md $D/seats/
[ -f $S/seats/MODEL_RECEIPTS.txt ] && cp $S/seats/MODEL_RECEIPTS.txt $D/seats/
for w in A_work R_work L_work W_scripts B_work; do [ -d $S/seats/$w ] && { mkdir -p $D/seats/$w; find $S/seats/$w -maxdepth 2 -type f \( -name '*.py' -o -name '*.log' -o -name '*.txt' -o -name '*.md' \) -size -2M -exec cp {} $D/seats/$w/ \; ; } ; done
( cd $S/seats && find W_src -type f -exec sha256sum {} \; ) > $D/seats/THIRD_PARTY_DOWNLOADS_NOT_REDISTRIBUTED.sha256 2>/dev/null || true
cp $S/live/*.txt $S/live/fc_371.lean $D/live/ 2>/dev/null || true
cp $S/entry/{entry371.js,headline.js,closed_by.txt,lean_label.txt,apply371.py,smoke371.mjs,render.mjs,entry_rendered.txt,alpha_table.html,indep_table.html,fc_issue_title.txt,fc_issue_body.md,make_bundle.sh} $D/entry/ 2>/dev/null || true
cp $S/entry/README.md $D/README.md
mkdir -p $D/entry/fixB $D/live/0900 && cp $S/entry/fixB/apply_B.py $D/entry/fixB/ && cp $S/entry/mkpage.py $D/entry/ && cp $S/live/0900/*.txt $D/live/0900/
find $D -name '__pycache__' -prune -exec rm -rf {} \;
( cd $D && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS )
echo "bundle: $(find $D -type f | wc -l) files, $(du -sh $D | cut -f1)"
