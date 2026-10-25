#!/bin/bash
# Freeze the line-lemma / coarse-torus work into the site bundle.  usage: bundle_lines.sh <worktree>
set -e
WT=${1:?worktree}; B=$WT/verification/203/line-lemma
SRC=~/MathDyad/erdos203
mkdir -p $B/scripts $B/results $B/pools $B/referee $B/logs
cp $SRC/lines/{linelemma.py,torus.py,census_lines.py,fivesevencut.py,LEMMA.md,REFEREE_BRIEF.md,batch_lines.sh,batch_small2.sh,batch_open2.sh,run_720720_coarse.sh,batch_feas_open.sh,batch_feas_small.sh,feas_undecided.sh,rerun_undecided.sh,batch_pp.sh,bundle_lines.sh,table.py} $B/scripts/ 2>/dev/null; cp $SRC/lines/README.md $B/README.md
cp $SRC/lines/ll_*.jsonl $B/results/ 2>/dev/null || true
cp $SRC/lines/torus_*.jsonl $B/results/ 2>/dev/null || true
cp $SRC/lines/milp_*.jsonl $SRC/lines/feas_*.jsonl $SRC/lines/pp_*.jsonl $SRC/lines/ll_*_rerun.jsonl $SRC/lines/fivesevencut.out $SRC/lines/undecided_now.txt $B/results/ 2>/dev/null || true
cp -r $SRC/lines/referee/. $B/referee/ 2>/dev/null || true
mkdir -p $B/referee/scratch && cp /tmp/ref203lines/*.py /tmp/ref203lines/*.md /tmp/ref203lines/*.txt /tmp/ref203lines/*.json /tmp/ref203lines/*.out $B/referee/scratch/ 2>/dev/null || true
mkdir -p $B/referee/consistency && cp /tmp/consist203/* $B/referee/consistency/ 2>/dev/null || true
cp $SRC/lines/run_5040.jsonl $B/results/ 2>/dev/null || true
cp $SRC/lines/controls.log $B/results/ 2>/dev/null || true
cp $SRC/lines/selftest_torus.log $B/results/ 2>/dev/null || true
cp $SRC/lines/batch_*.log $SRC/lines/pool2_scan.log $B/logs/ 2>/dev/null || true
for f in $SRC/lines/ll_*.jsonl; do N=$(basename $f .jsonl); N=${N#ll_}; N=${N%%_*}; cp $SRC/pool_$N.json $B/pools/ 2>/dev/null; done; cp $SRC/pool_720.json $SRC/pool_2520.json $B/pools/
cp $SRC/S8.txt $SRC/S8.log $B/results/ 2>/dev/null || true
python3 $SRC/lines/table.py > $B/results/TABLE.md
( cd $B && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS )
echo "bundled $(find $B -type f | wc -l) files into $B"
