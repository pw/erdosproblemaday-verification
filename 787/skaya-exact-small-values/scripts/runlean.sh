#!/bin/bash
cd /tmp/e1125/787work/lean
for f in Erdos787Standalone ThresholdsStandalone WitnessesStandalone InfiniteFamilyStandalone NewWitnessesStandalone GeometryAndCarriesStandalone AsymptoticClosureStandalone Threshold45Standalone; do
  start=$(date +%s)
  timeout 3600 ~/.elan/bin/elan run leanprover/lean4:v4.35.0-rc2 lean $f.lean > $f.out 2>&1
  rc=$?
  echo "$f rc=$rc time=$(( $(date +%s)-start ))s" >> results.txt
done
echo DONE >> results.txt
