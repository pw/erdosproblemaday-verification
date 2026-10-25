#!/bin/bash
cd /tmp/oaimath/191b/seats/G_work
for m in "" square_nu slab2 badshift; do
  echo "--- run [${m:-base}]"
  nice -n 19 bash -c "ulimit -v 8000000; exec timeout 3000 python3 -I cap_toy.py $m" 2>&1 | tail -2
  echo "rc=${PIPESTATUS[0]}"
done
