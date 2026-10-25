#!/bin/bash
# Rerun every UNKNOWN case with a long budget, racing cadical and kissat (first to finish wins), then verify.
# Usage: ./rerun_stragglers.sh <cases_dir> <parallel_cases> <seconds>
set -u
D=${1:-cases}; P=${2:-4}; T=${3:-14400}
cd "$D" || exit 1
one() {
  n="$1"; T="$2"; f="$n.cnf"
  grep -q "^UNKNOWN" "out/$n.status" || return 0
  start=$(date +%s)
  timeout "$T" cadical -q --binary=false "$f" "out/$n.c.drat" > "out/$n.c.out" 2>&1 & pc=$!
  timeout "$T" kissat -q --no-binary "$f" "out/$n.k.drat" > "out/$n.k.out" 2>&1 & pk=$!
  # wait for the first solver to produce a verdict, then kill the other
  while kill -0 $pc 2>/dev/null && kill -0 $pk 2>/dev/null; do sleep 5; done
  if ! kill -0 $pc 2>/dev/null; then wait $pc; rc=$?; who=c; kill $pk 2>/dev/null; wait $pk 2>/dev/null; else wait $pk; rc=$?; who=k; kill $pc 2>/dev/null; wait $pc 2>/dev/null; fi
  secs=$(( $(date +%s) - start ))
  if [ $rc -eq 10 ]; then echo "SAT $secs $who" > "out/$n.status"
  elif [ $rc -eq 20 ]; then
    if drat-trim "$f" "out/$n.$who.drat" -t 40000 2>/dev/null | grep -q "s VERIFIED"; then echo "UNSAT-VERIFIED $secs $who" > "out/$n.status"; rm -f out/$n.c.drat out/$n.k.drat
    else echo "UNSAT-UNVERIFIED $secs $who" > "out/$n.status"; fi
  else echo "UNKNOWN $secs rc=$rc $who" > "out/$n.status"; rm -f out/$n.c.drat out/$n.k.drat; fi
}
export -f one
grep -l "^UNKNOWN" out/*.status | xargs -n1 basename | sed 's/\.status$//' | xargs -P "$P" -I{} bash -c 'one "$@"' _ {} "$T"
echo "=== STRAGGLERS $(date -u +%FT%TZ)"; cat out/*.status | awk '{print $1}' | sort | uniq -c
