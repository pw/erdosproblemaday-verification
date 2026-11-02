#!/bin/bash
# Route B (C port): full enumeration of minimal distinct covering systems with moduli in S_x
# (sqrt(x)-smooth integers in [2,x]) for x = 25..36 at the points where S_x changes. 1800 s cap each.
cd "$(dirname "$0")"
for x in 25 27 30 32 36; do
  m=$(python3 -c "import kenc; print(' '.join(map(str, kenc.smooth_set($x))))")
  /usr/bin/time -f "x=$x time %es mem %MKB" nice -n 19 bash -c "ulimit -v 8000000; exec timeout 1800 ./routeBc 0 $m" > Bc_S$x.out 2> Bc_S$x.err
  echo "S_$x: $(grep -h 'TOTAL\|nodes' Bc_S$x.out | tr '\n' ' ') maxclasses=$(grep CLASSES Bc_S$x.out | tail -1) $(tail -1 Bc_S$x.err)"
done
echo ALLDONE
