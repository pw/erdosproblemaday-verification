#!/bin/bash
# bundle_1159.sh <worktree> <slug>  — freeze scripts, witnesses, logs, proofs (small ones), literature captures into the site bundle
set -e
WT=$1; SLUG=$2; SRC=~/MathDyad/erdos1159; DST=$WT/verification/1159/$SLUG
mkdir -p $DST/{scripts,runs,proofs,referee,literature,orbitzoo}
cp $SRC/{model1159.py,cnf_gf.py,plane_gf.py,equiv1159.py,klein1159.py,harvest.py,orbitsat.py,cubes1159.py,normalform_control.py,erdos1159_wavew035_reverify.py,bundle_1159.sh} $DST/scripts/
cp $SRC/ESTIMATE.md $SRC/ENTRY_DRAFT.md $SRC/REFEREE_BRIEF.md $DST/
cp $SRC/runs/*.json $DST/runs/ 2>/dev/null || true
cp $SRC/runs/*.log $DST/runs/ 2>/dev/null || true
cp $SRC/runs/orbitzoo_q*.log $DST/orbitzoo/ 2>/dev/null || true
# proofs: keep every DRAT under 200 MB; larger ones are listed by hash only
for f in $SRC/runs/proofs/*.drat; do sz=$(stat -c %s "$f"); if [ "$sz" -lt 200000000 ]; then cp "$f" $DST/proofs/; else echo "$(sha256sum "$f")  (not copied, $sz bytes)" >> $DST/proofs/LARGE_PROOFS.txt; fi; done
# CNFs for the cubes and the q=11/13 base instances (small); the generator reproduces all others
cp $SRC/runs/cube_q13_c4_*.cnf $SRC/runs/cube_q11_c4*_*.cnf $SRC/runs/pg11_c4*.cnf $SRC/runs/pg13_c4*.cnf $SRC/runs/pg13_c5_b2.cnf $DST/runs/ 2>/dev/null || true
cp -r $SRC/referee/* $DST/referee/ 2>/dev/null || true
cp /tmp/erdos1159_lit/illes_pisinger_97-13.pdf /tmp/erdos1159_lit/illes_pisinger_97-13.txt $DST/literature/ 2>/dev/null || true
sed -n 1530,1560p /tmp/erdos1159_lit/green.txt > $DST/literature/green_problem68_remark_excerpt.txt 2>/dev/null || true
cp $SRC/README.md $DST/README.md
cd $DST && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS && echo "bundle: $(wc -l < SHA256SUMS) files at $DST"
