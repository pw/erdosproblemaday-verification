#!/bin/bash
# Usage: certify.sh <cnf> <tsv>   — CaDiCaL with text DRAT, then drat-trim; one row appended.
ulimit -v 12000000
f=$1; OUT=$2; c=$(basename $f .cnf); p=${f%.cnf}.drat; t0=$(date +%s)
r=$(nice -n 19 timeout 10800 /usr/bin/cadical -q --no-binary $f $p | grep '^s ')
v=$(nice -n 19 timeout 10800 $HOME/.local/bin/drat-trim $f $p -t 10800 2>&1 | tr -d '\r' | grep -E '^s (VERIFIED|NOT VERIFIED)' | head -1)
echo -e "$c\t$r\t$(stat -c %s $p 2>/dev/null)\t${v:-NO VERDICT}\t$(( $(date +%s) - t0 ))\t$(sha256sum $f | cut -c1-16)" >> $OUT
rm -f $p
