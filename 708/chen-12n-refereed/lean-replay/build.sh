#!/bin/bash
# Replay of chy4pro/erdos-708-explicit-upper-bounds lean/ (commit dc150fd) — g_le 12 closure.
export PATH=$HOME/.elan/bin:$PATH
cd /tmp/e708/lean || exit 9
L=/tmp/e708/run/steps.tsv
step(){ local name=$1; shift; local t0=$(date +%s); "$@" > /tmp/e708/run/$name.log 2>&1; local rc=$?; echo -e "$name\t$rc\t$(( $(date +%s)-t0 ))\t$(date -u +%FT%TZ)" >> $L; return $rc; }
echo -e "step\trc\tsecs\tend" > $L
lean --version >> /tmp/e708/run/env.log 2>&1
for j in 4 5 6 7; do for Lv in 256 512; do for s in Rows ""; do
  m=Erdos708.H97.Proofs.Numeric${j}_${Lv}${s}
  step pre_$j_${Lv}${s}_$j lake build "$m" || { echo "prebuild failed $m" >> $L; }
done; done; done
step final_build lake build Erdos708.FinalCheck
step finalcheck lake env lean Erdos708/FinalCheck.lean
echo "DONE" >> $L
