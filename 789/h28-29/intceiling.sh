#!/bin/bash
# largest m with a POSITIVE m-set in [1,N] having no admissible 6-subset (where the real-arithmetic lemma (m,6) can be UNSAT at all)
cd /home/exedev/MathDyad/erdos789
for N in 17 20 24 28 32; do
  m=14
  while :; do
    nice -n 19 /home/exedev/.venv/bin/python intsearch789.py $N $m 6 | sed 's/admissible_subsets=[0-9/]* //'; rc=${PIPESTATUS[0]}
    [ $rc -eq 10 ] || break
    m=$((m+1))
  done
  echo "CEILING N=$N: largest positive witness m=$((m-1))"
done
echo "INTCEILING DONE"
