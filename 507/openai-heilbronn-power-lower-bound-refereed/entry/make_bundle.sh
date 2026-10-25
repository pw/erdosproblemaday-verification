#!/bin/bash
# Assemble verification/507/openai-heilbronn-power-lower-bound-refereed/ in the 15:00Z seat's worktree.
# Third-party PDFs are NOT redistributed (listed by sha256).
set -e
WT=$HOME/ErdosProblemADay-1022-1500; D=$WT/verification/507/openai-heilbronn-power-lower-bound-refereed; S=/tmp/oaimath/191
rm -rf $D; mkdir -p $D/{paper,replay/probe,replay/logs,replay/mut,bridge,compute,seats,live,entry}
( cd $S/paper/src && echo "openai/math @ 1581d4cbdd69a0faf34b2089614fe2a814316a6a, preprints/A-power-improvement-in-the-Heilbronn-triangle-lower-bound-September-25-2026/ (Apache-2.0; not redistributed here)"; sha256sum main.pdf build/main.tex build/sections/*.tex build/references.bib ) > $D/paper/SOURCE.txt
cp $S/paper/lean_doc_191.md $S/paper/fc_507.lean $D/paper/
L=$S/lean-build
cp $L/{drive.py,all_order.txt,modules.tsv,driver.log,steps.tsv,cacheget.sh,cacheget.out,post.sh,after.sh,post.log,statement_match.py,statement_match.txt,statement_match_v2.py,statement_match_v2.txt,probes.json,mutate_matcher.sh,lean_path.txt} $D/replay/ 2>/dev/null || true
cp $S/closure.py $S/closure_order.txt $D/replay/
cp $L/probe/*.lean $D/replay/probe/
for f in $L/logs/*.log; do cp $f $D/replay/logs/; done
tar -C $L/logs -cJf $D/replay/logs/module_logs.tar.xz $(cd $L/logs && ls mod_*.txt)
cp $L/mut/MUTATIONS.txt $D/replay/mut/
B=$S/bridge
cp $B/{EveryN507.lean,EveryN507.log,Bridge507.lean,Bridge507.log,Extra507.lean,Extra507.log,AxEveryN.lean,AxEveryN.log,AxEveryNMut.lean,AxEveryNMut.log,AxBridge.lean,AxBridge.log,AxMutSorry.lean,AxMutSorry.log,AxExtra.lean,AxExtra.log,FC_507.lean,FC_2d.lean,FC_Asymptotics.lean,FC_green77.lean,FC_SHA.txt,BOS_Statement.lean,BOS_SHA.txt,verbatim_check.py,verbatim.log,verbatim_mut.log,verbatim_mut2.log,verbatim_extra.log,verbatim_extra_mut.log,lean_env.sh,rsscap.sh,lc.sh,COMMANDS.txt} $D/bridge/ 2>/dev/null || true
for m in BridgeMutSorry BridgeMutExp BridgeMutAnswer ExtraMutTrue ExtraMutEta VerbMut VerbMut2; do cp $B/$m.lean $D/bridge/; [ -f $B/$m.log ] && cp $B/$m.log $D/bridge/; done
mkdir -p $D/bridge/bos_receipts; cp $B/bos_receipts/* $D/bridge/bos_receipts/; mkdir -p $D/bridge/bisect; cp $B/bisect/*.lean $D/bridge/bisect/ 2>/dev/null || true
cp $S/compute/* $D/compute/ 2>/dev/null || true
cp $S/seats/*.md $D/seats/
for w in R1_work R2_work C_work B_work; do [ -d $S/seats/$w ] && { mkdir -p $D/seats/$w; find $S/seats/$w -maxdepth 2 -type f \( -name '*.py' -o -name '*.gp' -o -name '*.log' -o -name '*.txt' -o -name '*.out' -o -name '*.md' -o -name '*.json' \) -size -2M -exec cp {} $D/seats/$w/ \; ; } ; done
mkdir -p $D/seats/W_work_scripts; find $S/seats/W_work -maxdepth 2 -name '*.py' -exec cp {} $D/seats/W_work_scripts/ \; 2>/dev/null || true
( cd $S/seats && find W_work R1_work R2_work C_work B_work -type f \( -name '*.pdf' -o -name '*.ps' -o -name '*.html' -o -name '*.png' -o -name '*.tex' \) -exec sha256sum {} \; 2>/dev/null ) > $D/seats/THIRD_PARTY_DOWNLOADS_NOT_REDISTRIBUTED.sha256 || true
cp $S/seats/receipts.sh $S/seats/MODEL_RECEIPTS.txt $D/seats/ 2>/dev/null || true
cp $S/live/*.txt $S/live/*.html $D/live/
cp $S/entry/{body.html,reading.html,world.html,world_replays.html,summary.txt,links.json,mkentry507.py,entry507.js,apply507.py,smoke507.mjs,headline.js,lean_label.txt,leanchecker_sentence.txt,fc_issue_body.md,make_bundle.sh} $D/entry/ 2>/dev/null || true
[ -f $S/entry/entry507.js.pre-blind ] && cp $S/entry/entry507.js.pre-blind $D/entry/
cp $S/entry/README.md $D/README.md
find $D -name '__pycache__' -prune -exec rm -rf {} \;
( cd $D && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS )
echo "bundle: $(find $D -type f | wc -l) files, $(du -sh $D | cut -f1)"
