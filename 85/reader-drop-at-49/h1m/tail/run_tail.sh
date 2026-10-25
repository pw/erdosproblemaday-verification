#!/bin/bash
# Tail probe runner (2026-10-20 00Z seat). OUR encoding (h1mcell.py, the campaign's flags) on the authors' 25 hardest H1
# orbits. Bounded diagnostic: 25 cells, cap $CAP s, P workers, nice 19, ulimit -v 4 GB. NOT the campaign (separate
# out/pid/log names so campaign.sh's resume + done files are untouched). Any SAT -> ALARM_SAT here and stop.
cd ~/MathDyad/erdos85/h1m
P=${1:-4}; CAP=${2:-3600}; OUT=tail/run.tsv; touch $OUT
echo $$ > tail/run.pid
cell() {
  j=$1; M=$2; tag=$3
  [ -e tail/ALARM_SAT ] && return
  s=$(date +%s.%N)
  full=$(bash -c "ulimit -v 4000000; /usr/bin/time -f MAXRSS_KB=%M timeout $((CAP+300)) nice -n 19 ~/.venv/bin/python h1mcell.py 7 $j $CAP kissat --pairsb --slots --ph --edgeswap --M $M" 2>&1)
  r=$(printf '%s\n' "$full" | grep -v MAXRSS_KB | tail -1); rss=$(printf '%s\n' "$full" | grep -o 'MAXRSS_KB=[0-9]*' | tail -1)
  case "$r" in SAT*) printf '%s\t%s\t%s\n%s\n' "$j" "$M" "$tag" "$full" >> tail/ALARM_SAT;; esac
  printf "%s\t%s\t%s\t%s\t%.1f\t%s\n" "$j" "$M" "$tag" "$r" "$(echo "$(date +%s.%N) - $s" | bc)" "$rss" >> $OUT
}
export -f cell; export CAP OUT
TODO=$(awk -F'\t' -v out="$OUT" 'FILENAME == out { if ($4 == "UNSAT") done[$1"\t"$2]=1; next } /^#/ {next}
       !(($1"\t"$2) in done) { print $1, $2, $3 }' "$OUT" tail/tail_cells.tsv)
echo "$(date -u +%FT%TZ) todo=$(printf '%s' "$TODO" | grep -c .) P=$P CAP=$CAP" >> tail/run.log
printf '%s\n' "$TODO" | grep . | xargs -r -P "$P" -L 1 bash -c 'cell "$0" "$1" "$2"'
echo "DONE $(date -u +%FT%TZ)" >> tail/run.log
