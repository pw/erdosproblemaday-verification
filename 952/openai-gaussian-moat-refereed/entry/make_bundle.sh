#!/bin/bash
# Assemble verification/952/openai-gaussian-moat-refereed/ in the 03:00Z seat's worktree. Third-party PDFs are NOT redistributed (listed by sha256).
set -e
WT=$HOME/ErdosProblemADay-1022-0300; D=$WT/verification/952/openai-gaussian-moat-refereed; S=/tmp/oaimath/028
rm -rf $D; mkdir -p $D/{paper,replay/probe,replay/logs,replay/mut,bridge,compute,seats,live,entry}
( cd $S/src && echo "openai/math @ 1581d4cbdd69a0faf34b2089614fe2a814316a6a, preprints/Bounded-Step-Walks-on-Gaussian-Primes-September-26-2026/ (Apache-2.0; not redistributed here)"; sha256sum paper.pdf build/*.tex ) > $D/paper/SOURCE.txt
L=$S/lean-build
cp $L/{drive.py,all_order.txt,modules.tsv,driver.log,steps.tsv,ESTIMATE.md,cacheget.sh,cacheget.out,post.sh,after.sh,post.log,statement_match.py,statement_match.txt,probes.json,mutate_matcher.sh,lean_path.txt} $D/replay/ 2>/dev/null || true
cp $L/probe/*.lean $D/replay/probe/
for f in $L/logs/*.log; do cp $f $D/replay/logs/; done
tar -C $L/logs -cJf $D/replay/logs/module_logs.tar.xz $(cd $L/logs && ls mod_*.txt)
cp $L/mut/MUTATIONS.txt $D/replay/mut/
B=$S/bridge
cp $B/{Bridge952.lean,Bridge952.log,FC_952.lean,FC_SHA.txt,AxBridge.lean,AxBridge.log,AxMutSorry.lean,AxMutSorry.log,bridge.sh,lean_env.sh,verbatim_check.py,verbatim.log,verbatim_mut.log} $D/bridge/
for m in BridgeMutSorry BridgeMutStep BridgeMutNoInj; do cp $B/$m.lean $B/$m.log $D/bridge/; done
C=$S/compute
cp $C/*.py $C/*.c $C/*.log $C/BFS_SUMMARY.txt $D/compute/
cp $S/seats/{BRIEF.md,main_reading.md,G_report.md,I_report.md,L_report.md,S_report.md,W_report.md} $D/seats/
[ -f $S/seats/B_BRIEF.md ] && cp $S/seats/B_BRIEF.md $D/seats/
[ -f $S/seats/B_report.md ] && cp $S/seats/B_report.md $D/seats/
for w in G_work I_work S_work B_work; do [ -d $S/seats/$w ] && { mkdir -p $D/seats/$w; find $S/seats/$w -maxdepth 1 -type f \( -name '*.py' -o -name '*.log' -o -name '*.txt' -o -name '*.md' \) -size -2M -exec cp {} $D/seats/$w/ \; ; } ; done
mkdir -p $D/seats/W_src $D/seats/W_work_scripts; cp $S/seats/W_work/scripts/*.py $D/seats/W_work_scripts/ 2>/dev/null || true; cp $S/seats/W_work/fc_3dfd999_msg.txt $D/seats/W_src/ 2>/dev/null || true; cp $S/seats/W_src/{FC_952_current.lean,erdos1977_p69_excerpt.txt,pitt_028_entry.txt,mo_515849_moat_answer.txt} $D/seats/W_src/ 2>/dev/null || true
( cd $S/seats && find W_src G_work/dl -type f \( -name '*.pdf' -o -name '*.ps' -o -name '*.html' -o -name '*.json' -o -name '*.xml' -o -name '*.txt' \) -exec sha256sum {} \; ) > $D/seats/THIRD_PARTY_DOWNLOADS_NOT_REDISTRIBUTED.sha256 2>/dev/null || true
cp $S/seats/receipts.sh $S/seats/MODEL_RECEIPTS.txt $D/seats/ 2>/dev/null || true
cp $S/live/*.txt $D/live/; cp $S/live/p952_0300.html $S/live/p952c_0300.html $D/live/ 2>/dev/null || true
cp $S/entry/* $D/entry/ 2>/dev/null || true
cp $S/entry/README.md $D/README.md 2>/dev/null || true
rm -f $D/entry/README.md
find $D -name '__pycache__' -prune -exec rm -rf {} \;
( cd $D && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS )
echo "bundle: $(find $D -type f | wc -l) files, $(du -sh $D | cut -f1)"
