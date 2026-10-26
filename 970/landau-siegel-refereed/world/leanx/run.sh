#!/bin/bash
source /tmp/oaimath/003/seats/W_work/leanx/env.sh
cd /tmp/oaimath/003/seats/W_work/leanx
for f in "$@"; do
  ./rsscap.sh 8000000 1800 nice -n 19 lean $f > ${f%.lean}.log 2>&1
  echo "$f rc=$?" >> results.txt
done
