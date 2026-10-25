#!/bin/bash
# H1 miss-matrix cube campaign (README §5). NOT launched by the 2026-10-19 21Z seat — needs Patrick's go (box-day).
#   campaign.sh kissat P [cap]   : Kissat pass over all 13,351 cells, P workers  -> runs/campaign_kissat.tsv
#   campaign.sh drat   P [cap]   : CaDiCaL writes binary DRAT, drat-trim checks, proof deleted -> runs/campaign_drat.tsv
# Resumable: a cell is DONE only if its row reads exactly UNSAT (kissat mode) or 's UNSATISFIABLE' + 's VERIFIED' (drat
# mode); everything else (UNKNOWN, none, s TIMEOUT, crashes) is retried on the next run (referee obj. 2). Any SAT result
# writes runs/ALARM_SAT and stops dispatch (a SAT cell would be a counterexample: recheck it by hand). Tally:
# `python3 tally.py <mode>` exits 0 only if all 13,351 keys have a done row.
# Every child: nice 19, ulimit -v 4 GB. Stop: kill the xargs PID printed in runs/campaign_<mode>.pid (NOT pkill -f).
cd ~/MathDyad/erdos85/h1m
MODE=$1; P=${2:-4}; CAP=${3:-3600}
CLASSES=${CLASSES:-classes_all.tsv}; OUT=${OUT:-runs/campaign_$MODE.tsv}; touch $OUT
echo $$ > runs/campaign_$MODE.pid
FLAGS="--pairsb --slots --ph --edgeswap"
cell() {   # j M
  j=$1; M=$2; key="$j"$'\t'"$M"
  s=$(date +%s.%N)
  [ -e runs/ALARM_SAT ] && return
  if [ "$MODE" = kissat ]; then
    [ -e runs/ALARM_SAT ] && return
    full=$(bash -c "ulimit -v 4000000; timeout $((CAP+300)) nice -n 19 ~/.venv/bin/python h1mcell.py 7 $j $CAP kissat $FLAGS --M $M" 2>&1)
    r=$(printf '%s\n' "$full" | tail -1)
    case "$r" in SAT*) printf '%s\n%s\n' "$key" "$full" >> runs/ALARM_SAT;; esac
    printf "%s\t%s\t%.1f\n" "$key" "$r" "$(echo "$(date +%s.%N) - $s" | bc)" >> $OUT
  else
    tag=$(echo "$j-$M" | sha256sum | cut -c1-16); cnf=/tmp/h1m-$tag.cnf; pf=/tmp/h1m-$tag.drat
    bash -c "ulimit -v 4000000; nice -n 19 ~/.venv/bin/python h1mcell.py 7 $j 1 kissat $FLAGS --M $M --emit $cnf" > /dev/null 2>&1
    r=$(bash -c "ulimit -v 4000000; nice -n 19 timeout $CAP cadical -q --binary=true $cnf $pf" | head -1)
    v=none
    [ "$r" = "s UNSATISFIABLE" ] && v=$(nice -n 19 timeout $((CAP*3+60)) $HOME/.local/bin/drat-trim $cnf $pf -t $((CAP*3)) 2>&1 | tr -d '\r' | grep -E '^s ' | head -1)
    [ "$r" = "s SATISFIABLE" ] && { printf '%s\tcadical SAT on %s (CNF kept)\n' "$key" "$cnf" >> runs/ALARM_SAT; cp $cnf runs/; }
    csha=$(sha256sum $cnf | cut -c1-16); sz=$(stat -c %s $pf 2>/dev/null || echo 0)
    rm -f $cnf $pf
    printf "%s\t%s\t%s\t%s\t%s\t%.1f\n" "$key" "${r:-none}" "${v:-none}" "$csha" "$sz" "$(echo "$(date +%s.%N) - $s" | bc)" >> $OUT
  fi
}
export -f cell; export MODE CAP OUT FLAGS
# (an NR==FNR idiom treats every class as done when $OUT is EMPTY — caught by the 1-cell test: use FILENAME)
TODO=$(awk -F'\t' -v out="$OUT" -v mode="$MODE" 'FILENAME == out { if ((mode == "kissat" && $3 == "UNSAT") || (mode == "drat" && $3 == "s UNSATISFIABLE" && $4 == "s VERIFIED")) done[$1"\t"$2]=1; next }
       !(($1"\t"$2) in done) { print $1, $2 }' "$OUT" "$CLASSES")
echo "$(date -u +%FT%TZ) mode=$MODE todo=$(printf '%s' "$TODO" | grep -c .) of $(grep -c . $CLASSES)" >> runs/campaign_$MODE.log
printf '%s\n' "$TODO" | grep . | xargs -r -P "$P" -L 1 bash -c 'cell "$0" "$1"'
echo "DONE $(date -u +%FT%TZ)" >> runs/campaign_$MODE.done
