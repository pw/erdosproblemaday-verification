#!/bin/bash
# regenerate every cube formula into ../allcnf and record sha256 vs ledger
cd $HOME/MathDyad/erdos112/kirtchakov/work
while read n N p q s pf qf sf; do
  f=../allcnf/$n.cnf
  [ -s $f ] || python3 make_structured.py $N $p $q $s $pf $qf $sf $f > /dev/null
  a=$(sha256sum $f | cut -d' ' -f1); b=$(grep "^$n VERIFIED" CERTLOG.txt | sed 's/.*cnf_sha256=\([0-9a-f]*\).*/\1/')
  echo "$n $a $([ "$a" = "$b" ] && echo MATCH || echo MISMATCH)"
done < cubes.txt > ../allcnf/sha_check.txt
awk '{print $3}' ../allcnf/sha_check.txt | sort | uniq -c
