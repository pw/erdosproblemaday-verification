#!/bin/bash
# controls for 8a7svk; run from subs-1029/531
set -u
G=checks/fs_grow; D=checks/fs5_direct; W=submitted/k5_w1513.txt; T=$(mktemp -d)
echo "== 1. all-zero colourings: grower / direct / direct-count / partition DP must all agree"
for N in 40 80 120; do
  python3 -c "print('0'*$N)" > $T/z$N.txt
  g=$($G $T/z$N.txt 5 | awk '/j=5/{split($3,a,"=");split($4,b,"=");print a[2]+b[2]}')
  d=$($D $T/z$N.txt | awk '/mono5/{split($3,a,"=");split($4,b,"=");print a[2]+b[2]}')
  c=$($D $T/z$N.txt $N count | awk '{split($2,a,"=");print a[2]}')
  p=$(python3 -c "import sys; sys.path.insert(0,'checks'); import fs_extend as F; print(F.eligible($N,5))")
  echo "N=$N grower=$g direct=$d direct_count=$c dp=$p $([ "$g" = "$d" ] && [ "$d" = "$c" ] && [ "$c" = "$p" ] && echo AGREE || echo DISAGREE)"
done
echo "== 1b. eligible 5-sets at N=1513 by DP (and direct count)"
python3 -c "import sys; sys.path.insert(0,'checks'); import fs_extend as F; print('dp', F.eligible(1513,5))"
echo "== 2. random colourings: grower vs direct mono-5 counts"
for seed in 1 2 3 4 5 6 7 8 9 10 11 12; do
  for spec in "1513 0.5" "1513 0.45" "600 0.3"; do set -- $spec
    python3 -c "import random; r=random.Random($seed); print(''.join('1' if r.random()<$2 else '0' for _ in range($1)))" > $T/r.txt
    g=$($G $T/r.txt 5 | awk '/j=5/{split($3,a,"=");split($4,b,"=");print a[2]+b[2]}')
    d=$($D $T/r.txt | awk '/mono5/{split($3,a,"=");split($4,b,"=");print a[2]+b[2]}')
    echo "seed=$seed N=$1 p=$2 grower=$g direct=$d $([ "$g" = "$d" ] && echo AGREE || echo DISAGREE)"
  done
done
echo "== 3. third instrument (python grower fs_extend.py, set-based) on the witness truncated to N=500 and on random [500]"
python3 checks/fs_extend.py $W 5 500 | tail -2; $G $W 5 500 | tail -2; $D $W 500 | tail -1
python3 -c "import random; r=random.Random(99); print(''.join('1' if r.random()<0.5 else '0' for _ in range(500)))" > $T/r500.txt
python3 checks/fs_extend.py $T/r500.txt 5 | grep -E 'k=5|RESULT'; $G $T/r500.txt 5 | grep -E 'j=5'; $D $T/r500.txt | head -1
echo "== 4. the wall at 1514"
for c in 0 1; do (tr -cd '01' < $W; echo $c) > $T/x$c.txt; echo "colour(1514)=$c: $($G $T/x$c.txt 5 | tail -1) | $($D $T/x$c.txt | head -1)"; done
echo "== 5. known small values through the grower"
$G known/k2_w8.txt 2 | tail -1; $G known/k3_w53.txt 3 | tail -1
for c in 0 1; do (tr -cd '01' < known/k3_w53.txt; echo $c) > $T/k3x$c.txt; echo "k3 [54] colour(54)=$c: $($G $T/k3x$c.txt 3 | tail -1)"; done
n9=0; for m in $(seq 0 511); do python3 -c "print(format($m,'09b'))" > $T/n9.txt; $G $T/n9.txt 2 >/dev/null && n9=$((n9+1)); done; echo "colourings of [9] with no mono 2-set: $n9 (F(2)=9 needs 0)"
rm -rf $T
