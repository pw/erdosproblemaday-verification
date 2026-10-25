#!/bin/bash
# Referee's independent census: the 27 seeds D u B u (49+B) u R, R subset of {7,56,14,63,28,77} hitting every rail,
# run with the referee's own greedy (ref_greedy) to 1e6 under both rules. Outputs in /tmp/ref341/census/.
cd "$(dirname "$0")"
OUT=/tmp/ref341/census
jobs=()
for r7 in "7" "56" "7 56"; do for r14 in "14" "63" "14 63"; do for r28 in "28" "77" "28 77"; do
  seed=$(echo 1 2 3 5 13 27 36 47 3 22 32 40 48 52 71 81 89 97 $r7 $r14 $r28 | tr ' ' '\n' | sort -n | uniq | paste -sd,)
  tag=$(echo "$r7 $r14 $r28" | tr ' ' '_')
  for rule in Q D; do
    echo "$rule $tag $seed"
  done
done; done; done > $OUT/jobs.txt
cat $OUT/jobs.txt | xargs -P 4 -L 1 bash -c 'nice -n 19 ./ref_greedy $0 1000000 /tmp/ref341/census/$0_$1.txt $2 2> /tmp/ref341/census/$0_$1.log'
echo done
