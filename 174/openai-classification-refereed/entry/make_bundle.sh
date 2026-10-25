#!/bin/bash
# Assemble verification/174/openai-classification-refereed/ in the seat's worktree. Third-party PDFs are NOT redistributed (listed by sha256).
set -e
WT=$HOME/ErdosProblemADay-1021-2100; D=$WT/verification/174/openai-classification-refereed; S=/tmp/oaimath/172
rm -rf $D; mkdir -p $D/{paper,replay/probe,replay/logs,replay/mut,bridge,compute,seats,live,entry}
# paper: hashes only
( cd $S/src && echo "openai/math @ 1581d4cbdd69a0faf34b2089614fe2a814316a6a, preprints/A-classification-of-finite-Euclidean-Ramsey-configurations-September-23-2026/ (Apache-2.0; not redistributed here)"; sha256sum paper.pdf build/main.tex build/sections/*.tex build/refs.bib ) > $D/paper/SOURCE.txt
# replay
L=$S/lean-build
cp $L/{drive.py,all_order.txt,modules.tsv,driver.log,steps.tsv,ESTIMATE.md,cacheget.sh,cacheget.out,post.sh,after.sh,post.log,statement_match.py,statement_match.txt,probes.json,mutate_matcher.sh,leanchecker.sh,leanchecker_fc.sh,lean_path.txt} $D/replay/ 2>/dev/null || true
cp $L/probe/*.lean $D/replay/probe/
for f in $L/logs/*.log; do case $(basename $f) in mod_*) ;; *) cp $f $D/replay/logs/;; esac; done
tar -C $L/logs -cJf $D/replay/logs/module_logs.tar.xz $(cd $L/logs && ls mod_*.txt)
cp $L/mut/MUTATIONS.txt $D/replay/mut/
# bridge
B=$S/bridge
cp $B/{Bridge174.lean,Bridge174FC.lean,Bridge174Main.lean,AxBridgeMain.lean,AxBridgeMain.log,FC_174.lean,FC_SHA.txt,AxBridge.lean,AxBridge.log,AxBridgeFC.lean,AxBridgeFC.log,LcAll.lean,lean_env.sh,verbatim_check.py,verbatim.log,verbatim_mut.log} $D/bridge/
for m in BridgeMutNoAlg BridgeMutNeg BridgeMutNoSphere BridgeFCMutSmall BridgeFCMutSub BridgeFCMutDef BridgeMainMutNoCrit BridgeMainMutNoSub; do cp $B/$m.lean $B/$m.log $D/bridge/; done
# compute
C=$S/compute
cp $C/*.py $C/*.log $D/compute/
# seats
cp $S/seats/{BRIEF.md,B_BRIEF.md,O_report.md,T_report.md,L_report.md,W_report.md,main_reading.md} $D/seats/; mkdir -p $D/seats/B_work; cp $S/seats/B_work/*.py $D/seats/B_work/ 2>/dev/null || true
[ -f $S/seats/B_report.md ] && cp $S/seats/B_report.md $D/seats/
mkdir -p $D/seats/O_work $D/seats/T_work $D/seats/L_scratch $D/seats/W_src
cp $S/seats/O_work/*.py $D/seats/O_work/ 2>/dev/null || true
cp $S/seats/T_work/*.py $D/seats/T_work/ 2>/dev/null || true
cp $S/seats/L_scratch/* $D/seats/L_scratch/ 2>/dev/null || true
cp -r $S/seats/W_src/prior $S/seats/W_src/wstrinz $D/seats/W_src/ 2>/dev/null || true
cp $S/seats/W_src/{fc_174.lean,fc_Paper_EuclideanRamseyCircle.lean,fc_main_head.txt,openai_CONTENTS_172.md} $D/seats/W_src/ 2>/dev/null || true
( cd $S/seats && find W_src/dl T_work/dl -type f -exec sha256sum {} \; ) > $D/seats/THIRD_PARTY_DOWNLOADS_NOT_REDISTRIBUTED.sha256 2>/dev/null || true
cp $S/seats/receipts.sh $S/seats/MODEL_RECEIPTS.txt $D/seats/ 2>/dev/null || true
# live
cp $S/live/*.html $S/live/*.txt $D/live/
# entry
cp $S/entry/{entry174.js,apply174.py,make_bundle.sh,vals.json,close_lc.py,fc_issue_title.txt,fc_issue_body.md,mkpage.py,render.mjs,entry_rendered_preblind.txt,entry174.js.pre-blind} $D/entry/; cp $S/entry/smoke174.mjs $D/entry/ 2>/dev/null || true
cp $S/entry/README.md $D/README.md 2>/dev/null || true
find $D -name '__pycache__' -prune -exec rm -rf {} \;
( cd $D && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS )
echo "bundle: $(find $D -type f | wc -l) files, $(du -sh $D | cut -f1)"
