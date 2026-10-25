#!/bin/bash
# certify_case.sh <cnf> [cap_s]: CaDiCaL (decorrelated from the kissat verdict) writes a binary DRAT proof, drat-trim
# checks it. Disk guard: needs >= 40 GB free. Memory cap 12 GB each. Appends one row to certify.tsv.
cnf=$1; cap=${2:-14400}; d=$(dirname $cnf); b=$(basename $cnf .cnf); pf=/tmp/erdos85-h1k-$b.drat
free=$(df --output=avail -BG / | tail -1 | tr -dc 0-9); [ "$free" -ge 40 ] || { echo -e "$b\tSKIP disk ${free}G" >> $d/certify.tsv; exit 2; }
ulimit -v 12000000
s=$(date +%s)
r=$(nice -n 19 timeout $cap /usr/bin/cadical -q $cnf $pf | grep '^s ')
t1=$(( $(date +%s)-s )); sz=$(stat -c %s $pf 2>/dev/null || echo 0)
if [ "$r" = "s UNSATISFIABLE" ]; then
  v=$(nice -n 19 timeout $((cap*3)) $HOME/.local/bin/drat-trim $cnf $pf 2>&1 | tr -d '\r' | grep -E '^s (VERIFIED|NOT VERIFIED)' | head -1)
else v="-"; fi
echo -e "$b\tcadical: ${r:-none} (${t1}s)\tdrat ${sz} B\tdrat-trim: ${v:-none}\t$(( $(date +%s)-s ))s total" >> $d/certify.tsv
rm -f $pf
